@csrf_exempt
def suggest_colors(request):
    try:
        print("➡️ suggest_colors called")

        data = json.loads(request.body)
        print("📦 Request data:", data)

        user_input = data.get("input")
        if not user_input:
            return JsonResponse({"error": "Input missing"}, status=400)

        gemini_api_key = os.getenv("GEMINI_API_KEY")
        print("🔑 API key present:", bool(gemini_api_key))

        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Suggest 3 color palette for {user_input}"
                }]
            }]
        }

        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_api_key}",
            json=payload,
            timeout=20
        )

        print("🌐 Gemini status:", response.status_code)
        print("🌐 Gemini raw response:", response.text)

        return JsonResponse({
            "status": "ok",
            "gemini_status": response.status_code,
            "gemini_response": response.text
        })

    except Exception as e:
        print("❌ Exception:", str(e))
        return JsonResponse({"error": str(e)}, status=500)
