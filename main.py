import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from lexicon_processor import LexiconProcessor
from chunker import TextChunker
from scripture_formatter import ScriptureFormatter

app = FastAPI()

lexicon = LexiconProcessor()
formatter = ScriptureFormatter()
chunker = TextChunker(max_words=8)

# Connected screen clients
connected_clients = set()

HTML_DISPLAY = """
<!DOCTYPE html>
<html>
<head>
    <title>Live Church Captions</title>
    <style>
        body {
            background-color: #0b0e14;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        #caption-box {
            font-size: 2.8rem;
            font-weight: 600;
            text-align: center;
            padding: 25px 45px;
            background: rgba(18, 24, 38, 0.85);
            border-radius: 16px;
            border: 2px solid #00E676;
            max-width: 80%;
            min-height: 120px;
            box-shadow: 0px 8px 32px rgba(0, 0, 0, 0.5);
            line-height: 1.4;
        }
    </style>
</head>
<body>
    <div id="caption-box">Ready for live speech...</div>

    <script>
        const ws = new WebSocket("ws://" + location.host + "/ws/captions");
        const box = document.getElementById("caption-box");

        ws.onmessage = function(event) {
            box.innerText = event.data;
        };
    </script>
</body>
</html>
"""

@app.get("/")
async def get_screen():
    return HTMLResponse(HTML_DISPLAY)

@app.websocket("/ws/captions")
async def caption_websocket(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    print(f"Client connected! Total active clients: {len(connected_clients)}")
    
    try:
        while True:
            raw_text = await websocket.receive_text()
            
            # Step 1: Lexicon cleaning
            clean_text = lexicon.process_text(raw_text)
            
            # Step 2: Scripture formatting
            scripture_formatted = formatter.format_scripture(clean_text)
            
            # Step 3: Chunking & Broadcasting to screen
            for word in scripture_formatted.split():
                chunk = chunker.add_word(word)
                if chunk:
                    # Send to all connected displays
                    for client in list(connected_clients):
                        await client.send_text(chunk)
                    await asyncio.sleep(0.1)
                    
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print(f"Client disconnected. Remaining clients: {len(connected_clients)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)