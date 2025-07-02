SYSTEM_URL_PROMPT = (
    "你是一个高级Web内容提取引擎，能够深入分析HTML和内联脚本，并输出详细的结构化JSON。"
)

JSON_TEMPLATE = '''{
  "metadata": {
    "title": "提取 <title> 标签内的文本",
    "description": "提取 <meta name='description'> 标签的 content 内容",
    "charset": "提取 <meta charset='...'> 的值",
    "viewport": "提取 <meta name='viewport'> 的 content 内容"
  },
  "assets": {
    "scripts": ["所有 <script> 标签的 src 列表"],
    "stylesheets": ["所有 <link rel='stylesheet'> 标签的 href 列表"],
    "images": ["所有 <img> 标签的 src 和 alt 文本，格式为 {'src': '...', 'alt': '...'}"],
    "favicons": ["所有 <link> 标签中 rel 包含 'icon' 的 href 列表"]
  },
  "page_structure": {
    "headings": {
      "h1": ["所有 <h1> 标签的文本列表"],
      "h2": ["所有 <h2> 标签的文本列表"],
      "h3": ["所有 <h3> 标签的文本列表"]
    },
    "language": "提取 <html> 标签的 lang 属性"
  },
  "interactive_elements": {
    "links": {
        "internal": ["所有相对路径的 <a> href 列表"],
        "external": ["所有绝对路径的 <a> href 列表"]
    },
    "forms": [
      {
        "id": "表单的 id 属性",
        "action": "表单的 action 属性",
        "method": "表单的 method 属性",
        "inputs": [
            {"type": "input 类型", "name": "input 名称", "placeholder": "占位符文本"}
        ]
      }
    ],
    "buttons": ["所有 <button> 标签的文本内容列表"]
  },
  "potential_api_endpoints": [
      "从内联JavaScript的 fetch()、axios() 或 XMLHttpRequest 中推断出的API URL列表"
  ]
}'''

def build_user_prompt(html: str) -> str:
    return f"""
# 任务：深度分析前端代码并提取详细信息

请深度分析以下提供的HTML、CSS和内联JavaScript代码。你的目标是提取元数据、资源、链接、页面结构、交互元素和潜在的API端点。请严格按照下面定义的JSON结构进行输出。

# JSON 输出结构要求:

{JSON_TEMPLATE}

# 规则:
1.  **严格遵守** 上述JSON结构。对于不存在的信息，使用 `""`, `[]`, 或 `null` 作为值，但**必须保留键**。
2.  **绝对不要** 添加任何解释或Markdown代码块 (```)。
3.  你的输出**必须**是纯净、有效的JSON。

---
# 需要分析的代码:
{html[:15000]}  <!-- 限制最大长度 -->
---
"""
