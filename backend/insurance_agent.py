from llm.groq_client import groq_client
from llm.prompts import INSURANCE_PROMPT
import json

class InsuranceAgent:
    def process(self, text: str):
        result_str = groq_client.get_completion(text, system_message=INSURANCE_PROMPT, json_mode=True)
        try:
            return json.loads(result_str)
        except:
            return {"policy_status": "Unknown", "coverage_details": "N/A", "eligibility": "N/A", "fraud_risk": "Unknown"}

insurance_agent = InsuranceAgent()
