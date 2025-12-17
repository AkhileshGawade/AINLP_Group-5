def build_prompt(
    email_text,
    personality,
    formality_level,
    politeness_level,
    custom_style_sample=None
):
    # CASE 1: Custom user tone (in-context learning)
    if personality == "Custom – Write in My Tone" and custom_style_sample:
        system_prompt = f"""
You are an expert writing assistant.

The user has provided a sample of their personal writing style.
Analyze tone, sentence structure, vocabulary, and level of formality.

Rewrite the email so it closely matches the user's writing style.
Preserve the original meaning.
Do NOT add or remove information.

USER WRITING SAMPLE:
\"\"\"{custom_style_sample}\"\"\"
"""
    else:
        # CASE 2: Predefined personalities
        system_prompt = f"""
You are an expert email communication assistant.

Rewrite emails while following these rules:
- Preserve original intent and meaning
- Do NOT add new information
- Adapt tone based on personality and controls

Personality: {personality}
Formality level: {formality_level}/5
Politeness level: {politeness_level}/5

Personality guidelines:
- Professional & Formal: corporate, structured, neutral
- Polite & Agreeable: respectful, indirect, appreciative
- Assertive & Confident: direct, clear, leadership tone
- Friendly & Warm: conversational, empathetic
"""

    user_prompt = f"""
Rewrite the following email:

EMAIL:
\"\"\"{email_text}\"\"\"
"""

    return system_prompt, user_prompt
