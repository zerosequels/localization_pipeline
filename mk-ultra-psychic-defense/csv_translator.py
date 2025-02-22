import os
import pandas as pd
from ollama.ollama_handler import OllamaHandler

def translate_csv_by_file_path(file_name, should_redo_all=False, is_batched=True):
    """
    Check if a CSV file exists in the output directory and translate its contents using Ollama.
    
    Args:
        file_name (str): Name of the CSV file to process
        should_redo_all (bool): If True, retranslate all entries regardless of existing translations
        is_batched (bool): If True, keeps Ollama running for batch processing, if False shuts down Ollama after completion
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    file_path = os.path.join(output_dir, file_name)
    
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist")
        return
    
    try:
        # Initialize the Ollama handler
        ollama = OllamaHandler()
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Get all column headers
        headers = df.columns.tolist()
        
        # Remove 'key' and 'en' from the list of target languages
        target_languages = [lang for lang in headers if lang not in ['key', 'en']]
        
        if 'en' not in headers:
            print("No 'en' column found in the CSV file")
            return
            
        # Process each row
        total_rows = len(df)
        for index, row in df.iterrows():
            english_text = row['en']
            
            # Skip if English text is empty or NaN
            if pd.isna(english_text) or str(english_text).strip() == "":
                print(f"\nSkipping entry {index + 1}/{total_rows}: Empty English text")
                continue
                
            print(f"\nProcessing entry {index + 1}/{total_rows}: {english_text}")
            
            # Translate to each target language
            for lang_code in target_languages:
                print(f"  Translating to {lang_code}...")
                if should_redo_all or pd.isna(row[lang_code]):  # Translate if forced or cell is empty
                    translation = ollama.translate_string_to_language_by_code(english_text, lang_code)
                    if translation:
                        df.at[index, lang_code] = translation
                        print(f"    ✓ {translation}")
                    else:
                        print(f"    ✗ Translation failed")
                else:
                    print(f"    ⚠ Translation already exists")
            
        # Save the updated DataFrame back to the CSV file
        df.to_csv(file_path, index=False)
        print(f"\nTranslations completed and saved to {file_path}")

        # Shutdown Ollama if not in batch mode
        if not is_batched:
            print("Shutting down Ollama...")
            ollama.shutdown()
            
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        # Ensure Ollama is shut down even if an error occurs (when not in batch mode)
        if not is_batched:
            print("Shutting down Ollama due to error...")
            ollama.shutdown()

def translate_all_csv_files():
    """
    Processes all CSV files found in the output directory by calling translate_csv_by_file_path
    on each file.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    
    if not os.path.exists(output_dir):
        print(f"Output directory {output_dir} does not exist")
        return
        
    # Get all files in the output directory
    files = os.listdir(output_dir)
    csv_files = [f for f in files if f.endswith('.csv')]
    
    if not csv_files:
        print("No CSV files found in output directory")
        return
        
    print(f"Found {len(csv_files)} CSV files to process")
    
    # Initialize Ollama handler for cleanup after all files are processed
    ollama = OllamaHandler()
    
    try:
        for csv_file in csv_files:
            print(f"\nProcessing {csv_file}:")
            print("-" * 50)
            # Keep Ollama running between files by setting is_batched=True
            translate_csv_by_file_path(csv_file, is_batched=True)
            print("-" * 50)
    finally:
        # Always ensure Ollama is shut down after processing all files
        print("\nShutting down Ollama after batch processing...")
        ollama.shutdown()

if __name__ == "__main__":
    print("\nProcessing all CSV files:")
    print("=" * 50)
    translate_all_csv_files()
