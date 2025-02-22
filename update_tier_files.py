import json
import os

def update_tier_file(file_path):
    # Read the existing file
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Create new data structure
    new_data = {}
    for key, value in data.items():
        new_data[key] = {
            "base": value,
            "ability": value,
            "description": value,
            "lore_1": value,
            "lore_2": value,
            "lore_3": value
        }
    
    # Write back to file with pretty printing
    with open(file_path, 'w') as f:
        json.dump(new_data, f, indent=4)
    
    print(f"Updated {file_path}")

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(script_dir, 'mk-ultra-psychic-defense', 'config')
    
    # Update all tier files
    for i in range(1, 11):
        tier_file = os.path.join(config_dir, f'tier_{i}.json')
        if os.path.exists(tier_file):
            update_tier_file(tier_file)
        else:
            print(f"Warning: {tier_file} not found")

if __name__ == "__main__":
    main() 