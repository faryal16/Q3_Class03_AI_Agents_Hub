import chainlit as cl
from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv

load_dotenv()

# 🌐 API Setup
provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=provider
)

config = RunConfig(
    model=model,
    model_provider=provider
)

# 🤖 Agents
mood_detector = Agent(
    name="Mood Detector",
    instructions="Detect the user's mood (happy, sad, stressed, angry, excited) from their message. Return ONLY the mood as one word.",
    model=model
)

activity_suggester = Agent(
    name="Activity Suggester",
    instructions="Suggest a positive activity if the user is feeling sad or stressed. Be kind and empathetic.",
    model=model
)

# 📢 Intro message
async def mood_intro():
    await cl.Message(
        author="🎯 Mood Analyzer",
        content="""# 💬 Mood Analyzer with Agent Handoff
Welcome! Let me understand how you're feeling and give suggestions if needed.

**Please type your current feeling or emotion.**
"""
    ).send()
    
    await cl.Message(
    content="💬 Mood Analyzer Ready! How are you feeling today?",
    actions=[
        cl.Action(name="menu_choice", label="🔙 Back to Menu", payload={"value": "menu"})
    ]
    ).send()


# 📥 Handle User Input
async def handle_mood_message(msg: cl.Message):
    user_input = msg.content

    await cl.Message(author="🧠 Mood Detector", content="🔍 *Analyzing your mood...*").send()
    mood_result = await Runner.run(mood_detector, input=user_input, run_config=config)
    mood = mood_result.final_output.strip().lower()

    await cl.Message(
        author="🧠 Mood Detector",
        content=f"### 😌 Detected mood: **`{mood}`**"
    ).send()

    if mood in ["sad", "stressed"]:
        await cl.Message(author="🤝 Activity Coach", content="💡 *Thinking of something comforting for you...*").send()
        activity_result = await Runner.run(activity_suggester, input=f"I'm feeling {mood}", run_config=config)

        await cl.Message(
            author="🧘‍♀️ Activity Coach",
            content=f"""### 🌈 Suggestion for You:
{activity_result.final_output.strip()}"""
        ).send()
    else:
        await cl.Message(
            author="🎉 Mood Agent",
            content="🎉 You're doing great! Keep enjoying your awesome mood. 💖"
        ).send()


    await cl.Message(
    content="💬 Mood Analyzer Ready! How are you feeling today?",
    actions=[
        cl.Action(name="menu_choice", label="🔙 Back to Menu", payload={"value": "menu"})
    ]
    ).send()
    
# Optional: manual runner
async def run_mood_handoff():
    cl.user_session.set("mode", "mood")
    await mood_intro()
