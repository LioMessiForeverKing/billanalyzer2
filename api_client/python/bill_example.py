#!/usr/bin/env python3
"""
   Bill Stance Classification


   This script uses the Library of Congress API to collect bill data and train a
   machine learning model to classify the bills as having a Republican, Democratic, or Middle stance.


   @copyright: 2022, Library of Congress
   @license: CC0 1.0
"""


import xml.etree.ElementTree as ET
from cdg_client import CDGClient  # Ensure this module is in your path
from configparser import ConfigParser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)

# Configuration
BILL_HR = "hr"
CONGRESS = 117
API_KEY_PATH = "../secrets.ini"
BILL_NUMS = [21, 22, 23, 24, 25, 29, 65, 69, 71, 75, 79, 108, 112, 208, 340, 355, 370, 401, 410, 450]  # Example bill numbers to fetch


def get_bill_details(client, congress, bill_type, bill_num):
   """Fetch bill details from the Library of Congress API."""
   endpoint = f"bill/{congress}/{bill_type}/{bill_num}"
   data, _ = client.get(endpoint)
   return ET.fromstring(data)


def extract_bill_info(bill_xml):
   """Extract relevant information from the bill XML."""
   bill_info = {
       'title': bill_xml.findtext(".//title"),
       'text': bill_xml.findtext(".//text"),
       'sponsor': bill_xml.findtext(".//sponsor"),
       'cosponsors': [cosponsor.text for cosponsor in bill_xml.findall(".//cosponsors/item")]
       # Add more fields as needed
   }
   return bill_info


def fetch_bill_data(client, congress, bill_type, bill_nums):
   """Fetch data for multiple bills."""
   bills = []
   for bill_num in bill_nums:
       bill_xml = get_bill_details(client, congress, bill_type, bill_num)
       bill_info = extract_bill_info(bill_xml)
       bills.append(bill_info)
       print(f"Fetched Bill Title: {bill_info['title']}")  # Display the title of each bill
   return bills


@app.route('/api/bill/<int:bill_number>', methods=['GET'])
def get_bill_data(bill_number):
    try:
        # Fetch bill data using the existing logic
        bill_xml = get_bill_details(client, CONGRESS, BILL_HR, bill_number)
        bill_info = extract_bill_info(bill_xml)
        
        # Example stance data
        stance = {
            'democrat': 40,
            'republican': 50,
            'independent': 10
        }
        
        response = {
            'title': bill_info['title'],
            'stance': stance
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
   # Initialize API client
   config = ConfigParser()
   config.read(API_KEY_PATH)
   api_key = config.get("cdg_api", "api_auth_key")
   client = CDGClient(api_key, response_format="xml")


   # Fetch bill data
   print(f"Fetching bill data for Congress {CONGRESS}...")
   bill_data = fetch_bill_data(client, CONGRESS, BILL_HR, BILL_NUMS)


   # Create a DataFrame
   df = pd.DataFrame(bill_data)
   df['party'] = [
       'Middle', 'Republican', 'Middle', 'Republican', 'Republican',
       'Democratic', 'Middle', 'Republican', 'Republican', 'Democratic',
       'Middle', 'Republican', 'Republican', 'Middle', 'Republican',
       'Democratic', 'Republican', 'Middle', 'Republican', 'Democratic'
   ]  # Example labels including "Middle"


   # Preprocess data
   texts = df['text'].fillna('')  # Ensure there are no missing texts
   labels = df['party']


   # Split the data
   X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.80, random_state=32)


   # Create and train the model
   model = make_pipeline(TfidfVectorizer(), MultinomialNB())
   model.fit(X_train, y_train)


   # Predict and evaluate
   predictions = model.predict(X_test)
   accuracy = accuracy_score(y_test, predictions)
   report = classification_report(y_test, predictions)


   print(f'Accuracy: {accuracy}')
   print(f'Classification Report:\n{report}')

   app.run(debug=True)


# Although they come out as bipartisn; they always lean towards one party. A bill might be 53% republican and 47% democratic.
# Build a ML Model using library of congress api and sklearn to train the model to analyze bills and basically write system
# and give out like a percentage.