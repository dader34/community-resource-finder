#!/usr/bin/python
import json
import os

# Clear screen command for mac and windows
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
# Short helper for getting user input
def get_user_input(message='\nUser choice: '):
    print(message, end='')
    return input()

# Main menu screen
def run_main_menu():
    print('------------------------------')
    print('| Community Resource Finder  |')
    print('------------------------------')
    print('| 1: Browse by Category      |')
    print('| 2: Search by Name          |')
    print('| 3: Filter by Language      |')
    print('| 4: View All Resources.     |')
    print('| 5: Exit Program            |')
    print('------------------------------')
    

# Resource search menu
def search_resources(_resources):
    clear_screen()
    
    search_term = get_user_input("Enter a search term: ")
    
    # Keep track of resources that fit the search term criteria
    matched_resources = []
    
    # Loop through every resource and search for a match
    for resource in _resources:
        if search_term.lower() in resource['name'].lower():
            matched_resources.append(resource)
            
    # if there are search results, display them with list_resources
    if len(matched_resources) > 0:
        clear_screen()
        list_resources([resource for resource in matched_resources], by_category=False, by_language=False)
    else:
        # If no search results, offer to run the search again
        user_choice = get_user_input("No search results found, try again? (y/n): ")
        if user_choice.lower() == 'y':
            clear_screen()
            search_resources(_resources)

# Single resource info menu
def print_resource_menu(resource):
    clear_screen()
    
    # Get length for visual padding with minimum 15 chars
    resource_name_length = len(resource['name'])
    name_padding_size = (resource_name_length + 5) if (resource_name_length + 5) > 15 else 15
    
    print(f'{"-" * name_padding_size}')
    print(f'| {resource["name"]}{" " * (name_padding_size - resource_name_length - 3)}|')
    print(f'{"-" * name_padding_size}')
    
    # Loop through every key excluding the "Name" key since we just displayed in the header
    for key in list(resource.keys())[1:]:
        
        # Languages needs to print every language in the array, not just the whole array
        if key == 'languages':
            
            print(f'| {key}: ',end='')
            
            # print every language with correct commas
            for index, language in enumerate(resource[key]):
                
                if index != len(resource[key]) - 1:
                    print(f'{language}, ',end='')
                else:
                    print(language)
        else:
            print(f'| {key}: {resource[key]}      ')

    print(f'{"-" * name_padding_size}\n')
    input("Press any key to continue...")


# Resource list with filters
def list_resources(_resources, by_language, by_category=True):
    clear_screen()
    print('------------------------------')
    print('| Community Resource Results |')
    print('------------------------------')
    
    # Reference for later when we need to know what option a user chose
    index_reference = {}
    
    # Get dynamic text and dynamic fields based on filters
    mode = 'Categories' if by_category else 'Resources'
    field = 'category' if by_category else 'name'
    
    # List to keep track of added categories/languages since we only need to display them once
    added_items = []
    
    if by_language:
        mode = 'Languages'
        field = 'languages'
        
    print(f'| {mode}:                ',end='')

    
    # Apply filters (Category/Language)
    # Check if item has been saved already, if not add it, if it has, skip loop (continue)
    index = 0
    for resource in _resources:
        if by_category:
            if resource[field] in added_items:
                continue
            else:
                added_items.append(resource[field])
                
        
        if by_language:
            for language in resource[field]:
                if language in added_items:
                    continue
                else:
                    added_items.append(language)
                    
                # Print language options 
                padding = 24 - len(resource[field])
                print(f'\n| {index}: {language}{" " * padding}',end='')
                index_reference[str(index)] = resource
                index+=1
                
        else:
            # Print resources/categories
            padding = 24 - len(resource[field])
            print(f'\n| {index}: {resource[field]}{" " * padding}',end='')
            index_reference[str(index)] = resource
            index+=1
    
    print('\n-------------------------------')
    
    user_choice = get_user_input()
    
    # Check if user chose a real item
    if not index_reference.get(user_choice):
        print("\nInvalid user input! Press any key to continue...",end='')
        input()
        return
    
    # Show all resources in the chosen category
    if by_category:
        selected_category = added_items[int(user_choice)]
        list_resources([resource for resource in _resources if resource['category'] == selected_category], by_language=False, by_category=False)
    
    # Show all resources with chosen language
    elif by_language:
        selected_language = added_items[int(user_choice)]
        list_resources([resource for resource in _resources if selected_language in resource['languages']], by_language=False, by_category=False)
    
    # Go to resource detail page
    else:
        print_resource_menu(index_reference[user_choice])
        

# Load resources into memory from json file
def load_resources():
    with open('resources.json') as file:
        data = json.load(file)
        return data['resources']

# Main loop
def main():
    
    # Keep track of program status
    running = 1
    resources = load_resources()
    
    while running:
        clear_screen()
        run_main_menu()
        
        user_choice = get_user_input()
        
        # Map user inputs to corresponding screens 
        resource_map = {
            '1': lambda: list_resources(resources, by_language=False),
            '2': lambda: search_resources(resources),
            '3': lambda: list_resources(resources, by_language=True, by_category=False),
            '4': lambda: list_resources(resources, by_language=False, by_category=False),
        }
        
        # Exit program
        if user_choice == '5':
            running = 0
            break
            
        # Call correct function for user choice
        if resource_map.get(user_choice):
            resource_map[user_choice]()
        else:
            # Handle bad input
            print("\nInvalid user input! Press any key to continue...",end='')
            input()
        
        clear_screen()
        
# Start program
if __name__ == '__main__':
    main()