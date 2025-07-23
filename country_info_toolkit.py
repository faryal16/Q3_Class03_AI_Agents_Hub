import chainlit as cl
from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv

load_dotenv()

# 🔧 Model Setup
provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=provider
)

config = RunConfig(model=model, model_provider=provider)

# 🌍 Country Capital Tool
capital_tool = Agent(
    name="Capital Finder",
    instructions="You are a capital expert. Given a country name, return its capital city only. Just the name, no explanation.",
    model=model
)

# 🗣️ Language Tool
language_tool = Agent(
    name="Language Finder",
    instructions="You are a language expert. Given a country name, return the official or primary language spoken. Just the name, no explanation.",
    model=model
)

# 👥 Population Tool
population_tool = Agent(
    name="Population Finder",
    instructions="You are a population expert. Given a country name, return the population as of the most recent estimate. Keep it short.",
    model=model
)

# 🧠 Orchestrator
orchestrator = Agent(
    name="Orchestrator",
    instructions="""
You are an orchestrator. Given a user query, decide which of the following 3 categories are being asked about:

- capital
- language
- population

Respond with one or more of these keywords as a comma-separated list. 
Do NOT explain. Just output: e.g., "capital, language", or "population"
""",
    model=model
)

# 🧭 Intro message
async def country_intro():
    await cl.Message(
        author="🌍 Country Info Bot",
        content="""# 🌐 Country Info Assistant
Ask me anything about a country's **capital**, **language**, or **population**.

Examples:
- What is the capital of Japan?
- Language spoken in Brazil?
- Population of Canada?
"""
    ).send()
    
    


# 📥 Message handler
async def handle_country_info_message(msg: cl.Message):
    question = msg.content.strip()

    await cl.Message("🤔 Figuring out what you want to know...").send()
    task_type_result = await Runner.run(orchestrator, input=question, run_config=config)
    task_types = [t.strip() for t in task_type_result.final_output.lower().split(",")]

    await cl.Message(f"🔍 You asked about: **{', '.join(task_types)}**").send()

    for task in task_types:
        if task == "capital":
            result = await Runner.run(capital_tool, input=question, run_config=config)
            await cl.Message(f"🏛️ Capital: **{result.final_output.strip()}**").send()

        elif task == "language":
            result = await Runner.run(language_tool, input=question, run_config=config)
            await cl.Message(f"🗣️ Language: **{result.final_output.strip()}**").send()

        elif task == "population":
            result = await Runner.run(population_tool, input=question, run_config=config)
            await cl.Message(f"👥 Population: **{result.final_output.strip()}**").send()

        else:
            await cl.Message(f"⚠️ Unrecognized task: `{task}`").send()

    await cl.Message(
    content="🌍 Country Info Ready! Ask about a country’s capital, language, or population.",
    actions=[
        cl.Action(name="menu_choice", label="🔙 Back to Menu", payload={"value": "menu"})
    ]
    ).send()
    
# Optional manual runner
async def run_country_info_toolkit():
    cl.user_session.set("mode", "country")
    await country_intro()
