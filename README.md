# GitHub Searching App

A simple Python application that searches GitHub repositories using the GitHub API, sorts them by forks, and exports the results into a text file.

---

## 🚀 Features

- Search GitHub repositories
- Fetch multiple pages of results
- Handle GitHub API rate limits
- Sort repositories by forks
- Export results to a `.txt` file
- Input validation and error handling

---

## 🛠 Tech Stack

- Python 3
- Requests
- Pandas
- GitHub REST API

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/github-searching-app.git
cd github-searching-app
```

Install dependencies:

```bash
pip install pandas requests
```

---

## ▶️ Run the Application

```bash
python main.py
```

The program will ask for:
- Repository name
- Maximum repositories
- Results per page

---

## 📁 Output

The application creates a text file containing:
- Repository name
- Repository URL
- Fork count

---

## 📌 Main Functions

### `fetch_github_user(username)`
Fetches GitHub user information.

### `fetch_repos(repo_name, max_repos, per_page)`
Searches repositories using the GitHub API.

### `get_valid_input()`
Validates user input.

### `create_csv(df, name_file)`
Exports repository data to a text file.

---

## 🔒 Error Handling

The application handles:
- Invalid user input
- Network errors
- GitHub API rate limits
