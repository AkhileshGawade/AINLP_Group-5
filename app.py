import gradio as gr
import openai
import os
from dotenv import load_dotenv
from prompts import build_prompt

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def rewrite_email(
    email_text,
    personality,
    formality,
    politeness,
    temperature,
    custom_style_sample
):
    if not email_text.strip():
        return "Please enter an email to rewrite."

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

    return response.choices[0].message["content"]


with gr.Blocks(title="PersonaWrite – Personality-Based Email Rewriter") as demo:
    gr.Markdown("## ✉️ PersonaWrite")
    gr.Markdown(
        "A prompt-engineered GenAI system to rewrite emails based on personality traits and custom writing style."
    )

    email_input = gr.Textbox(
        label="Original Email",
        placeholder="Paste your email here...",
        lines=6
    )

    personality = gr.Dropdown(
        choices=[
            "Professional & Formal",
            "Polite & Agreeable",
            "Assertive & Confident",
            "Friendly & Warm",
            "Custom – Write in My Tone"
        ],
        value="Professional & Formal",
        label="Personality Style"
    )

    custom_style = gr.Textbox(
        label="Your Writing Style Sample (Only for Custom Tone)",
        placeholder="Paste a paragraph or email written by you...",
        lines=4
    )

    formality = gr.Slider(
        minimum=1,
        maximum=5,
        value=3,
        step=1,
        label="Formality Level"
    )

    politeness = gr.Slider(
        minimum=1,
        maximum=5,
        value=3,
        step=1,
        label="Politeness Level"
    )

    temperature = gr.Slider(
        minimum=0.0,
        maximum=1.0,
        value=0.5,
        step=0.1,
        label="Creativity (Temperature)"
    )

    rewrite_button = gr.Button("Rewrite Email")

    output = gr.Textbox(
        label="Rewritten Email",
        lines=6
    )

    rewrite_button.click(
        fn=rewrite_email,
        inputs=[
            email_input,
            personality,
            formality,
            politeness,
            temperature,
            custom_style
        ],
        outputs=output
    )

demo.launch()
