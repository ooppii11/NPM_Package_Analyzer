import requests
import tarfile
import shutil
import re
import os
from bs4 import BeautifulSoup


def get_tag_name(repo, version):
    try:
        version_first_number = int(version.split('.')[0])
        tag_text = ""  

        while True:
            tags_url = f"https://github.com/{repo}/tags"
            tags_url += f"?after={tag_text}" if tag_text else ""
            response = requests.get(tags_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            tags = soup.find_all('a', class_='Link--primary')
            if not tags:
                return None

            version_pattern = version.replace('.', r'[\.\-_]?')
            pattern = re.compile(rf'v?{version_pattern}')
            
            last_tag = tags[-1].text.strip()
            last_tag_number = int(re.match(r'v?(\d+)', last_tag).group(1))
            if last_tag_number > version_first_number:
                tag_text = tags[-1].text.strip()
                continue

            first_tag = tags[0].text.strip()
            first_tag_number = int(re.match(r'v?(\d+)', first_tag).group(1))
            if first_tag_number < version_first_number:
                return None

            for tag in tags:
                tag_text = tag.text.strip()
                if pattern.match(tag_text):
                    return tag_text

    except Exception as e:
        print(f"Error: {e}")  # Optionally log the error
        return None


def get_file_github(repo, file_name, tag):
    

    if not tag:
        raise Exception("Tag not found")
    
    url = f"https://raw.githubusercontent.com/{repo}/{tag}/{file_name}"
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def generate_possible_file_names(file_name):
    name, extension = file_name.rsplit('.', 1) if '.' in file_name else (file_name, '')
    name_cases = {name.lower(), name.upper(), name.capitalize()}
    extension_cases = {extension.lower(), extension.upper()} if extension else {''}

    for name_case in name_cases:
        for extension_case in extension_cases:
            yield f"{name_case}.{extension_case}" if extension_case else name_case
    

def run_on_posebile_file_names_github(repo, version, file_name):
    tag = get_tag_name(repo, version)
    for readme_name in generate_possible_file_names(file_name):
        try:
            return get_file_github(repo, readme_name, tag)
        except Exception:
            continue
    raise Exception("Failed to download from github")


def get_file_npm(tarball_url, file_name):
    tarball_response = requests.get(tarball_url)
    tarball_response.raise_for_status()

    download_folder = "tempDownload"
    tarball_path = os.path.join(download_folder, "package.tgz")
    os.makedirs(download_folder, exist_ok=True)

    with open(tarball_path, "wb") as tarball_file:
        tarball_file.write(tarball_response.content)
        
    with tarfile.open(tarball_path) as tar:
        tar.extractall(path=download_folder)
        
    file_path = None
    for root, dirs, files in os.walk("./tempDownload/"):
            
            package_file_name = get_file_name(files, file_name)
            if package_file_name:
                file_path = os.path.join(root, package_file_name)
                break

    content = None
    if file_path:
        with open(file_path, "r") as f:
            content = f.read()
    else:
        print(f"{file_name} not found in the package.")
        
 
    os.remove(tarball_path)
    shutil.rmtree("./tempDownload/")
    return content


def get_file_name(package_files, file_name):
    for file in package_files:
        if file.upper() == file_name.upper():
            return file
    return None


def extract_data_from_package_json(package_name, version):
    response = requests.get(f"https://registry.npmjs.org/{package_name}/{version}")
    response.raise_for_status()
    package_info = response.json()
    return package_info


def get_file(package_name, version, file_name):
    try:
        
        package_info = extract_data_from_package_json(package_name, version)
        version_files = package_info.get("files")
        
        if not version_files:
            package_file_name = None
        else:
            package_file_name = get_file_name(version_files, file_name)
            
        try:
            github_url = package_info.get("repository").get("url")
            repo = github_url.split("github.com/")[1].replace(".git", "")

            if not repo:
                raise Exception("Repository URL not found")
            
            if not package_file_name:
                return run_on_posebile_file_names_github(repo, version, file_name)
            else:
                tag = get_tag_name(repo, version)
                return get_file_github(repo, package_file_name, tag)
            
        except Exception:
            tarball_url = package_info.get("dist").get("tarball")
            return get_file_npm(tarball_url, file_name)
            
 
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {file_name} for package {package_name} at version {version}:\n {e}")
        return None


def download_file(package_name, version, file_name):
    content = get_file(package_name, version, file_name)
    cwd = os.getcwd()
    path = os.path.join(cwd, package_name.capitalize()) 
    if not os.path.exists(path):
        os.makedirs(path)

    path = os.path.join(path, file_name.capitalize())
    if not os.path.exists(path):
        os.makedirs(path)

    if content:
        path = os.path.join(path, f"{package_name}_{version}_{file_name}")
        with open(path, "w", errors='ignore') as f:
            f.write(content)
        print(f"{file_name} for package {package_name} downloaded successfully")


def get_last_versions(package_name, num_of_versions):
    try:
        response = requests.get(f"https://registry.npmjs.org/{package_name}/")
        response.raise_for_status()
        package_info = response.json()
        versions = package_info.get("versions")
        if not versions:
            print(f"There are no versions for package {package_name}")
            return None
        return list(versions.keys())[-num_of_versions:] #might need to change this
    except requests.exceptions.RequestException as e:
        print(f"Failed to get versions for package {package_name}:\n {e}")
        return None


def get_adjacent_versions(package_name, version):
    try:
        response = requests.get(f"https://registry.npmjs.org/{package_name}")
        response.raise_for_status()
        package_info = response.json()
        versions = list(package_info.get("versions").keys())
        version_index = versions.index(version)
        if version_index == 0:
            return None, versions[version_index + 1]
        elif version_index == len(versions) - 1:
            return versions[version_index - 1], None
        else:
            return versions[version_index - 1], versions[version_index + 1]
    except requests.exceptions.RequestException as e:
        print(f"Failed to get versions for package {package_name}:\n {e}")
        return None, None


def already_downloaded(package_name, version, file_name):
    try:
        with open(f"{package_name.capitalize()}/{file_name.capitalize()}/{package_name}_{version}_{file_name}", "r"):
            return True
    except FileNotFoundError:
        return False

def feach_files_from_last_version(package_name, num_of_versions, file_name):
    versions = get_last_versions(package_name, num_of_versions)
    if versions:
        for version in versions:
            if not already_downloaded(package_name, version, file_name):
                download_file(package_name, version, file_name)


def feach_files_for_specific_version(package_name, versions, file_name):
    for version in versions:
        if not already_downloaded(package_name, version, file_name):
            download_file(package_name, version, file_name)