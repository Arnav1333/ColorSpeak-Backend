import os
import json
import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def suggest_colors(request):
    """
    Accepts a text prompt and returns AI-suggested color palettes.
    """

    # Allow only POST requests
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST method allowed"},
            status=405
        )

    try:
        # Parse request body
        body = json.loads(request.body.decode("utf-8"))
        prompt = body.get("prompt")

        if not prompt:
            return JsonResponse(
                {"error": "Prompt is required"},
                status=400
            )

        # Get API key from environment variables
        API_KEY = os.getenv("GEMINI_API_KEY")

        if not API_KEY:
            return JsonResponse(
                {"error": "API key not configured"},
                status=500
            )

        # Gemini API endpoint
        url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            f"models/gemini-pro:generateContent?key={API_KEY}"
        )

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": (
                                "Suggest a color palette for the following idea. "
                                "Return only color names or hex codes.\n\n"
                                f"Idea: {prompt}"
                            )
                        }
                    ]
                }
            ]
        }

        # Call Gemini API
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=15
        )

        if response.status_code != 200:
            return JsonResponse(
                {
                    "error": "Failed to fetch response from Gemini",
                    "details": response.text
                },
                status=500
            )

        data = response.json()

        # Extract response safely
        text_output = (
            data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
        )

        return JsonResponse(
            {"colors": text_output},
            status=200
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500
        )
