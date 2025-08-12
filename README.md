# Math MCQ Generator

This project generates new multiple-choice math questions similar to provided base questions using Google's Gemini AI. The system preserves LaTeX formatting and generates image prompts for diagrams when needed.

## Features

- Generates new math MCQs based on sample questions
- Preserves LaTeX formatting for equations and formulas
- Creates image prompts for diagrams
- Ensures questions follow curriculum standards
- Outputs questions in a structured JSON format

## Requirements

- Python 3.7+
- Google Generative AI Python SDK

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the generator script with various options:

```bash
python mcq_generator.py [options]
```

### Command-line Options

- `-n, --num NUM`: Number of questions to generate (default: 2)
- `-o, --output FILE`: Output file path (default: generated_questions.json)
- `-s, --sample`: Use sample questions instead of API generation
- `-v, --verbose`: Show verbose output including example generated question

### Examples

```bash
# Generate 2 questions using the API (default)
python mcq_generator.py

# Generate 5 questions using sample questions
python mcq_generator.py -s -n 5

# Generate 3 questions and save to custom file with verbose output
python mcq_generator.py -n 3 -o custom_questions.json -v
```

The script will:
1. Generate new math questions similar to the base questions
2. Save the generated questions to the specified output file
3. Print an example of a generated question (if verbose mode is enabled)

## Output Format

The generated questions follow this JSON structure:

```json
{
  "title": "Assessment title",
  "description": "Assessment description",
  "question": "The question text",
  "instruction": "Instructions for the student",
  "difficulty": "easy|moderate|hard",
  "order": 1,
  "options": ["Option A", "Option B", "Option C", "Option D", "Option E"],
  "correct_option": "The correct option text",
  "explanation": "Detailed explanation of the solution",
  "subject": "Subject from curriculum",
  "unit": "Unit from curriculum",
  "topic": "Topic from curriculum",
  "plusmarks": 1,
  "image_prompt": "Text prompt to create the diagram/image",
  "image_alt": "Alt text for the image"
}
```

## Customization

You can modify the base questions in the `mcq_generator.py` file to generate different types of math questions. You can also adjust the number of questions to generate by changing the `num_questions_to_generate` variable in the `main()` function.