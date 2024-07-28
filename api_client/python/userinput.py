from flask import Flask, request, jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET
from cdg_client import CDGClient
from configparser import ConfigParser
import joblib
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration Constants
BILL_HR = "hr"
API_KEY_PATH = "../secrets.ini"

# Preprocessing Functions
def preprocess_text(text):
    """Clean and preprocess text data."""
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\W', ' ', text)
    text = text.strip()
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [w for w in words if w not in stop_words]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(w) for w in words]
    return ' '.join(words)

def get_bill_details(client, congress, bill_type, bill_num):
    """Fetch bill details from the Library of Congress API."""
    endpoint = f"bill/{congress}/{bill_type}/{bill_num}"
    data, _ = client.get(endpoint)
    return ET.fromstring(data)

def extract_bill_info(bill_xml):
    """Extract relevant information from the bill XML."""
    bill_info = {
        'title': bill_xml.findtext(".//title").strip(),
        'text': bill_xml.findtext(".//text"),
        'sponsor': bill_xml.findtext(".//sponsor"),
        'cosponsors': [cosponsor.text for cosponsor in bill_xml.findall(".//cosponsors/item")]
    }
    return bill_info

def fetch_bill_data(client, congress, bill_type, bill_num):
    """Fetch data for a single bill."""
    bill_xml = get_bill_details(client, congress, bill_type, bill_num)
    bill_info = extract_bill_info(bill_xml)
    return bill_info

def summarize_bill_with_gemini(bill_title):
    """Summarize the bill using the Gemini API."""
    api_key = os.getenv("GOOGLE_API_KEY")
    # Ensure the title is not empty
    if not bill_title:
        raise ValueError("Bill title is empty. Cannot summarize an empty title.")
    # Set the API key
    genai.configure(api_key=api_key)
    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    # Start a chat session
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"""Please provide an informational and educational summary of the
                    following bill titled '{bill_title}':\n\n The summary should be factual and
                    provide key details about the bill's purpose, main provisions, and any
                    significant impacts. Please do not generate any information that doesn't directly have
                    to do with the bill (such as informing me that I did not provide enough information).
                    Please search the web for the information if you can. If you are unable to, please create a
                    summary from the information you know. Please keep your response educational and precise, and style
                    it for better user readability. If there are multiple bills with the same number, list all of
                    them."""
                ],
            }
        ]
    )
    # Send a valid message
    response = chat_session.send_message("Please provide a summary.")
    return response.text

@app.route('/fetch-bill', methods=['POST'])
def fetch_bill():
    data = request.json
    congress = data.get('congress')
    bill_num = data.get('bill_num')

    if not congress or not bill_num:
        return jsonify({'error': 'Congress number and Bill number are required'}), 400

    try:
        # Initialize API client
        config = ConfigParser()
        config.read(API_KEY_PATH)
        api_key = config.get("cdg_api", "api_auth_key")
        client = CDGClient(api_key, response_format="xml")
        # Set the Google API key environment variable
        google_api_key = config.get("google_api", "api_key")
        os.environ["GOOGLE_API_KEY"] = google_api_key
        # Load the trained model
        model = joblib.load('best_model.pkl')
        # Fetch bill data
        bill_data = fetch_bill_data(client, congress, BILL_HR, bill_num)
        # Summarize the bill using Gemini API
        bill_title = bill_data['title']
        if not bill_title:
            return jsonify({'error': 'The fetched bill has no title. Cannot proceed with summarization.'}), 400
        summary = summarize_bill_with_gemini(bill_title)
        # Preprocess the text
        bill_text = preprocess_text(bill_data['text'])
        # Predict and display the result
        prediction = model.predict([bill_text])[0]
        probabilities = model.predict_proba([bill_text])[0]
        # Create a dictionary of probabilities for each class
        class_probabilities = {label: prob for label, prob in zip(model.classes_, probabilities)}
        # Return the response
        return jsonify({
            'title': bill_title,
            'summary': summary,
            'classification': class_probabilities,
            'stance': {
                'democrat': class_probabilities.get('Democrat', 0),
                'republican': class_probabilities.get('Republican', 0),
                'independent': class_probabilities.get('Independent', 0)
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)