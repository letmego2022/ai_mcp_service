import gradio as gr
import pandas as pd
import json
import re
from openai import OpenAI
from prompt import SYSTEM_PROMPT

# ✅ 初始化 Moonshot API
client = OpenAI(
    api_key="sk-",
    base_url="https://api.moonshot.cn/v1"
)

# ✅ 提取 JSON 数组块
def extract_json_block(text):
    json_match = re.search(r"\[\s*{.*?}\s*]", text, re.DOTALL)
    if json_match:
        return json_match.group(0)
    return None

# ✅ 初次生成测试用例
def get_test_cases_from_story(user_story: str, state: list):
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_story}
        ]
        response = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=messages,
            temperature=0.3
        )
        content = response.choices[0].message.content
        json_text = extract_json_block(content)
        if not json_text:
            raise ValueError("未能从返回中提取出 JSON 块")

        new_cases = json.loads(json_text)

        # ✅ 用最新2条更新 state
        state = new_cases[:6]

        df = pd.DataFrame(state)
        return df, json.dumps(state, indent=2, ensure_ascii=False), state

    except Exception as e:
        return pd.DataFrame(), f"生成或解析失败: {str(e)}", state

# ✅ 继续生成后续测试用例
def generate_more_test_cases(user_story: str, state: list):
    try:
        # ✅ 构造继续生成 prompt
        previous_case_text = json.dumps(state, ensure_ascii=False, indent=2)
        user_prompt = f"""以下是之前已经生成的测试用例（请避免重复）：
{previous_case_text}

请继续为相同的用户故事追加 2 条不同角度的测试用例，保持格式一致，输出 JSON 数组格式。"""

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        response = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=messages,
            temperature=0.3
        )
        content = response.choices[0].message.content
        json_text = extract_json_block(content)
        if not json_text:
            raise ValueError("未能从返回中提取出 JSON 块")

        new_cases = json.loads(json_text)

        # ✅ 合并历史 + 截断最多保留6条
        state += new_cases
        state = state[-6:]

        df = pd.DataFrame(state)
        return df, json.dumps(state, indent=2, ensure_ascii=False), state

    except Exception as e:
        return pd.DataFrame(), f"继续生成失败: {str(e)}", state

# ✅ Gradio UI
with gr.Blocks(title="MCP - 用户故事转测试用例") as demo:
    gr.Markdown("## 🧠 用户故事 → 测试用例生成器")

    history_state = gr.State([])  # ✅ 独立缓存每个用户的测试用例列表

    with gr.Row():
        story_input = gr.Textbox(
            label="📘 输入用户故事",
            lines=6,
            placeholder="如：作为招聘专员，我希望能够发布职位，以便员工可以申请。"
        )
        submit_btn = gr.Button("🚀 初次生成测试用例")
        more_btn = gr.Button("➕ 继续生成", interactive=False)

    with gr.Row():
        table_output = gr.Dataframe(
            label="📊 测试用例表格（最多显示最近6条）",
            interactive=True
        )

    with gr.Row():
        json_output = gr.Textbox(
            label="🧾 原始 JSON 数据",
            lines=12,
            interactive=True,
            show_copy_button=True
        )

    # ✅ 初次生成逻辑
    submit_btn.click(
        fn=get_test_cases_from_story,
        inputs=[story_input, history_state],
        outputs=[table_output, json_output, history_state]
    ).then(lambda: gr.update(interactive=True), None, [more_btn])

    # ✅ 继续生成逻辑
    more_btn.click(
        fn=generate_more_test_cases,
        inputs=[story_input, history_state],
        outputs=[table_output, json_output, history_state]
    )

# ✅ 启动服务
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7861)
