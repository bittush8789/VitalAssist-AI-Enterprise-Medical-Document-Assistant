import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqClient:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

    def get_completion(self, prompt: str, system_message: str = "You are a helpful medical assistant.", json_mode: bool = False):
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                response_format={"type": "json_object"} if json_mode else None,
                temperature=0.1,
                max_tokens=4096
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

groq_client = GroqClient()
