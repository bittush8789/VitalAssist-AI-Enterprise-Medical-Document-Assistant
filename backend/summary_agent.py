from llm.groq_client import groq_client
from llm.prompts import SUMMARY_PROMPT

class SummaryAgent:
    def process(self, text: str):
        summary = groq_client.get_completion(text, system_message=SUMMARY_PROMPT)
        return summary

summary_agent = SummaryAgent()
