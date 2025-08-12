import json
import os
import google.generativeai as genai
from typing import List, Dict, Any, Optional

# Configure the Gemini API
API_KEY = "ADD YOUR GEMINI API KEY HERE"
genai.configure(api_key=API_KEY)

# Define the allowed curriculum options
ALLOWED_CURRICULUM = [
    "Quantitative Math -> Problem Solving -> Numbers and Operations",
    "Quantitative Math -> Problem Solving -> Algebra",
    "Quantitative Math -> Problem Solving -> Geometry",
    "Quantitative Math -> Problem Solving -> Probability and Statistics",
    "Quantitative Math -> Problem Solving -> Data Analysis",
    "Quantitative Math -> Algebra -> Algebraic Word Problems",
    "Quantitative Math -> Algebra -> Interpreting Variables",
    "Quantitative Math -> Algebra -> Polynomial Expressions (FOIL/Factoring)",
    "Quantitative Math -> Algebra -> Rational Expressions",
    "Quantitative Math -> Algebra -> Exponential Expressions (Product rule, negative exponents)",
    "Quantitative Math -> Algebra -> Quadratic Equations & Functions (Finding roots/solutions, graphing)",
    "Quantitative Math -> Algebra -> Functions Operations",
    "Quantitative Math -> Geometry and Measurement -> Area & Volume",
    "Quantitative Math -> Geometry and Measurement -> Perimeter",
    "Quantitative Math -> Geometry and Measurement -> Lines, Angles, & Triangles",
    "Quantitative Math -> Geometry and Measurement -> Right Triangles & Trigonometry",
    "Quantitative Math -> Geometry and Measurement -> Circles (Area, circumference)",
    "Quantitative Math -> Geometry and Measurement -> Coordinate Geometry",
    "Quantitative Math -> Geometry and Measurement -> Slope",
    "Quantitative Math -> Geometry and Measurement -> Transformations (Dilating a shape)",
    "Quantitative Math -> Geometry and Measurement -> Parallel & Perpendicular Lines",
    "Quantitative Math -> Geometry and Measurement -> Solid Figures (Volume of Cubes)",
    "Quantitative Math -> Numbers and Operations -> Basic Number Theory",
    "Quantitative Math -> Numbers and Operations -> Prime & Composite Numbers",
    "Quantitative Math -> Numbers and Operations -> Rational Numbers",
    "Quantitative Math -> Numbers and Operations -> Order of Operations",
    "Quantitative Math -> Numbers and Operations -> Estimation",
    "Quantitative Math -> Numbers and Operations -> Fractions, Decimals, & Percents",
    "Quantitative Math -> Numbers and Operations -> Sequences & Series",
    "Quantitative Math -> Numbers and Operations -> Computation with Whole Numbers",
    "Quantitative Math -> Numbers and Operations -> Operations with Negatives",
    "Quantitative Math -> Data Analysis & Probability -> Interpretation of Tables & Graphs",
    "Quantitative Math -> Data Analysis & Probability -> Trends & Inferences",
    "Quantitative Math -> Data Analysis & Probability -> Probability (Basic, Compound Events)",
    "Quantitative Math -> Data Analysis & Probability -> Mean, Median, Mode, & Range",
    "Quantitative Math -> Data Analysis & Probability -> Weighted Averages",
    "Quantitative Math -> Data Analysis & Probability -> Counting & Arrangement Problems",
    "Quantitative Math -> Reasoning -> Word Problems"
]

# Base questions for reference
BASE_QUESTION_1 = """
1. Each student at Central Middle School wears a uniform consisting of 1 shirt
and 1 pair of pants. The table shows the colors available for each item of
clothing. How many different uniforms are possible?

## Uniform Choices

| Shirt Color | Pants Color |
| :---: | :---: |

| Tan | Black |
| Red | Khaki |
| White | Navy |
| Yellow | |

(A) Three
(B) Four
(C) Seven
(D) Ten
(E) Twelve
"""

