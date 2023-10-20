import os
import PyPDF2
import nltk
import re
from flask import Flask, request, render_template
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("agg")

app = Flask(__name__)

# Download NLTK stopwords and wordnet
nltk.download("stopwords")
nltk.download("wordnet")

# Define the upload folder for PDF files
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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
def analyze_esg_in_text(pdf_text):
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
        plt.title(f"{category.capitalize()} Keywords in Uploaded PDF")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        chart_filename = f"static/{category}_chart.png"
        plt.savefig(chart_filename)
        plt.close()

    return esg_counts


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if a file was uploaded
        if "file" not in request.files:
            return render_template("index.html", error="No file provided.")

        file = request.files["file"]

        # Check if the file has a filename
        if file.filename == "":
            return render_template("index.html", error="No file selected.")

        # Check if the file is a PDF
        if not file.filename.endswith(".pdf"):
            return render_template("index.html", error="Only PDF files are supported.")

        # Save the uploaded PDF to the uploads folder
        pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(pdf_path)

        # Extract text from the PDF and analyze ESG keywords
        pdf_text = extract_text_from_pdf(pdf_path)
        esg_counts = analyze_esg_in_text(pdf_text)

        return render_template("results.html", pdf_path=pdf_path, esg_counts=esg_counts)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
