import json
import os
from datetime import datetime
import csv
import re

# Global configuration
HEADERS = ['key', 'en', 'de', 'es', 'fr', 'it', 'ja', 'ko', 'pt', 'ru', 'tr', 'zh']
LANGUAGE_COUNT = len(HEADERS) - 1  # Subtract 1 to account for 'key' column

# Directory configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(SCRIPT_DIR, 'config')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output')

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_text(text):
    # Convert to uppercase, remove special characters, replace spaces with underscore
    cleaned = text.upper()
    cleaned = re.sub(r'[^A-Z0-9\s]', '', cleaned)
    cleaned = cleaned.replace(' ', '_')
    return cleaned

def generate_base_theory_csv_file():
    # Use fixed filename
    output_file = os.path.join(OUTPUT_DIR, 'base_theory.csv')
    
    # Dictionary to store all theories
    theories = {}
    
    # Read all tier files
    for i in range(1, 11):
        tier_file = os.path.join(CONFIG_DIR, f'tier_{i}.json')
        try:
            with open(tier_file, 'r') as f:
                tier_data = json.load(f)
                print(f"Processing tier {i} with {len(tier_data)} theories")
                for key, theory_data in tier_data.items():
                    # Clean the text and add to theories dict
                    cleaned_key = clean_text(key)  # Use the key for the cleaned key
                    if cleaned_key not in theories:
                        theories[cleaned_key] = [''] * LANGUAGE_COUNT  # Empty strings for all language columns
                        theories[cleaned_key][0] = theory_data['base']  # Set English value to the base value
        except FileNotFoundError:
            print(f"Warning: {tier_file} not found")
            continue
        except json.JSONDecodeError as e:
            print(f"Error reading {tier_file}: {e}")
            continue
    
    print(f"Total theories collected: {len(theories)}")
    
    # Write to CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write headers
        writer.writerow(HEADERS)
        # Write data
        for theory_key in sorted(theories.keys()):
            row = [theory_key] + theories[theory_key]
            writer.writerow(row)
            print(f"Writing theory: {theory_key}")
    
    print(f"CSV file generated: {output_file}")

def generate_theory_description_csv_file():
    # Use fixed filename
    output_file = os.path.join(OUTPUT_DIR, 'theory_description.csv')
    
    # Dictionary to store all theories
    theories = {}
    
    # Read all tier files
    for i in range(1, 11):
        tier_file = os.path.join(CONFIG_DIR, f'tier_{i}.json')
        try:
            with open(tier_file, 'r') as f:
                tier_data = json.load(f)
                print(f"Processing tier {i} with {len(tier_data)} theories")
                for key, theory_data in tier_data.items():
                    # Clean the text and add to theories dict
                    cleaned_key = clean_text(key) + '_DESCRIPTION'  # Use the key for the cleaned key
                    if cleaned_key not in theories:
                        theories[cleaned_key] = [''] * LANGUAGE_COUNT  # Empty strings for all language columns
                        theories[cleaned_key][0] = theory_data['description']  # Set English value to the description value
        except FileNotFoundError:
            print(f"Warning: {tier_file} not found")
            continue
        except json.JSONDecodeError as e:
            print(f"Error reading {tier_file}: {e}")
            continue
    
    print(f"Total theory descriptions collected: {len(theories)}")
    
    # Write to CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write headers
        writer.writerow(HEADERS)
        # Write data
        for theory_key in sorted(theories.keys()):
            row = [theory_key] + theories[theory_key]
            writer.writerow(row)
            print(f"Writing theory description: {theory_key}")
    
    print(f"CSV file generated: {output_file}")

def generate_theory_ability_csv_file():
    # Use fixed filename
    output_file = os.path.join(OUTPUT_DIR, 'theory_ability.csv')
    
    # Dictionary to store all theories
    theories = {}
    
    # Read all tier files
    for i in range(1, 11):
        tier_file = os.path.join(CONFIG_DIR, f'tier_{i}.json')
        try:
            with open(tier_file, 'r') as f:
                tier_data = json.load(f)
                print(f"Processing tier {i} with {len(tier_data)} theories")
                for key, theory_data in tier_data.items():
                    # Clean the text and add to theories dict
                    cleaned_key = clean_text(key) + '_ABILITY'  # Use the key for the cleaned key
                    if cleaned_key not in theories:
                        theories[cleaned_key] = [''] * LANGUAGE_COUNT  # Empty strings for all language columns
                        theories[cleaned_key][0] = theory_data['ability']  # Set English value to the ability value
        except FileNotFoundError:
            print(f"Warning: {tier_file} not found")
            continue
        except json.JSONDecodeError as e:
            print(f"Error reading {tier_file}: {e}")
            continue
    
    print(f"Total theory abilities collected: {len(theories)}")
    
    # Write to CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write headers
        writer.writerow(HEADERS)
        # Write data
        for theory_key in sorted(theories.keys()):
            row = [theory_key] + theories[theory_key]
            writer.writerow(row)
            print(f"Writing theory ability: {theory_key}")
    
    print(f"CSV file generated: {output_file}")

