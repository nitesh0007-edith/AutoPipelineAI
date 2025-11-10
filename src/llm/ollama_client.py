"""
Ollama Client - Manages connections to local Ollama LLM server
"""
import openai
import requests
from typing import Optional, Dict, List
from loguru import logger


class OllamaClient:
    """Client for interacting with Ollama LLM server"""

    def __init__(self, base_url: str = "http://localhost:11434", api_key: str = "ollama"):
        """
        Initialize Ollama client

        Args:
            base_url: Base URL for Ollama server
            api_key: API key (default: "ollama" for local)
        """
        self.base_url = base_url
        self.api_key = api_key
        self.client = openai.OpenAI(base_url=f"{base_url}/v1", api_key=api_key)
        logger.info(f"Initialized Ollama client with base URL: {base_url}")

    def check_connection(self) -> bool:
        """
        Check if Ollama server is running and accessible

        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                logger.success("Ollama server is running")
                return True
            else:
                logger.warning(f"Ollama server returned status code: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Ollama server. Is it running?")
            return False
        except Exception as e:
            logger.error(f"Error checking Ollama connection: {e}")
            return False

    def list_models(self) -> List[str]:
        """
        List available models on Ollama server

        Returns:
            List of model names
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [model["name"] for model in models]
                logger.info(f"Found {len(model_names)} models: {model_names}")
                return model_names
            return []
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []

    def generate_completion(
        self,
        prompt: str,
        model: str = "llama3",
        system_prompt: Optional[str] = None,
        temperature: float = 0.4,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> str:
        """
        Generate completion from Ollama model

        Args:
            prompt: User prompt
            model: Model name (default: llama3)
            system_prompt: Optional system prompt
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream response

        Returns:
            Generated text completion
        """
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            kwargs = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "stream": stream
            }

            if max_tokens:
                kwargs["max_tokens"] = max_tokens

            response = self.client.chat.completions.create(**kwargs)

            if stream:
                return response  # Return stream object
            else:
                return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error generating completion: {e}")
            raise

    def generate_structured_output(
        self,
        prompt: str,
        model: str = "llama3",
        temperature: float = 0.2
    ) -> Dict:
        """
        Generate structured JSON output from model

        Args:
            prompt: User prompt requesting JSON output
            model: Model name
            temperature: Sampling temperature

        Returns:
            Parsed JSON dictionary
        """
        import json

        system_prompt = "You are a helpful assistant that responds ONLY with valid JSON. No other text."

        response = self.generate_completion(
            prompt=prompt,
            model=model,
            system_prompt=system_prompt,
            temperature=temperature
        )

        try:
            # Try to extract JSON from markdown code blocks
            import re
            match = re.search(r"```(?:json)?\s*(.*?)\s*```", response, re.DOTALL)
            if match:
                json_str = match.group(1)
            else:
                json_str = response

            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response was: {response}")
            raise ValueError(f"Model did not return valid JSON: {e}")
