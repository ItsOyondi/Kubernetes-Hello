import dotenv
import os
from PyPDF2 import PdfReader  # You can replace with pdfplumber if needed
import openai

# Load environment variables
dotenv.load_dotenv()

# Get Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set.")

# Initialize Groq client
client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1", api_key=groq_api_key
)


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using PyPDF2.
    """
    try:
        if not os.path.exists(pdf_path):
            print(f"Error: File not found at {pdf_path}")
            return None

        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""  # Handle None from extract_text()
            return text.strip()  # Remove leading/trailing whitespace
    except Exception as e:
        print(f"An error occurred while processing the PDF: {e}")
        return None


def get_groq_chat_response(messages, model="gemma2-9b-it"):
    """
    Get a response from the Groq chat API.
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model
        )
        return chat_completion.choices[0].message.content
    except openai.OpenAIError as e:
        print(f"Error calling Groq API: {e}")
        return None


def process_pdf_and_get_response(pdf_path, query, model="gemma2-9b-it"):
    """
    Process the PDF file, extract text, and get a response from the Groq API.
    """
    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(pdf_path)
    if pdf_text is None:
        return None  # Error already handled in extract_text_from_pdf

    # Truncate text if too long for API
    max_chars = 2000  # Adjust based on token limits
    if len(pdf_text) > max_chars:
        print(f"PDF content is too long. Truncating to {max_chars} characters.")
        pdf_text = pdf_text[:max_chars]

    # Prepare messages for the Groq API
    messages = [
        {"role": "system", "content": "You are a helpful assistant that answers questions about provided PDF documents."},
        {"role": "user", "content": f"Here's the content of a PDF:\n{pdf_text}\n\nMy question is: {query}"},
    ]

    # Get response from Groq API
    try:
        response = get_groq_chat_response(messages, model)
        return response
    except Exception as e:
        print(f"Error getting Groq response: {e}")
        return None


# Example usage:
pdf_path = "docs/Poster.pdf"  # Replace with the actual path to your PDF
query = "Give me the table of the datasets mentioned in the document?"
if not os.path.exists(pdf_path):
    print(f"Error: File not found at {pdf_path}. Please provide a valid file path.")
else:
    # print("File exists. Processing...")

    # Process the PDF and get the response
    response = process_pdf_and_get_response(pdf_path, query)

    if response:
        print("Answer:")
        print(response)
    else:
        print("No response received or an error occurred.")
