import re

class ScriptureFormatter:
    def __init__(self):
        # Map Yoruba/English spoken book names to standard Bible abbreviations
        self.book_mappings = {
            r"rómù|romu|romans": "Romans",
            r"jẹ́nẹ́sísì|genesis": "Genesis",
            r"ẹ́ksódù|exodus": "Exodus",
            r"sálmù|psalms|psalm": "Psalms",
            r"mátíù|matthew": "Matthew",
            r"jòhánù|john": "John",
            r"ìṣe àwọn àpọ́sítélì|acts": "Acts"
        }

    def format_scripture(self, text: str) -> str:
        processed = text

        # Match patterns like: "Rómù chapter 8 verse 28" or "Romans 8 verse 28"
        for yoruba_book, standard_book in self.book_mappings.items():
            # Pattern captures: [Book] + optional words + [Chapter] + optional words + [Verse]
            pattern = rf"\b({yoruba_book})\b\s*(?:chapter|káàkiri|ori)?\s*(\d+)\s*(?:verse|ẹsẹ)?\s*(\d+)"
            
            def replace_match(match):
                chapter = match.group(2)
                verse = match.group(3)
                return f"📖 [{standard_book} {chapter}:{verse} (KJV)]"

            processed = re.sub(pattern, replace_match, processed, flags=re.IGNORECASE)

        return processed

# --- Test Task 3 ---
if __name__ == "__main__":
    formatter = ScriptureFormatter()
    
    # Test cases matching the document
    test_1 = "Ẹ sí péèjì Rómù chapter 8 verse 28"
    test_2 = "Let us open our Bibles to Genesis chapter 1 verse 3"

    print("--- Task 3 Scripture Formatter Test ---")
    print(f"Original 1: {test_1}")
    print(f"Formatted 1: {formatter.format_scripture(test_1)}\n")
    
    print(f"Original 2: {test_2}")
    print(f"Formatted 2: {formatter.format_scripture(test_2)}")