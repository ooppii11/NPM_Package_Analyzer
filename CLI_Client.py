import npm_package_analyzer
import os



def get_user_input():
    package_name = input("Enter the package name: ")
    num_of_versions = int(input("Enter num of versions: "))

    print("Choose a method to compare the versions: ")
    for i, method in zip(range(len(npm_package_analyzer.compere_method.get_methods())), npm_package_analyzer.compere_method.get_methods()):
        print(f"{i+1}. {method}")
    compare_method = npm_package_analyzer.compere_method.get_methods()[int(input("Enter the number of the method: ")) - 1]
    
    if f"{compare_method.upper()}_API_KEY" not in os.environ:
        os.environ[f"{compare_method.upper()}_API_KEY"] = input(f"Enter the API key for {compare_method}: ")
   
    return package_name, num_of_versions, compare_method

def main():

    while True:
        try:  
            package_name, num_of_versions, compare_method = get_user_input()
            npm_package_analyzer.feach_readme_files(package_name, num_of_versions)
            for change in npm_package_analyzer.compere_readme_versions(package_name, num_of_versions, compare_method):
                print(f"from: {change['from']}\nto: {change['to']}")
                print(change["changes"], end="\n\n")

            stop = input("Do you want to exit? (y/n): ")
            if stop == "y":
                break

        except (IndexError, ValueError):
            print("Invalid input, please try again")
        except KeyboardInterrupt:
            print("Exiting...")
            stop = True
        except Exception as e:
            print(f"An error has occured: {e}")

    

if __name__ == "__main__":
    main()