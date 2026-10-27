# 🚀 Days of GenAI with Python

Welcome to my **Days of GenAI with Python** repository! This repo documents my daily hands-on journey learning Generative AI engineering, from foundational API calls and prompt engineering to building production-grade LLM applications with memory, databases, and modern frameworks.

---

## 🛠️ Tech Stack & Tools Mastered
- **Languages:** Python
- **LLM Providers & APIs:** Google Gemini (`langchain-google-genai`), Groq (`ChatGroq`)
- **Orchestration & Frameworks:** LangChain (LCEL), LangGraph
- **State & Memory Management:** Streamlit Session State, SQLite, LangChain Message Histories
- **Frontend / UI:** Streamlit

---

## 📅 Daily Progress Tracker

| Day | Topic / Project Focus | Key Concepts Learned |
| :--- | :--- | :--- |
| **Day 1** | *Introduction to LLM APIs* | Setting up API keys, environment variables (`.env`), and making basic completion calls. |
| **Day 2** | *Prompt Engineering & Templates* | Using ChatPromptTemplate, system/human messages, and formatting dynamic inputs. |
| **Day 3** | *Building Streamlit Web Apps* | Creating interactive UIs and managing chat UI rendering. |
| **Day 4** | *Chatbot Memory & Context* | Moving from stateless LLMs to state management using `st.session_state` and LangChain memory. |
| **Day 5** | *Production Memory (SQLite + LCEL)* | Implementing database-backed conversation persistence with `RunnableWithMessageHistory` and SQLite (`chat.db`). |
| **Day 6-21** | *Coming Soon...* | *Advanced RAG, Agents, Vector Databases, and LangGraph workflows.* |

---

## 💡 Key Architectural Takeaways

Throughout this journey, I focused on understanding **why** production systems are built a certain way:
1. **Stateless to Stateful:** LLMs don't remember past turns by default. We must inject chat history into prompt templates using `MessagesPlaceholder`.
2. **Production-Grade Memory:** Local RAM state (`st.session_state`) wipes out on page refreshes. Real production systems use database-backed persistence (like PostgreSQL or SQLite via `RunnableWithMessageHistory`) to survive server reboots and scale horizontally.
3. **Modern LCEL:** Transitioning away from legacy chains (`ConversationChain`) toward explicit LangChain Expression Language (LCEL) pipelines using the pipe (`|`) operator.

---

## 🚀 How to Run Any Day's Code

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR-USERNAME/21-days-of-Gen-AI-With-Python.git](https://github.com/YOUR-USERNAME/21-days-of-Gen-AI-With-Python.git)
   cd 21-days-of-Gen-AI-With-Python
