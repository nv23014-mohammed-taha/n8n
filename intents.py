from openai import OpenAI

client = OpenAI(api_key=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)

def detect_intent(text):

    prompt = f"""
    Identify intent:
    - book_appointment
    - reschedule
    - cancel
    - inquiry

    Extract name, date, time if available.

    Text: {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