BASE_QUESTION_2 = """
2. The top view of a rectangular package of 6 tightly packed balls is shown. If
each ball has a radius of 2 centimeters, which of the following are closest to
the dimensions, in centimeters, of the rectangular package?

[](https://cdn.mathpix.com/cropped/2025_07_31_dc2e3d22c70b1617b86dg-33.jpg?height=451&width=307&top_left_y=113&top_left_x=280)
(A) $2 \times 3 \times 6$
(B) $4 \times 6 \times 6$
(C) $2 \times 4 \times 6$
(D) $4 \times 8 \times 12$
(E) $6 \times 8 \times 12$
"""

# Function to generate a new question using Gemini
def generate_question(base_questions: List[str], num_questions: int = 1) -> List[Dict[str, Any]]:
    """
    Generate new math questions similar to the base questions using Gemini.
    
    Args:
        base_questions: List of base questions to use as reference
        num_questions: Number of new questions to generate
        
    Returns:
        List of generated question objects
    """
    # Initialize Gemini model
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
    except Exception as e:
        print(f"Error initializing gemini-1.5-pro model: {e}")
        print("Falling back to gemini-1.0-pro model...")
        model = genai.GenerativeModel('gemini-pro')
    
    # Create prompt for Gemini
    prompt = f"""
    You are an expert math teacher creating multiple-choice questions (MCQs) for middle/high school students.
    
    I'll provide you with two base math questions. Your task is to create {num_questions} new, original math question(s) 
    that are similar in style, difficulty, and topic to these base questions.
    
    BASE QUESTIONS:
    {base_questions[0]}
    
    {base_questions[1]}
    
    REQUIREMENTS FOR THE OUTPUT:
    - Output ONLY a single JSON object (no extra text) with the following keys:
      {{
        "title": string,                                         # A meaningful title for the assessment
        "description": string,                                  # Brief description of the assessment
        "question": string,                                     # The actual question text
        "instruction": string,                                  # Instructions for the student
        "difficulty": "easy"|"moderate"|"hard",                # Difficulty level
        "order": 1|2,                                          # Question number
        "options": [string, string, string, string, ...],      # 4-5 options preferred
        "correct_option": string,                              # Must match exactly one option text
        "explanation": string,                                  # Detailed explanation of the solution
        "subject": string,                                      # Choose from allowed curriculum list
        "unit": string,                                         # Choose from allowed curriculum list
        "topic": string,                                        # Choose from allowed curriculum list
        "plusmarks": 1,                                         # Points for the question
        "image_prompt": string,                                # Text prompt to create the diagram/image
        "image_alt": string                                    # Alt text for the image
      }}
    
    - The allowed subject/unit/topic MUST be chosen from this list (pick the best fit):
    {ALLOWED_CURRICULUM}
    
    - Make the question clear for a middle/high-school audience, include only necessary numbers.
    - Ensure exactly one option is correct.
    - If the question requires an image, provide a detailed image_prompt that describes what should be in the image.
    - Preserve any LaTeX formatting for equations and formulas.
    - Keep JSON compact and valid. Use double quotes.
    """
    
    # Generate response from Gemini
    try:
        response = model.generate_content(prompt)
    except Exception as e:
        print(f"Error generating content: {e}")
        print("Returning a default question template...")
        # Return a default template if generation fails
        return [{
            "title": "Math Assessment",
            "description": "Basic math assessment for middle school students",
            "question": "If a rectangle has a length of 8 units and a width of 6 units, what is its area?",
            "instruction": "Calculate the area of the rectangle.",
            "difficulty": "easy",
            "order": 1,
            "options": ["14 square units", "24 square units", "48 square units", "54 square units"],
            "correct_option": "48 square units",
            "explanation": "The area of a rectangle is calculated by multiplying its length by its width. In this case, 8 × 6 = 48 square units.",
            "subject": "Quantitative Math",
            "unit": "Geometry and Measurement",
            "topic": "Area & Volume",
            "plusmarks": 1,
            "image_prompt": "A rectangle with length 8 units and width 6 units, with grid lines showing the area.",
            "image_alt": "Rectangle with dimensions 8×6 units"
        }]
    
    # Extract and parse JSON from response
    try:
        # Find JSON in the response
        response_text = response.text
        json_start = response_text.find('{')
        json_end = response_text.rfind('}')
        
        if json_start >= 0 and json_end >= 0:
            json_str = response_text[json_start:json_end+1]
            question_data = json.loads(json_str)
            return [question_data]
        else:
            print("Error: Could not find JSON in the response")
            return []
    except Exception as e:
        print(f"Error parsing response: {e}")
        print(f"Response text: {response.text}")
        return []

