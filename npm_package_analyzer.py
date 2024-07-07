import requests
from openai import OpenAI
import tarfile
import os
import shutil
import google.generativeai as genai

class compere_method:
    OPENAI = "openai"
    GOOGLE = "google"

    def __str__(self):
        return "compere_method"
    
    def __repr__(self):
        return "compere_method"
    
    def get_methods(self):
        return [self.OPENAI, self.GOOGLE]

def get_readme_file_github(repo, version, readme_file_name):
    url = f"https://raw.githubusercontent.com/{repo}/{version}/{readme_file_name}"
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def run_on_posebile_readme_file_github(repo, version):
    for readme_name in ["README.md", "README.MD", "readme.md", "readme.MD", "Readme.md", "Readme.MD"]:
        try:
            return get_readme_file_github(repo, version, readme_name)
        except Exception:
            continue
    raise Exception("Failed to download from github")

def get_readme_file_npm(tarball_url):
    tarball_response = requests.get(tarball_url)
    tarball_response.raise_for_status()

    download_folder = "tempDownload"
    tarball_path = os.path.join(download_folder, "package.tgz")
    os.makedirs(download_folder, exist_ok=True)

    with open(tarball_path, "wb") as tarball_file:
        tarball_file.write(tarball_response.content)
        
    with tarfile.open(tarball_path) as tar:
        tar.extractall(path=download_folder)
        
    readme_path = None
    for root, dirs, files in os.walk("./tempDownload/"):
            readme_file_name = get_readme_file_name(files)
            if readme_file_name:
                readme_path = os.path.join(root, readme_file_name)
                break

    readme_content = None
    if readme_path:
        with open(readme_path, "r") as readme_file:
            readme_content = readme_file.read()
    else:
        print("README.md file not found in the package.")
        
 
    os.remove(tarball_path)
    shutil.rmtree("./tempDownload/")
    return readme_content


def get_readme_file_name(package_files):
    for file in package_files:
        if file.upper() == "README.MD":
            return file
    return None

def extract_data_from_package_json(package_name, version):
    response = requests.get(f"https://registry.npmjs.org/{package_name}/{version}")
    response.raise_for_status()
    package_info = response.json()
    return package_info


def get_readme_file(package_name, version):
    try:
        
        package_info = extract_data_from_package_json(package_name, version)
        version_files = package_info.get("files")
        
        if not version_files:
            readme_file_name = None
        else:
            readme_file_name = get_readme_file_name(version_files)
            
        try:
            github_url = package_info.get("repository").get("url")
            repo = github_url.split("github.com/")[1].replace(".git", "")
            
            if not repo:
                raise Exception("Repository URL not found")
            
            if not readme_file_name:
                return run_on_posebile_readme_file_github(repo, version)
            else:
                return get_readme_file_github(repo, version, readme_file_name)
            
        except Exception:
            tarball_url = package_info.get("dist").get("tarball")
            return get_readme_file_npm(tarball_url)
            
 
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


def compere_readme_breaking_changes_openai(readme1, readme2):
    try:
        prompt = (
            f"Compare the following two READMEs and identify any breaking changes:\n\n"
            f"Previous version README:\n{readme1}\n\n"
            f"Current version README:\n{readme2}\n\n"
            f"Breaking changes:"
        )

        client = OpenAI(
            api_key=os.getenv(f"{compere_method.OPENAI.upper()}_API_KEY"),
        )

        response = client.completions.create(
            prompt=prompt,
            max_tokens=150,
            model="gpt-3.5-turbo",
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f'Error comparing READMEs: {e}')
        return 'Error comparing READMEs'
    

def compere_readme_breaking_changes_google(readme1, readme2):
    try:
        prompt = (
            f"Compare the following two READMEs and identify any breaking changes:\n\n"
            f"Previous version README:\n{readme1}\n\n"
            f"Current version README:\n{readme2}\n\n"
            f"Breaking changes:"
        )       
        genai.configure(api_key=os.getenv(f"{compere_method.GOOGLE.upper()}_API_KEY"))
        model = genai.get_model("models/text-bison-001")
        response = genai.generate_text(prompt=prompt, model=model)
        return response.result
    except Exception as e:
        print(f'Error comparing READMEs: {e}')
        return 'Error comparing READMEs'


def compere_readme_files(package_name, version1, version2, method):
    try:
        with open(f"{package_name}_{version1}_readme.md", "r") as f:
            readme1 = f.read()
        with open(f"{package_name}_{version2}_readme.md", "r") as f:
            readme2 = f.read()
        if method == compere_method.OPENAI:
            return {"from" : version1, "to" : version2, "changes" : compere_readme_breaking_changes_openai(readme1, readme2)}
        elif method == compere_method.GOOGLE:
            return {"from" : version1, "to" : version2, "changes" : compere_readme_breaking_changes_google(readme1, readme2)}
    except FileNotFoundError:
        print(f"README file for package {package_name} at version {version1} or {version2} is missing")


def compere_readme_versions(package_name, num_of_versions, method):
    if num_of_versions < 2:
        print("Number of versions must be at least 2")
        return None
    versions = get_last_versions(package_name, num_of_versions)
    if versions:
        if len(versions) < 2:
            print(f"Package {package_name} has less than 2 versions")
            return None
        
        for i in range(len(versions) - 1):
            yield compere_readme_files(package_name, versions[i], versions[i+1], method)

        
def main():
    package_name = "express"
    """
    shx
    json-diff
    passwordless
    blessed-contrib
    """
    num_of_versions = 5
    feach_readme_files(package_name, num_of_versions)
    for change in compere_readme_versions(package_name, num_of_versions, compere_method.GOOGLE):
        
        print(f"from: {change['from']}\nto: {change['to']}")
        print(change["changes"], end="\n\n")

if __name__ == "__main__":
    main()
    


