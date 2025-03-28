📜 Task 1: Process & Structure Negotiation Data

📌 Overview

This project processes and structures a dataset of customer-chatbot bargaining dialogues into a structured format suitable for model input. The script, process_data.py, reads a raw text dataset, parses the dialogues into a structured JSON format, and applies basic NLP preprocessing.

🚀 Features

📥 Reads raw text-based conversation datasets.

🔍 Parses user-bot dialogues into structured JSON format.

📝 Applies basic NLP preprocessing:

Lowercasing

Punctuation removal

Tokenization

📤 Outputs structured data to negotiation_data.json.

🛠 Installation

Ensure you have Python installed on your system. Install the necessary dependencies using:

pip install nltk

▶️ Usage

Run the script with the following command:

python process_data.py

📂 Input Format

The input should be a raw text file containing conversations in the following format:

User: Hey, I like this jacket. How much is it?
Bot: It's $80.
User: Can I get a discount?
Bot: Hmm... I can offer $75 if you buy now.
User: $70?
Bot: Sorry, I can't go below $73. Deal?
User: Alright, I'll take it.

🛒 Task 2: LLM-Based Negotiation Bot

📌 Overview

This project is a simple yet powerful LLM-based negotiation chatbot designed to act as a tough, street-smart vendor. It engages users in bargaining conversations, resists extreme low offers, suggests counteroffers, and adds urgency to close deals. The chatbot uses TinyLlama-1.1B-Chat-v1.0 as the LLM model for generating dynamic responses.

🚀 Features

✅ LLM-Powered: Uses TinyLlama-1.1B-Chat-v1.0 for natural conversations.
✅ Context-Aware: Remembers past offers and negotiation history within a session.
✅ Tough Negotiation: Pushes back against low offers while maintaining engagement.
✅ Counteroffer Strategy: Adjusts prices dynamically based on user input.
✅ Urgency Tactics: Creates a sense of urgency to encourage quicker deal


🤖 Task 3: Advanced LLM-Based Sales Chatbot

📌 Overview

This project is an advanced LLM-powered sales chatbot that enhances the customer interaction experience by combining negotiation, persuasion, and product recommendations. It uses TinyLlama-1.1B-Chat-v1.0 to simulate a skilled salesperson who engages users, understands preferences, and adapts responses dynamically.

🚀 Features

✅ LLM-Powered: Uses TinyLlama-1.1B-Chat-v1.0 for intelligent and natural conversations.
✅ Personalized Sales Pitch: Adapts to customer needs and preferences.
✅ Smart Negotiation: Handles pricing discussions with counteroffers and persuasion techniques.
✅ Product Recommendations: Suggests alternatives if the user hesitates.
✅ Engaging & Persuasive: Uses storytelling and urgency to drive conversions.
✅ Clean HTML Frontend: A simple and aesthetic frontend for user interaction.
✅ Postman API Testing: Supports API calls via Postman for seamless testing.


Imageho
