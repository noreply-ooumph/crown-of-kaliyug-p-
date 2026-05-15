"""
Crown of Kaliyug — Character Seeder
Phase 0: Foundation

Seeds all 9 major characters from Series Bible v1.0.
Every field is sourced directly from the actual document.
"""
from database.db import get_db
from database.models import Character
from loguru import logger
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CHARACTERS = [
    {
        "id": "yudhishthira",
        "name": "Yudhishthira",
        "nation_id": "kuruvansa",
        "archetype": "The Just King Who Cannot Win",
        "arc_summary": (
            "From entitled prince to broken gambler to reluctant emperor. "
            "He tells the truth even when lies would save lives. "
            "His dharma destroys everything he loves."
        ),
        "voice_profile_path": "story_bible/characters/yudhishthira.md",
        "hidden_truth": (
            "His rigid virtue is also a form of cowardice — 'righteousness' "
            "lets him avoid the messier choices of leadership."
        ),
        "writing_rules": [
            "Speaks slowly, deliberately. Never raises his voice.",
            "The quieter he gets, the more dangerous the moment.",
            "Says the most by saying the least.",
            "Will never lie — not even to save lives.",
            "Will never refuse a challenge he has accepted. This is his downfall.",
            "Dharma must never be given as a clean answer in his dialogue.",
        ],
        "season_first_appears": 1,
        "season_dies": 7,
        "casting_directive": "North Indian / Dravidian composite. Regal bearing. Precise.",
    },
    {
        "id": "draupadi",
        "name": "Draupadi",
        "nation_id": "panchala",
        "archetype": "The Woman the World Made a Prize",
        "arc_summary": (
            "From princess bred for political alliance, to queen humiliated before "
            "a thousand kings, to the woman whose rage becomes the fire of war. "
            "She is the moral center AND the most dangerous character in the series."
        ),
        "voice_profile_path": "story_bible/characters/draupadi.md",
        "hidden_truth": (
            "She could have stopped the war three times. She chose not to. "
            "She will spend 7 seasons not knowing if she made the right choice."
        ),
        "writing_rules": [
            "ABSOLUTE: Never write her as passive in any scene.",
            "If any scene ends with Draupadi having less agency than when she entered — REWRITE.",
            "Precise and devastating. She never repeats herself.",
            "Addresses powerful men as equals and makes them uncomfortable.",
            "When she is angry, she laughs — a performance that fools everyone until it doesn't.",
            "Cast before any other character — she is the soul of the series.",
        ],
        "season_first_appears": 1,
        "season_dies": 7,
        "casting_directive": (
            "East African or East African-Indian actress, 25-32. Stage-trained. Multilingual. "
            "Her otherness in the Kuru court is structural — she is never 'from here.'"
        ),
    },
    {
        "id": "karna",
        "name": "Karna",
        "nation_id": "anga",
        "archetype": "The Tragic Hero Who Chose the Wrong Side",
        "arc_summary": (
            "The greatest warrior in Bharatavarsha, born to the highest possible parentage, "
            "raised as a charioteer's son. He knows who he is. He is offered the truth. "
            "He refuses it. He will die on the wrong side because loyalty is the only "
            "identity he has left."
        ),
        "voice_profile_path": "story_bible/characters/karna.md",
        "hidden_truth": (
            "He is Kunti's firstborn. The Pandavas' eldest brother. "
            "He will die in battle against his own family, and both sides will weep. "
            "DO NOT reveal before Season 3."
        ),
        "writing_rules": [
            "Warm, generous, self-deprecating about everything EXCEPT his worth as a warrior.",
            "Gives gifts compulsively — it is a trauma response. He was given away as an infant.",
            "Karna must ALWAYS be right about the moral stakes — even when he chooses wrong.",
            "His tragedy is not stupidity — it is clarity about what loyalty costs.",
            "Key line ref for formal speech: precision + courtesy simultaneously.",
            "Avatar MUST show glowing golden divine armor (Surya's kavacha) — grown into skin from birth.",
            "DO NOT reference his true parentage before Season 3, Episode 1.",
        ],
        "season_first_appears": 1,
        "season_dies": 4,
        "episode_dies": "S4E16",
        "casting_directive": (
            "East Asian-South Asian. Bengali or Assamese. 30-38. "
            "Carries physical memory of manual labor. His hands should show it. "
            "Cast alongside Draupadi — together they are the soul of the series."
        ),
    },
    {
        "id": "krishna",
        "name": "Krishna",
        "nation_id": "dwarka",
        "archetype": "The God Who Plays Chess With Mortal Lives",
        "arc_summary": (
            "He knows the outcome. He always has. His arc is about what it costs a god "
            "to love mortals when he cannot prevent their suffering. By Season 6, the "
            "question is whether divinity is an excuse for cruelty."
        ),
        "voice_profile_path": "story_bible/characters/krishna.md",
        "hidden_truth": (
            "He carries the weight of knowing everything that will happen. He cannot change it. "
            "The Bhagavad Gita is not triumphant — it is the speech of a god who has run out "
            "of other options."
        ),
        "writing_rules": [
            "ABSOLUTE HARD RULE: Krishna NEVER lies. He only withholds, redirects, asks questions.",
            "Playful, warm, oblique. He answers questions with questions.",
            "He laughs at moments others find sacred. He is solemn when others celebrate.",
            "Most intelligent being in every room — works hard to make sure nobody notices.",
            "Divinity NEVER shown directly before Season 5. Implied through atmosphere only.",
            "The Bhagavad Gita in Season 5 is NOT triumphant — write it as last resort.",
        ],
        "season_first_appears": 1,
        "season_dies": 7,
        "casting_directive": (
            "South Indian — ideally Tamil or Telugu. 35-45. "
            "The most intelligent face in every scene. "
            "Krishna is from Dwarka: coastal, Dravidian, not North Indian. Historically accurate."
        ),
    },
    {
        "id": "duryodhana",
        "name": "Duryodhana",
        "nation_id": "kuruvansa",
        "archetype": "The Villain Who Is Right About Everything Except What Matters",
        "arc_summary": (
            "He wants the throne he was promised. He is, by most measures, a better "
            "administrator than Yudhishthira. He is loyal to Karna when every social "
            "rule says he shouldn't be. He has one great evil: he cannot share."
        ),
        "voice_profile_path": "story_bible/characters/duryodhana.md",
        "hidden_truth": (
            "He knows the dice game was wrong. He knows Draupadi's humiliation was wrong. "
            "He cannot admit it — admitting it would mean everything he did was meaningless. "
            "He will die in the mud rather than be right about that."
        ),
        "writing_rules": [
            "Audience MUST fall in love with Duryodhana — especially in S1E01 Karna coronation scene.",
            "Loud, generous with allies, magnetic in a crowd. He tells great stories.",
            "Write him as the protagonist of a show about a prince denied his birthright.",
            "He would be the most popular king ever if he could only tolerate rivals existing.",
            "Never caricature — his evil is the evil of a man who cannot share, not cruelty.",
        ],
        "season_first_appears": 1,
        "season_dies": 4,
        "episode_dies": "S4E18",
        "casting_directive": "North Indian / Pashtun composite (via Gandhari). Magnetic. Physically imposing.",
    },
    {
        "id": "bhishma",
        "name": "Bhishma",
        "nation_id": "kuruvansa",
        "archetype": "The Prisoner of His Own Honor",
        "arc_summary": (
            "The greatest warrior alive, sworn to protect whoever sits on the Kuru throne — "
            "even when the throne is occupied by injustice. He dies on a bed of arrows in "
            "Season 4, Day 10 of Kurukshetra, dispensing wisdom he should have used 50 years earlier."
        ),
        "voice_profile_path": "story_bible/characters/bhishma.md",
        "hidden_truth": (
            "He knows the Pandavas are right. He fights against them anyway. "
            "This is the most honest thing in the series: sometimes good people fight "
            "on the wrong side because honor demands it."
        ),
        "writing_rules": [
            "Formal to the point of archaism. Speaks in verse when emotional — [verse_mode] tag.",
            "200 years old by divine grace — every year shows. He is geological.",
            "The kindest person in the series — also responsible for most of its suffering.",
            "Dies on bed of arrows Day 10 Kurukshetra. Both armies pause. Season-level event.",
            "Never write him as a fool — he is a man who has made his choice and lives by it.",
        ],
        "season_first_appears": 1,
        "season_dies": 4,
        "episode_dies": "S4E10",
        "casting_directive": "75+ but physically formidable. Any South Asian ethnicity. Silver-white. Ancient eyes.",
    },
    {
        "id": "shakuni",
        "name": "Shakuni",
        "nation_id": "gandhara",
        "archetype": "The Man Who Burned a Kingdom for Revenge",
        "arc_summary": (
            "He is not cruel because he enjoys cruelty. He is cruel because Kuruvansa "
            "destroyed his family and he has spent 40 years becoming the weapon that "
            "will destroy them back. He genuinely loves Duryodhana — as a tool he shaped with great care."
        ),
        "voice_profile_path": "story_bible/characters/shakuni.md",
        "hidden_truth": (
            "The dice he uses are made from the bones of his father, who died in a "
            "Kuruvansa prison. Every throw is a prayer for vengeance."
        ),
        "writing_rules": [
            "Self-effacing, avuncular, funny. He is the person at every court dinner who makes everyone laugh.",
            "While making them laugh, he catalogues their weaknesses.",
            "Speaks five languages but pretends to speak only two.",
            "His dice are always warm — carved from his father's bones. Always come up the same.",
            "Must visually read as 'foreign' in the Kuru court — Gandhara is not India.",
            "Key line ref: 'You cannot fight virtue. You have to invite it to defeat itself.'",
        ],
        "season_first_appears": 1,
        "season_dies": 4,
        "casting_directive": "Central Asian or Pashtun features. 50-60. The weight of grief carried as wit. Afghan, Pakistani, Tajik.",
    },
    {
        "id": "kunti",
        "name": "Kunti",
        "nation_id": "kuruvansa",
        "archetype": "The Mother Who Cannot Tell the Truth",
        "arc_summary": (
            "She carries a secret that would change the war: her firstborn son, Karna, "
            "fights against her other sons. She goes to Karna by the river in Season 3 "
            "and reveals the truth — and asks for his divine armor. He gives it."
        ),
        "voice_profile_path": "story_bible/characters/kunti.md",
        "hidden_truth": (
            "She met Karna by the river before the war (Season 3) and asked for his divine armor "
            "— the protection grown into his skin from birth. He gave it to her. "
            "She will carry that memory for the rest of her life."
        ),
        "writing_rules": [
            "Composed, regal, devastating when she chooses to be honest.",
            "Has survived the most and shows it the least.",
            "Her love for her sons is absolute — and has cost each of them something.",
            "DO NOT have her reveal Karna's identity to others before Season 3.",
            "The river scene with Karna in Season 3 is the most devastating mother-son scene in television history — write accordingly.",
        ],
        "season_first_appears": 1,
        "season_dies": 6,
        "casting_directive": "South Indian / Dravidian. Composure that reads as power. Originally from Vidarbha.",
    },
    {
        "id": "arjuna",
        "name": "Arjuna",
        "nation_id": "kuruvansa",
        "archetype": "The Hero Who Breaks",
        "arc_summary": (
            "The most celebrated warrior alive. Peerless in combat, beloved by gods and mortals, "
            "and completely unprepared for the moral dimensions of greatness. "
            "His breakdown at Kurukshetra — when he sees his family on both sides — "
            "is the hinge of the entire story."
        ),
        "voice_profile_path": "story_bible/characters/arjuna.md",
        "hidden_truth": (
            "On the last night before Kurukshetra, he will ask Krishna to drive him close "
            "enough to see the faces of the men he must kill. He recognizes every one of them."
        ),
        "writing_rules": [
            "Charming and a little vain — with a self-awareness that prevents it from being insufferable.",
            "Used to being the best — the series is about what happens when that stops being enough.",
            "His relationship with Krishna is the most intimate in the series.",
            "Kurukshetra breakdown is the hinge — build every S1-S3 scene toward it.",
            "After Karna's challenge in S1E01 — something shifts in him. He does not miss again.",
        ],
        "season_first_appears": 1,
        "season_dies": 7,
        "casting_directive": "North Indian / South Indian composite. Charming. Bow is his natural extension.",
    },
]


def seed_characters():
    with get_db() as db:
        for char_data in CHARACTERS:
            existing = db.query(Character).filter_by(id=char_data["id"]).first()
            if existing:
                logger.info(f"Character '{char_data['id']}' already exists — skipping.")
                continue
            char = Character(**char_data)
            db.add(char)
            logger.info(f"Seeded character: {char_data['name']}")
        logger.success(f"All {len(CHARACTERS)} characters seeded.")


if __name__ == "__main__":
    seed_characters()