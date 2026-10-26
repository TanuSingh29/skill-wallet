"""
Gemini Client Module for Multimodal Construction Intelligence Platform.
Handles communication with Google Gemini API with fallback to Demo Mode.
"""

import os
import json
import re
from typing import Optional, Dict, Any, Union
from PIL import Image
import io

class GeminiPlatformClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.is_demo_mode = not bool(self.api_key.strip())
        self._client = None
        self._init_client()

    def _init_client(self):
        """Initializes the Gemini client if an API key is provided."""
        if not self.is_demo_mode:
            try:
                # Prefer modern google-genai SDK
                from google import genai
                self._client = genai.Client(api_key=self.api_key.strip())
                self._sdk_type = "google-genai"
            except ImportError:
                try:
                    # Fallback to legacy google-generativeai
                    import google.generativeai as legacy_genai
                    legacy_genai.configure(api_key=self.api_key.strip())
                    self._client = legacy_genai
                    self._sdk_type = "google-generativeai"
                except Exception as e:
                    self.is_demo_mode = True
                    self._error = f"Failed to initialize Gemini SDK: {str(e)}"
            except Exception as e:
                self.is_demo_mode = True
                self._error = str(e)

    def set_api_key(self, api_key: str):
        """Update API key dynamically."""
        self.api_key = api_key.strip()
        self.is_demo_mode = not bool(self.api_key)
        self._init_client()

    def analyze_image_multimodal(
        self,
        image: Image.Image,
        prompt: str,
        system_instruction: str = "You are an expert structural and site safety engineer.",
        model_name: str = "gemini-2.5-flash"
    ) -> Dict[str, Any]:
        """
        Submits an image and prompt to Gemini Multimodal.
        Returns extracted structured dict or raw text.
        """
        if self.is_demo_mode:
            return {"demo_mode": True, "error": "No API key provided"}

        try:
            if self._sdk_type == "google-genai":
                from google.genai import types
                
                # Convert PIL image to bytes
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                img_bytes = buffered.getvalue()

                # Call modern SDK
                response = self._client.models.generate_content(
                    model=model_name,
                    contents=[
                        types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"),
                        prompt
                    ],
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.2,
                        response_mime_type="application/json"
                    )
                )
                raw_text = response.text
                return self.parse_json_response(raw_text)

            elif self._sdk_type == "google-generativeai":
                # Legacy SDK fallback
                model = self._client.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=system_instruction,
                    generation_config={"response_mime_type": "application/json", "temperature": 0.2}
                )
                response = model.generate_content([image, prompt])
                return self.parse_json_response(response.text)

        except Exception as e:
            return {"demo_mode": True, "error": f"Gemini API Error: {str(e)}"}

    def chat_query(
        self,
        messages: list,
        system_instruction: str,
        model_name: str = "gemini-2.5-flash"
    ) -> str:
        """
        Conduct multi-turn chat with the Gemini assistant.
        """
        if self.is_demo_mode:
            return ""

        try:
            if self._sdk_type == "google-genai":
                from google.genai import types
                formatted_contents = []
                for msg in messages:
                    role = "user" if msg["role"] == "user" else "model"
                    formatted_contents.append(
                        types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
                    )

                response = self._client.models.generate_content(
                    model=model_name,
                    contents=formatted_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.4
                    )
                )
                return response.text
            elif self._sdk_type == "google-generativeai":
                chat = self._client.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=system_instruction
                ).start_chat(history=[])
                # Replay conversation except the last prompt
                for m in messages[:-1]:
                    if m["role"] == "user":
                        chat.send_message(m["content"])
                resp = chat.send_message(messages[-1]["content"])
                return resp.text
        except Exception as e:
            return f"⚠️ Error querying Gemini: {str(e)}. Falling back to local advisory."

    @staticmethod
    def parse_json_response(text: str) -> Dict[str, Any]:
        """Safely parses JSON even if wrapped in markdown code blocks."""
        if not text:
            return {"error": "Empty response"}
        cleaned = text.strip()
        # Remove markdown ```json ... ``` wrapper if present
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # Try to match the first JSON object or array
            match = re.search(r"(\{.*\}|\[.*\])", cleaned, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except Exception:
                    pass
            return {"raw_text": text, "error": "Could not parse JSON"}
