from flask import Flask, request, jsonify
from flask_cors import CORS
from astrapy import DataAPIClient
from dotenv import load_dotenv
import os
import pandas as pd
import requests
from typing import Optional

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load environment variables
load_dotenv()
ASTRA_TOKEN = os.environ.get("ASTRA_TOKEN")
LANGFLOW_ID = os.environ.get("LANGFLOW_ID")
FLOW_ID = os.environ.get("FLOW_ID")
APPLICATION_TOKEN = os.environ.get("APPLICATION_TOKEN")

# ASTRA DB setup
client = DataAPIClient(ASTRA_TOKEN)
db = client.get_database_by_api_endpoint(
  "https://c1ed2c64-01fc-4cd3-b5e7-27b27dd472d7-us-east-2.apps.astra.datastax.com"
)
print("Connected to AstraDB")

# LANGFLOW constants
BASE_API_URL = "https://api.langflow.astra.datastax.com"

# Dataset columns
CATEGORIAL = ["post_type", "sentiment", "platform", "day_of_week", "post_time"]
NUMERICAL = ["likes", "shares", "comments", "engmnt_time", "react", "impressions"]
TWEAKS = {
    "GroqModel-uPBO8": {"temperature": 0},
    "ChatInput-eb2bV": {},
    "ChatOutput-5ZQTb": {}
}

def run_flow(message: str,
             endpoint: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             application_token: Optional[str] = None) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    try:
        data = request.json
        post_type = data.get('postType')
        
        # Get data from AstraDB
        collection = db.get_collection("social_media_data")
        df = pd.DataFrame(collection.find({"post_type": post_type}))

        # Generate summaries
        numerical_summary = df.describe()
        categorial_summary = ""
        for category in CATEGORIAL:
            categorial_summary += str(df[category].value_counts()) + "\n"
        
        # Create prompt
        prompt_message = f'''I have given you a summary about a dataset's numerical columns and categorial columns.
        Numerical summary:\n{numerical_summary}\nCategorial summary:\n{categorial_summary}
        Your job is to generate simple one liner analytics about the data. For example, "Carousel posts have 20% higher engagement than static posts" and "Reels drive 2x more comments compared to other formats".
        Limit the insights to a maximum of 5. Maintain simple language. Prefer to use percentages.
        Do not add any supplementary text around the analytics and only return the analytics.'''
        
        # Run flow
        response = run_flow(
            message=prompt_message,
            endpoint=FLOW_ID,
            application_token=APPLICATION_TOKEN,
            tweaks=TWEAKS
        )
        
        return jsonify({
            'success': True,
            'insights': response["outputs"][0]["outputs"][0]["messages"][0]["message"]
        })
    
    except Exception as e:
        print(f"Error: {e}")  # Print the error to the console
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
