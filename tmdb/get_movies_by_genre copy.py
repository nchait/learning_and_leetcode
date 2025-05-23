import requests
import json

API_KEY = "c9ca6cf6544612d4a3364af41ee98b63"  # Replace with your TMDb API key
BASE_URL = "https://api.themoviedb.org/3"
MIN_VOTE_AVG = 8.0  # Minimum number of votes to filter movies
MIN_VOTE_COUNT = 15000  # Minimum number of votes to filter movies
GENRE_ID = 28  # Replace with your desired genre ID (e.g., 28 = Action)
OUTPUT_FILE = f"movies_genre_{GENRE_ID}.json"

def fetch_movies_by_genre(api_key, genre_id, max_results=200):
    all_movies = []
    page = 1
    total_pages = (max_results // 20)
    
    while page <= total_pages:
        url = f"{BASE_URL}/discover/movie"
        params = {
            "api_key": api_key,
            # "with_genres": genre_id,
            "page": page,
            # "sort_by": "vote_count.desc",
            "sort_by": "vote_average.desc",  # You can change sorting
            # "sort_by": "popularity.desc",  # You can change sorting
            "vote_average.gte": MIN_VOTE_AVG,  # Minimum average rating
            "vote_count.gte": MIN_VOTE_COUNT,
            "language": "en-US"
        }

        response = requests.get(url, params=params)
        # {
        #     "status_code": 200,
        #     "results": [
        #         {
        #             "id": 1,
        #             "title": "Movie Title",
        #             "release_date": "2023-01-01",
        #             "overview": "Movie overview here."
        #         }
        #     ],
        #     "total_pages": 5
        # }
        if response.status_code != 200:
            print(f"Error: {response.status_code} on page {page}")
            break
        
        data = response.json()
        results = data.get("results", [])
        results = [
            {
                "id": result["id"], 
                "title": result["title"],
                "vote_count": result["vote_count"],
                "vote_average": result["vote_average"],
                "genre_ids": result["genre_ids"]
                }
            for result in results
        ]
        for result in results:
            for genre in result["genre_ids"]:
                
        page_limit = data.get("total_pages", 0)
        print(f"Page limit: {page_limit}")
        all_movies.extend(results)
        print(f"Fetched page {page} with {len(results)} movies")

        if not results or page >= data.get("total_pages", page):
            break

        page += 1

    # Limit to exactly max_results in case we fetched extra
    all_movies = all_movies[:max_results]

    # Save to file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_movies, f, indent=2)

    print(f"\nSaved {len(all_movies)} movies to '{OUTPUT_FILE}'")

# Run the script
if __name__ == "__main__":
    fetch_movies_by_genre(API_KEY, GENRE_ID)
