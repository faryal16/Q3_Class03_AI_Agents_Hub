# 🤖 AI Agent Assignment Hub

[![🚀 Live Demo on Railway](https://img.shields.io/badge/Demo-Railway-purple?style=for-the-badge&logo=railway)](https://ai-agent-assignment-hub.up.railway.app)

Welcome to the **AI Agent Assignment Hub** — a Chainlit-based chatbot application showcasing multiple specialized AI agents. Users can interact with various tools such as a product recommender, mood analyzer, and country info assistant — all in one seamless interface.

---

## 🧰 Features

- 🛒 **OTC Product Suggester**  
  Suggests over-the-counter products based on user symptoms or health concerns.

- 💬 **Mood Analyzer**  
  Analyzes user input to detect their emotional tone and respond empathetically.

- 🌍 **Country Info Assistant**  
  Provides factual details such as capital cities, languages, and population data for any country.

- 🧭 **Central Menu Navigation**  
  A unified menu lets users switch between tools easily without cluttering the chat interface.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- `chainlit` SDK
- `dotenv`
- API keys (if any tools use external APIs like OpenAI or Gemini)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/ai-agent-assignment-hub.git
   cd ai-agent-assignment-hub

### 2. Create a .env file:

```env

GEMINI_API_KEY=your-api-key-here
```
### 3. Run the app:

```bash

chainlit run main.py -w
```

## 📁 Project Structure
```bash

.
├── main.py                        # Central router and UI logic
├── product_suggester.py          # Product tool: health-related suggestions
├── mood_handoff.py               # Mood detection and response logic
├── country_info_toolkit.py       # Country-related information toolkit

└── .env                          # API credentia(not committed)
```
## 🎨 UI/UX Highlights
- Styled action buttons for better visual feedback

- Clean screen flow with section dividers (---)

- Easy navigation back to the main menu

- Each tool introduces itself with an onboarding message

## 📌 To-Do / Enhancements
- Add tool icons or emojis inline with responses

- Cache previous tool results to speed up switching

- Add streaming responses for real-time interaction

- Add support for more tools (e.g., weather, finance)

## 🙌 Credits
Built with ❤️ using Chainlit and OpenAI/Gemini APIs.

## 📄 License
This project is licensed under the MIT License. Feel free to fork and build on it!


