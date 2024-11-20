import requests
import json
import time

# 配置你的 GitHub Token 和用户名,这里换成你的token和username
GITHUB_TOKEN = "ghp_arZpdmj9xxxxxxxxxxxxxxxxxxxxxxx"
USERNAME = "ChikaKomari"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# 导出 stars 的函数
def export_stars():
    stars_url = f"https://api.github.com/users/{USERNAME}/starred"
    all_stars = []
    page = 1
    while True:
        response = requests.get(stars_url, headers=HEADERS, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            print(f"Error: Unable to fetch stars (status code: {response.status_code})")
            break
        stars = response.json()
        if not stars:
            break
        all_stars.extend(stars)
        page += 1
        time.sleep(1)  # 避免过于频繁请求,添加延迟

    # 保存到文件
    with open("stars_export.json", "w", encoding="utf-8") as file:
        json.dump(all_stars, file, indent=4)
    print(f"Exported {len(all_stars)} starred repositories to 'stars_export.json'")

# 删除 starred 项目函数
def delete_starred_repos():
    with open("stars_export.json", "r", encoding="utf-8") as file:
        stars = json.load(file)
    
    for repo in stars:
        repo_url = repo["html_url"]
        owner, repo_name = repo["full_name"].split("/")
        star_url = f"https://api.github.com/user/starred/{owner}/{repo_name}"
        response = requests.delete(star_url, headers=HEADERS)
        if response.status_code == 204:
            print(f"Unstarred: {repo_url}")
        else:
            print(f"Failed to unstar: {repo_url} (status code: {response.status_code})")
        time.sleep(1)  # 避免速率限制,添加延迟

# 导入 stars 到新的项目
def import_stars():
    with open("stars_export.json", "r", encoding="utf-8") as file:
        stars = json.load(file)
    
    for repo in stars:
        repo_url = repo["html_url"]
        owner, repo_name = repo["full_name"].split("/")
        star_url = f"https://api.github.com/user/starred/{owner}/{repo_name}"
        response = requests.put(star_url, headers=HEADERS)
        if response.status_code == 204:
            print(f"Starred: {repo_url}")
        else:
            print(f"Failed to star: {repo_url} (status code: {response.status_code})")
        time.sleep(1)  # 避免速率限制,添加延迟

if __name__ == "__main__":
    print("1. Export stars")
    print("2. Delete starred repositories")
    print("3. Import stars to new project")
    choice = input("Choose an option (1/2/3): ")

    if choice == "1":
        export_stars()
    elif choice == "2":
        confirm = input("Are you sure you want to unstar all repositories? (yes/no): ")
        if confirm.lower() == "yes":
            delete_starred_repos()
        else:
            print("Operation cancelled.")
    elif choice == "3":
        import_stars()
    else:
        print("Invalid choice!")
