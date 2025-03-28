import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

logging.basicConfig(
    filename="bargain_api.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

logging.info("Loading model and tokenizer...")
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=dtype,
        device_map="auto"
    ).to(device)
    tokenizer.pad_token_id = tokenizer.eos_token_id
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load model: {e}")
    raise RuntimeError("Model initialization failed.")

class BargainRequest(BaseModel):
    user_offer: float
    base_price: float

SALESPERSON_PERSONA = """
You are a polished and persuasive negotiator, known for turning conversations into delightful experiences. 
You never reject an offer outright but guide the customer toward a fair price with charm and intelligence.

**Your approach:**
- If the offer is too low, remain warm and positive while subtly guiding them upward.
- Use psychology: “A smart deal benefits both sides.”
- Justify value through **quality, exclusivity, and long-term benefits.**
- Always make a counteroffer that feels like a rare opportunity, not a compromise.
- If they hesitate, gently remind them: **"Great deals don’t wait forever."**

Keep the tone **polite, confident, and engaging.** Your goal is to make the customer feel good while securing the best price.
"""

def generate_response(user_offer, base_price):
    try:
        logging.info(f"User offered: ${user_offer}, Base price: ${base_price}")

        min_acceptable_price = base_price * 0.9
        counteroffer = max(min_acceptable_price, (user_offer + base_price * 1.1) / 2)

        if user_offer < min_acceptable_price * 0.8:
            bot_reply = (
                f"That’s a bold offer, and I love a good negotiation! However, this item is known for its **exceptional quality and exclusivity.** "
                f"I’d love to get you a fantastic deal, and for serious buyers, I can offer **${min_acceptable_price}**—but only for a limited time. "
                f"Shall we move forward?"
            )
        else:
            bot_reply = (
                f"That’s an interesting offer! I truly appreciate your negotiation skills. "
                f"Since I believe in fair deals, how about we meet at **${counteroffer}**? "
                f"That way, you walk away with an exclusive deal, and I keep my reputation for offering quality at the right price. Sounds good?"
            )

        logging.info(f"Generated response: {bot_reply}")
        return {"response": bot_reply}

    except Exception as e:
        logging.exception("Error while generating response")
        return {"error": str(e)}

@app.post("/bargain")
def bargain(request: BargainRequest):
    return generate_response(request.user_offer, request.base_price)

if __name__ == "__main__":
    import uvicorn
    logging.info("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
