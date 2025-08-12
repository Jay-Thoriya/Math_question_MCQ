import json
import os
import sys

def display_question(question, question_number=1):
    """
    Display a math question in a formatted way.
    
    Args:
        question: The question object
        question_number: The question number to display
    """
    print(f"\n{'='*50}")
    print(f"Question {question_number}: {question['question']}")
    print(f"{'='*50}")
    
    print("Instructions:", question['instruction'])
    print(f"Difficulty: {question['difficulty']}\n")
    
    # Display options
    for i, option in enumerate(question['options']):
        option_letter = chr(65 + i)  # A, B, C, D, E...
        print(f"({option_letter}) {option}")
    
    print("\nPress Enter to see the answer...")
    input()
    
    # Find the correct option letter
    correct_option_index = question['options'].index(question['correct_option'])
    correct_option_letter = chr(65 + correct_option_index)
    
    print(f"\nCorrect Answer: ({correct_option_letter}) {question['correct_option']}")
    print(f"\nExplanation: {question['explanation']}")
    
    # Display image information
    if question.get('image_prompt') and question.get('image_alt'):
        print(f"\nImage Description: {question['image_alt']}")
        print("(Note: This question includes an image prompt that could be used to generate an actual image)")
    else:
        print("\n(This question does not include an image)")

def main():
    # Check if a file was provided as an argument
    if len(sys.argv) > 1:
        questions_file = sys.argv[1]
    else:
        questions_file = 'generated_questions.json'
    
    # Check if the file exists
    if not os.path.exists(questions_file):
        print(f"Error: File '{questions_file}' not found.")
        print("Please run 'python mcq_generator.py' first to generate questions.")
        return
    
    # Load the questions
    try:
        with open(questions_file, 'r') as f:
            questions = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: File '{questions_file}' is not a valid JSON file.")
        return
    except Exception as e:
        print(f"Error loading questions: {e}")
        return
    
    if not questions:
        print("No questions found in the file.")
        return
    
    # Display each question
    for i, question in enumerate(questions):
        display_question(question, i+1)
        
        # If not the last question, ask to continue
        if i < len(questions) - 1:
            print("\nPress Enter to continue to the next question...")
            input()
    
    print("\nAll questions completed!")

if __name__ == "__main__":
    main()