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

def process_repo_data(response_dict: dict):
    """Pull relevant repo information for plotting on a chart."""
    if not response_dict or "items" not in response_dict:
        print("No valid repo data was found")
        return [], [], [], []

    repo_dicts = response_dict["items"]

    repo_links, stars, hover_texts, repo_names = [], [], [], []

    for repo_dict in repo_dicts:
        repo_name = repo_dict["name"]
        repo_url = repo_dict["html_url"]

        repo_links.append(f"<a href='{repo_url}'>{repo_name}</a>")
        stars.append(repo_dict["stargazers_count"])

        owner = repo_dict["owner"]["login"]
        description = repo_dict.get ("description") or "Description N/A"

        hover_texts.append(f"Owner: {owner} | Description: {description}")
        repo_names.append(repo_name)

    return repo_links, stars, hover_texts, repo_names

    
def main():
    target_language = "rust"
    print(f"Pulling top {target_language.capitalize()} repos.")

    response_dict = fetch_repository_data(target_language)

    if response_dict:
        repo_links, stars, hover_texts, repo_names = process_repo_data(response_dict)

        print(f"Pulled {len(repo_names)} repos")
        print("\nTop 3 repos:")
        for i in range(3):
            print(f"-> {repo_names[i]}: {stars[i]} stars | Hover Text: {hover_texts[i][:60]}...")



if __name__ == "__main__":
    main()