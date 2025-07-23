import os
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
import chainlit as cl

from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.tool import function_tool

# 🔐 Load environment
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise EnvironmentError("❌ GEMINI_API_KEY not found in .env file.")

# 🔗 Gemini-compatible client setup
provider = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=provider
)

config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

# 🌍 Translate any input to English
def normalize_input(user_input: str) -> str:
    try:
        return GoogleTranslator(source="auto", target="en").translate(user_input)
    except Exception as e:
        print(f"Translation error: {e}")
        return user_input  # fallback if translation fails

# 🧠 OTC product suggestion tool
@function_tool
def suggest_product(symptom: str) -> str:
    symptom = symptom.lower()
    suggestions = {
        "headache": "💊 You might try ibuprofen or paracetamol.",
        "fever": "🌡️ Paracetamol or ibuprofen can help reduce fever.",
        "vomiting": "🤢 Try an antiemetic like dimenhydrinate (Gravol) or consult a pharmacist.",
        "bloating": "😣 Simethicone (Gas-X) or activated charcoal may help with bloating.",
        "toothache": "🦷 You can use a topical anesthetic gel like Orajel or take ibuprofen for pain.",
        "foot pain": "🦶 Ibuprofen or a topical pain relief cream may help with foot pain.",
        "stomach ache": "🤒 Antacids like Pepto-Bismol or omeprazole can be useful.",
    }

    for key in suggestions:
        if key in symptom:
            return suggestions[key]

    return f"For '**{symptom}**', you might try a common OTC product like paracetamol. If symptoms continue, please consult a healthcare provider. 🩺"

# 💬 Agent setup
agent = Agent(
    name="Smart Store Assistant 🛒",
    instructions=(
        "You're a helpful health assistant. When a user describes symptoms (e.g., 'fever', 'headache'), "
        "call the `suggest_product` tool with that symptom."
    ),
    tools=[suggest_product],
    model=model,
)

# ✅ Intro message
async def product_intro():
    await cl.Message(
        content=(
            "## 👋 Welcome to Smart Store Assistant!\n"
            "I’m your virtual health helper. Just tell me how you're feeling, and I’ll suggest an OTC product that might help.\n\n"
            "**You can try messages like:**\n"
            "- 🤕 *I have a headache*\n"
            "- 🤢 *I'm vomiting a lot*\n"
            "- 🤧 *I feel bloated and uncomfortable*\n\n"
            "💬 **Go ahead — type your symptom below!**"
        )
    ).send()
    
    

# 🔁 Handle messages routed by main
async def handle_product_message(msg: cl.Message):
    user_input = msg.content

    thinking_msg = await cl.Message(content="⏳ Let me check the best suggestion for you...").send()

    symptom = normalize_input(user_input)
    try:
        result = await Runner.run(agent, input=symptom, run_config=config)
        await thinking_msg.remove()

        await cl.Message(
            content=f"✅ **Suggestion:**\n{result.final_output.strip()}"
        ).send()

    except Exception as e:
        await thinking_msg.remove()
        await cl.Message(
            content=f"⚠️ **Oops! Something went wrong:**\n```{str(e)}```"
        ).send()
        
        
    await cl.Message(
    content="🛒 Product Suggester Ready! What symptom are you experiencing?",
    actions=[
        cl.Action(name="menu_choice", label="🔙 Back to Menu", payload={"value": "menu"})
    ]
    ).send()
             

# 🚀 Entry point for main.py
async def run_suggest_product():
    cl.user_session.set("mode", "product")
    await product_intro()
