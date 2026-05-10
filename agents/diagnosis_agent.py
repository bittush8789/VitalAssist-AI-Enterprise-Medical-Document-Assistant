from llm.groq_client import groq_client
from llm.prompts import DIAGNOSIS_PROMPT
import json

class DiagnosisAgent:
    def process(self, text: str):
        result_str = groq_client.get_completion(text, system_message=DIAGNOSIS_PROMPT, json_mode=True)
        try:
            return json.loads(result_str)
        except:
            return {"diagnosis": [], "medications": [], "symptoms": [], "procedures": []}

diagnosis_agent = DiagnosisAgent()