def generate_theory_lore_csv_file():
    # Use fixed filename
    output_file = os.path.join(OUTPUT_DIR, 'theory_lore.csv')
    
    # Dictionary to store all theories
    theories = {}
    
    # Read all tier files
    for i in range(1, 11):
        tier_file = os.path.join(CONFIG_DIR, f'tier_{i}.json')
        try:
            with open(tier_file, 'r') as f:
                tier_data = json.load(f)
                print(f"Processing tier {i} with {len(tier_data)} theories")
                for key, theory_data in tier_data.items():
                    # Clean the text and add to theories dict with three lore entries
                    base_key = clean_text(key)
                    for lore_num in range(1, 4):  # Create three lore entries
                        lore_key = f"{base_key}_LORE_{lore_num}"
                        if lore_key not in theories:
                            theories[lore_key] = [''] * LANGUAGE_COUNT  # Empty strings for all language columns
                            theories[lore_key][0] = theory_data[f'lore_{lore_num}']  # Set English value to the corresponding lore value
        except FileNotFoundError:
            print(f"Warning: {tier_file} not found")
            continue
        except json.JSONDecodeError as e:
            print(f"Error reading {tier_file}: {e}")
            continue
    
    print(f"Total theory lore entries collected: {len(theories)}")
    
    # Write to CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write headers
        writer.writerow(HEADERS)
        # Write data
        for theory_key in sorted(theories.keys()):
            row = [theory_key] + theories[theory_key]
            writer.writerow(row)
            print(f"Writing theory lore: {theory_key}")
    
    print(f"CSV file generated: {output_file}")

def generate_terminology_term_csv_file():
    # Use fixed filename
    output_file = os.path.join(OUTPUT_DIR, 'terminology_term.csv')
    
    # Dictionary to store all terms
    terms = {}
    
    # Read terminology file
    terminology_file = os.path.join(CONFIG_DIR, 'terminology.json')
    try:
        with open(terminology_file, 'r') as f:
            terminology_data = json.load(f)
            print(f"Processing terminology with {len(terminology_data)} terms")
            for key, term_data in terminology_data.items():
                # Clean the text and add to terms dict
                cleaned_key = clean_text(key)
                if cleaned_key not in terms:
                    terms[cleaned_key] = [''] * LANGUAGE_COUNT  # Empty strings for all language columns
                    terms[cleaned_key][0] = term_data['term']  # Set English value to the term value
    except FileNotFoundError:
        print(f"Warning: {terminology_file} not found")
    except json.JSONDecodeError as e:
        print(f"Error reading {terminology_file}: {e}")
    
    print(f"Total terms collected: {len(terms)}")
    
    # Write to CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write headers
        writer.writerow(HEADERS)
        # Write data
        for term_key in sorted(terms.keys()):
            row = [term_key] + terms[term_key]
            writer.writerow(row)
            print(f"Writing term: {term_key}")
    
    print(f"CSV file generated: {output_file}")

def generate_terminology_description_csv_file():
    # Use fixed filename
    output_file = os.path.join(OUTPUT_DIR, 'terminology_description.csv')
    
    # Dictionary to store all terms
    terms = {}
    
    # Read terminology file
    terminology_file = os.path.join(CONFIG_DIR, 'terminology.json')
    try:
        with open(terminology_file, 'r') as f:
            terminology_data = json.load(f)
            print(f"Processing terminology with {len(terminology_data)} descriptions")
            for key, term_data in terminology_data.items():
                # Clean the text and add to terms dict
                cleaned_key = clean_text(key) + '_DESCRIPTION'
                if cleaned_key not in terms:
                    terms[cleaned_key] = [''] * LANGUAGE_COUNT  # Empty strings for all language columns
                    terms[cleaned_key][0] = term_data['explanation']  # Set English value to the explanation value
    except FileNotFoundError:
        print(f"Warning: {terminology_file} not found")
    except json.JSONDecodeError as e:
        print(f"Error reading {terminology_file}: {e}")
    
    print(f"Total descriptions collected: {len(terms)}")
    
    # Write to CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write headers
        writer.writerow(HEADERS)
        # Write data
        for term_key in sorted(terms.keys()):
            row = [term_key] + terms[term_key]
            writer.writerow(row)
            print(f"Writing description: {term_key}")
    
    print(f"CSV file generated: {output_file}")

def main():
    print("MK Ultra Psychic Defense System - Config Transformer")
    generate_base_theory_csv_file()
    generate_theory_description_csv_file()
    generate_theory_ability_csv_file()
    generate_theory_lore_csv_file()
    generate_terminology_term_csv_file()
    generate_terminology_description_csv_file()

if __name__ == "__main__":
    main() 