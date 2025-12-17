import streamlit as st
import openai
import os
from dotenv import load_dotenv
from prompts import build_prompt

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="PersonaWrite", layout="centered")

st.title("✉️ PersonaWrite – Personality-Based Email Rewriter")
st.write(
    "Rewrite emails using personality traits or your own writing style using prompt-engineered GenAI."
)

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

if st.button("Rewrite Email"):
    if not email_text.strip():
        st.warning("Please enter an email.")
    else:
        system_prompt, user_prompt = build_prompt(
            email_text,
            personality,
            formality,
            politeness,
            custom_style_sample
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=300
        )

        st.subheader("Rewritten Email")
        st.write(response.choices[0].message["content"])
