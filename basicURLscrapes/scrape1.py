import requests
from bs4 import BeautifulSoup

import nltk
from nltk.corpus import stopwords
import spacy
from spacy.lang.en.examples import sentences
from collections import Counter

# Download NLTK stopwords
nltk.download("stopwords")
nltk.download("punkt")

# Load the English spaCy model
nlp = spacy.load("en_core_web_sm")


# Function to scrape a web page and extract ESG-related keywords
def scrape_and_analyze_esg(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch the web page.")
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

    # Define ESG-related keywords
    esg_keywords = ["environment", "social", "governance"]

    # Count the occurrences of ESG keywords
    esg_counts = Counter()

    for token in doc:
        if token.text.lower() in esg_keywords:
            esg_counts[token.text.lower()] += 1

    # Calculate a simple ESG score based on keyword occurrences
    total_keywords = sum(esg_counts.values())
    esg_score = (total_keywords / len(words)) * 100

    # Provide a summary
    print("ESG Score: {:.2f}%".format(esg_score))
    print("ESG Keyword Counts:")
    for keyword, count in esg_counts.items():
        print(f"{keyword}: {count}")


# Replace this URL with the webpage you want to scrape
url = "https://www.alibabagroup.com/en-US/esg"

# Call the function to scrape and analyze ESG-related keywords
scrape_and_analyze_esg(url)
