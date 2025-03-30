# 🚀 ChatBot Toolkit  
The **ChatBot Toolkit** is designed for **rapid development** of chatbots, ranging from **basic to advanced** implementations.  

This toolkit provides **plug-and-play modules** that streamline chatbot development, making the process **faster, more efficient, and scalable**. By using pre-built, reusable components, we:  

✅ Reduce development time ⏳  
✅ Improve code quality 🔥  
✅ Minimize errors from rushed coding 💡  

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
2. `OPENAI_API_BASE` → Specifies OpenRouter as the API endpoint (since LangChain doesn’t support it natively).  

#### 🔹 **LangSmith Tracing Variables** (For monitoring LLM behavior)  
3. `LANGSMITH_API_KEY` → API key for LangSmith, enabling tracing.  
4. `LANGSMITH_TRACING` → Enables/disables LangSmith tracing. (`true` = enabled)  
5. `LANGSMITH_ENDPOINT` → API endpoint for sending tracing data.  
6. `LANGSMITH_PROJECT` → Project name under which traces will be logged.  

---

This setup ensures **secure authentication** and enables **tracing capabilities** while keeping sensitive credentials **out of the codebase**.  

---