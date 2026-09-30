import time

class TextChunker:
    def __init__(self, max_words=8, max_pause_seconds=1.5):
        self.max_words = max_words
        self.max_pause_seconds = max_pause_seconds
        self.buffer = []
        self.last_word_time = time.time()

    def add_word(self, word: str):
        """Adds a new word to the buffer and checks if it's time to output a chunk."""
        current_time = time.time()
        self.buffer.append(word)
        
        time_elapsed = current_time - self.last_word_time
        self.last_word_time = current_time

        # Conditions to release a chunk:
        # 1. Word count reached max line limit
        # 2. End of sentence punctuation hit (. ! ?)
        # 3. Speaker paused for too long
        is_sentence_end = word.endswith(('.', '!', '?'))
        is_buffer_full = len(self.buffer) >= self.max_words
        is_pause_long = time_elapsed > self.max_pause_seconds

        if is_buffer_full or is_sentence_end or (is_pause_long and len(self.buffer) > 0):
            chunk = " ".join(self.buffer)
            self.buffer = []  # Clear buffer for next line
            return chunk
        
        return None  # Still waiting for more words to complete the line

# --- Simple Simulation Test ---
if __name__ == "__main__":
    chunker = TextChunker(max_words=6)
    
    # Simulating word-by-word streaming from Speech AI
    streamed_words = [
        "Welcome", "everyone", "to", "church", "today.",
        "We", "are", "glad", "you", "are", "here", "with", "us."
    ]

    print("--- Text Chunking Simulation ---")
    for word in streamed_words:
        time.sleep(0.3)  # Simulate word stream delay
        line = chunker.add_word(word)
        if line:
            print(f"[DISPLAY ON SCREEN]: {line}")