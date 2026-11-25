# 🏦 BankBuddy PK: Digital Banking Helper Chatbot

A domain-specific chatbot that helps people in Pakistan with **digital banking and mobile wallet problems**: failed transfers, card issues, scams, and how to file and escalate a bank complaint.

Its behaviour comes mainly from a carefully designed **system prompt**. It runs on the **Groq API** and is deployed with **Streamlit Cloud**.

🔗 **Live app:** https://bank-buddy-chatbot.streamlit.app/

---

## 📌 Domain

**Digital banking & mobile wallets in Pakistan** (JazzCash, Easypaisa, SadaPay, NayaPay, bank apps, IBFT, Raast, debit cards).

- ✅ Answers: failed/stuck transfers, wrong-account transfers, ATM and card issues, wallet limits and KYC, fraud awareness, complaint and escalation steps
- ❌ Politely declines: anything else (recipes, coding, sports, general chat) and points the user back to banking topics

---

## 🧠 System Prompt Design

The prompt has three parts:

| Part | What it defines |
|---|---|
| **Role** | "BankBuddy PK", a friendly helper with the knowledge of an experienced bank complaints officer. Warm, calm, simple tone, because users are often stressed about money. |
| **Context** | Audience: everyday Pakistani customers, many new to digital banking, writing in English or Roman Urdu. Scope: the list of banking topics above. |
| **Rules / Constraints** | 1) Stay in domain, politely decline off-topic questions. 2) Never ask for PIN, OTP, password, card number or CVV, and warn users about scams. 3) It is not the bank: it can't see or reverse transactions. 4) Don't invent fees, limits or time frames. 5) No investment advice. 6) Short, numbered, practical steps. |

The full prompt is in `app.py` (`SYSTEM_PROMPT`).

---

## ⚙️ Model Configuration

| Setting | Value | Why |
|---|---|---|
| **Models** | `llama-3.3-70b-versatile`, backup `llama-3.1-8b-instant` | Both are stable "production" models on Groq. If the main model is ever retired, the app automatically switches to the backup, so it keeps working. |
| **Temperature** | `0.3` | Low temperature gives accurate, consistent answers. For money problems we want the same correct steps every time, not creative ones. It is not 0, so replies still sound natural and friendly. |
| **Max tokens** | `600` | About 450 words: enough for a clear step-by-step answer, but it stops very long replies. Short replies are faster and use less of the free Groq limit. |
| **History limit** | last 20 messages | The bot remembers the conversation, but very long chats don't grow too big for the model. |

The notebook includes a test that compares temperature `0.3` with `1.2` on the same question.

---

## ✅ Features

- **Stays in its domain** and politely redirects off-topic questions
- **Remembers the conversation** across turns (`st.session_state`)
- **Handles API failures gracefully**: wrong key, rate limit, no internet and server errors all show a friendly message instead of crashing
- **Safety-first**: never asks for sensitive details and warns about OTP scams
- Replies in **English or Roman Urdu**, matching the user
- "Start new chat" button in the sidebar

---

## 📁 Project Files

| File | Purpose |
|---|---|
| `bankbuddy_chatbot.ipynb` | Step-by-step build and tests (normal question, memory, off-topic, safety, API failure, temperature comparison) |
| `app.py` | The Streamlit chatbot app |
| `requirements.txt` | Libraries needed (`streamlit`, `groq`) |
| `.gitignore` | Keeps the API key out of GitHub |

---

## 🚀 Run It on Your Computer (Windows)

```powershell
pip install -r requirements.txt
$env:GROQ_API_KEY = "your_key_here"
streamlit run app.py
```

Get a free API key at https://console.groq.com/keys

## ☁️ Deploy on Streamlit Cloud

1. Push this repo to GitHub.
2. Go to https://share.streamlit.io, click **Create app**, and pick this repo with `app.py` as the main file.
3. Open **Advanced settings → Secrets** and paste:
   ```toml
   GROQ_API_KEY = "your_key_here"
   ```
4. Click **Deploy** to get your public link.

---

⚠️ *BankBuddy PK gives general guidance only. It is not connected to any bank. For actions on your account, contact your bank's official helpline.*
