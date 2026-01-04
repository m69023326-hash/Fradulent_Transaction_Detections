# download_background.py
import requests

url = "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=1920&q=80"
response = requests.get(url)
os.makedirs("assets", exist_ok=True)
with open("assets/credit-card-bg.jpg", "wb") as f:
    f.write(response.content)
print("✅ Background image downloaded!")