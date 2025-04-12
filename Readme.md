# 🚀 ChatBot Toolkit

The **ChatBot Toolkit** is designed for **rapid development** of LLM-powered chatbot applications — from simple chat interfaces to advanced RAG systems and agentic workflows using tools.

This toolkit provides **plug-and-play modules** that streamline chatbot and LLM application development, making the process **faster, more efficient, and scalable**. By using pre-built, reusable components, we:  

✅ Reduce development time ⏳  
✅ Improve code quality 🔥  
✅ Minimize errors from rushed coding 💡  

---

## 🧰 What's Inside?

This repository is a **modular toolkit** with multiple standalone modules to help you build LLM-based systems, including:

- `/chatbot_toolkit/chatbot` – Basic to advanced chatbot frameworks 🤖  
- `/chatbot_toolkit/rag` – Retrieval-Augmented Generation pipelines 📚  
- `/chatbot_toolkit/tools` – Agentic workflows with tool integration 🛠️  

Each module is **self-contained**, extensible, and designed to be used individually or combined together.

---

## 🌍 Environment Variables Setup

To ensure smooth operation, the project requires certain **environment variables**. These should be stored in a `.env` file at the root of the project.

### 📌 **.env File Structure**

Create a `.env` file in the project root and add the following:

```ini
# 🔹 OpenRouter API Configuration  
OPENAI_API_KEY="your_openrouter_api_key_here"  
OPENAI_API_BASE="https://openrouter.ai/api/v1"  

# 🔹 LangSmith Tracing (for debugging & monitoring model behavior)  
LANGSMITH_API_KEY="your_langsmith_api_key_here"  
LANGSMITH_TRACING="true"  
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"  
LANGSMITH_PROJECT="your_project_name_here"
```

### 🔍 **Explanation of Variables**

#### 🔹 **OpenRouter API Variables**  
1. `OPENAI_API_KEY` → API key for authentication with OpenRouter.  
2. `OPENAI_API_BASE` → Specifies OpenRouter as the API endpoint (LangChain doesn’t support it natively).

#### 🔹 **LangSmith Tracing Variables**  
3. `LANGSMITH_API_KEY` → API key for LangSmith to enable tracing.  
4. `LANGSMITH_TRACING` → Enables/disables LangSmith tracing. (`true` = enabled)  
5. `LANGSMITH_ENDPOINT` → Endpoint for sending trace data.  
6. `LANGSMITH_PROJECT` → Your project name in LangSmith.

---

## 🐳 Docker Setup (Dev Environment)

The toolkit includes a **Dockerized development environment** to simplify setup.  
After launching the container, you can manually run any module you'd like to work on.

### ⚙️ **Quick Start**

1. **Build the Docker image**

```bash
docker build -t chatbot .
```

2. **Start the container using Docker Compose**

```bash
docker-compose up
```

> ✅ Make sure your `.env` file is in the root directory before starting.

---

### 🧪 Running a Module

Once the container is up and running:

```bash
# Access the container
docker exec -it <container_name_or_id> /bin/bash

# Run a specific module using its test script
python3 /chatbot_toolkit/chatbot/test.py   # 🔹 ChatBot module  
python3 /chatbot_toolkit/rag/test.py       # 🔹 RAG module  
python3 /chatbot_toolkit/tools/test.py     # 🔹 Agentic tools module
```

Each module is designed to be:

- **Plug-and-play**
- **Easy to extend**
- **Useful for real-world LLM apps**

---

## 📦 Benefits of the Toolkit

✨ Rapid prototyping of LLM-powered apps  
🧩 Modular architecture for flexibility  
🐳 Dev-containerized for easy onboarding  
📈 Production-ready with LangSmith tracing support  
🔐 Secure & clean separation of environment variables

---

## 📬 Contributions

Want to add a new module or improve an existing one? PRs are welcome! Please follow the modular design style and keep `test.py` as the entry point for new components.