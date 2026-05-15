from orchestrator.state_schema import create_initial_state
from agents.visual_prod.avatar.avatar_agent import run as avatar_run
from agents.visual_prod.video.video_agent import run as video_run
from agents.audio_prod.voiceover.voiceover_agent import run as vo_run
from agents.post_prod.editor.agent import run as editor_run
from loguru import logger
import sys

# Configure logger for visibility
logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}")

print("--- STARTING MINI-PIPELINE REGENERATION ---")
state = create_initial_state('S1E01', 1, 1, 'The Weight of Crowns', 'Mukut Ka Bojh')
state['script_draft_path'] = 'output/scripts/S1E01_draft_1.json'

print("\n1. Avatar Agent...")
state = avatar_run(state)

print("\n2. Video Generation (Ken Burns)...")
state = video_run(state)

print("\n3. Voiceover (Edge TTS)...")
state = vo_run(state)

print("\n4. Video Editor (Assembly)...")
state = editor_run(state)

print("\n--- REGENERATION COMPLETE ---")
print(f"Master Video Path: {state.get('master_video_path')}")
