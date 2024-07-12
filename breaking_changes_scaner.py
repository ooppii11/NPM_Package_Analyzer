from openai import OpenAI
import os
import google.generativeai as genai
import files_featcher

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


def check_changelog_for_breaking_changes_openai(changelog):
    try:
        prompt = (
            f"Check the following changelog and identify the breaking changes:\n\n"
            f"{changelog}\n\n"
            f"Breaking changes:"
        )
        model = "gpt-3.5-turbo"
        full_msgs = [
            {"role": "system", "content": "Given the following data, your job is to check the changelog and identify any breaking changes."}, 
            {"role": "user", "content": prompt}]
        return openai_call(full_msgs, model, 300)
    except Exception as e:
        print(f'Error checking changelog: {e}')
        return 'Error checking changelog'
    

def check_changelog_for_updates_openai(changelog):
    try:
        prompt = (
            f"Check the following changelog and identify any updates:\n\n"
            f"{changelog}\n\n"
            f"Updates:"
        )
        model = "gpt-3.5-turbo"
        full_msgs = [
            {"role": "system", "content": "Given the following data, your job is to check the changelog and identify any updates."}, 
            {"role": "user", "content": prompt}]
        return openai_call(full_msgs, model, 300)
    except Exception as e:
        print(f'Error checking changelog: {e}')
        return 'Error checking changelog'
    

def check_changelog_for_deprecations_openai(changelog):
    try:
        prompt = (
            f"Check the following changelog and identify any deprecations:\n\n"
            f"{changelog}\n\n"
            f"Deprecations:"
        )
        model = "gpt-3.5-turbo"
        full_msgs = [
            {"role": "system", "content": "Given the following data, your job is to check the changelog and identify any deprecations."}, 
            {"role": "user", "content": prompt}]
        return openai_call(full_msgs, model, 300)
    except Exception as e:
        print(f'Error checking changelog: {e}')
        return 'Error checking changelog'
    

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


        return openai_call(full_msgs, model, 300)
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
        return openai_call(full_msgs, model, 300)
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
        return openai_call(full_msgs, model, 300)
    except Exception as e:
        print(f'Error comparing files: {e}')
        return 'Error comparing files'
    

def check_changelog_for_breaking_changes_google(changelog):
    try:
        prompt = (
            f"Check the following changelog and identify the breaking changes:\n\n"
            f"{changelog}\n\n"
            f"Breaking changes:"
        )
        model = "models/text-bison-001"
        return google_call(prompt, model)
    except Exception as e:
        print(f'Error checking changelog: {e}')
        return 'Error checking changelog'

def check_changelog_for_updates_google(changelog):
    try:
        prompt = (
            f"Check the following changelog and identify any updates:\n\n"
            f"{changelog}\n\n"
            f"Updates:"
        )
        model = "models/text-bison-001"
        return google_call(prompt, model)
    except Exception as e:
        print(f'Error checking changelog: {e}')
        return 'Error checking changelog'
    

def check_changelog_for_deprecations_google(changelog):
    try:
        prompt = (
            f"Check the following changelog and identify any deprecations:\n\n"
            f"{changelog}\n\n"
            f"Deprecations:"
        )
        model = "models/text-bison-001"
        return google_call(prompt, model)
    except Exception as e:
        print(f'Error checking changelog: {e}')
        return 'Error checking changelog'


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





def compere_files_for_breaking_changes(package_name, version1, version2, file_name, method):
    file1, file2 = files_featcher.read_md_file_from_disk(package_name, version1, file_name), files_featcher.read_md_file_from_disk(package_name, version2, file_name)
    if not file1 or not file2:
        return None
    
    length = len(file1) + len(file2)
   

    if method == compere_method.OPENAI:
        if length > 16000:
            print("Files are over 16000 tokens and are too large to compare")
            return None

        return {
            "from" : version1, 
            "to" : version2, 
            "updates" : compere_md_files_updates_openai(file1, file2),
            "deprecations" : compere_md_files_deprecations_openai(file1, file2),
            "breaking changes" : compere_md_files_breaking_changes_openai(file1, file2)}
    elif method == compere_method.GOOGLE:
        if length > 8000:
            print("Files are over 8000 tokens and are too large to compare")
            return None
        return {
            "from" : version1, 
            "to" : version2, 
            "updates" : compere_md_files_updates_google(file1, file2),
            "deprecations" : compere_md_files_deprecations_google(file1, file2),
            "breaking changes" : compere_md_files_breaking_changes_google(file1, file2)}        
    

