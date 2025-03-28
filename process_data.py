import json
import re

def load_raw_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def preprocess_text(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s$]', '', text)
    return text

def parse_conversation(raw_lines):
    dialogues = []
    temp_dialogue = {}

    for line in raw_lines:
        line = line.strip()

        if line.startswith("User:"):
            if "user_message" in temp_dialogue and "bot_response" in temp_dialogue:
                dialogues.append(temp_dialogue)
                temp_dialogue = {}

            temp_dialogue["user_message"] = preprocess_text(line.replace("User:", "").strip())

        elif line.startswith("Bot:"):
            temp_dialogue["bot_response"] = preprocess_text(line.replace("Bot:", "").strip())

    if "user_message" in temp_dialogue and "bot_response" in temp_dialogue:
        dialogues.append(temp_dialogue)

    return dialogues

def save_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    input_file = "negotiation_dataset.txt"
    output_file = "negotiation_data.json"

    raw_data = load_raw_data(input_file)
    structured_data = parse_conversation(raw_data)
    save_to_json(structured_data, output_file)

    print(f"Structured data saved to {output_file}")
