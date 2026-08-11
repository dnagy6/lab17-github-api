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
import plotly.express as ex

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

def create_bar_graph_visual(repo_links: list, stars: list, hover_texts: list, repo_names: list, language: str) -> None:
    """Creating a bar graph for visual reference of repo information and saving as an HTML file
       for lab requirements.
    """
    title = f"Most-Starred {language.title()} Projects on GitHub"
    labels = {"x": "Repository", "y": "Stars"}
    
    fig = ex.bar(
        x=repo_links,
        y=stars,
        title=title,
        labels=labels,
        hover_name=repo_names,
        hover_data={"Description": hover_texts},
    )

    fig.update_layout(
        title_font_size=24,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
        hoverlabel=dict(bgcolor="white", font_size=12)
    )
    
    output_filename = f"{language.lower()}_repos.html"
    fig.write_html(output_filename)
    print(f"Graph saved: '{output_filename}'.")

def main():
    target_language = "rust"
    print(f"Pulling top {target_language.capitalize()} repos.")

    response_dict = fetch_repository_data(target_language)

    if response_dict:
        repo_links, stars, hover_texts, repo_names = process_repo_data(response_dict)
        if repo_links:
            create_bar_graph_visual(repo_links, stars, hover_texts, repo_names, target_language)



if __name__ == "__main__":
    main()