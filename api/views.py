import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def suggest_colors(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get("input", "")
        gemini_api_key = os.getenv("GEMINI_API_KEY")

        prompt = f"""
        Based on the organizational identity "{user_input}", suggest a 3-5 color palette.
        For each color, provide a descriptive name and its hex code.
        Output a JSON array of objects: [{{"name": "Deep Ocean Blue", "hex": "#0F4C81"}}, ...]
        """

        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "responseMimeType": "application/json"
            }
        }

        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_api_key}",
            headers={"Content-Type": "application/json"},
            json=payload
        )

        if response.status_code == 200:
            result_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return JsonResponse({"result": result_text})
        else:
            return JsonResponse({"error": "Gemini API failed"}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)
