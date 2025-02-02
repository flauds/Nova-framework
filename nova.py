import datetime
import webbrowser
import random

def greet_user():
    print("Hello! I'm Nova, your personal virtual assistant.")
    print("How can I assist you today?")

def tell_time():
    now = datetime.datetime.now()
    print(f"The current date and time is: {now.strftime('%Y-%m-%d %H:%M:%S')}")

def perform_calculation():
    try:
        print("Enter the first number:")
        num1 = float(input("> "))
        print("Enter an operation (+, -, *, /):")
        operator = input("> ")
        print("Enter the second number:")
        num2 = float(input("> "))
        
        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            result = num1 / num2 if num2 != 0 else "undefined (cannot divide by zero)"
        else:
            result = "Invalid operator"
        
        print(f"The result is: {result}")
    except ValueError:
        print("Invalid input. Please enter numbers only.")

def search_web():
    print("What do you want to search for?")
    query = input("> ")
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    print("I have opened the search results in your browser.")

def tell_joke():
    jokes = [
        "Why don’t scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What do you call fake spaghetti? An impasta!"
    ]
    print(random.choice(jokes))

def main():
    greet_user()
    while True:
        print("\nOptions:")
        print("1. Tell me the time")
        print("2. Perform a calculation")
        print("3. Search the web")
        print("4. Tell me a joke")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")
        if choice == "1":
            tell_time()
        elif choice == "2":
            perform_calculation()
        elif choice == "3":
            search_web()
        elif choice == "4":
            tell_joke()
        elif choice == "5":
            print("Goodbye! Have a great day!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    topic = voice_input() or "Default Topic"
content = voice_input() or "Default Content"
nova.add_knowledge("Atlantic", topic, content)
import requests

response = requests.post("http://127.0.0.1:5000/add_knowledge", json={
    "sea": "Atlantic",
    "topic": "AI",
    "content": "AI stands for Artificial Intelligence"
})
print(response.json())

    