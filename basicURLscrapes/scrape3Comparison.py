import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import spacy
import matplotlib.pyplot as plt
from collections import Counter

# Download NLTK stopwords
nltk.download("stopwords")
nltk.download("punkt")

# Load the English spaCy model
nlp = spacy.load("en_core_web_sm")


# Function to scrape a web page and extract ESG-related keywords
def scrape_and_analyze_esg(url, title):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch the web page for {title}.")
        return

    # Parse the HTML content of the web page using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract text content from the HTML
    page_text = soup.get_text()

    # Tokenize the text using NLTK
    words = nltk.word_tokenize(page_text)

    # Remove stopwords and non-alphabetic words
    words = [
        word.lower()
        for word in words
        if word.isalpha() and word.lower() not in stopwords.words("english")
    ]

    # Create a spaCy Doc object for NLP analysis
    doc = nlp(" ".join(words))

    # Define a list of ESG-related keywords
    esg_keywords = [
        "environment",
        "social",
        "governance",
        "sustainability",
        "responsibility",
        "ethics",
        "climate",
        "green",
        "ethical",
        "carbon",
        "diversity",
        "equality",
        "corporate governance",
        "ESG",
        "responsible",
    ]

    # Count the occurrences of ESG keywords
    esg_counts = Counter()

    for token in doc:
        if token.text.lower() in esg_keywords:
            esg_counts[token.text.lower()] += 1

    # Calculate a simple ESG score based on keyword occurrences
    total_keywords = sum(esg_counts.values())
    esg_score = (total_keywords / len(words)) * 100

    # Create a bar chart for ESG keyword counts
    plt.figure(figsize=(10, 6))
    plt.bar(esg_counts.keys(), esg_counts.values())
    plt.xlabel("ESG Keywords")
    plt.ylabel("Keyword Count")
    plt.title(f"ESG Keyword Counts for {title}")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Provide a summary
    print(f"{title} ESG Score: {esg_score:.2f}%")
    print(f"{title} ESG Keyword Counts:")
    for keyword, count in esg_counts.items():
        print(f"{keyword}: {count}")

    # Show the bar chart
    plt.show()


# Replace these URLs and titles with the web pages you want to scrape and their corresponding titles
urls = [
    {"url": "https://finance.yahoo.com/quote/BABA/", "title": "BABA from Yahoo"},
    {"url": "https://finance.yahoo.com/quote/SONY", "title": "SONY from Yahoo Finance"},
]

for url_info in urls:
    scrape_and_analyze_esg(url_info["url"], url_info["title"])
