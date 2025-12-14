# 🦖 Digital Dinosaur AI

![Python Version](https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12-blue)
![Framework](https://img.shields.io/badge/Backend-Flask-green)
![AI](https://img.shields.io/badge/AI-OpenAI%20GPT--4o-orange)
![Database](https://img.shields.io/badge/Vector%20DB-ChromaDB-purple)

## 📖 Project Overview

**Digital Dinosaur AI** is an interactive virtual companion powered by Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG). Unlike traditional virtual pets with pre-scripted dialogues, this Dino possesses **long-term memory**, **dynamic personality**, and **emotional intelligence**.

This project demonstrates the integration of **game state management** (Hunger, Mood, Affinity) with **generative AI**, allowing the pet to remember past interactions and react dynamically to the user's care—or neglect.

### ✨ Key Features

- **🧠 Long-Term Memory (RAG):** Powered by **ChromaDB**, the Dino remembers facts you told it (e.g., your name, favorite food) and references them in future conversations.
- **🌍 Worldview Consistency:** The Dino has a consistent worldview setting that shapes how it interprets and responds to everything. It maintains character consistency throughout conversations.
- **🎭 Dynamic Persona:** The AI's tone changes based on game stats (Hunger, Mood, Time of Day). A hungry Dino is grumpy; a well-fed one is cheerful.
- **🕰️ Simulated Time System:** Includes a Day/Night cycle. Waking the Dino up at night has consequences!
- **❤️ Relationship Evolution:** Affinity levels determine how intimate or cold the Dino acts towards you.

---

## ⚠️ Prerequisites

Due to dependency compatibility with **ChromaDB** and **NumPy**, this project **strictly requires**:

- **Python 3.10, 3.11, or 3.12**
- ❌ **DO NOT use Python 3.13 or 3.14** (Will cause build errors during installation).

You also need an **OpenAI API Key**.

---

## 🚀 Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone <YOUR_REPO_URL>
cd Project_Digital_Dinosaur_AI
```

### 2. Create a Virtual Environment (Recommended)

It is highly recommended to use a virtual environment to manage dependencies.

**Windows:**

```bash
# Ensure you are using Python 3.12 or lower
py -3.12 -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add your OpenAI API Key:

```ini
# .env file
API_KEY=your_api_key_here
BASE_URL=your_base_url_here
MODEL=your_model_name_here
```

### 5. (Optional) Customize Worldview Settings

The Dino has a default worldview that defines its background, knowledge, and personality. You can customize it by:

1. Copy the example file:

```bash
cp worldview.json.example worldview.json
```

2. Edit `worldview.json` to customize:
   - World background and lore
   - Character background and beliefs
   - Rules and limitations
   - Knowledge base (what the Dino knows/doesn't know)
   - Speech patterns
   - Personality traits

The worldview ensures the Dino maintains consistent character behavior and interprets everything through its unique perspective.

### 6. Run the Application

```bash
python run.py
```

The application will be available at `http://127.0.0.1:5000` in your web browser.

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API)
- **Backend:** Python (Flask)
- **AI Engine:** OpenAI API
- **Memory/Database:** ChromaDB (Vector Search)

## 👨‍💻 Contributors

Xingyi Shen

Zhichuan Jing

Juandan Luo

Zekai Gong
