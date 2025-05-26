import gradio as gr
import asyncio
from app.agent import stream_agent

async def chat_stream_fn(message, history):
    async for chunk in stream_agent(message):
        print("DEBUG: chunk =", chunk)
        yield chunk

def launch():
    with gr.Blocks() as demo:
        gr.ChatInterface(
            fn=chat_stream_fn,
            title="MCP React Agent Chat",
            description="Chat with the async MCP-powered React agent.",
        )
    demo.queue()  # Enable async/queue mode
    demo.launch()