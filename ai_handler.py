import google.generativeai as genai
import config_manager
import ollama
import requests


class AIHandler:
    def __init__(self, _):
        self._ = _
        self.config = config_manager.get_config()
        self.api_key = self.config.get("api_key")
        self.model = self.config.get("model")
        self.ai_provider = self.config.get("ai_provider", "gemini")
        self.ollama_model = self.config.get("ollama_model", "gemma3")
        self.llama_cpp_url = self.config.get("llama_cpp_url", "http://localhost:8080/v1")
        self.llama_cpp_model = self.config.get("llama_cpp_model", "local-model")
        if self.api_key and self.ai_provider == "gemini":
            genai.configure(api_key=self.api_key)

    def generate_text(self, prompt, text):
        if self.ai_provider == "gemini":
            if not self.api_key:
                return self._("API key not found. Please set it in the settings.")

            try:
                model = genai.GenerativeModel(self.model)
                full_prompt = f"{prompt}:\n\n{text}"
                response = model.generate_content(full_prompt)
                full_response_text = "".join(part.text for part in response.parts)
                return full_response_text
            except Exception as e:
                return self._(f"Error generating text with Gemini: {e}")
        elif self.ai_provider == "ollama":
            try:
                full_prompt = f"{prompt}:\n\n{text}"
                response = ollama.chat(
                    model=self.ollama_model,
                    messages=[
                        {
                            "role": "user",
                            "content": full_prompt,
                        },
                    ],
                )
                return response["message"]["content"]
            except Exception as e:
                return self._(f"Error generating text with Ollama: {e}")
        elif self.ai_provider == "llama_cpp":
            try:
                url = self.llama_cpp_url.rstrip("/")
                full_prompt = f"{prompt}:\n\n{text}"
                payload = {
                    "model": self.llama_cpp_model,
                    "messages": [{"role": "user", "content": full_prompt}],
                }
                response = requests.post(f"{url}/chat/completions", json=payload, timeout=30)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                return self._(f"Error generating text with llama.cpp: {e}")
        else:
            return self._("Invalid AI provider selected.")

    def fix_grammar(self, text):
        prompt = self._(
            "Fix the grammar and structure of the following text. Only return the corrected text, without any other comments. Keep the original language."
        )
        return self.generate_text(prompt, text)

    def change_style(self, text, style):
        prompt = self._(
            f"Change the writing style of the following text to {style}. Only return the modified text, without any other comments. Keep the original language."
        )
        return self.generate_text(prompt, text)

    def direct_instruction(self, text, instruction):
        prompt = self._(
            f"{instruction}. Only return the modified text, without any other comments. Keep the original language."
        )
        return self.generate_text(prompt, text)
