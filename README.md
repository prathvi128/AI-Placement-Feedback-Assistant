# 🎯 AI-Placement-Feedback-Assistant

An AI-powered interview preparation platform that helps students become placement-ready through role-based interview questions, automated answer evaluation, and personalized feedback.

## ✨ Features

- 🤖 **AI Question Generation** – Generate technical interview questions based on your target job role.
- ✍️ **Custom Questions** – Practice using your own interview questions.
- 📊 **Answer Evaluation** – Get AI-powered scores out of 10.
- 🔍 **Answer Analysis** – Identify strengths and weaknesses in your responses.
- 💡 **Personalized Feedback** – Receive suggestions to improve your answers.
- 📄 **Evaluation Reports** – Download detailed performance reports.
- 📈 **Performance Dashboard** – Track your completed evaluations.

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- LangGraph
- OpenRouter
- LangSmith

## 🏗️ Workflow

text

```text
START
  |
  v
Analyze Answer
  |
  v
Evaluate Answer
  |
  v
Conditional Routing
  |
  +---- Score < 7 ----> Generate Feedback
  |                            |
  +---- Score >= 7 ------------+
                               |
                               v
                       Generate Report
                               |
                               v
                              END
```

## ⚙️ Installation & Setup

**1\. Clone the repository**

bash

```bash
git clone https://github.com/prathvi128/AI-Placement-Feedback-Assistant.git
cd AI-Placement-Feedback-Assistant
```

**2\. Install dependencies**

bash

```bash
pip install -r requirements.txt
```

**3\. Configure environment variables**

Create a `.env` file:

env

```env
OPENROUTER_API_KEY=your_api_key_here
```

**4\. Run the application**

bash

```bash
streamlit run app.py
```


⭐ If you find this project useful, don't forget to give it a star\!

**Practice. Evaluate. Improve. Get Placement Ready. 🚀**

_PlacementAI is an educational tool. AI-generated evaluations are intended for interview practice and do not represent official hiring decisions._
