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
    print('| 4: View All Resources      |')
    print('| 5: Language Coverage Stats |')
    print('| 6: Exit Program            |')
    print('------------------------------')


# Calculate language coverage stats across all resources
def calculate_language_coverage(_resources):
    total = len(_resources)
    language_counts = {}

    for resource in _resources:
        for language in resource['languages']:
            if language not in language_counts:
                language_counts[language] = 0
            language_counts[language] += 1

    # Build result: language -> (count, percentage)
    coverage = {}
    for language, count in language_counts.items():
        percentage = (count / total) * 100
        coverage[language] = {
            'count': count,
            'total': total,
            'percentage': round(percentage, 1)
        }

    # Sort by percentage descending
    coverage = dict(sorted(coverage.items(), key=lambda x: x[1]['percentage'], reverse=True))
    return coverage


# Display language coverage stats screen
def show_language_coverage(_resources):
    clear_screen()
    coverage = calculate_language_coverage(_resources)
    total = len(_resources)

    W = 38  # total width including pipes
    border = '-' * W
    print(border)
    print(f'| {"Language Coverage Stats":<{W-4}}  |')
    print(border)
    print(f'| {"Total Resources: " + str(total):<{W-4}}  |')
    print(border)
    print(f'| {"Language":<13} {"Count":<9} {"Coverage":<8}    |')
    print(border)

    for language, stats in coverage.items():
        bar_filled = int(stats['percentage'] / 10)
        bar = '█' * bar_filled + '░' * (10 - bar_filled)
        count_str = f'{stats["count"]}/{total}'
        pct_str = f'{stats["percentage"]}%'
        print(f'| {language:<13} {count_str:<9} {pct_str:<8}    |')
        print(f'| [{bar}]{"":>{W-15}} |')
        print(f'|{" " * (W-1)}|')

    print(border)
    input("\nPress any key to continue...")


# Resource search menu
def search_resources(_resources):
    clear_screen()
    
    search_term = get_user_input("Enter a search term: ")
    
    matched_resources = []
    
    for resource in _resources:
        if search_term.lower() in resource['name'].lower():
            matched_resources.append(resource)
            
    if len(matched_resources) > 0:
        clear_screen()
        list_resources([resource for resource in matched_resources], by_category=False, by_language=False)
    else:
        user_choice = get_user_input("No search results found, try again? (y/n): ")
        if user_choice.lower() == 'y':
            clear_screen()
            search_resources(_resources)


# Single resource info menu
def print_resource_menu(resource):
    clear_screen()
    
    resource_name_length = len(resource['name'])
    name_padding_size = (resource_name_length + 5) if (resource_name_length + 5) > 15 else 15
    
    print(f'{"-" * name_padding_size}')
    print(f'| {resource["name"]}{" " * (name_padding_size - resource_name_length - 3)}|')
    print(f'{"-" * name_padding_size}')
    
    for key in list(resource.keys())[1:]:
        if key == 'languages':
            print(f'| {key}: ', end='')
            for index, language in enumerate(resource[key]):
                if index != len(resource[key]) - 1:
                    print(f'{language}, ', end='')
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
    
    index_reference = {}
    
    mode = 'Categories' if by_category else 'Resources'
    field = 'category' if by_category else 'name'
    
    added_items = []
    
    if by_language:
        mode = 'Languages'
        field = 'languages'

        # Pre-calculate coverage for display alongside language options
        coverage = calculate_language_coverage(_resources)
        
    print(f'| {mode}:                ', end='')

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
                    
                # Show language with coverage percentage
                stats = coverage.get(language, {})
                pct = stats.get('percentage', 0)
                label = f'{language} ({pct}%)'
                padding = 24 - len(label)
                print(f'\n| {index}: {label}{" " * padding}', end='')
                index_reference[str(index)] = resource
                index += 1
                
        else:
            padding = 24 - len(resource[field])
            print(f'\n| {index}: {resource[field]}{" " * padding}', end='')
            index_reference[str(index)] = resource
            index += 1
    
    print('\n-------------------------------')
    
    user_choice = get_user_input()
    
    if not index_reference.get(user_choice):
        print("\nInvalid user input! Press any key to continue...", end='')
        input()
        return
    
    if by_category:
        selected_category = added_items[int(user_choice)]
        list_resources([resource for resource in _resources if resource['category'] == selected_category], by_language=False, by_category=False)
    
    elif by_language:
        selected_language = added_items[int(user_choice)]
        list_resources([resource for resource in _resources if selected_language in resource['languages']], by_language=False, by_category=False)
    
    else:
        print_resource_menu(index_reference[user_choice])


# Load resources into memory from json file
def load_resources():
    with open('resources.json') as file:
        data = json.load(file)
        return data['resources']


# Main loop
def main():
    running = 1
    resources = load_resources()
    
    while running:
        clear_screen()
        run_main_menu()
        
        user_choice = get_user_input()
        
        resource_map = {
            '1': lambda: list_resources(resources, by_language=False),
            '2': lambda: search_resources(resources),
            '3': lambda: list_resources(resources, by_language=True, by_category=False),
            '4': lambda: list_resources(resources, by_language=False, by_category=False),
            '5': lambda: show_language_coverage(resources),
        }
        
        if user_choice == '6':
            running = 0
            break
            
        if resource_map.get(user_choice):
            resource_map[user_choice]()
        else:
            print("\nInvalid user input! Press any key to continue...", end='')
            input()
        
        clear_screen()

        
# Start program
if __name__ == '__main__':
    main()