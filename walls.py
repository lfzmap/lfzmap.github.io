import requests
import random
import os

def list_files_in_github_folder(repo_owner, repo_name, file_path=None):
    if file_path:
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    else:
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def download_file(url, output_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(output_path, 'wb') as f:
        f.write(response.content)

def download_random_file_from_github(repo_owner, repo_name):
    folders = list_files_in_github_folder(repo_owner, repo_name)
    if not folders:
        raise ValueError("No folders found in the specified folder.")
    random_folder = random.choice(folders)
    while random_folder["name"][0] == "." or random_folder["name"][-3:]=="txt":
        random_folder = random.choice(folders)

    files = list_files_in_github_folder(repo_owner, repo_name, random_folder["name"])
    random_file = random.choice(files)
    while random_file["name"][-2:]=="md" or random_file["name"][-4:]=="webp":
        random_file = random.choice(files)
    file_url = random_file['download_url']
    file_name = random_file['name']
    output_path = os.path.join("/home/lfz/Pictures/wallpaper", file_name)
    download_file(file_url, output_path)
    return output_path

if __name__ == "__main__":
    repo_owner = "dharmx"
    repo_name = "walls"

    os.system("rm ~/Pictures/wallpaper/*")
    output_path = download_random_file_from_github(repo_owner, repo_name)
    os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri "+output_path)
