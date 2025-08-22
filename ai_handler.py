import google.generativeai as genai
import config_manager

class AIHandler:
    def __init__(self):
        self.config = config_manager.get_config()
        self.api_key = self.config.get('api_key')
        if self.api_key:
            genai.configure(api_key=self.api_key)

    def generate_text(self, prompt, text):
        if not self.api_key:
            return "API key not found. Please set it in the settings."

        try:
            model = genai.GenerativeModel('gemini-2.5-flash-lite')
            full_prompt = f"{prompt}:\n\n{text}"
            response = model.generate_content(full_prompt)
            # Combine text from all parts of the response
            full_response_text = "".join(part.text for part in response.parts)
            return full_response_text
        except Exception as e:
            return f"Error generating text: {e}"

    def fix_grammar(self, text):
        prompt = "Fix the grammar and structure of the following text. Only return the corrected text, without any other comments. Keep the original language."
        return self.generate_text(prompt, text)

    def change_style(self, text, style):
        prompt = f"Change the writing style of the following text to {style}. Only return the modified text, without any other comments. Keep the original language."
        return self.generate_text(prompt, text)

    def direct_instruction(self, text, instruction):
        prompt = f"{instruction}. Only return the modified text, without any other comments. Keep the original language."
        return self.generate_text(prompt, text)

