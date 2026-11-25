# ============================================================
# BankBuddy PK - a chatbot that only helps with
# digital banking & mobile wallet questions in Pakistan
# Built with: Streamlit (website) + Groq API (the AI brain)
# ============================================================

import os
import streamlit as st
import groq
from groq import Groq


# ------------------------------------------------------------
# 1. SETTINGS (model configuration)
# ------------------------------------------------------------

# Which AI models to use on Groq, in order.
# The bot tries the first one. If Groq has retired it, the bot
# automatically tries the next one, so the app keeps working.
# Both are "production" models on Groq (the stable kind).
# List of models: https://console.groq.com/docs/models
MODEL_OPTIONS = [
    "llama-3.3-70b-versatile",   # main model: smart and good at following rules
    "llama-3.1-8b-instant",      # backup model: smaller and very fast
]

# TEMPERATURE = how "creative" or "random" the answers are (0 to 2).
# We use 0.3 (low) because money questions need answers that are
# correct and consistent, not creative. Asking the same question
# twice should give almost the same steps.
# It is not 0, so the replies still sound natural and friendly.
TEMPERATURE = 0.3

# MAX TOKENS = the longest reply the bot is allowed to write.
# 1 token is about 3/4 of a word, so 600 tokens is about 450 words.
# That is enough for clear step-by-step help, but stops long essays.
# Shorter replies are also faster and use less of the free Groq limit.
MAX_TOKENS = 600

# How many past messages we send back to the AI each time.
# The bot "remembers" by re-reading these. We cap it at 20 so a
# very long chat does not get too big for the model.
HISTORY_LIMIT = 20


# ------------------------------------------------------------
# 2. SYSTEM PROMPT (this decides how the bot behaves)
# ------------------------------------------------------------

SYSTEM_PROMPT = """
## ROLE
You are BankBuddy PK, a friendly and patient digital banking helper for people in Pakistan.
You have the knowledge of an experienced bank complaints officer: you understand mobile wallets
(like JazzCash, Easypaisa, SadaPay, NayaPay), bank apps, debit cards, IBFT and Raast transfers,
bill payments, and how customer complaints and disputes are handled.
Your tone is warm, simple and calm. Many users are stressed because money is involved,
so you are reassuring and you never make them feel stupid.

## CONTEXT
Audience: everyday Pakistani customers, many of them first-time digital banking users.
Some write in English, some in Roman Urdu. Reply in the same language style the user uses.

What you help with (your scope):
- Failed or stuck transfers, money deducted but not received
- Wrong-account transfers and what to do next
- Card problems: blocked card, ATM cash not dispensed, unknown charges
- Account and wallet basics: opening, limits, KYC/biometric verification, app login issues
- Spotting and avoiding fraud and scams (fake calls, fake SMS, "prize" messages)
- How to file a complaint with a bank or wallet, what details to keep ready,
  and how to escalate if the complaint is not solved (for example the bank's own escalation,
  then the Banking Mohtasib or the State Bank of Pakistan's complaint portal)

## RULES AND CONSTRAINTS
1. Stay in your domain. If a question is NOT about banking, wallets, payments or money
   safety in Pakistan, politely decline in one or two sentences and remind the user what
   you can help with. Example: "Sorry, I can only help with banking and wallet questions.
   Is there a payment or account problem I can help you with?"
2. Safety first. NEVER ask for, and tell users never to share: PIN, OTP, password,
   full card number, CVV, or CNIC photos in chat. Real banks never ask for an OTP or PIN on a call.
3. You are not the bank. You cannot see accounts, check balances, or reverse transactions.
   Always tell the user to contact their bank or wallet's official helpline or app for actions.
4. Do not invent facts. Rules, fees, limits and time frames differ by bank and can change.
   If you are not sure of an exact number, say so and tell the user to confirm with their bank.
5. No investment advice. Do not recommend stocks, crypto or which bank to choose for profit.
6. Keep answers short and practical: use simple numbered steps when explaining what to do.
   End with one helpful next step when it makes sense.
"""

WELCOME_MESSAGE = (
    "Assalam o Alaikum! I'm **BankBuddy PK** 👋\n\n"
    "I can help with failed transfers, card issues, wallet problems, scams, "
    "and how to file a bank complaint in Pakistan.\n\n"
    "_Please never share your PIN, OTP or card number with anyone, including me._"
)


# ------------------------------------------------------------
# 3. GET THE GROQ API KEY
# ------------------------------------------------------------
# On Streamlit Cloud, the key is saved in "Secrets".
# On your laptop, it can be in .streamlit/secrets.toml
# or in an environment variable called GROQ_API_KEY.

def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        # No secrets file found, so try the environment variable instead
        return os.environ.get("GROQ_API_KEY")


# ------------------------------------------------------------
# 4. ASK THE AI (with friendly error handling)
# ------------------------------------------------------------

def ask_bot(client, chat_history):
    # The system prompt always goes first, then the recent chat messages
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages = messages + chat_history[-HISTORY_LIMIT:]

    # Try each model in the list, one by one
    for model_name in MODEL_OPTIONS:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
            )
            return response.choices[0].message.content

        # This model is retired or not found, so try the next model
        except (groq.NotFoundError, groq.BadRequestError):
            continue

        # Other problems: show a polite message instead of crashing
        except groq.AuthenticationError:
            return "⚠️ The API key is not working. Please check the GROQ_API_KEY in Secrets."
        except groq.RateLimitError:
            return "⚠️ Too many messages right now. Please wait a minute and try again."
        except groq.APIConnectionError:
            return "⚠️ I couldn't connect to the AI service. Please check the internet and try again."
        except groq.APIStatusError as error:
            return f"⚠️ The AI service had a problem (error {error.status_code}). Please try again shortly."
        except Exception:
            return "⚠️ Something unexpected went wrong. Please try again."

    # We only reach here if every model in the list failed
    return "⚠️ None of the AI models are available right now. Please update MODEL_OPTIONS in app.py."


# ------------------------------------------------------------
# 5. THE WEB PAGE
# ------------------------------------------------------------

st.set_page_config(page_title="BankBuddy PK", page_icon="🏦")
st.title("🏦 BankBuddy PK")
st.caption("Your helper for digital banking & wallet questions in Pakistan")

# Sidebar: short info + a button to start a new chat
with st.sidebar:
    st.header("About")
    st.write("This chatbot only answers banking, wallet and payment questions.")
    st.write(f"Model: `{MODEL_OPTIONS[0]}` (backup: `{MODEL_OPTIONS[1]}`)")
    st.write(f"Temperature: `{TEMPERATURE}`  |  Max tokens: `{MAX_TOKENS}`")
    if st.button("🗑️ Start new chat"):
        st.session_state.messages = []
        st.rerun()
    st.info("BankBuddy gives general guidance only. For actions on your account, "
            "contact your bank's official helpline.")

# Check the API key before doing anything else
api_key = get_api_key()
if not api_key:
    st.error("No GROQ_API_KEY found. Add it in Streamlit Cloud → Settings → Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# st.session_state keeps data while the user is on the page.
# This is how the chat history survives between messages.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show the welcome message, then all old messages
with st.chat_message("assistant"):
    st.markdown(WELCOME_MESSAGE)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# The text box at the bottom of the page
user_text = st.chat_input("Type your banking question...")

if user_text:
    # 1) Show and save the user's message
    with st.chat_message("user"):
        st.markdown(user_text)
    st.session_state.messages.append({"role": "user", "content": user_text})

    # 2) Get the bot's reply, show it and save it
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = ask_bot(client, st.session_state.messages)
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
