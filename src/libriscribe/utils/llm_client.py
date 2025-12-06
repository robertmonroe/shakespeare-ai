# src/libriscribe/utils/llm_client.py
import openai
from openai import OpenAI  # For OpenAI
import logging
from tenacity import retry, stop_after_attempt, wait_random_exponential
from libriscribe.settings import Settings

import anthropic  # For Claude
import google.generativeai as genai  # For Google AI Studio
import requests  # For DeepSeek and Mistral
import re # For regex operations

# ADDED THIS: Import the function
from libriscribe.utils.file_utils import extract_json_from_markdown

logger = logging.getLogger(__name__)

# Configure httpx logger to be less verbose
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)  # Or ERROR, to suppress even warnings


class LLMClient:
    """Unified LLM client for multiple providers."""

    def __init__(self, llm_provider: str):
        self.settings = Settings()
        self.llm_provider = llm_provider
        self.client = self._get_client()  # Initialize the correct client
        self.model = self._get_default_model()

    def _get_client(self):
        """Initializes the appropriate client based on the provider."""
        if self.llm_provider == "openrouter":
            return OpenAI(
                api_key=self.settings.openrouter_api_key,
                base_url=self.settings.openrouter_base_url
            )
        elif self.llm_provider == "openai" or self.llm_provider == "openrouter":
            if not self.settings.openai_api_key:
                raise ValueError("OpenAI API key is not set.")
            return OpenAI(api_key=self.settings.openai_api_key)
        elif self.llm_provider == "claude":
            if not self.settings.claude_api_key:
                raise ValueError("Claude API key is not set.")
            return anthropic.Anthropic(api_key=self.settings.claude_api_key)
        elif self.llm_provider == "google_ai_studio":
            if not self.settings.google_ai_studio_api_key:
                raise ValueError("Google AI Studio API key is not set.")
            genai.configure(api_key=self.settings.google_ai_studio_api_key)
            return genai  # We don't instantiate a client, we use the module directly
        elif self.llm_provider == "deepseek":
             if not self.settings.deepseek_api_key:
                raise ValueError("DeepSeek API key is not set.")
             return None  # No client object, we'll use requests directly
        elif self.llm_provider == "mistral":
             if not self.settings.mistral_api_key:
                raise ValueError("Mistral API key is not set")
             return None
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")

    def _get_default_model(self):
        """Gets the default model name for the selected provider."""
        if self.llm_provider == "openrouter":
            return self.settings.openrouter_model
        elif self.llm_provider == "openai" or self.llm_provider == "openrouter":
            return "gpt-4o-mini"
        elif self.llm_provider == "claude":
            return "claude-3-opus-20240229" # Or another appropriate Claude 3 model
        elif self.llm_provider == "google_ai_studio":
            return "gemini-2.0-flash-exp" if self.settings.app_env == "production" else "gemini-2.0-flash"
        elif self.llm_provider == "deepseek":
             return "deepseek-coder-6.7b-instruct"
        elif self.llm_provider == "mistral":
            return "mistral-medium-latest"
        else:
            return "unknown"  # Should not happen, but good for safety
    def set_model(self, model_name: str):
      self.model = model_name

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def generate_content(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.7, language: str = "English") -> str:
        """
        Generates text using the selected LLM provider.
        Now supports specifying the output language explicitly.
        """
        try:
            # Append language instruction to prompt if not already included
            if "IMPORTANT: The content should be written entirely in" not in prompt and language != "English":
                prompt += f"\n\nIMPORTANT: Generate the response in {language}."
                
            if self.llm_provider == "openai" or self.llm_provider == "openrouter":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt + "\n\nPlease format any JSON output in markdown code blocks with ```json```" if self.llm_provider == "openrouter" else prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                content = response.choices[0].message.content.strip()
                # Post-process OpenRouter responses to ensure markdown JSON format
                if self.llm_provider == "openrouter" and "```json" not in content and "{" in content:
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        content = f"```json\n{json_match.group()}\n```"
                return content

            elif self.llm_provider == "claude":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()

            elif self.llm_provider == "google_ai_studio":
                model = self.client.GenerativeModel(model_name=self.model)
                response = model.generate_content(prompt) # No need for messages list with genai
                return response.text.strip()

            elif self.llm_provider == "deepseek":
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.settings.deepseek_api_key}"
                }
                data = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }
                response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data, timeout=120) # Timeout
                response.raise_for_status() # Raise for HTTP errors
                return response.json()["choices"][0]["message"]["content"].strip()
            elif self.llm_provider == "mistral":
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.settings.mistral_api_key}"
                }
                data = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }

                response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=data, timeout=120)
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content'].strip()

            else:
                return "" #  Should not happen, provider checked in init

        except Exception as e:
            logger.exception(f"Error during {self.llm_provider} API call: {e}")
            print(f"ERROR: {self.llm_provider} API error: {e}")
            return ""
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
    def generate_content_with_json_repair(self, original_prompt: str, max_tokens:int = 2000, temperature:float=0.7) -> str:
        """Generates content and attempts to repair JSON errors."""
        response_text = self.generate_content(original_prompt, max_tokens, temperature)
        logger.info(f"[CHAR_DEBUG] LLM response length: {len(response_text) if response_text else 0}")
        if response_text:
            json_data = extract_json_from_markdown(response_text)
            logger.info(f"[CHAR_DEBUG] JSON extraction result: {type(json_data) if json_data is not None else 'None'}")
            if json_data is not None:
                return response_text # Return the original markdown
            else:
                repair_prompt = f"You are a helpful AI that only returns valid JSON.  Fix the following broken JSON:\n\n```json\n{response_text}\n```"
                repaired_response = self.generate_content(repair_prompt, max_tokens=max_tokens, temperature=0.2) #Low temp for corrections
                if repaired_response:
                    repaired_json = extract_json_from_markdown(repaired_response)
                    if repaired_json is not None:
                        # CRITICAL CHANGE:  Return the JSON *string*, not wrapped in Markdown.
                        return repaired_response 
        logger.error(f"[CHAR_DEBUG] JSON repair failed. Response was: {response_text[:200] if response_text else 'empty'}")
        return "" # Return empty
    def generate_content_with_image(self, prompt: str, image_base64: str, max_tokens: int = 500) -> str:
        '''Generate content with image input (vision). Only supports Google AI Studio (Gemini).'''
        import google.generativeai as genai
        import base64
        from io import BytesIO
        from PIL import Image
        
        try:
            genai.configure(api_key=self.settings.google_ai_studio_api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            # Decode base64 to image
            image_data = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_data))
            
            # Generate content with image
            response = model.generate_content([prompt, image])
            return response.text.strip()
        except Exception as e:
            import logging
            logging.getLogger(__name__).exception(f'Vision analysis error: {e}')
            return '[Vision analysis failed]'
