"""
Program Name: Top GitHub Rust Repositories Visual
Author: Dakota Nagy
Purpose: Fetches data via the GitHub API for top-starred projects in Rust
        programming language, processes the JSON response, and generates an 
        interactive Plotly HTML bar chart.
Starter Code: Adapted and tailored code based on tutorial provided in class lecture video.
Date: August 14, 2026
"""
import requests

def fetch_repository_data(language: str) -> dict:
    """Pull repo data from GitHub Rust (REST) API with exception handling."""
    url = f"https://api.github.com/search/repositories?q=language:rust&sort=stars"
    headers = {"Accept": "application/vnd.github.v3+json"}

    try:
        response = requests.get(url,headers=headers,timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Error fetching data from GitHub API: {error}")
        return{}
    
def main():
    target_language = "rust"
    print(f"Pulling top {target_language.capitalize()} repos.")

    response_dict = fetch_repository_data(target_language)

    if response_dict:
        print(f"Success")
        print(f"Repos found: {response_dict.get('total_count')}")
        print(f"Items on first page: {len(response_dict.get('items', []))}")


if __name__ == "__main__":
    main()