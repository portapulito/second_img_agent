from google.adk.tools import ToolContext
from google.genai import types
import requests

    

async def download_and_save_image_tool(
    tool_context: ToolContext,
    image_url: str,
    filename: str 
) -> dict:
    """Tool per scaricare e salvare immagini come artefatti chiedi all'utente il filename con cui vuoi salvare l'immagine."""
    
    try:
        # Download dell'immagine
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        # Crea Part con i dati binari
        image_part = types.Part.from_bytes(
            data=response.content,
            mime_type=response.headers.get('content-type', 'image/jpeg')
        )
        
        # Salva come artefatto
        version = await tool_context.save_artifact(
            filename=filename,
            artifact=image_part
        )
        
        # Aggiorna lo state
        tool_context.state[f"saved_images"] = tool_context.state.get("saved_images", [])
        tool_context.state["saved_images"].append({
            "filename": filename,
            "version": version,
            "url": image_url
        })
        
        return {
            "status": "success",
            "filename": filename,
            "version": version,
            "message": f"Image saved as artifact version {version}"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to save image: {str(e)}"
        }    





