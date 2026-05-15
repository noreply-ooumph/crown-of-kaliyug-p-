"""
Crown of Kaliyug — Nations Seeder
Phase 0 · A-00 · database/seed_nations.py
Source: Series Bible v1.0 — Part Four: World Architecture
"""
from database.db import get_db
from database.models import Nation
from loguru import logger
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

NATIONS = [
    {
        "id": "kuruvansa",
        "name": "Kuruvansa",
        "got_analog": "King's Landing",
        "capital": "Hastinapur — city of elephants, built where three rivers meet",
        "ethnicity_ref": "Diverse South Asian — North Indian, Dravidian, Bengali composite court culture",
        "aesthetics": (
            "Hampi/Vijayanagara ruins + Mughal court grandeur. "
            "Iron grey stone towers. River-facing ghats. Enormous elephant stables. "
            "The dominant empire — internally fractured by Pandava-Kaurava succession crisis."
        ),
        "color_palette": "grey, deep blue, gold",
        "music_theme": "kuru_court_theme",
        "notes": "GoT analog: King's Landing. Every faction wants to control it.",
    },
    {
        "id": "panchala",
        "name": "Panchala",
        "got_analog": "Highgarden — wealth, culture, pride",
        "capital": "Kampilya",
        "ethnicity_ref": "East African + South Indian composite",
        "aesthetics": (
            "Dark volcanic stone architecture. Vibrant orange and purple textiles. "
            "Warriors who fight with rhythm — their army advances to drumbeats. "
            "Draupadi's court is the only one in Bharatavarsha where women speak freely in political councils."
        ),
        "color_palette": "orange, deep purple, volcanic black",
        "music_theme": "panchala_theme",
        "notes": "King Drupada rules with pride and a burning grudge against Dronacharya.",
    },
    {
        "id": "dwarka",
        "name": "Dwarka",
        "got_analog": "Braavos — cosmopolitan island republic",
        "capital": "Dwarka — island city reachable only by sea",
        "ethnicity_ref": "Coastal Dravidian + Southeast Asian (Javanese, Balinese) composite",
        "aesthetics": (
            "White stone on blue sea. No defensive walls — it needs none. "
            "40% of interiors on water platforms — every interior has a water reflection. "
            "Krishna's flute is the sound of Dwarka itself. "
            "Markets where traders from every nation mingle."
        ),
        "color_palette": "white, ocean blue, gold",
        "music_theme": "dwarka_theme",
        "notes": (
            "The world's first republic. Krishna rules as First Among Equals. "
            "When the flute goes silent — something terrible is coming. "
            "Dwarka sinks into the sea in Season 7."
        ),
    },
    {
        "id": "gandhara",
        "name": "Gandhara",
        "got_analog": "The North — fierce, proud, conquered",
        "capital": "Taxila — carved into mountainsides",
        "ethnicity_ref": "Central Asian + Pashtun + Tibetan composite",
        "aesthetics": (
            "Architecture carved into mountainsides. Heavy wool and leather clothing. "
            "Gold jewelry that tells genealogy. "
            "Kuruvansa subjugated through political marriage — Gandhari married to Dhritarashtra. "
            "Shakuni carries weighted dice carved from his father's bones."
        ),
        "color_palette": "brown, cream, deep red",
        "music_theme": "gandhara_theme",
        "notes": (
            "The architecture says: we survived here, we were not invited. "
            "Shakuni has spent 40 years becoming the weapon that will destroy Kuruvansa."
        ),
    },
    {
        "id": "anga",
        "name": "Anga",
        "got_analog": "A vassal kingdom — overlooked, underestimated",
        "capital": "Champa — river delta city",
        "ethnicity_ref": "East Asian (Bengali + Assamese + traces of Chinese trade influence)",
        "aesthetics": (
            "River delta culture — everything moves by water. "
            "Bronze and copper metalwork of extraordinary quality. "
            "The people of Anga make the finest bows in Bharatavarsha. "
            "Karna is installed as king — the first low-born man to ever wear a crown."
        ),
        "color_palette": "bronze, copper, river blue",
        "music_theme": "anga_theme",
        "notes": "The people of Anga see themselves in Karna: overlooked, underestimated, capable of greatness if given the chance.",
    },
    {
        "id": "magadha",
        "name": "Magadha",
        "got_analog": "The Golden Empire — vast, old, certain of its superiority",
        "capital": "Rajgriha",
        "ethnicity_ref": "East Asian + Chinese + Tibetan Buddhist composite",
        "aesthetics": (
            "The largest standing army in Bharatavarsha. "
            "Architecture of red lacquer and dark stone. "
            "Their rulers wear no crowns — only war helmets, even in court. "
            "Everything in Magadha is weaponized, including diplomacy."
        ),
        "color_palette": "red lacquer, dark stone, iron grey",
        "music_theme": "magadha_theme",
        "notes": "Jarasandha has attempted to conquer Dwarka seventeen times and failed. Alliance with Kauravas is purely transactional.",
    },
    {
        "id": "naga_territories",
        "name": "Naga Territories",
        "got_analog": "The underground — ancient beyond measure",
        "capital": "Underground city-systems beneath forests and rivers",
        "ethnicity_ref": "Pacific Islander + Indigenous South American + Aboriginal Australian composite",
        "aesthetics": (
            "Bioluminescent architecture. Serpent motifs not as monsters but as wisdom symbols. "
            "Ancient beyond measure — custodians of knowledge surface civilizations have lost. "
            "The Nagas know the truth of every nation's founding — and they trade in secrets."
        ),
        "color_palette": "bioluminescent blue-green, deep cavern black",
        "music_theme": "naga_theme",
        "notes": (
            "Arjuna's marriage to Uloopi (a Naga princess) gives the Pandavas their only "
            "intelligence network that operates across all nations simultaneously. "
            "First appears Season 1 Episode 4."
        ),
    },
]


def seed_nations():
    with get_db() as db:
        count = 0
        for data in NATIONS:
            existing = db.query(Nation).filter_by(id=data["id"]).first()
            if existing:
                logger.info(f"Nation '{data['id']}' already exists — skipping.")
                continue
            db.add(Nation(**data))
            count += 1
            logger.info(f"Seeded nation: {data['name']}")
        logger.success(f"Seeded {count} nations.")


if __name__ == "__main__":
    seed_nations()