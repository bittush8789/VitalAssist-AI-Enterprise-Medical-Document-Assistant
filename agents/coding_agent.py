from llm.groq_client import groq_client
from llm.prompts import CODING_PROMPT
import json

class CodingAgent:
    def process(self, diagnosis_text: str):
        prompt = CODING_PROMPT.format(input_text=diagnosis_text)
        result_str = groq_client.get_completion(prompt, system_message="You are a medical coding expert.", json_mode=True)
        try:
            return json.loads(result_str)
        except:
            return {"icd_10_codes": [], "cpt_codes": []}

coding_agent = CodingAgent()
