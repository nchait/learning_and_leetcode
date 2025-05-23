import requests

API_KEY = "c9ca6cf6544612d4a3364af41ee98b63"  # Replace with your TMDb API key
BASE_URL = "https://api.themoviedb.org/3"
SEARCH_QUERY = "Blade Runner"  # Replace with your search term

def search_all_pages(query, api_key):
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": api_key,
        "query": query,
        "page": 1
    }

    all_results = []
    while True:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        data = response.json()
        results = data.get("results", [])
        all_results.extend(results)

        print(f"Fetched page {params['page']} with {len(results)} results")

        if params["page"] >= data.get("total_pages", 1):
            break

        params["page"] += 1

    return all_results

# Run the search
movies = search_all_pages(SEARCH_QUERY, API_KEY)

# Example output
print(f"\nFound {len(movies)} total results for '{SEARCH_QUERY}'\n")
for movie in movies[:5]:
    print(f"- {movie['title']} ({movie['release_date']})")
