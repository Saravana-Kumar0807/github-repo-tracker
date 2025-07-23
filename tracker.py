import requests
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load GitHub token from .env
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["github_tracker"]
collection = db["repo_data"]

#Correct function with proper variable name
def fetch_repo_data(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Failed to fetch repos for {username}")
        return []

    repos = response.json()
    repo_summary = []

    for repo in repos:
        repo_summary.append({
            "username": username,
            "repo_name": repo["name"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "last_updated": repo["updated_at"]
        })

    return repo_summary

# Function to save to MongoDB
def save_to_mongo(data):
    for repo in data:
        query = {"username": repo["username"], "repo_name": repo["repo_name"]}
        collection.update_one(query, {"$set": repo}, upsert=True)

# Main code
if __name__ == "__main__":
    usernames = ["google", "facebook", "Saravana-Kumar0807"]  # Your GitHub username is valid here
    for user in usernames:
        print(f" Fetching data for {user}")
        data = fetch_repo_data(user)
        save_to_mongo(data)
    print("Data saved to MongoDB.")
