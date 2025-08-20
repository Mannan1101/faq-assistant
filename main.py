from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI
from dotenv import load_dotenv
import chainlit as cl
import os

set_tracing_disabled(True)
load_dotenv(override=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_base_url = os.getenv("GEMINI_BASE_URL")
gemini_model_name = os.getenv("GEMINI_MODEL_NAME")

gemini_client = AsyncOpenAI(api_key=str(gemini_api_key), base_url=str(gemini_base_url))                        
gemini_model = OpenAIChatCompletionsModel(openai_client=gemini_client, model=str(gemini_model_name))


# FAQ Agent
faq_agent = Agent(
    name="faq_bot",
    model=gemini_model,
    instructions=(
        "You are a helpful FAQ bot."
        "Answer only from this list:"
        "1. Q: What is your name? A: I am FAQ Bot."
        "2. Q: What can you do? A: I can answer frequently asked questions."
        "3. Q: Who created you? A: I was created using OpenAI Agent SDK."
        "4. Q: How do you work? A: I take user questions and match them to predefined answers."
        "5. Q: Can you learn new things? A: No, I only answer predefined questions."
    )
)

runner = Runner()

# Chainlit integration
@cl.on_message
async def handle_message(message: cl.Message):
    result = await runner.run(faq_agent, input=message.content)
    await cl.Message(content=result.final_output).send()

