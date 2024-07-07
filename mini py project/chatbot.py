import re

def chatbot_response(user_input):
    user_input = user_input.lower()

    if re.search(r'\bhello\b|\bhi\b|\bhey\b', user_input):
        return "Hello! How can I assist you today?"
    
    elif re.search(r'\bbye\b|\bexit\b|\bquit\b', user_input):
        return "Goodbye! Have a great day!"
    
    elif re.search(r'\bname\b|\byou\b|\byour\b|\bbot\b', user_input):
        return "I am a simple chatbot created by vikas to assist you."
    
    elif re.search(r'\bhow are you\b|\bhow do you do\b', user_input):
        return "I'm just a bot, but I'm here to help you!"

    elif re.search(r'\bweather\b', user_input):
        return "I can't provide live weather updates yet, but you can check a weather website for the latest information."

    elif re.search(r'\btime\b', user_input):
        from datetime import datetime
        current_time = datetime.now().strftime('%H:%M:%S')
        return f"The current time is {current_time}."

    else:
        return "I'm sorry, I didn't understand that. Can you please rephrase?"

def main():
    print("Welcome to the chatbot! Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['bye', 'exit', 'quit']:
            print("Bot: Goodbye! Have a great day!")
            break
        response = chatbot_response(user_input)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
