import PyPDF2
import nltk
from collections import Counter
import matplotlib.pyplot as plt

# Download NLTK stopwords and wordnet
nltk.download("stopwords")
nltk.download("wordnet")

# Load the ESG keywords related to Environment, Social, and Governance
esg_keywords = {
    "environment": ["environment", "sustainability", "green", "carbon", "ecosystem"],
    "social": ["social", "community", "diversity", "inclusion", "equality"],
    "governance": [
        "governance",
        "ethics",
        "corporate governance",
        "transparency",
        "compliance",
    ],
}


# Function to categorize ESG words into Environment, Social, or Governance
def categorize_esg_word(word):
    for category, keywords in esg_keywords.items():
        if word in keywords:
            return category
    return None


# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    with open(pdf_file, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()
    return text


# Function to analyze ESG keywords in text and create bar charts
def analyze_esg_in_pdf(pdf_file):
    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(pdf_file)

    # Convert the text to lowercase for case-insensitive matching
    pdf_text = pdf_text.lower()

    # Tokenize the text into words
    words = nltk.word_tokenize(pdf_text)

    # Remove stopwords and non-alphabetic words
    words = [
        word
        for word in words
        if word.isalpha() and word not in nltk.corpus.stopwords.words("english")
    ]

    # Initialize counters for each ESG category
    esg_counts = {category: Counter() for category in esg_keywords}

    # Count the occurrences of ESG keywords and categorize them
    for word in words:
        category = categorize_esg_word(word)
        if category:
            esg_counts[category][word] += 1

    # Create a bar chart for ESG keyword counts
    for category, category_keywords in esg_counts.items():
        plt.figure(figsize=(8, 4))
        plt.bar(
            category_keywords.keys(), category_keywords.values(), color="dodgerblue"
        )
        plt.xlabel(f"{category.capitalize()} Keywords")
        plt.ylabel("Keyword Count")
        plt.title(f"{category.capitalize()} Keywords in {pdf_file}")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()


# Replace this with the path to your PDF file
pdf_file = "2021_Apple_ESG_Report.pdf"

# Call the function to analyze ESG-related words in the PDF
analyze_esg_in_pdf(pdf_file)
