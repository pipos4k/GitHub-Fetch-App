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
    
json_file = fetch_github_user("pipos4k")

repo_name = "python"

def fetch_repos(repo_name, max_repos=2000, per_page=100):

    all_repos = []
    page = 1

    while len(all_repos) < max_repos:
        try:
            search_url = f"https://api.github.com/search/repositories?q={repo_name}&per_page={per_page}&page={page}"
            response = requests.get(search_url)

            print(f"Remaining: {response.headers['X-RateLimit-Remaining']}/{response.headers['X-RateLimit-Limit']}")
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
        
    return pd.DataFrame(all_repos[:max_repos])
    # df = pd.DataFrame(data["items"]) # Find all items from repo
    # return df.sort_values(by="forks", ascending=False)

def create_csv(df):
    pass

data_ = fetch_repos(repo_name=repo_name)
print(data_.head(20))
