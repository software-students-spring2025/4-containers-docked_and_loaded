"""Module to classify images of player for rock paper scissors game"""

from openai import OpenAI
import dotenv

dotenv.load_dotenv()

client = OpenAI()


def classify_rps_base64(image_base64):
    """Classify image of player's hand as rock, paper, or scissors"""
    prompt = """This image contains a person playing the game rock paper scissors.
    Determine which of the three options they chose and output it as a single word."""

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_base64,
                        },
                    },
                ],
            }
        ],
    )

    classification = completion.choices[0].message.content.strip().lower()

    choices = {"rock": 1, "paper": 2, "scissors": 3}

    return choices.get(classification, 0)
