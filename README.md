# github-repo-tracker

A Python-based tool that fetches public GitHub repositories of multiple users and visualizes key metrics like stars, forks, and watchers using an interactive dashboard (Plotly Dash). MongoDB is used for storage and data retrieval.

---

##  Features

-  Fetch public repos of any GitHub user
-  Store data in a MongoDB collection
-  Visual dashboard for repo analytics
-  Easy to customize GitHub usernames
-  Environment variable support for secure API access

---

##  Tech Stack

- **Python**
- **MongoDB** with "pymongo"
- **GitHub REST API**
- **Plotly Dash** for dashboards
- **dotenv** for managing secrets

---

##  How It Works

1. tracker.py:
   - Reads GitHub usernames from a list
   - Calls GitHub API to fetch repo data
   - Saves the info into MongoDB

2. dashboard.py:
   - Connects to MongoDB
   - Creates bar charts for stars, forks, and watchers
   - Runs a Dash server to show insights in the browser

---

##  Setup Instructions

1. **Clone this repo:**

   git clone https://github.com/Saravana-Kumar0807/github-repo-tracker.git
   cd github-repo-tracker
   
2.**Create virtual environment** (optional but recommended):

  python -m venv venv
  source venv/Scripts/activate  # On Windows

3.**Install dependencies:**

  pip install -r requirements.txt
  Create a .env file with your GitHub token:

  GITHUB_TOKEN=your_personal_access_token

4.**Run tracker to fetch data:**

  python tracker.py

5.**Start dashboard:**

  python dashboard.py
