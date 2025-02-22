import os
import subprocess

def activate_mk_ultra_localization_pipeline():
    print("Activating MK Ultra Localization Pipeline...")
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to config_transformer.py
    config_transformer_path = os.path.join(script_dir, 'mk-ultra-psychic-defense', 'config_transformer.py')
    
    try:
        # Run the config transformer script
        print("Running Config Transformer...")
        subprocess.run(['python3', config_transformer_path], check=True)
        print("Config Transformer completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running Config Transformer: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

def main():
    print("Master Localization Pipeline - Starting...")
    try:
        activate_mk_ultra_localization_pipeline()
        print("Master Localization Pipeline completed successfully.")
    except Exception as e:
        print(f"Master Localization Pipeline failed: {e}")
        exit(1)

if __name__ == "__main__":
    main() 