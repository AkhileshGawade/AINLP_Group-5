def build_prompt(
    email_text,
    personality,
    formality_level,
    politeness_level,
    custom_style_sample=None
):
    # Case 1: Custom user tone (few-shot / in-context learning)
    if personality == "Custom – Write in My Tone" and custom_style_sample:
        system_prompt = f"""
You are an expert writing assistant.

The user has provided a sample of their personal writing style.
Carefully analyze the tone, sentence structure, word choice, and level of formality.

Rewrite the given email so that it closely matches the user's writing style.
Preserve the original intent and meaning.
Do NOT add new information.
Do NOT remove important details.

USER WRITING SAMPLE:
\"\"\"{custom_style_sample}\"\"\"
"""
    else:
        # Case 2: Predefined personality-based rewriting
        system_prompt = f"""
You are an expert email communication assistant.

Rewrite emails while strictly following these rules:
- Preserve the original intent and meaning
- Do NOT add new information
- Do NOT remove important details
- Adapt the tone based on personality and control settings

Personality style: {personality}
Formality level: {formality_level}/5
Politeness level: {politeness_level}/5

Personality guidelines:
- Polite & Agreeable: respectful, indirect, appreciative
- Assertive & Confident: direct, clear, leadership tone
- Friendly & Warm: conversational, approachable, empathetic
- Professional & Formal: structured, neutral, corporate tone
"""

    user_prompt = f"""
Rewrite the following email accordingly:

EMAIL:
\"\"\"{email_text}\"\"\"
"""

    return system_prompt, user_prompt
