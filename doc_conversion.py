import pandas as pd  
import PyPDF2 as pdf  

import nltk  
import re  

# Download necessary NLTK data
nltk.download('punkt')  
nltk.download('stopwords')  
nltk.download('wordnet')  

from nltk.tokenize import word_tokenize  
from nltk.corpus import stopwords  
from nltk.stem import WordNetLemmatizer  

# Importing job_description from a local module
from job_description import job_description  

def convert_pdf_to_text(pdf_filepath):
    reader = pdf.PdfReader(pdf_filepath)  # Create a PDF reader object
    text = ''
    for page in reader.pages:
        text += page.extract_text()  # Extract text from each page
    return text

# Convert the PDF resume to text
resume = convert_pdf_to_text('/Users/tanaymehrish/Downloads/TM.pdf')

def tokenize(text):
    tokens = word_tokenize(text)  # Tokenize the text
    lemmatizer = WordNetLemmatizer()  # Create a lemmatizer object

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()  # Lemmatize, lowercase, and strip each token
        clean_tokens.append(clean_tok)

    return clean_tokens

# Tokenize the resume text
tokens = tokenize(resume)
# Tokenize the job description text
description_tokens = tokenize(job_description)

def get_contact():
    email = re.findall(r'\S+@\S+', resume)  # Find all email addresses in the resume
    return email

# Print the extracted email addresses
email = get_contact()


# Revised regex pattern to match Month Year format
def get_dates(tokens):
    processed_text = ' '.join(tokens)

    date_pattern = re.compile(
    r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',
    re.IGNORECASE)

    # Find all matches
    dates = date_pattern.findall(processed_text)
    # Convert matches to title case for consistent formatting
    formatted_dates = [date.title() for date in dates]
    return formatted_dates
formatted_dates = get_dates(tokens)
formatted_description_dates = get_dates(description_tokens) 


# Make a pd.datetime to get today's date
def find_grad(formatted_dates):
    today = pd.to_datetime('today').date()
    for date in formatted_dates:
        date = pd.to_datetime(date).date()  
        if date > today:
            grad_date = date  # If the date is in the future, set it as the graduation date
            print("Graduation Date: ", grad_date) 
    return grad_date
grad_date = find_grad(formatted_dates)

# Find latest date in the job description
def find_latest(formatted_description_dates):
    if not formatted_description_dates:
        return None
    latest_date = max(formatted_description_dates, key=lambda x: pd.to_datetime(x))
    return latest_date
latest_date = find_latest(formatted_description_dates)



# See if student will get is eligible for the job
def get_eligibility(grad_date, latest_date):
    if grad_date < pd.to_datetime(latest_date).date():
        eligibility = "Candidate is eligible for the job."
    else:
        eligibility = "Candidate is not eligible for the job."
    return eligibility
eligibility = get_eligibility(grad_date, latest_date)

# Find all matches in the resume
def get_matches(tokens, description_tokens):
    matches = []
    for token in tokens:
        if token in description_tokens:
            matches.append(token)  # Append token to matches if it is in description_tokens

    # Delete all spaces and special characters and remove repeats
    matches = [re.sub(r'\W+', '', match) for match in matches]  # Remove non-word characters from each match
    matches = list(set(matches))  # Remove duplicate matches by converting to a set and back to a list 

    # Take out unnecessary words in matches
    stop_words = set(stopwords.words('english'))  # Create a set of stopwords
    matches = [match for match in matches if match not in stop_words]  # Filter out stopwords
    return matches
matches = get_matches(tokens, description_tokens)
print(matches)

# Get the strength of the resume
def get_strength(matches):
    strength = ""
    length = len(matches)
    if length >= 35:
        strength = "Strong"
    elif length >= 25:
        strength = "Moderate"
    else:
        strength = "Weak"
    return strength
strength = get_strength(matches)
print(strength)









