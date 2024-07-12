import breaking_changes_scaner as bcs
import files_featcher


    

def print_changes_files_compere(change):
    print(f"from: {change['from']}\nto: {change['to']}")
    print("updates:")
    print(change["updates"], end="\n\n")
    print("deprecations:")
    print(change["deprecations"], end="\n\n")
    print("breaking changes:")
    print(change["breaking changes"], end="\n\n")


def print_changes_one_file_check(change):
    print(f"version: {change['version']}")
    print("updates:")
    print(change["updates"], end="\n\n")
    print("deprecations:")
    print(change["deprecations"], end="\n\n")
    print("breaking changes:")
    print(change["breaking changes"], end="\n\n")


def from_last_version(package_name, num_of_versions, method):
    print("downloading readme.md and compering files for the last versions")
    files_featcher.feach_files_from_last_version(package_name, num_of_versions, "readme.md")
    for change in bcs.compere_readme_files_versions_from_last_version(package_name, num_of_versions, "readme.md", method):
        if change:
            print_changes_files_compere(change)

    print("downloading changelog.md and checking files for the last versions")
    files_featcher.get_file_namefeach_files_from_last_version(package_name, num_of_versions, "changelog.md")
    for change in bcs.check_changelog_for_breaking_changes_from_last_version(package_name, num_of_versions, "changelog.md", method):
        if change:
            print_changes_one_file_check(change)
 

def specific_version(package_name, version, method):
    previes_version, next_version = files_featcher.get_adjacent_versions(package_name, version)
    versions = [previes_version, version, next_version]

    print("downloading readme.md and compering files for the specific version")
    files_featcher.feach_files_for_specific_version(package_name, versions, "readme.md")
    for change in bcs.compere_readme_files_for_breaking_changes_specific_version(package_name, versions, "readme.md", method):
        if change:
            print_changes_files_compere(change)

    print("downloading changelog.md and checking file for the specific version")
    files_featcher.download_file(package_name, version, "changelog.md")
    change = bcs.check_changelog_for_breaking_changes_specific_version(package_name, version, "changelog.md", method)
    if change:
        print_changes_one_file_check(change)



def main():
    package_name = "react" #other options: express, shx
    num_of_versions = 5
    version = "17.0.0"

    from_last_version(package_name, num_of_versions, bcs.compere_method.OPENAI)
    specific_version(package_name, version, bcs.compere_method.OPENAI)
    
    
    

if __name__ == "__main__":
    main()
    


