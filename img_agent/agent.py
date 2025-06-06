from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService, GcsArtifactService
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.tools.load_artifacts_tool import load_artifacts_tool
from .tools import download_and_save_image_tool


# Configurazione con servizio in memoria (per test/sviluppo)
artifact_service = InMemoryArtifactService()
session_service = InMemorySessionService()

# O con Google Cloud Storage (per produzione)
# artifact_service = GcsArtifactService()

root_agent = LlmAgent(
    name="my_agent", 
    model="gemini-2.0-flash",
    description="un agente per gestire immagini e fornire descrizioni",
    tools=[download_and_save_image_tool,
            load_artifacts_tool,
        ]
    )

runner = Runner(
    agent=root_agent,
    app_name="my_artifact_app",
    session_service=InMemorySessionService(),
    artifact_service=artifact_service  
)