from openai import OpenAI
from config import KIMI_API_KEY, KIMI_BASE_URL
from prompt_template import SYSTEM_URL_PROMPT, build_user_prompt

def get_kimi_response(system_prompt, user_prompt):
    client = OpenAI(api_key=KIMI_API_KEY, base_url=KIMI_BASE_URL)

    try:
        completion = client.chat.completions.create(
            model="moonshot-v1-auto",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f'{{"error": "Failed to call Kimi API", "details": "{str(e)}"}}'


def extract_json_from_html_with_kimi(html: str) -> str:
    prompt = build_user_prompt(html)
    return get_kimi_response(SYSTEM_URL_PROMPT, prompt)
