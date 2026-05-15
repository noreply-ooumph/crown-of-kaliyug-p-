"""
Crown of Kaliyug — Continuity Log Pre-Seeder
Phase 0: Foundation

Seeds the critical protected facts from Series Bible v1.0.
These are the HARD RULES the Canon Guardian agent checks against.
Any script that violates these triggers a CRITICAL violation.
"""
from database.db import get_db
from database.models import ContinuityLog, Character
from loguru import logger
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PROTECTED_FACTS = [
    # ── KARNA ──────────────────────────────────────────────────────────────────
    {
        "episode_id": None,                         # pre-loaded before any episode
        "character_id": "karna",
        "fact_text": (
            "Karna is Kunti's firstborn son — the Pandavas' eldest brother. "
            "This truth must NOT be revealed to characters or audience before Season 3. "
            "Krishna tells him privately in Season 3. Kunti meets him by the river also in Season 3."
        ),
        "severity": "CRITICAL",
        "reveal_not_before_season": 3,
        "source": "series_bible",
    },
    {
        "episode_id": None,
        "character_id": "karna",
        "fact_text": (
            "Karna possesses divine armor (Surya's kavacha) grown into his skin from birth. "
            "Kunti asks for this armor in their river meeting in Season 3. He gives it. "
            "After this point, Karna's avatar must NOT show the glowing armor."
        ),
        "severity": "CRITICAL",
        "reveal_not_before_season": 3,
        "source": "series_bible",
    },
    {
        "episode_id": None,
        "character_id": "karna",
        "fact_text": (
            "Karna's father is Adhiratha — a charioteer. This IS public knowledge from S1E01 "
            "(he states it at the tournament). The SECRET is that his biological mother is Kunti."
        ),
        "severity": "STANDARD",
        "reveal_not_before_season": 1,
        "reveal_not_before_ep": "S1E01",
        "source": "series_bible",
    },
    {
        "episode_id": "S1E01",
        "character_id": "karna",
        "fact_text": (
            "Duryodhana made Karna King of Anga in S1E01 — placed his own signet ring on Karna's hand "
            "in front of every king in Bharatavarsha. Karna is now officially royalty."
        ),
        "severity": "STANDARD",
        "source": "pilot_script",
    },
    {
        "episode_id": None,
        "character_id": "karna",
        "fact_text": (
            "Karna dies on Day 16 of Kurukshetra (S4E16). His chariot wheel sinks into earth. "
            "He steps down unarmed to free it. Arjuna kills him on Krishna's instruction. "
            "The rules of honorable combat are broken. Everyone knows it."
        ),
        "severity": "CRITICAL",
        "reveal_not_before_season": 4,
        "source": "series_bible",
    },

    # ── KRISHNA ─────────────────────────────────────────────────────────────────
    {
        "episode_id": None,
        "character_id": "krishna",
        "fact_text": (
            "Krishna's divine nature (Vishwarupa / Avatar of Vishnu) must NEVER be shown "
            "directly before Season 5. Until then: implied through atmosphere, light, heat "
            "distortion, and others' reactions. Any full CGI divine reveal before S5 is CRITICAL violation."
        ),
        "severity": "CRITICAL",
        "reveal_not_before_season": 5,
        "source": "series_bible",
    },
    {
        "episode_id": None,
        "character_id": "krishna",
        "fact_text": (
            "Krishna NEVER lies — not even once. He only withholds, redirects, and asks questions. "
            "This is an ABSOLUTE rule from the source material. Any dialogue where Krishna "
            "directly states something false must be rewritten immediately."
        ),
        "severity": "CRITICAL",
        "source": "series_bible",
    },
    {
        "episode_id": None,
        "character_id": "krishna",
        "fact_text": (
            "Dwarka sinks into the sea in Season 7 after Krishna's death. "
            "This is the series' defining VFX sequence — 18% of total VFX budget. "
            "Krishna's flute goes permanently silent before this event."
        ),
        "severity": "CRITICAL",
        "reveal_not_before_season": 7,
        "source": "series_bible",
    },

    # ── BHISHMA ─────────────────────────────────────────────────────────────────
    {
        "episode_id": None,
        "character_id": "bhishma",
        "fact_text": (
            "Bhishma falls on Day 10 of Kurukshetra (S4E10). He lands on a bed of arrows. "
            "He requests the right astronomical moment to die — both armies pause and come "
            "to pay respects. He dispenses wisdom from his arrow-bed. This is a season-level event."
        ),
        "severity": "CRITICAL",
        "reveal_not_before_season": 4,
        "source": "series_bible",
    },
    {
        "episode_id": None,
        "character_id": "bhishma",
        "fact_text": (
            "Bhishma knows the Pandavas are right. He fights against them anyway "
            "because his vow binds him to whoever sits on the Kuru throne. "
            "He has the power to stop the war and will not use it."
        ),
        "severity": "STANDARD",
        "source": "series_bible",
    },

    # ── SHAKUNI ─────────────────────────────────────────────────────────────────
    {
        "episode_id": None,
        "character_id": "shakuni",
        "fact_text": (
            "Shakuni's dice are carved from the bones of his father, who died in a Kuruvansa prison. "
            "They always come up the same. Every throw is a prayer for vengeance. "
            "This must be established in S1E01 (late night scene, Duryodhana's chambers)."
        ),
        "severity": "CRITICAL",
        "reveal_not_before_ep": "S1E01",
        "source": "series_bible",
    },

    # ── KUNTI ──────────────────────────────────────────────────────────────────
    {
        "episode_id": None,
        "character_id": "kunti",
        "fact_text": (
            "Kunti recognises Karna at the S1E01 tournament. She says nothing. "
            "The camera holds on her face. She is thinking about a sixth son. "
            "This is the first hint — no dialogue, only Kunti's expression."
        ),
        "severity": "STANDARD",
        "reveal_not_before_ep": "S1E01",
        "source": "pilot_script",
    },

    # ── DRAUPADI ──────────────────────────────────────────────────────────────
    {
        "episode_id": None,
        "character_id": "draupadi",
        "fact_text": (
            "Draupadi's sons are killed in their sleep by Ashwatthama in Season 6. "
            "This is one of the most devastating events of the aftermath arc. "
            "Do not reference this before Season 6."
        ),
        "severity": "CRITICAL",
        "reveal_not_before_season": 6,
        "source": "series_bible",
    },
    {
        "episode_id": None,
        "character_id": "draupadi",
        "fact_text": (
            "Draupadi could have stopped the war three times. She chose not to. "
            "This is her hidden truth — she is not merely a victim. She is an agent. "
            "Write every scene with this knowledge, even if unspoken."
        ),
        "severity": "STANDARD",
        "source": "series_bible",
    },

    # ── MUSIC / SCORE RULES ──────────────────────────────────────────────────
    {
        "episode_id": "S1E01",
        "character_id": None,
        "fact_text": (
            "THE KURUKSHETRA THEME: A melody that appears FRAGMENTED and barely noticeable "
            "in S1E01. It must return FULLY FORMED only when the war begins in Season 4. "
            "Using the full Kurukshetra theme before Season 4 is a CRITICAL violation."
        ),
        "severity": "CRITICAL",
        "reveal_not_before_season": 4,
        "source": "series_bible",
    },
    {
        "episode_id": None,
        "character_id": None,
        "fact_text": (
            "ABHIMANYU DEATH SEQUENCE (S4E13): Scored ENTIRELY by a single sarangi. "
            "ZERO percussion. This is non-negotiable and hardcoded in the Music Agent. "
            "Abhimanyu is the most beloved young warrior — he dies alone in the Chakravyuha."
        ),
        "severity": "CRITICAL",
        "reveal_not_before_season": 4,
        "source": "series_bible",
    },

    # ── VFX RULES ────────────────────────────────────────────────────────────
    {
        "episode_id": None,
        "character_id": None,
        "fact_text": (
            "BATTLEFIELD RULE: Never film battle as heroic. Shoot as agriculture — "
            "repetitive, exhausting, productive of death. The audience must NOT know "
            "which side they are watching in the first battle sequence."
        ),
        "severity": "WARNING",
        "source": "series_bible",
    },
    {
        "episode_id": None,
        "character_id": None,
        "fact_text": (
            "NIGHT SCENE RULE: Only fire and oil lamp as light sources in all INT/NIGHT scenes. "
            "No 'film night' bright fills. Characters' faces should be half-known. "
            "Hardcoded in cinematic_prompt_builder.py."
        ),
        "severity": "WARNING",
        "source": "series_bible",
    },
]


def seed_continuity():
    with get_db() as db:
        count = 0
        for fact in PROTECTED_FACTS:
            existing = db.query(ContinuityLog).filter_by(
                fact_text=fact["fact_text"]
            ).first()
            if existing:
                continue
            log = ContinuityLog(**fact)
            db.add(log)
            count += 1
        logger.success(f"Seeded {count} protected facts into continuity_log.")


if __name__ == "__main__":
    seed_continuity()