# Function to generate image prompt for a question
def generate_image_prompt(question_data: Dict[str, Any]) -> str:
    """
    Generate a detailed image prompt based on the question data.
    
    Args:
        question_data: Question data including image_prompt
        
    Returns:
        Detailed image prompt for Gemini
    """
    # If image_prompt is not provided or empty, return empty string
    if not question_data.get('image_prompt'):
        return ""
    
    # Create a detailed prompt for Gemini
    prompt = f"""
    Create a detailed description for generating an image for the following math question:
    
    QUESTION: {question_data['question']}
    
    BASE IMAGE PROMPT: {question_data['image_prompt']}
    
    Please provide a detailed, specific description that would help generate a clear, 
    educational diagram or illustration for this math problem. Include specific details 
    about what elements should be in the image, their arrangement, colors, labels, and any 
    other relevant information. The image should be suitable for middle/high school students.
    """
    
    # Generate response from Gemini
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
    except Exception as e:
        print(f"Error initializing gemini-1.5-pro model for image prompt: {e}")
        print("Falling back to gemini-pro model...")
        model = genai.GenerativeModel('gemini-pro')
    
    try:
        response = model.generate_content(prompt)
    except Exception as e:
        print(f"Error generating image prompt: {e}")
        return "A clear, educational diagram for the math problem."
    
    return response.text.strip()

# Function to create sample questions without using the API
def create_sample_questions() -> List[Dict[str, Any]]:
    """
    Create sample questions without using the API.
    This is useful for testing and demonstration purposes.
    
    Returns:
        List of sample question objects
    """
    sample_questions = [
        {
            "title": "Math Combinations Assessment",
            "description": "Assessment on counting principles and combinations",
            "question": "At Westside High School, students can choose from 3 different styles of shirts (polo, button-up, or t-shirt) and 4 different colors of pants (black, navy, khaki, or gray) for their uniform. How many different uniform combinations are possible?",
            "instruction": "Calculate the total number of possible combinations.",
            "difficulty": "easy",
            "order": 1,
            "options": ["3 combinations", "4 combinations", "7 combinations", "12 combinations", "15 combinations"],
            "correct_option": "12 combinations",
            "explanation": "To find the total number of possible uniform combinations, we multiply the number of shirt options by the number of pants options. There are 3 shirt options and 4 pants options, so the total number of possible combinations is 3 × 4 = 12 combinations.",
            "subject": "Quantitative Math",
            "unit": "Problem Solving",
            "topic": "Numbers and Operations",
            "plusmarks": 1,
            "image_prompt": "A visual representation showing 3 different shirt styles and 4 different pants colors arranged in a grid to illustrate all possible combinations.",
            "image_alt": "Grid showing shirt and pants combinations for school uniforms"
        },
        {
            "title": "Geometry and Measurement Assessment",
            "description": "Assessment on geometric shapes and measurements",
            "question": "A cylindrical container holds 8 identical spherical balls arranged in a 2×2×2 configuration. If each ball has a diameter of 3 centimeters, what is the minimum volume of the cylindrical container in cubic centimeters?",
            "instruction": "Calculate the minimum volume of the cylindrical container.",
            "difficulty": "moderate",
            "order": 2,
            "options": ["27π cubic cm", "36π cubic cm", "54π cubic cm", "72π cubic cm", "108π cubic cm"],
            "correct_option": "54π cubic cm",
            "explanation": "For a 2×2×2 configuration of spherical balls, the minimum cylindrical container would have a diameter equal to twice the ball radius (3 cm) and a height equal to twice the ball radius (3 cm) multiplied by the number of layers (2). So the radius of the cylinder is 1.5 cm and the height is 6 cm. The volume of a cylinder is V = πr²h = π(1.5)²(6) = π(2.25)(6) = 13.5π cubic cm.",
            "subject": "Quantitative Math",
            "unit": "Geometry and Measurement",
            "topic": "Solid Figures (Volume of Cubes)",
            "plusmarks": 1,
            "image_prompt": "A transparent cylindrical container with 8 identical spherical balls arranged in a 2×2×2 configuration. Each ball has a diameter of 3 centimeters.",
            "image_alt": "Cylindrical container with 8 spherical balls in 2×2×2 arrangement"
        }
    ]
    
    return sample_questions