def compere_readme_files_versions_from_last_version(package_name, num_of_versions, file_name, method):
    if num_of_versions < 2:
        print("Number of versions must be at least 2")
        return None
    versions = files_featcher.get_last_versions(package_name, num_of_versions)
    if versions:
        if len(versions) < 2:
            print(f"Package {package_name} has less than 2 versions")
            return None
        
        for i in range(len(versions) - 1):
            yield compere_files_for_breaking_changes(package_name, versions[i], versions[i+1], file_name, method)


def check_changelog_for_breaking_changes_from_last_version(package_name, num_of_versions, file_name, method):
    for version in files_featcher.get_last_versions(package_name, num_of_versions):
        changelog = files_featcher.read_md_file_from_disk(package_name, version, file_name)
    
        if changelog:
            length = len(changelog)
            if method == compere_method.OPENAI:
                if length > 16000:
                    print("Changelog is over 16000 tokens and is too large to check")
                    yield None
                yield {
                    "version" : version,
                    "updates" : check_changelog_for_updates_openai(changelog),
                    "deprecations" : check_changelog_for_deprecations_openai(changelog),
                    "breaking changes" : check_changelog_for_breaking_changes_openai(changelog)
                    }
            elif method == compere_method.GOOGLE:
                if length > 8000:
                    print("Changelog is over 8000 tokens and is too large to check")
                    yield None
                yield {
                    "version" : version,
                    "updates" : check_changelog_for_updates_google(changelog),
                    "deprecations" : check_changelog_for_deprecations_google(changelog),
                    "breaking changes" : check_changelog_for_breaking_changes_google(changelog)
                    }


def compere_readme_files_for_breaking_changes_specific_version(package_name, versions, file_name, method):
    if not files_featcher.already_downloaded(package_name, versions[1], file_name):
        return []
    if not files_featcher.already_downloaded(package_name, versions[0], file_name) and not files_featcher.already_downloaded(package_name, versions[2], file_name):
        return []
    elif not files_featcher.already_downloaded(package_name, versions[0], file_name):
        return [compere_files_for_breaking_changes(package_name, versions[1], versions[2], file_name, method)]
    elif not files_featcher.already_downloaded(package_name, versions[2], file_name):
        return [compere_files_for_breaking_changes(package_name, versions[0], versions[1], file_name, method)]
    else:
        return [
            compere_files_for_breaking_changes(package_name, versions[0], versions[1], file_name, method),
            compere_files_for_breaking_changes(package_name, versions[1], versions[2], file_name, method)]


def check_changelog_for_breaking_changes_specific_version(package_name, version, file_name, method):
    changelog = files_featcher.read_md_file_from_disk(package_name, version, file_name)
    length = len(changelog)
    if not changelog:
        return None
    if method == compere_method.OPENAI:
        if length > 16000:
            print("Changelog is over 16000 tokens and is too large to check")
            return None
        return {
            "version" : version,
            "updates" : check_changelog_for_updates_openai(changelog),
            "deprecations" : check_changelog_for_deprecations_openai(changelog),
            "breaking changes" : check_changelog_for_breaking_changes_openai(changelog)
            }
    elif method == compere_method.GOOGLE:
        if length > 8000:
            print("Changelog is over 8000 tokens and is too large to check")
            return None
        return {
            "version" : version,
            "updates" : check_changelog_for_updates_google(changelog),
            "deprecations" : check_changelog_for_deprecations_google(changelog),
            "breaking changes" : check_changelog_for_breaking_changes_google(changelog)
            }