import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
from prompts import build_prompt

# Load environment variables (for local use)
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="PersonaWrite", layout="centered")

st.title("✉️ PersonaWrite – Personality-Based Email Rewriter")
st.write(
    "Rewrite emails using personality traits or your own writing style "
    "using prompt-engineered GenAI (free, no training)."
)

# ---------------- UI ---------------- #

email_text = st.text_area(
    "Original Email",
    placeholder="Paste your email here...",
    height=150
)

personality = st.selectbox(
    "Personality Style",
    [
        "Professional & Formal",
        "Polite & Agreeable",
        "Assertive & Confident",
        "Friendly & Warm",
        "Custom – Write in My Tone"
    ]
)

custom_style_sample = ""
if personality == "Custom – Write in My Tone":
    custom_style_sample = st.text_area(
        "Your Writing Style Sample",
        placeholder="Paste a paragraph or email written by you...",
        height=120
    )

formality = st.slider("Formality Level", 1, 5, 3)
politeness = st.slider("Politeness Level", 1, 5, 3)
temperature = st.slider("Creativity (Temperature)", 0.0, 1.0, 0.5, 0.1)

# Prevent multiple API calls on rerun
if "last_output" not in st.session_state:
    st.session_state.last_output = ""

# ---------------- ACTION ---------------- #

if st.button("Rewrite Email"):
    if not email_text.strip():
        st.warning("Please enter an email.")
    else:
        with st.spinner("Rewriting email..."):
            system_prompt, user_prompt = build_prompt(
                email_text,
                personality,
                formality,
                politeness,
                custom_style_sample if custom_style_sample.strip() else None
            )

            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",  # ✅ CURRENTLY SUPPORTED
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=float(temperature),
                    max_tokens=300
                )

                st.session_state.last_output = (
                    response.choices[0].message.content
                )

            except Exception as e:
                st.error("Error while generating response")
                st.exception(e)

# ---------------- OUTPUT ---------------- #

st.subheader("Rewritten Email")
st.write(st.session_state.last_output)
