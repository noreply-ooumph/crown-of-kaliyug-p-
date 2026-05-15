"""
Crown of Kaliyug — RAG Retriever
Phase 1 · A-02 · agents/story_engine/script_writer/rag_retriever.py
Uses chromadb directly — no langchain dependency.
"""
import os
import json
import chromadb
from loguru import logger

CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8000))
COLLECTION  = "crown_of_kaliyug_story_bible"


def _get_collection():
    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    return client.get_or_create_collection(COLLECTION)


def retrieve_context(episode_id: str, characters_present: list, season: int) -> str:
    chunks = []

    for char_id in characters_present:
        try:
            with open(f"story_bible/characters/{char_id}.md") as f:
                chunks.append(f"## CHARACTER: {char_id.upper()}\n{f.read()}")
        except FileNotFoundError:
            pass

    try:
        with open("story_bible/world_rules.md") as f:
            chunks.append(f"## WORLD RULES\n{f.read()}")
    except FileNotFoundError:
        pass

    try:
        from database.db import get_db
        from database.models import ContinuityLog
        with get_db() as db:
            facts = db.query(ContinuityLog).filter(
                ContinuityLog.reveal_not_before_season <= season
            ).all()
            if facts:
                lines = "\n".join(f"- [{f.severity}] {f.fact_text}" for f in facts)
                chunks.append(f"## CONTINUITY FACTS\n{lines}")
    except Exception as e:
        logger.warning(f"Could not load continuity facts: {e}")

    try:
        with open("story_bible/season_arc.json") as f:
            arc = json.load(f)
        s = next((x for x in arc["seasons"] if x["id"] == season), None)
        if s:
            chunks.append(
                f"## SEASON {season}\n"
                f"Tone: {s['tone_reference']}\n"
                f"Theme: {s['thematic_identity']}"
            )
    except Exception:
        pass

    context = "\n\n---\n\n".join(chunks)
    logger.info(f"RAG: {len(chunks)} blocks for {episode_id}")
    return context


def embed_series_bible():
    col = _get_collection()
    documents, ids, metadatas = [], [], []

    char_dir = "story_bible/characters"
    if os.path.exists(char_dir):
        for fname in os.listdir(char_dir):
            if fname.endswith(".md"):
                char_id = fname.replace(".md", "")
                with open(f"{char_dir}/{fname}") as f:
                    documents.append(f.read())
                    ids.append(f"char_{char_id}")
                    metadatas.append({"type": "character"})

    for path, doc_id in [
        ("story_bible/world_rules.md", "world_rules"),
        ("story_bible/season_arc.json", "season_arc"),
        ("story_bible/s1_episode_outlines.json", "s1_outlines"),
    ]:
        if os.path.exists(path):
            with open(path) as f:
                documents.append(f.read())
                ids.append(doc_id)
                metadatas.append({"type": doc_id})

    col.add(documents=documents, ids=ids, metadatas=metadatas)
    logger.success(f"Embedded {len(documents)} documents into ChromaDB.")


if __name__ == "__main__":
    embed_series_bible()