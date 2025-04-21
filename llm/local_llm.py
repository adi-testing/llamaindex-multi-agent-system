import os
import json
import logging
import requests
from typing import Dict, List, Optional, Any

from llama_index.llms.openai import OpenAI
from llama_index.llms.openai_like import OpenAILike
from llama_index.core.llms import LLM

logger = logging.getLogger(__name__)

class CustomOpenAILike(OpenAILike):
    """Custom OpenAILike class to align with the required payload format."""
    
    def _post(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Sends a POST request to the specified URL with the given payload.
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()                    # Handle HTTP errors
            logger.debug(f"Raw response: {response.text}") # Log the raw response for debugging purposes
            return response.json()                         # Return the JSON response from the server
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP request failed: {e}")      # Log the error
            raise

    def _complete(self, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        """Override the _complete method to send the correct 'messages' payload."""
        # Constructs the payload to match the expected format for local LLMs
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": self.model,
        }
        if "temperature" in kwargs:
            payload["temperature"] = kwargs["temperature"]
        if "max_tokens" in kwargs:
            payload["max_tokens"] = kwargs["max_tokens"]

        logger.debug(f"Sending payload: {payload}")         # Log the payload for debugging
        response = self._post(self.api_base, payload)       # Call the POST method to send the request to the LLM server
        logger.debug(f"Received response: {response}")

        # Parses the response from the server to extract the completion text and other metadata.
        try:
            completion_text = response["choices"][0]["message"]["content"]
            
            # Create a response dictionary
            response_dict = {
                "id": response.get("id", ""),
                "object": response.get("object", "chat.completion"),
                "created": response.get("created", 0),
                "model": response.get("model", self.model),
                "choices": [{"text": completion_text}],
                "usage": response.get("usage", {}),
            }
            
            # Convert to a class with attributes
            class AttrDict(dict):
                def __init__(self, *args, **kwargs):
                    super(AttrDict, self).__init__(*args, **kwargs)
                    self.__dict__ = self
                    
            # Create an object that has both dictionary access and attribute access
            result = AttrDict(response_dict)
            
            # Add the required attributes explicitly
            result.text = completion_text
            result.additional_kwargs = {}  # Add empty additional_kwargs
            
            # Add other common attributes the OpenAI class might expect
            result.raw = response  # Store the original response
            result.delta = None    # Often used in streaming responses
            
            return result
            
        except (KeyError, IndexError) as e:
            logger.error(f"Invalid response format: {response}")
            raise ValueError("Invalid response format from local LLM server") from e

def get_llm(config: Dict[str, Any]) -> LLM:
    """Factory function to get the appropriate LLM based on config."""
    llm_type = config.get("LLM_TYPE", "local")
    
    if llm_type == "openai":
        logger.info("Using OpenAI LLM")
        return OpenAI(
            model=config["OPENAI_LLM_MODEL"],
            api_key=config["OPENAI_API_KEY"]
        )
    else:
        logger.info("Using Local LLM via LM Studio")
        return CustomOpenAILike(
            model=config.get("LOCAL_LLM_MODEL", "local-model"),                # Just a placeholder for local model
            api_base=config.get("LOCAL_LLM_URL", "http://localhost:1234/v1"),  # The URL for the local LLM server, 1234 is a common default
            api_key="fake"                                                     # Set to a dummy value for local LLMs
        )

