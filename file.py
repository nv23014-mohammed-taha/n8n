from fastapi import FastAPI, Request
from intents import detect_intent
from automation import handle_intent

app = FastAPI()

@app.post("/incoming-call")
async def incoming_call(request: Request):
    data = await request.json()
    transcript = data.get("transcript")

    intent_data = detect_intent(transcript)
    response = handle_intent(intent_data)

    return {"response": response}