# Main function to generate questions
def main():
    import argparse
    
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Generate math MCQ questions similar to base questions.')
    parser.add_argument('-n', '--num', type=int, default=2, help='Number of questions to generate (default: 2)')
    parser.add_argument('-o', '--output', type=str, default='generated_questions.json', help='Output file path (default: generated_questions.json)')
    parser.add_argument('-s', '--sample', action='store_true', help='Use sample questions instead of API generation')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show verbose output')
    
    args = parser.parse_args()
    
    # Generate new questions
    base_questions = [BASE_QUESTION_1, BASE_QUESTION_2]
    num_questions_to_generate = args.num
    
    print(f"Generating {num_questions_to_generate} new math questions...")
    generated_questions = []
    
    # Use sample questions if requested
    if args.sample:
        print("Using sample questions as requested.")
        generated_questions = create_sample_questions()
        # If we need more questions than we have samples, duplicate the samples
        while len(generated_questions) < num_questions_to_generate:
            generated_questions.extend(create_sample_questions())
        # Trim to the requested number
        generated_questions = generated_questions[:num_questions_to_generate]
    else:
        # Try to use the API first
        try:
            # First attempt to generate using the API
            for i in range(num_questions_to_generate):
                if args.verbose:
                    print(f"Generating question {i+1}/{num_questions_to_generate}...")
                questions = generate_question(base_questions)
                if questions:
                    generated_questions.extend(questions)
                    
            # If we couldn't generate any questions or got duplicates, use sample questions
            if not generated_questions or (len(generated_questions) > 1 and 
                                          all(generated_questions[0]['question'] == q['question'] for q in generated_questions[1:])):
                print("API generation failed or returned duplicates. Using sample questions instead.")
                generated_questions = create_sample_questions()
                # If we need more questions than we have samples, duplicate the samples
                while len(generated_questions) < num_questions_to_generate:
                    generated_questions.extend(create_sample_questions())
                # Trim to the requested number
                generated_questions = generated_questions[:num_questions_to_generate]
        except Exception as e:
            print(f"Error using API: {e}")
            print("Using sample questions instead.")
            generated_questions = create_sample_questions()
            # If we need more questions than we have samples, duplicate the samples
            while len(generated_questions) < num_questions_to_generate:
                generated_questions.extend(create_sample_questions())
            # Trim to the requested number
            generated_questions = generated_questions[:num_questions_to_generate]
    
    # Save generated questions to file
    if generated_questions:
        output_file = args.output
        with open(output_file, "w") as f:
            json.dump(generated_questions, f, indent=2)
        
        print(f"Successfully generated {len(generated_questions)} questions.")
        print(f"Questions saved to {output_file}")
        
        # Print the first generated question as an example if verbose
        if args.verbose:
            print("\nExample generated question:")
            print(json.dumps(generated_questions[0], indent=2))
        else:
            print("\nGeneration complete. Use -v flag to see example output.")
    else:
        print("Failed to generate questions.")

if __name__ == "__main__":
    main()