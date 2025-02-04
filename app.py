import gradio as gr
import os
from huggingface_hub import InferenceClient

# Hugging Face API anahtarını Vercel ortam değişkenlerinden alın
api_key = os.environ.get("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")

# Hugging Face modeline bağlantı kurun
client = InferenceClient("HuggingFaceH4/zephyr-7b-beta", token=api_key)

def respond(message, history: list[tuple[str, str]], system_message, max_tokens, temperature, top_p):
    # Mesajları hazırlayın
    messages = [{"role": "system", "content": system_message}]
    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})
    messages.append({"role": "user", "content": message})

    # Modelden gelen yanıtı alın
    response = ""
    for message in client.chat_completion(
        messages,
        max_tokens=max_tokens,
        stream=True,
        temperature=temperature,
        top_p=top_p,
    ):
        token = message.choices[0].delta.content
        response += token
        yield response

# Gradio arayüzü
demo = gr.ChatInterface(
    respond,
    additional_inputs=[
        gr.Textbox(value="You are a friendly Chatbot.", label="System message"),
        gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens"),
        gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(minimum=0.1, maximum=1.0, value=0.95, step=0.05, label="Top-p"),
    ],
)

if __name__ == "__main__":
    demo.launch()
