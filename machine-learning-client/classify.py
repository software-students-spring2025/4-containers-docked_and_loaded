"""Module to classify images of player for rock paper scissors game"""

import base64
from openai import OpenAI
import dotenv

dotenv.load_dotenv()

client = OpenAI()

def encode_image(image_path):
    """Encode image from given file path to base64"""

    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def classify_rps(image_path):
    """Classify image of player's hand as rock, paper, or scissors"""

    image = encode_image(image_path)

    prompt = """This image contains a person playing the game rock paper scissors.
    Determine which of the three options they chose and output it as a single word."""

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": prompt },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image}",
                        },
                    },
                ],
            }
        ],
    )

    return completion.choices[0].message.content
