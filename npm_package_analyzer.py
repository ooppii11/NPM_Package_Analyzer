import requests
import openai

def get_readme_file(package_name, version):
    try:
        response = requests.get(f"https://registry.npmjs.org/{package_name}/{version}")
        response.raise_for_status()
        package_info = response.json()
        readme_url = package_info.get("readme")
        if not readme_url:
            print(f"There is no README file for package {package_name} at version {version}")
            return None
        response = requests.get(readme_url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Failed to download README file for package {package_name} at version {version}:\n {e}")
        return None
    
def download_readme_file(package_name, version):
    readme = get_readme_file(package_name, version)
    if readme:
        with open(f"{package_name}_{version}_readme.md", "w") as f:
            f.write(readme)
        print(f"README file for package {package_name} downloaded successfully")


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
    
def already_downloaded(package_name, version):
    try:
        with open(f"{package_name}_{version}_readme.md", "r"):
            return True
    except FileNotFoundError:
        return False

def feach_readme_files(package_name, num_of_versions):
    versions = get_last_versions(package_name, num_of_versions)
    if versions:
        for version in versions:
            if not already_downloaded(package_name, version):
                download_readme_file(package_name, version)


def compere_readme_breaking_changes(readme1, readme2):
    try:
        prompt = (
            f"Compare the following two READMEs and identify any breaking changes:\n\n"
            f"Previous version README:\n{readme1}\n\n"
            f"Current version README:\n{readme2}\n\n"
            f"Breaking changes:"
        )
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f'Error comparing READMEs: {e}')
        return 'Error comparing READMEs'
    

def compere_readme_files(package_name, version1, version2):
    try:
        with open(f"{package_name}_{version1}_readme.md", "r") as f:
            readme1 = f.read()
        with open(f"{package_name}_{version2}_readme.md", "r") as f:
            readme2 = f.read()
        return {"from" : version1, "to" : version2, "changes" : compere_readme_breaking_changes(readme1, readme2)}
    except FileNotFoundError:
        print(f"README file for package {package_name} at version {version1} or {version2} is missing")


def compere_readme_versions(package_name, num_of_versions):
    versions = get_last_versions(package_name, num_of_versions)
    breaking_changes = []
    if versions:
        for i in range(len(versions) - 1):
            breaking_changes.append(compere_readme_files(package_name, versions[i], versions[i+1]))

    return breaking_changes
        
def main():
    OPENAI_API_KEY = 'key_here'
    openai.api_key = OPENAI_API_KEY
    package_name = "express"
    num_of_versions = 3
    feach_readme_files(package_name, num_of_versions)
    breaking_changes = compere_readme_versions(package_name, num_of_versions)
    for change in breaking_changes:
        print(change)
    
