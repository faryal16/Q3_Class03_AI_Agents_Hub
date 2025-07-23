# main.py
import chainlit as cl
from product_suggester import product_intro, handle_product_message
from mood_handoff import mood_intro, handle_mood_message
from country_info_toolkit import country_intro, handle_country_info_message

# 🎬 On Chat Start
@cl.on_chat_start
async def start():
    await cl.Message(
        content="""
# 🤖AI Agent Assignment Hub

Explore different projects powered by specialized AI agents.\n

---
"""
    ).send()

    await show_main_menu()


async def show_main_menu():
    await cl.Message(
        content="## 🧭 Choose a Project Below:",
        actions=[
            cl.Action(name="menu_choice", label="🛒 OTC Product Suggester", style="primary", payload={"value": "product"}),
            cl.Action(name="menu_choice", label="💬 Mood Analyzer", style="primary", payload={"value": "mood"}),
            cl.Action(name="menu_choice", label="🌍 Country Info Assistant", style="primary", payload={"value": "country"}),
        ]
    ).send()


# 🔀 Menu Selection Handler
@cl.action_callback("menu_choice")
async def handle_menu_choice(action: cl.Action):
    choice = action.payload["value"]
    last_mode = cl.user_session.get("last_mode")

    if choice == "menu":
        await show_main_menu()
        return

    # if choice != last_mode:
    #     await cl.Message(content="🔄 Switching to selected tool...").send()

    cl.user_session.set("mode", choice)
    # cl.user_session.set("last_mode", choice)

    if choice == "product":
        await product_intro()
    elif choice == "mood":
        await mood_intro()
    elif choice == "country":
        await country_intro()



# 💬 Main Message Handler
@cl.on_message
async def main_handler(msg: cl.Message):
    mode = cl.user_session.get("mode")

    if mode == "product":
        await handle_product_message(msg)
    elif mode == "mood":
        await handle_mood_message(msg)
    elif mode == "country":
        await handle_country_info_message(msg)
    else:
        await cl.Message(
            content="⚠️ Please select a project from the menu first."
        ).send()
