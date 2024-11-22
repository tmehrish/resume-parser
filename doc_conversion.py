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

# Import example job description
from job_description import job_description  

# Convert a pdf to text
def convert_pdf_to_text(pdf_filepath):
    reader = pdf.PdfReader(pdf_filepath)  
    text = ''
    for page in reader.pages:
        text += page.extract_text()  
    return text

resume = convert_pdf_to_text('/Users/tanaymehrish/Downloads/TM.pdf')


# Tokenize the text for analysis
def tokenize(text):
    tokens = word_tokenize(text)  # Tokenize the text
    lemmatizer = WordNetLemmatizer()  # Create a lemmatizer object

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()  
        clean_tokens.append(clean_tok)

    return clean_tokens


tokens = tokenize(resume)
description_tokens = tokenize(job_description)


# Extract email address from the resume using regex
def get_contact():
    email = re.findall(r'\S+@\S+', resume) 
    return email

email = get_contact()
print(email)


# Return all dates in the resume using a regex pattern
def get_dates(tokens):
    processed_text = ' '.join(tokens)

    date_pattern = re.compile(
    r'\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}\b')

    # Find all matches and format them
    dates = date_pattern.findall(processed_text)
    formatted_dates = [date.title() for date in dates]
    return formatted_dates
formatted_dates = get_dates(tokens)
formatted_description_dates = get_dates(description_tokens) 



# Find the graduation date using the current date
def find_grad(formatted_dates):
    today = pd.to_datetime('today').date() # Use a pd.to_datetime() function to get the current date
    for date in formatted_dates:
        date = pd.to_datetime(date).date()  
        if date > today:
            grad_date = date  
            #print("Graduation Date: ", grad_date) 
    return grad_date
grad_date = find_grad(formatted_dates)

# Find latest date in the job description and if there is no date, return None
def find_latest(formatted_description_dates):
    if not formatted_description_dates:
        return None
    latest_date = max(formatted_description_dates, key=lambda x: pd.to_datetime(x)) # Use a lambda function for simple formatting
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
print(eligibility)

# Return the filtered/cleaned matches between the resume and job description
def get_matches(tokens, description_tokens):
    matches = []
    for token in tokens:
        if token in description_tokens:
            matches.append(token)  

    # Delete all spaces and special characters and remove repeats
    matches = [re.sub(r'\W+', '', match) for match in matches]  
    matches = list(set(matches))  

    # Take out unnecessary words in matches
    stop_words = set(stopwords.words('english'))  # Create a set of stopwords
    matches = [match for match in matches if match not in stop_words]  
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









