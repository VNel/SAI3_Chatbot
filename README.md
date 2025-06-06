# 🛡️ Cybersecurity RAG Chatbot

# Introduction

A context-based chatbot designed to answer specialized cybersecurity questions based on **500+ scientific cybersecurity articles** (in text format). It provides **quick, fact-based answers** – solely grounded in the available documents.

---

# 📌 Project Team

This project was created as part of a module at the Bern University of Applied Sciences by:

* Carlos Gomez
* Nelson Vidovic
* Lirim Zahiri
* Mouad Medini
* Niklaus Joel

---

# ✅ Prerequisites (one-time setup)

## 1. 🔧 Install Python (version 3.9 or higher)

* Official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
* During setup, **enable "Add Python to PATH"**
* Then verify installation in your terminal:

```bash
python --version
```

## 2. 🧑🏽‍💻 Create a Together.ai Account

1. Go to [https://www.together.ai](https://www.together.ai).
2. Click "Sign Up" and register (no credit card needed).
3. After logging in, go to your dashboard at [https://api.together.ai](https://api.together.ai).
4. Navigate to "API Keys" (bottom-left corner).
5. Click "Create new API key", give it a name (e.g. chatbot-key), and copy the key.
6. Save the key securely.
7. This key is free, but subject to rate limits (e.g. \~50 requests/min, \~200,000 tokens/day).

---

# 🔧 Setup – Step by Step

# !For the following steps use CMD (Windows) / Terminal (Mac)!

## 1. 📁 Clone the Project

```bash
git clone https://github.com/VNel/SAI3_Chatbot.git
cd SAI3_Chatbot/online_chatbot
```

## 2. 🪪 Set Up Virtual Environment 

* **Windows:**

```bash
py -m venv venv
```

* **macOS/Linux:**

```bash
python -m venv venv
```

### Then activate:

* **Windows:**

```bash
venv\Scripts\activate.bat
```

* **macOS:**

```bash
source venv/bin/activate
```

---

## 3. 📦 Install Required Dependencies

```bash
pip install -r requirements.txt
```

### `requirements.txt` content:

```text
fastapi
uvicorn
requests
gradio
python-dotenv
faiss-cpu
sentence-transformers
numpy
faiss-cpu
```

---

## 4. 🔐 Add Your API Key

1. Select the file `.env.template`
2. Rename it to `.env`
3. Then open `.env` and insert your API key:

```env
TOGETHER_API_KEY=<your_api_key>
```

> Without `.env`, the chatbot cannot communicate with Together.ai.

---

## 5. 📚 Prepare Vector Database

* **Windows:**
```bash
py load_data.py
```
* **macOS:**
```bash
python load_data.py
```

* Creates `documents.json` (text chunks)

* **Windows:**
```bash
py build_index.py
```
* **macOS:**
```bash
python build_index.py
```

* Creates `index.faiss` (semantic search index)

---

## 6. 🚀 Launch Web Interface
* **Windows:**
```bash
py web_ui.py
```
* **macOS:**
```bash
python web_ui.py
```

Automatically opens:
[http://localhost:7860](http://localhost:7860)

---

# 💬 Features

* Ask questions in German or English
* Answers are based **only on local documents**
* No hallucination
* Transparent source citation for each answer
* If no relevant info is found → clear feedback

---

# 🔒 Security & Privacy

| Item                       | Status |
| -------------------------- | ------ |
| API key remains local      | ✅      |
| No cloud storage           | ✅      |
| No login required          | ✅      |
| Local access via localhost | ✅      |

---

# ✅ All Set! – Functionality Checklist

| Requirement                     | ✅ |
| ------------------------------- | - |
| Python 3.9 or higher installed  | ✅ |
| Virtual environment active      | ✅ |
| `pip install` successful        | ✅ |
| `.env` with API key present     | ✅ |
| `load_data.py` ran successfully | ✅ |
| `build_index.py` successful     | ✅ |
| `web_ui.py` started             | ✅ |

---

# 📂 Folder Structure (excerpt)

```bash
├── clean_data/               # 500 cybersecurity articles (.txt)
├── vectorstore/             # Vector DB (auto-generated)
│   ├── documents.json
│   └── index.faiss
├── .env                     # (created by you)
├── load_data.py             # Process texts
├── build_index.py           # Create FAISS index
├── query_pipeline.py        # Retrieval logic
├── llm_api.py               # Together.ai API integration
├── web_ui.py                # Launch web interface
├── requirements.txt         # Python dependencies
└── README.md                # This guide
```

---

# 📌 Note

This project is solely intended for **research and educational purposes** within the Business Information Technology program. It is **not** intended for production or commercial use.
