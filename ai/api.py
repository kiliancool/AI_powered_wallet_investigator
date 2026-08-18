import requests
from .config import MODEL,API_KEY,FALLBACK_MODEL

def send_to_model(conversation):
    DEFAULT_MODEL = MODEL
    try:
        response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": DEFAULT_MODEL,
            "messages": conversation,
              },
        timeout=30
    )

        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        if response.status_code in [429,500,502,503,504]:
            print(f"\nRate limit exceeded/Too many requests.\nDefault model: {MODEL} unavailable and AI model in use switched to : {FALLBACK_MODEL}\n")
            backup_response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": FALLBACK_MODEL,
                "messages": conversation,
              },
            timeout=30
        )


            if backup_response.status_code == 200:
                data = backup_response.json()
                return data["choices"][0]["message"]["content"]

            else:
                return (
                    f"\nBackup model error "
                    f"{backup_response.status_code}: "
                    f"{backup_response.text}"
)

        else:
            print(f"Error {response.status_code}: {response.text}")

    except Exception as e:
        return (f"Error: {str(e)}")
