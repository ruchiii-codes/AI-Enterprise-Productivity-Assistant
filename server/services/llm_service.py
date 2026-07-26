import logging

from openai import (
    OpenAI,
    APIConnectionError,
    APITimeoutError,
    APIError,
)

from server.config import OPENROUTER_API_KEY

logger = logging.getLogger(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


def generate_response(prompt: str):
    try:
        logger.info("Sending request to OpenRouter")

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        logger.info("Response received successfully")

        return response.choices[0].message.content

    except APITimeoutError as e:
        logger.error(f"OpenRouter request timed out: {e}")
        raise

    except APIConnectionError as e:
        logger.error(f"Unable to connect to OpenRouter: {e}")
        raise

    except APIError as e:
        logger.error(f"OpenRouter API error: {e}")
        raise

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise