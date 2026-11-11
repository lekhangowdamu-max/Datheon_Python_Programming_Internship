
import json
import re
from pathlib import Path



# 1. LOAD FAQ DATA


def load_faq_data():
    file_path = Path(__file__).with_name("sample_faq.json")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data

    except FileNotFoundError:
        print("Error: sample_faq.json file not found!")
        return {"greetings": [], "faqs": []}

    except json.JSONDecodeError:
        print("Error: Invalid JSON format!")
        return {"greetings": [], "faqs": []}



# 2. NORMALIZE USER INPUT

def normalize_text(message):
    return message.lower().strip()



# 3. CHECK GREETINGS


def check_greeting(message, greetings):

    for greeting in greetings:

        pattern = r"\b" + re.escape(greeting.lower()) + r"\b"

        if re.search(pattern, message):
            return True

    return False



# 4. FIND FAQ ANSWERS


def find_answers(message, faqs):

    user_words = set(
        re.findall(r"\b[a-z0-9]+\b", message)
    )

    stop_words = {
        "what", "are", "your", "how", "do", "i",
        "my", "when", "will", "the", "is", "a",
        "to", "of", "and", "can", "you", "me",
        "please", "does", "for", "get", "about"
    }

    matches = []

    for faq in faqs:

        question = faq.get("question", "").lower()

        question_words = set(
            re.findall(r"\b[a-z0-9]+\b", question)
        )

        keywords = question_words - stop_words

        matched_words = user_words.intersection(keywords)

        if matched_words:

            score = len(matched_words)

            matches.append((score, faq))

    # Sort answers by relevance
    matches.sort(key=lambda item: item[0], reverse=True)

    # Return up to three matching answers
    return [faq for score, faq in matches[:3]]



# 5. START CHATBOT

def start_chatbot():

    data = load_faq_data()

    greetings = data.get("greetings", [])
    faqs = data.get("faqs", [])

    print("\n======================================")
    print("       CUSTOMER SUPPORT CHATBOT")
    print("======================================")

    print("Bot: Hello! Welcome to Customer Support.")
    print("Bot: How can I help you today?")
    print("\nAvailable topics:")
    print("- Business hours")
    print("- Internship project submission")
    print("- Certificate information")

    print("\nType 'bye', 'exit' or 'quit' to close.")
    print("--------------------------------------")

    # Conversational loop
    while True:

        try:

            user_input = input("\nYou: ").strip()

            # Empty input handling
            if not user_input:
                print("Bot: Please enter a question.")
                continue

            message = normalize_text(user_input)

            # Exit commands
            if re.fullmatch(r"(bye|exit|quit)", message):
                print("Bot: Thank you for contacting us!")
                print("Bot: Have a great day. Goodbye!")
                break

            # Greeting response
            greeting_found = check_greeting(message, greetings)

            if greeting_found:
                print("Bot: Hello! Nice to meet you.")

            # Identify FAQ intents
            answers = find_answers(message, faqs)

            if answers:

                for faq in answers:
                    print("Bot:", faq["answer"])

            elif not greeting_found:

                print(
                    "Bot: Sorry, I couldn't understand your question."
                )

                print(
                    "Bot: Please ask about business hours, "
                    "project submission or certificates."
                )

        except KeyboardInterrupt:

            print("\nBot: Chat interrupted. Goodbye!")
            break

        except (KeyError, TypeError) as error:

            print("Bot: There was a problem reading the FAQ data.")
            print("Error:", error)

        except Exception as error:

            print("Bot: Something went wrong. Please try again.")
            print("Error:", error)



# 6. PROGRAM ENTRY POINT


if __name__ == "__main__":
    start_chatbot()
