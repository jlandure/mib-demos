import os
import base64
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from google.genai import types

# Import the agent
from agent import root_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- LOAD DATA (STATIC RAG) ---
ALIEN_DATA = ""
try:
    # Look for data/data.yaml relative to this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Try several possible paths (local vs Docker structure)
    possible_paths = [
        os.path.join(current_dir, "data", "data.yaml"),
        os.path.join(current_dir, "..", "data", "data.yaml"), # Local dev case
        "data/data.yaml"
    ]
    
    for p in possible_paths:
        if os.path.exists(p):
            print(f"Loading alien database from: {p}")
            with open(p, "r") as f:
                ALIEN_DATA = f.read()
            break
            
    if not ALIEN_DATA:
        print("WARNING: data.yaml not found. Agent will run without database.")
        ALIEN_DATA = "Error: Alien database unavailable."
        
except Exception as e:
    print(f"Error loading data: {e}")
    ALIEN_DATA = "Error loading database."

@app.get("/")
def health_check():
    return {"status": "ok", "agent": "bodysafety", "db_loaded": len(ALIEN_DATA) > 100}

@app.post("/agent/chat")
async def chat_endpoint(
    file: UploadFile = File(None),
    prompt: str = Form("Analyze this alien image"),
):
    try:
        contents = []
        contents.append(prompt)
        
        if file:
            image_bytes = await file.read()
            image_part = types.Part.from_bytes(
                data=image_bytes,
                mime_type=file.content_type or "image/jpeg"
            )
            contents.append(image_part)
            
        # Convert text prompts to Parts explicitly
        # types.Content expects a list of Part objects, not strings
        final_contents = []
        for item in contents:
            if isinstance(item, str):
                final_contents.append(types.Part.from_text(text=item))
            else:
                final_contents.append(item)

        # Inject database into the system instruction
        # Take the agent's original system instruction and append the DB
        full_instruction = root_agent.instruction + "\n\n=== MIB ALIEN DATABASE ===\n" + ALIEN_DATA
        
        # Force the model to use the provided data
        full_instruction += "\n\nIMPORTANT: USE the 'MIB ALIEN DATABASE' provided above to identify the alien. Do not use external tools."

        response = root_agent.model.api_client.models.generate_content(
            model=root_agent.model.model,
            contents=[types.Content(role="user", parts=final_contents)],
            config=types.GenerateContentConfig(
                system_instruction=full_instruction,
                temperature=0.4,
                 safety_settings=[
                    types.SafetySetting(
                        category="HARM_CATEGORY_DANGEROUS_CONTENT",
                        threshold="BLOCK_ONLY_HIGH"
                    )
                ]
            )
        )
        
        return {"response": response.text}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
