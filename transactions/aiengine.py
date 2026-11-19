
import json
from google import genai
from django.conf import settings
from decouple import config 
api_key=config('GEMINI_API_KEY')


client = genai.Client(api_key=GEMINI_API_KEY)


def scan_bill(image):

    image_bytes = image.read()

    prompt = """
    Analyze this bill or receipt.
    Extract the following information:
    1. Total amount paid.
    2. Expense category.
    3. Payment method.
    Available categories:
    Food, Travel, Shopping, Bills, Health,
    Education, Entertainment, Groceries, Others.
    Available payment methods:
    Cash, Upi.
    If the payment method cannot be identified,
    return null.
    Return only valid JSON with these fields:
    amount, category, payment_method,title.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=[
            prompt,
            {
                "inline_data": {
                    "mime_type": image.content_type,
                    "data": image_bytes
                }
            }
        ],
        config={
            "response_mime_type": "application/json"
        }
    )

    return json.loads(response.text)