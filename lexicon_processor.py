import json
import re

class LexiconProcessor:
    def __init__(self, lexicon_path="church_lexicon.json"):
        with open(lexicon_path, "r", encoding="utf-8") as f:
            self.lexicon = json.load(f)

    def process_text(self, text: str) -> str:
        processed = text

        # 1. Correct Misheard Pastor Names
        for correct_name, misheard_list in self.lexicon.get("name_corrections", {}).items():
            for misheard in misheard_list:
                pattern = re.compile(re.escape(misheard), re.IGNORECASE)
                processed = pattern.sub(correct_name, processed)

        # 2. Map Yoruba/Church Phrases
        for key, value in self.lexicon.get("phrase_mappings", {}).items():
            if isinstance(value, list):
                for pattern_str in value:
                    pattern = re.compile(re.escape(pattern_str), re.IGNORECASE)
                    processed = pattern.sub(key, processed)
            else:
                pattern = re.compile(re.escape(key), re.IGNORECASE)
                processed = pattern.sub(value, processed)

        return processed

if __name__ == "__main__":
    processor = LexiconProcessor()
    
    # Test sample
    test_input = "Welcome pastor add a kunle, let us pray to Oluwa and say halleluyah."
    result = processor.process_text(test_input)
    
    print("\n--- Lexicon Processor Test ---")
    print(f"Original: {test_input}")
    print(f"Cleaned:  {result}\n")