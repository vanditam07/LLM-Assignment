import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import logging
import re

logging.basicConfig(
    filename="bargain_bot.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=dtype,
    device_map="auto"
).to(device)

tokenizer.pad_token_id = tokenizer.eos_token_id

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

conversation_history = []

def extract_offer(user_input):
    match = re.search(r'\$?(\d+\.?\d*)', user_input)
    return float(match.group(1)) if match else None

def generate_counteroffer(user_offer, base_price=50, min_discount=0.1, max_discount=0.3):
    if user_offer is None:
        return None
    threshold_price = base_price * (1 - max_discount)
    if user_offer < threshold_price:
        counteroffer = max(threshold_price, user_offer + (base_price * min_discount))
        return round(counteroffer, 2)
    return None

def generate_response(user_input):
    try:
        user_offer = extract_offer(user_input)
        counteroffer = generate_counteroffer(user_offer) if user_offer else None
        
        conversation_history.append(f"User: {user_input}")
        prompt = f"{SALESPERSON_PERSONA}\n" + "\n".join(conversation_history[-5:]) + "\nAssistant:"
        
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=True,
            temperature=0.7,
            top_p=0.85,
            pad_token_id=tokenizer.eos_token_id
        )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        bot_reply = response.split("Assistant:")[-1].strip().split("User:")[0].strip()
        
        if counteroffer:
            bot_reply = (
                f"I love your enthusiasm! But considering the quality and exclusivity, "
                f"how about **${counteroffer}** instead? This is a fantastic deal for what you’re getting!"
            )
        
        conversation_history.append(f"Assistant: {bot_reply}")
        return bot_reply

    except Exception as e:
        logging.error(f"Error: {e}")
        return "Sorry, I encountered an error while responding."

if __name__ == "__main__":
    print("🛍️ Sales Chatbot Initialized! (Type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Assistant: Goodbye! Have a great day!")
            break
        bot_response = generate_response(user_input)
        print(f"Assistant: {bot_response}")
