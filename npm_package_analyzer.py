import requests

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
        return list(versions.keys())[-num_of_versions:]
    except requests.exceptions.RequestException as e:
        print(f"Failed to get versions for package {package_name}:\n {e}")
        return None
    

def feach_readme_files(package_name, num_of_versions):
    versions = get_last_versions(package_name, num_of_versions)
    if versions:
        for version in versions:
            download_readme_file(package_name, version)       

