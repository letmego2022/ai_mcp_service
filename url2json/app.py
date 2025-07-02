import gradio as gr
from utils.html_fetcher import fetch_html_from_url
from parser.kimi_parser import extract_json_from_html_with_kimi

def process_url(url: str):
    html = fetch_html_from_url(url)
    if html.startswith("ERROR"):
        return html
    json_output = extract_json_from_html_with_kimi(html)
    return json_output

iface = gr.Interface(
    fn=process_url,
    inputs=gr.Textbox(label="Input URL", placeholder="https://example.com"),
    outputs=gr.Code(label="Formatted JSON output"),
    title="url2json",
    description="Enter a web URL to analyze its HTML content and generate structured JSON output.",
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
