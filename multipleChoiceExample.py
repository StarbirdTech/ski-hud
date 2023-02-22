# Define your questions and answers
questions = [
    {
        "question": "What is the capital of France?",
        "options": ["a) Madrid", "b) Paris", "c) Berlin", "d) London"],
        "answer": "b"
    },
    {
        "question": "What is the largest planet in our solar system?",
        "options": ["a) Jupiter", "b) Saturn", "c) Uranus", "d) Neptune"],
        "answer": "a"
    },
    {
        "question": "What is the currency of Japan?",
        "options": ["a) Yen", "b) Euro", "c) Dollar", "d) Pound"],
        "answer": "a"
    }
]

# Initialize variables for the current question and answer
current_question = 0
current_answer = ""

# Print the first question and options


def print_question(question, options):
    print(question)
    for option in options:
        print(option)


print_question(questions[current_question]["question"], questions[current_question]["options"])

# Loop until all questions are answered
while current_question < len(questions):
    # Get user input
    user_input = input("Enter your answer (a, b, c, or d) or press 'q' to quit: ")

    # Check for quit command
    if user_input == "q":
        break

    # Check for valid input
    if user_input not in ["a", "b", "c", "d"]:
        print("Invalid input. Please enter a, b, c, or d.")
        continue

    # Check the answer
    current_answer = user_input
    if current_answer == questions[current_question]["answer"]:
        print("Correct!")
    else:
        print("Incorrect. The correct answer is", questions[current_question]["answer"])

    # Move to the next question
    current_question += 1
    if current_question < len(questions):
        print_question(questions[current_question]["question"], questions[current_question]["options"])

print("Thanks for playing!")
