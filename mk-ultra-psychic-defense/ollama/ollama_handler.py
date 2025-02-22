from ollama import Client
from typing import List, Dict, Optional
import re
import subprocess

class OllamaHandler:
    def __init__(self, model: str = "deepseek-r1:32b"):
        """
        Initialize the Ollama handler
        
        Args:
            model (str): The model to use for chat (default: "deepseek-r1:32b")
        """
        self.client = Client(host='http://localhost:11434')
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []

    def chat(self, message: str, temperature: float = 0.7) -> Optional[str]:
        """
        Send a message to the model and get a response
        
        Args:
            message (str): The message to send
            temperature (float): Controls randomness in the response (0.0 to 1.0)
        
        Returns:
            Optional[str]: The model's response or None if there's an error
        """
        try:
            # Add user message to history
            self.conversation_history.append({
                'role': 'user',
                'content': message
            })

            # Get response from model
            response = self.client.chat(
                model=self.model,
                messages=self.conversation_history,
                options={
                    "temperature": temperature
                }
            )

            # Add assistant's response to history
            if response and response.message:
                self.conversation_history.append({
                    'role': 'assistant',
                    'content': response.message.content
                })
                return response.message.content

            return None

        except Exception as e:
            print(f"Error in chat: {str(e)}")
            return None

    def reset_conversation(self):
        """Clear the conversation history"""
        self.conversation_history = []

    def _clean_think_tags(self, text: str) -> str:
        """
        Remove content between <think></think> tags from the text
        
        Args:
            text (str): The text to clean
            
        Returns:
            str: The cleaned text with think tag content removed
        """
        # Remove everything between <think> and </think> tags, including the tags
        cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        return cleaned_text.strip()

    def translate_string_to_language_by_code(self, text: str, language_code: str, temperature: float = 0.3) -> Optional[str]:
        """
        Translate a given string to the specified language using the language code
        
        Args:
            text (str): The text to translate
            language_code (str): The target language code (e.g., 'fr' for French)
            temperature (float): Controls randomness in the response (0.0 to 1.0)
            
        Returns:
            Optional[str]: The translated text or None if there's an error
        """
        # Reset conversation to ensure clean context
        self.reset_conversation()
        
        prompt = f"""You are a translation engine. Translate the following text to {language_code}.

Rules:
1. DO NOT modify any '%s' characters as they are formatting placeholders
2. Output ONLY the final translation, no explanations or thinking process
3. Do not include quotes around the translation
4. Do not include any other text or formatting in your response, simply output the translation as it's own string. I.e do not include "Translation: " or anything else.

Text to translate: {text}

Translation:"""

        try:
            response = self.chat(prompt, temperature)
            if response:
                # Clean the response by removing think tags and their content
                cleaned_response = self._clean_think_tags(response)
                return cleaned_response
            return None
        except Exception as e:
            print(f"Error in translation: {str(e)}")
            return None

    def test_translation(self):
        """
        Test the translation functionality with a simple example
        """
        test_word = "bread"
        test_language = "fr"
        print(f"\nTesting translation of '{test_word}' to {test_language}...")
        
        result = self.translate_string_to_language_by_code(test_word, test_language)
        
        if result:
            print(f"Translation result: {result}")
        else:
            print("Translation failed!")

    def shutdown(self):
        """
        Cleanup and shutdown the Ollama instance
        """
        try:
            # Run terminal command to stop Ollama service
            subprocess.run(['pkill', 'ollama'], check=False)
            print("\nOllama service has been stopped.")
        except Exception as e:
            print(f"\nError stopping Ollama service: {str(e)}")

def main():
    # Example usage
    handler = OllamaHandler()
    
    while True:
        # Get user input
        user_input = input("\nEnter your message (or 'quit' to exit and stop Ollama, 'reset' to clear history, 'test' to run translation test): ")
        
        # Check for quit command
        if user_input.lower() == 'quit':
            handler.shutdown()
            break
            
        # Check for reset command
        if user_input.lower() == 'reset':
            handler.reset_conversation()
            print("Conversation history cleared!")
            continue
            
        # Check for test command
        if user_input.lower() == 'test':
            handler.test_translation()
            continue
        
        # Get response from model
        print("\nThinking...")
        response = handler.chat(user_input, 0.5)
        
        if response:
            print("\nAssistant:", response)
        else:
            print("\nError: Failed to get response")

if __name__ == "__main__":
    print("Starting MK Ultra Psychic Defense Chat System...")
    print("Using deepseek:r1 model")
    print("Type 'quit' to exit or 'reset' to clear conversation history")
    main() 