import npm_package_analyzer
import os

OPTIONS = ["1. Check Package last versions for breaking changes", "2. Check Package specific version for breaking changes", "3. Update API key", "4. Exit"]

def print_options():
    for option in OPTIONS:
        print(option)


def update_api_key():
    print("Choose a method to update the API key for: ")
    for i, method in zip(range(len(npm_package_analyzer.bcs.compere_method.get_methods())), npm_package_analyzer.bcs.compere_method.get_methods()):
        print(f"{i+1}. {method}")
    compare_method = npm_package_analyzer.bcs.compere_method.get_methods()[int(input("Enter the number of the method: ")) - 1]
    
    os.environ[f"{compare_method.upper()}_API_KEY"] = input(f"Enter the API key for {compare_method}: ")


def get_user_input_last():
    package_name = input("Enter the package name: ")
    num_of_versions = int(input("Enter num of versions: "))

    print("Choose a method to compare the versions: ")
    for i, method in zip(range(len(npm_package_analyzer.bcs.compere_method.get_methods())), npm_package_analyzer.bcs.compere_method.get_methods()):
        print(f"{i+1}. {method}")
    compare_method = npm_package_analyzer.bcs.compere_method.get_methods()[int(input("Enter the number of the method: ")) - 1]
    
    if f"{compare_method.upper()}_API_KEY" not in os.environ:
        os.environ[f"{compare_method.upper()}_API_KEY"] = input(f"Enter the API key for {compare_method}: ")
   
    return package_name, num_of_versions, compare_method

def get_user_input_specific():
    package_name = input("Enter the package name: ")
    version = input("Enter the version: ")

    print("Choose a method to compare the versions: ")
    for i, method in zip(range(len(npm_package_analyzer.bcs.compere_method.get_methods())), npm_package_analyzer.bcs.compere_method.get_methods()):
        print(f"{i+1}. {method}")
    compare_method = npm_package_analyzer.bcs.compere_method.get_methods()[int(input("Enter the number of the method: ")) - 1]
    
    if f"{compare_method.upper()}_API_KEY" not in os.environ:
        os.environ[f"{compare_method.upper()}_API_KEY"] = input(f"Enter the API key for {compare_method}: ")
   
    return package_name, version, compare_method

def main():

    while True:
        try:
            print_options()
            option = int(input("Enter the number of the option: "))
            if option == 4:
                break
            elif option == 3:
                update_api_key()
            elif option == 1:
                package_name, num_of_versions, compare_method = get_user_input_last()
                npm_package_analyzer.from_last_version(package_name, num_of_versions, compare_method)
            elif option == 2:
                package_name, version, compare_method = get_user_input_specific()
                npm_package_analyzer.specific_version(package_name, version, compare_method)
            else:
                print("Invalid input, please try again")

            print("\n")
        except (IndexError, ValueError):
            print("Invalid input, please try again")
        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as e:
            print(f"An error has occured: {e}")

    

if __name__ == "__main__":
    main()