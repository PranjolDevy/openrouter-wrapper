import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY or "sk-or-" not in API_KEY:
    print("Missing or invalid API key.")
    exit()

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def load_prompt(file_number):
    path = f"prompts/{file_number}.txt"
    if not os.path.isfile(path):
        print(f"Prompt file not found: {path}")
        exit()

    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def select_mode():
    print("\nWelcome to AI. Choose a mode:\n")
    print("1. Lyra – prompt optimizer")
    print("2. Echo – message rewriter")
    print("3. Ghostwriter – story assistant")
    print("4. Codex – code helper")
    print("5. Plain – no system prompt\n")

    mode = input("Pick 1, 2, 3, 4 or 5: ").strip()
    if mode not in ["1", "2", "3", "4", "5"]:
        print("Invalid choice. Exiting.")
        exit()

    return mode

def chat_loop(chat_history):
    print("\nType 'exit' to quit.")

    while True:
        user_input = input("\nYou: ")

        if user_input.strip().lower() in ["exit", "quit", "bye"]:
            print("AI: Later.")
            break

        if not user_input.strip():
            print("AI: Say something.")
            continue

        chat_history.append({"role": "user", "content": user_input})

        payload = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": chat_history,
        }

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )

            if response.status_code != 200:
                print(f"HTTP {response.status_code}: {response.text}")
                continue

            data = response.json()
            AI_reply = data["choices"][0]["message"]["content"].strip()
            print(f"AI: {AI_reply}")

            chat_history.append({"role": "assistant", "content": AI_reply})

        except Exception as e:
            print("Error talking to AI:", e)
            break

if __name__ == "__main__":
    mode = select_mode()

    if mode == "5":
        chat_history = []
    else:
        system_prompt = load_prompt(mode)
        chat_history = [{"role": "system", "content": system_prompt}]

    chat_loop(chat_history)
