import asyncio
import websockets

async def test_full_sentences():
    uri = "ws://localhost:8000/ws/captions"
    
    print("Connecting to live caption server...")
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected! Sending complete test phrases...\n")
            
            # Full sentences targeting Pastor names, Yoruba terms, and Spoken Scriptures
            test_phrases = [
                "Welcome pastor add a kunle to the service today.",
                "Let us pray to Oluwa and say halleluyah for His goodness.",
                "Ẹ sí péèjì Rómù chapter 8 verse 28 right now.",
                "Please turn your Bibles to Genesis chapter 1 verse 3."
            ]
            
            for i, phrase in enumerate(test_phrases, 1):
                print(f"[{i}] Sending Raw: {phrase}")
                await websocket.send(phrase)
                await asyncio.sleep(4)  # Pause to observe the display output on screen
                
            print("Finished sending all test phrases.")

    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(test_full_sentences())