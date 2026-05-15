# Crown of Kaliyug — AI Production Pipeline

## Overview
End-to-end AI pipeline for producing Crown of Kaliyug — a mythological web series based on the Mahabharata. 13 agents across 6 phases automate script generation, audio production, video assembly, and distribution.

## Architecture
Story Bible (RAG) → Script Writer → Dialogue Agent → Canon Guardian
→ Avatar Agent → Video Generation
→ Voiceover (Edge TTS) → Music → SFX
→ Video Editor → Platform Formatter
→ Analytics + Distribution

## Phase Breakdown
- **Phase 0: Foundation** — Story Bible, ChromaDB, SQLite
- **Phase 1: Story Engine** — A-02 Script, A-03 Dialogue, A-04 Canon Guardian
- **Phase 2: Visual Production** — A-05 Avatar, A-06 Video Generation
- **Phase 3: Audio Production** — A-07 Voiceover, A-08 Music, A-09 SFX
- **Phase 4: Post-Production** — A-10 Video Editor, A-11 Platform Formatter
- **Phase 5: Distribution** — A-12 Analytics Agent

## Setup
1. Clone repo
2. `python -m venv venv` && `venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill API keys
5. `python main.py`

## API Keys Required (in .env)
```env
GROQ_API_KEY=         # LLM — script generation (free)
HUGGINGFACE_API_KEY=  # Video generation (free)
DID_API_KEY=          # Lip sync (D-ID)
ELEVENLABS_API_KEY=   # Production voice (optional)
ANTHROPIC_API_KEY=    # Claude Sonnet for production (optional)
```

## Run Pipeline
- `python main.py`                   # Full S1E01 pipeline
- `python main.py --skip-video`      # Skip video generation
- `python main.py --phase 1`         # Run specific phase
- `python main.py --episode S1E02`   # Different episode

## Test Suite
- `python tests/test_phase0.py`
- `python tests/test_phase1.py`
- `python tests/test_phase3.py`
- `python tests/test_phase4.py`
- `python tests/test_phase5.py`

## Team
- **Praveen Agrawal** — CRM & Agent Development
- **Anagh Dwivedi** — Visual Pipeline (A-05, A-06)
- **Shristi Khanna** — Coordination & HITL
- **Dipanshu Singh** — Tech Lead
- **Priya / Shelly** — Creative Directors

## Production Status
- **Phase 0-5**: Complete
- **S1E01**: Demo episode generating
- **Pending**: Real video generation (Runway/Kling), ElevenLabs voice, Suno music
