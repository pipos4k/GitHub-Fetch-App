# GitHub Searching App
import requests
import pandas as pd
from requests.exceptions import RequestException
import time

def fetch_github_user(username):

    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Returns user data as dictionary
    else:
        return None  # User not found
    
def fetch_repos(repo_name, max_repos, per_page):

    print(f"Serching: {repo_name}, (Max:{max_repos}, Per page: {per_page})")
    all_repos = []
    page = 1

    while len(all_repos) < max_repos:
        
        try:
            search_url = f"https://api.github.com/search/repositories?q={repo_name}&per_page={per_page}&page={page}"
            response = requests.get(search_url)

            # Handle rate limits 
            if response.status_code == 403: # 403 = too many requests
                reset_time = int(response.headers.get("X-RateLimit-Reset", 60))
                wait_time = max(reset_time - time.time(), 0) + 5
                print(f"Rate limited. Waiting {wait_time:.0f} seconds...")
                time.sleep(wait_time)
                continue

            data = response.json()
            repos = data.get("items", [])
            print(f"Page {page}: {len(data.get('items', []))} repos")  # Debug line
    
            if not data.get('items'):
                print(f"Stopping: No items in response. Full response: {data}")
                break

            if "items" not in data or not data["items"]:
                print(f"No repo found for {repo_name}")
                return pd.DataFrame() # Return emptry DataFrame 
            
            if not repos:
                break # No more results

            all_repos.extend(repos)
            page += 1

            # Progress update
            print(f"Fetched page {page} | Total: {len(all_repos)} repos")
            time.sleep(2)

        except RequestException as e:
            print(f"Network/Request error: {e}")
            return pd.DataFrame()
    
    df = pd.DataFrame(all_repos[:max_repos])
    
    return df.sort_values(by="forks", ascending=False) # Return DataFame sorting by forks

def get_valid_input():

    print("Enter 'Repo name' 'Max repos' 'Per page' (e.g. 'python 100 30'):")
    while True:
        user_input = input().strip()
        parts = user_input.split()

        # Check if input has 3 parts
        if len(parts) != 3:
            print("Error: Format must be 'REPO_NAME MAX_REPOS PER_PAGE'")
            continue

        repo_name, max_repos, per_page = parts

        # Check for numeric 
        if not (max_repos.isdigit() and per_page.isdigit()):
            print("Error: MAX_REPOS and PER_PAGE must be numbers")
            continue

        return repo_name, int(max_repos), int(per_page)

def create_csv(df, name_file):
    # Save to text file with aligned columns
    with open(f"{name_file}_github_repos.txt", "w") as f:
        # Write header
        f.write(f"{'Repository name':<35} {'URL' :<60} {'Forks' :10}\n")
        f.write("-" *105 + "\n")

        # Write each row
        for _, row in df.iterrows():
            f.write(f"{row['name']:<35} {row['html_url']:<60} {row['forks']:<10}\n")

# json_file = fetch_github_user("pipos4k")
repo_name , max_repos, per_page = get_valid_input()
repo_data = fetch_repos(repo_name=repo_name, max_repos=int(max_repos), per_page=int(per_page))
clear_html_repo = repo_data[["name", "html_url", "forks"]] # Create new Dataframe (more readable for urls)
create_csv(clear_html_repo, repo_name)
print(clear_html_repo)

