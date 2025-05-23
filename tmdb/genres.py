import requests
import json

API_KEY = "c9ca6cf6544612d4a3364af41ee98b63"  # Replace with your TMDb API key
BASE_URL = "https://api.themoviedb.org/3"
GENRE_ENDPOINT = f"{BASE_URL}/genre/movie/list"

def fetch_genres(api_key):
    params = {
        "api_key": api_key,
        "language": "en-US"
    }

    response = requests.get(GENRE_ENDPOINT, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch genres: {response.status_code}")

    data = response.json()
    genres = data.get("genres", [])

    # Save to JSON file
    with open("genres.json", "w", encoding="utf-8") as f:
        json.dump(genres, f, indent=2)

    print(f"Saved {len(genres)} genres to 'genres.json'.")

# Run the script
if __name__ == "__main__":
    fetch_genres(API_KEY)
