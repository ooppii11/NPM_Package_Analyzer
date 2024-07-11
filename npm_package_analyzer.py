import requests
from openai import OpenAI
import tarfile
import os
import shutil
import google.generativeai as genai
from bs4 import BeautifulSoup
import re

class compere_method:
    OPENAI = "openai"
    GOOGLE = "google"

    def __str__(self):
        return "compere_method"
    
    def __repr__(self):
        return "compere_method"
    
    @staticmethod
    def get_methods():
        return [compere_method.OPENAI, compere_method.GOOGLE]


def get_tag_name(repo, version):
    try:
        tags_url = f"https://github.com/{repo}/tags"
        response = requests.get(tags_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        version_pattern = version.replace('.', r'[\.\-_]?')
        pattern = re.compile(rf'v?{version_pattern}')
        
        for tag in soup.find_all('a', class_='Link--primary'):
            tag_text = tag.text.strip()
            if pattern.match(tag_text):
                return tag_text
        return None
    except Exception:
        return None


def get_file_github(repo, version, file_name):
    tag = get_tag_name(repo, version)

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
    for readme_name in generate_possible_file_names(file_name):
        try:
            return get_file_github(repo, version, readme_name)
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
                return get_file_github(repo, version, package_file_name)
            
        except Exception:
            tarball_url = package_info.get("dist").get("tarball")
            return get_file_npm(tarball_url, file_name)
            
 
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {file_name} for package {package_name} at version {version}:\n {e}")
        return None


def download_file(package_name, version, file_name):
    readme = get_file(package_name, version, file_name)
    cwd = os.getcwd()
    path = os.path.join(cwd, package_name.capitalize()) 
    if not os.path.exists(path):
        os.makedirs(path)

    path = os.path.join(path, file_name.capitalize())
    if not os.path.exists(path):
        os.makedirs(path)

    if readme:
        path = os.path.join(path, f"{package_name}_{version}_{file_name}")
        with open(path, "w") as f:
            f.write(readme)
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
        response = requests.get(f"https://registry.npmjs.org/{package_name}/{version}")
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

def openai_call(full_msgs, model, max_tokens):
    client = OpenAI(
        api_key=os.getenv(f"{compere_method.OPENAI.upper()}_API_KEY"),
    )
    response = client.chat.completions.create(
        model=model,
        messages=full_msgs,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content


def google_call(prompt, model):
    genai.configure(api_key=os.getenv(f"{compere_method.GOOGLE.upper()}_API_KEY"))
    model = genai.get_model(model)
    response = genai.generate_text(prompt=prompt, model=model)
    return response.result

def compere_md_files_breaking_changes_openai(file1, file2):
    try:
        prompt = (
            f"Compare the following two files and identify the breaking changes:\n\n"
            f"Previous version:\n{file1}\n\n"
            f"Current version:\n{file2}\n\n"
            f"Breaking changes:"
        )

        model = "gpt-3.5-turbo"
        full_msgs = [
            {"role": "system", "content": "Given the following data, your job is to compare the two files and identify any breaking changes."}, 
            {"role": "user", "content": prompt}]


        return openai_call(full_msgs, model, 150)
    except Exception as e:
        print(f'Error comparing files: {e}')
        return 'Error comparing files'

def compere_md_files_updates_openai(file1, file2):
    try:
        prompt = (
            f"Compare the following two files and identify any updates:\n\n"
            f"Previous version:\n{file1}\n\n"
            f"Current version:\n{file2}\n\n"
            f"Updates:"
        )

        model = "gpt-3.5-turbo"
        full_msgs = [
            {"role": "system", "content": "Given the following data, your job is to compare the two files and identify any updates."}, 
            {"role": "user", "content": prompt}]
        return openai_call(full_msgs, model, 150)
    except Exception as e:
        print(f'Error comparing files: {e}')
        return 'Error comparing files'

def compere_md_files_deprecations_openai(file1, file2):
    try:
        prompt = (
            f"Compare the following two files and identify any deprecations:\n\n"
            f"Previous version:\n{file1}\n\n"
            f"Current version:\n{file2}\n\n"
            f"Deprecations:"
        )

        model = "gpt-3.5-turbo"
        full_msgs = [
            {"role": "system", "content": "Given the following data, your job is to compare the two files and identify any deprecations."}, 
            {"role": "user", "content": prompt}]
        return openai_call(full_msgs, model, 150)
    except Exception as e:
        print(f'Error comparing files: {e}')
        return 'Error comparing files'
    

def compere_md_files_breaking_changes_google(file1, file2):
    try:
        prompt = (
            f"Compare the following two files and identify the breaking changes:\n\n"
            f"Previous version:\n{file1}\n\n"
            f"Current version:\n{file2}\n\n"
            f"Breaking changes:"
        )

        model = "models/text-bison-001"
        return google_call(prompt, model)
    except Exception as e:
        print(f'Error comparing files: {e}')
        return 'Error comparing files'


def compere_md_files_updates_google(file1, file2):
    try:
        prompt = (
            f"Compare the following two files and identify any updates:\n\n"
            f"Previous version:\n{file1}\n\n"
            f"Current version:\n{file2}\n\n"
            f"Updates:"
        )

        model = "models/text-bison-001"
        return google_call(prompt, model)
    except Exception as e:
        print(f'Error comparing files: {e}')
        return 'Error comparing files'


def compere_md_files_deprecations_google(file1, file2):
    try:
        prompt = (
            f"Compare the following two files and identify any deprecations:\n\n"
            f"Previous version:\n{file1}\n\n"
            f"Current version:\n{file2}\n\n"
            f"Deprecations:"
        )

        model = "models/text-bison-001"
        return google_call(prompt, model)
    except Exception as e:
        print(f'Error comparing files: {e}')
        return 'Error comparing files'


def read_md_file_from_disk(package_name, version, file_name):
    with open(f"{package_name.capitalize()}/{file_name.capitalize()}/{package_name}_{version}_{file_name}", "r") as f:
        file = f.read()
    return file


def compere_files_for_breaking_changes(package_name, version1, version2, file_name, method):
    try:
        file1, file2 = read_md_file_from_disk(package_name, version1, file_name), read_md_file_from_disk(package_name, version2, file_name)
        if method == compere_method.OPENAI:
            return {
                "from" : version1, 
                "to" : version2, 
                "updates" : compere_md_files_updates_openai(file1, file2),
                "deprecations" : compere_md_files_deprecations_openai(file1, file2),
                "breaking changes" : compere_md_files_breaking_changes_openai(file1, file2)}
        elif method == compere_method.GOOGLE:
            return {
                "from" : version1, 
                "to" : version2, 
                "updates" : compere_md_files_updates_google(file1, file2),
                "deprecations" : compere_md_files_deprecations_google(file1, file2),
                "breaking changes" : compere_md_files_breaking_changes_google(file1, file2)}
    except FileNotFoundError:
        print(f"{file_name} file for package {package_name} at version {version1} or {version2} is missing")


def compere_md_files_versions_from_last_version(package_name, num_of_versions, file_name, method):
    if num_of_versions < 2:
        print("Number of versions must be at least 2")
        return None
    versions = get_last_versions(package_name, num_of_versions)
    if versions:
        if len(versions) < 2:
            print(f"Package {package_name} has less than 2 versions")
            return None
        
        for i in range(len(versions) - 1):
            yield compere_files_for_breaking_changes(package_name, versions[i], versions[i+1], file_name, method)


def compere_md_files_for_breaking_changes_specific_version(package_name, versions, file_name, method):
    try:
        previes_version = read_md_file_from_disk(package_name, versions[0], file_name)
        current_version = read_md_file_from_disk(package_name, versions[1], file_name)
        next_version = read_md_file_from_disk(package_name, versions[2], file_name)
        if method == compere_method.OPENAI:
            return [
                {
                    "from" : versions[0], 
                    "to" : versions[1], 
                    "updates" : compere_md_files_updates_openai(previes_version, current_version), 
                    "deprecations" : compere_md_files_deprecations_openai(previes_version, current_version), 
                    "breaking changes" : compere_md_files_breaking_changes_openai(previes_version, current_version)
                }, 
                {
                    "from" : versions[1],
                    "to" : versions[2],
                    "updates" : compere_md_files_updates_openai(current_version, next_version),
                    "deprecations" : compere_md_files_deprecations_openai(current_version, next_version),
                    "breaking changes" : compere_md_files_breaking_changes_openai(current_version, next_version)
                }]
        elif method == compere_method.GOOGLE:
            return [
                {
                    "from" : versions[0],
                    "to" : versions[1],
                    "updates" : compere_md_files_updates_google(previes_version, current_version),
                    "deprecations" : compere_md_files_deprecations_google(previes_version, current_version),
                    "breaking changes" : compere_md_files_breaking_changes_google(previes_version, current_version)
                },
                {
                    "from" : versions[1],
                    "to" : versions[2],
                    "updates" : compere_md_files_updates_google(current_version, next_version),
                    "deprecations" : compere_md_files_deprecations_google(current_version, next_version),
                    "breaking changes" : compere_md_files_breaking_changes_google(current_version, next_version)
                }]

    except FileNotFoundError:
        print(f"{file_name} file for package {package_name} at version {versions[0]} or {versions[1]} or {versions[2]} is missing")


def from_last_version(package_name, num_of_versions, method):
    feach_files_from_last_version(package_name, num_of_versions, "readme.md")
    for change in compere_md_files_versions_from_last_version(package_name, num_of_versions, "readme.md", method):
        if change:
            print(f"from: {change['from']}\nto: {change['to']}")
            print(change["breaking changes"], end="\n\n")

    feach_files_from_last_version(package_name, num_of_versions, "chnagelog.md")
    for change in compere_md_files_versions_from_last_version(package_name, num_of_versions, "chnagelog.md", method):
        if change:
            print(f"from: {change['from']}\nto: {change['to']}")
            print(change["breaking changes"], end="\n\n")
 

def specific_version(package_name, version, method):
    previes_version, next_version = get_adjacent_versions(package_name, version)
    versions = [previes_version, version, next_version]
    feach_files_for_specific_version(package_name, versions, "readme.md")
    for change in compere_files_for_breaking_changes_specific_version(package_name, versions, "readme.md", method):
        if change:
            print(f"from: {change['from']}\nto: {change['to']}")
            print(change["breaking changes"], end="\n\n")

    feach_files_for_specific_version(package_name, versions, "chnagelog.md")
    for change in compere_files_for_breaking_changes_specific_version(package_name, versions, "chnagelog.md", method):
        if change:
            print(f"from: {change['from']}\nto: {change['to']}")
            print(change["breaking changes"], end="\n\n")



def main():
    package_name = "react" #other options: express, shx
    num_of_versions = 5
    version = "17.0.0"

    from_last_version(package_name, num_of_versions, compere_method.OPENAI)
    specific_version(package_name, version, compere_method.OPENAI)
    
    
    

if __name__ == "__main__":
    main()
    


