"""
Crown of Kaliyug — Episodes Seeder
Phase 0 · A-00 · database/seed_episodes.py
Source: Series Bible v1.0 — Part Six: Seven-Season Story Architecture
"""
from database.db import get_db
from database.models import Season, Episode
from loguru import logger
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SEASONS = [
    {"id": 1, "title": "The Weight of Crowns",    "episode_count": 10, "parvas_covered": "Adi + Sabha",              "tone_reference": "Succession meets The Crown",              "thematic_id": "Succession, Betrayal, The Fall",             "status": "in_production"},
    {"id": 2, "title": "The Long Exile",          "episode_count": 8,  "parvas_covered": "Vana + Virata",            "tone_reference": "The Revenant meets Downton Abbey",        "thematic_id": "Survival, Disguise, Identity",               "status": "planned"},
    {"id": 3, "title": "The Art of Peace",        "episode_count": 8,  "parvas_covered": "Udyoga",                   "tone_reference": "The Spy Who Came in from the Cold",       "thematic_id": "Diplomacy, Espionage, Inevitability",         "status": "planned"},
    {"id": 4, "title": "Kurukshetra: The War",    "episode_count": 10, "parvas_covered": "Bhishma + Drona + Karna",  "tone_reference": "Dunkirk meets Apocalypse Now",            "thematic_id": "The War — Honor to Darkness",                 "status": "planned"},
    {"id": 5, "title": "Kurukshetra: The Dark",   "episode_count": 10, "parvas_covered": "Shalya + Sauptika",        "tone_reference": "Apocalypse Now (descent)",                "thematic_id": "Rules Break, Darkness Wins, Cost of Survival","status": "planned"},
    {"id": 6, "title": "The Aftermath",           "episode_count": 8,  "parvas_covered": "Stri + Shanti + Anushasana","tone_reference": "The Remains of the Day",                 "thematic_id": "The Cost of Winning",                         "status": "planned"},
    {"id": 7, "title": "The Long Road Home",      "episode_count": 6,  "parvas_covered": "Mausala + Mahaprasthanika + Svargarohan", "tone_reference": "All Quiet on the Western Front", "thematic_id": "The Final Journey, What Dharma Means",      "status": "planned"},
]

EPISODES = [
    # ── SEASON 1 ──────────────────────────────────────────────────────────────
    {
        "id": "S1E01", "season_id": 1, "episode_number": 1,
        "title_english": "The Weight of Crowns", "title_hindi": "Mukut Ka Bojh",
        "synopsis": "The Pandavas and Kauravas return from Gurukul. The graduation tournament of Hastinapur. Karna walks in from nowhere and challenges Arjuna. Duryodhana makes him King of Anga. The seeds of all hatred are planted in one afternoon.",
        "key_events": ["Tournament of Hastinapur", "Karna's entrance and challenge", "Duryodhana crowns Karna King of Anga", "Kunti recognises Karna — says nothing", "Shakuni and Duryodhana — first dice lesson"],
        "parvas_covered": "Adi Parva", "runtime_target": 70, "status": "in_production",
    },
    {
        "id": "S1E02", "season_id": 1, "episode_number": 2,
        "title_english": "The House of Lac", "title_hindi": "Laksha Graha",
        "synopsis": "Vidura warns Yudhishthira of the Lakshagraha plot. The Pandavas escape the burning house — everyone believes them dead. Kunti tells them: say nothing. Survive first, mourn later.",
        "key_events": ["Vidura's warning to Yudhishthira", "Lakshagraha — the burning house", "Pandavas escape through tunnel", "World believes Pandavas dead", "Duryodhana's moment of relief and doubt"],
        "parvas_covered": "Adi Parva", "runtime_target": 55, "status": "planned",
    },
    {
        "id": "S1E03", "season_id": 1, "episode_number": 3,
        "title_english": "The Fire Princess", "title_hindi": "Agni Ki Putri",
        "synopsis": "The Panchala swayamvara. The impossible bow. Arjuna in disguise wins Draupadi. Five brothers, one wife — and the political earthquake this creates.",
        "key_events": ["Swayamvara of Panchala", "Arjuna shoots the fish in disguise", "Draupadi's choice", "Five brothers — one wife announced", "Drupada's political calculation"],
        "parvas_covered": "Adi Parva", "runtime_target": 58, "status": "planned",
    },
    {
        "id": "S1E04", "season_id": 1, "episode_number": 4,
        "title_english": "The Return", "title_hindi": "Wapsi",
        "synopsis": "The Pandavas emerge from 'death.' Dhritarashtra must acknowledge them. Bhishma brokers the kingdom's division: Indraprastha for the Pandavas. Shakuni watches and smiles. First appearance of the Rakshasa forest kingdoms.",
        "key_events": ["Pandavas revealed alive", "Bhishma brokers Indraprastha division", "Shakuni's quiet satisfaction", "Bhima meets Hidimbi — Rakshasa alliance begins"],
        "parvas_covered": "Adi Parva", "runtime_target": 55, "status": "planned",
    },
    {
        "id": "S1E05", "season_id": 1, "episode_number": 5,
        "title_english": "The Building of Heaven", "title_hindi": "Swarg Ka Nirman",
        "synopsis": "The Pandavas build Indraprastha with Maya Danava's architectural magic. The most beautiful city ever made. Duryodhana visits, is humiliated by a false floor, and Draupadi laughs. This is the point of no return.",
        "key_events": ["Maya Danava builds Indraprastha", "Duryodhana's visit", "The false floor humiliation", "Draupadi laughs — Duryodhana's rage crystallises", "The friendship between cousins ends here"],
        "parvas_covered": "Sabha Parva", "runtime_target": 55, "status": "planned",
    },
    {
        "id": "S1E06", "season_id": 1, "episode_number": 6,
        "title_english": "Dice", "title_hindi": "Chausar",
        "synopsis": "The invitation to Hastinapur. Yudhishthira cannot refuse. The dice game. Shakuni's weighted throws. Yudhishthira loses everything: his wealth, his kingdom, his brothers, himself. Then Draupadi.",
        "key_events": ["Invitation to Hastinapur dice game", "Yudhishthira accepts — cannot refuse", "Shakuni's weighted dice", "Yudhishthira loses kingdom + brothers", "Yudhishthira stakes Draupadi"],
        "parvas_covered": "Sabha Parva", "runtime_target": 60, "status": "planned",
    },
    {
        "id": "S1E07", "season_id": 1, "episode_number": 7,
        "title_english": "The Hall of Kings", "title_hindi": "Raajsabha",
        "synopsis": "Draupadi is dragged into the assembly hall. Dushasana attempts to disrobe her. Krishna's divine protection. Draupadi's vow. The assembly of kings who say nothing. Season's emotional peak.",
        "key_events": ["Draupadi dragged to assembly", "Dushasana's attempt", "Krishna's protection — divine cloth", "Draupadi's vow — hair unbound until Dushasana's blood", "Bhishma, Drona, Vidura — all watch. None act."],
        "parvas_covered": "Sabha Parva", "runtime_target": 62, "status": "planned",
    },
    {
        "id": "S1E08", "season_id": 1, "episode_number": 8,
        "title_english": "The Second Game", "title_hindi": "Doosra Daanv",
        "synopsis": "Dhritarashtra returns everything. Shakuni demands a second game. The terms: losers go to 13 years of forest exile, the 13th year in disguise. Yudhishthira plays. Loses.",
        "key_events": ["Dhritarashtra briefly returns everything", "Shakuni's second game demand", "13-year exile terms — 13th year in disguise", "Yudhishthira plays again", "Pandavas lose exile terms"],
        "parvas_covered": "Sabha Parva", "runtime_target": 52, "status": "planned",
    },
    {
        "id": "S1E09", "season_id": 1, "episode_number": 9,
        "title_english": "Into the Forest", "title_hindi": "Van Mein",
        "synopsis": "The Pandavas and Draupadi leave Hastinapur. The people of Indraprastha weep. Draupadi walks out with her hair unbound — she will not bind it until she washes it in Dushasana's blood.",
        "key_events": ["Pandavas depart Hastinapur", "People of Indraprastha grieve", "Draupadi's unbound hair — the living vow", "Vidura's last words to Yudhishthira", "Karna watches them leave"],
        "parvas_covered": "Sabha Parva", "runtime_target": 50, "status": "planned",
    },
    {
        "id": "S1E10", "season_id": 1, "episode_number": 10,
        "title_english": "What the Dice Left Behind", "title_hindi": "Jo Chausar Chod Gaya",
        "synopsis": "Season finale. Twin perspectives: the Pandavas settling into forest life with unexpected dignity; and the Kauravas realising the court feels wrong without them. Karna visits Duryodhana at night: 'I hope you know what you've started.'",
        "key_events": ["Pandavas first night in forest", "Kauravas — the empty court", "Karna visits Duryodhana — 'I hope you know what you've started'", "Shakuni alone — smiles", "Kurukshetra theme: first fragmented notes"],
        "parvas_covered": "Sabha Parva", "runtime_target": 58, "status": "planned",
    },

    # ── SEASON 2 ──────────────────────────────────────────────────────────────
    {"id": "S2E01", "season_id": 2, "episode_number": 1, "title_english": "The Forest Years Begin", "title_hindi": "Van Ka Aarambh", "synopsis": "Pandavas settle into forest exile. Bhima vs Kirmira. Draupadi's kidnapping attempt foiled.", "key_events": ["Pandavas in Kamyaka forest", "Bhima vs Kirmira", "First kidnap attempt on Draupadi"], "parvas_covered": "Vana Parva", "runtime_target": 52, "status": "planned"},
    {"id": "S2E02", "season_id": 2, "episode_number": 2, "title_english": "The Yaksha's Questions", "title_hindi": "Yaksha Prashna", "synopsis": "Yudhishthira vs the Yaksha — television's greatest philosophical dialogue. The riddle sequence that defines dharma for the entire series.", "key_events": ["Yaksha takes brothers one by one", "Yudhishthira faces the Yaksha", "The philosophical riddle sequence", "Yudhishthira answers — brothers restored", "Dharma defined and immediately complicated"], "parvas_covered": "Vana Parva", "runtime_target": 55, "status": "planned"},
    {"id": "S2E03", "season_id": 2, "episode_number": 3, "title_english": "Arjuna's Ascent", "title_hindi": "Arjun Ki Tapasya", "synopsis": "Arjuna leaves for divine training. Learns celestial weapons from the gods.", "key_events": ["Arjuna departs for divine training", "Indra tests Arjuna", "Celestial weapons learned", "Arjuna returns fundamentally changed"], "parvas_covered": "Vana Parva", "runtime_target": 55, "status": "planned"},
    {"id": "S2E04", "season_id": 2, "episode_number": 4, "title_english": "The Greatest Archer Returns", "title_hindi": "Mahaan Dhanurdhar Ki Wapsi", "synopsis": "Arjuna returns with divine weapons. Performs the greatest archery feat ever seen. The Pandavas have a weapon advantage for the first time.", "key_events": ["Arjuna returns", "Divine weapons displayed", "Brothers reunited", "Karna hears — begins training harder"], "parvas_covered": "Vana Parva", "runtime_target": 52, "status": "planned"},
    {"id": "S2E05", "season_id": 2, "episode_number": 5, "title_english": "Disguise Year Begins", "title_hindi": "Agyatvas", "synopsis": "The 13th year. Each Pandava takes a disguise at King Virata's court. Draupadi as maid. Arjuna as dance teacher. Comedy and unbearable tension simultaneously.", "key_events": ["Pandavas enter Virata's court in disguise", "Yudhishthira as dice player", "Bhima as cook", "Arjuna as dance teacher", "Draupadi as Sairandhri"], "parvas_covered": "Virata Parva", "runtime_target": 58, "status": "planned"},
    {"id": "S2E06", "season_id": 2, "episode_number": 6, "title_english": "Keechaka", "title_hindi": "Keechak", "synopsis": "Keechaka harasses Draupadi. Bhima kills him in the dead of night. The disguise strains.", "key_events": ["Keechaka's harassment of Draupadi", "Draupadi approaches Bhima", "Bhima kills Keechaka", "Disguise nearly broken"], "parvas_covered": "Virata Parva", "runtime_target": 52, "status": "planned"},
    {"id": "S2E07", "season_id": 2, "episode_number": 7, "title_english": "The Matsya War", "title_hindi": "Matsya Yuddha", "synopsis": "Kauravas attack Virata's kingdom. Arjuna must fight without revealing himself. The disguise is almost broken.", "key_events": ["Kaurava attack on Matsya", "Arjuna fights as Brihannala", "Disguise nearly broken", "Arjuna uses divine weapons reluctantly", "13 years complete — the war is now inevitable"], "parvas_covered": "Virata Parva", "runtime_target": 55, "status": "planned"},
    {"id": "S2E08", "season_id": 2, "episode_number": 8, "title_english": "The Exile Ends", "title_hindi": "Agyatvas Ka Ant", "synopsis": "Exile complete. The throne must now be returned — or war is the only answer. Pandavas revealed. Duryodhana will not give back a needle's point of land.", "key_events": ["Pandavas reveal themselves", "Exile formally complete", "Demand for Indraprastha return", "Duryodhana refuses — not a needle's point of land", "Both sides begin assembling armies"], "parvas_covered": "Virata Parva", "runtime_target": 55, "status": "planned"},

    # ── SEASON 3 ──────────────────────────────────────────────────────────────
    {"id": "S3E01", "season_id": 3, "episode_number": 1, "title_english": "The Peace Mission", "title_hindi": "Shanti Prayas", "synopsis": "Krishna goes to Hastinapur as Pandava ambassador. Last chance for peace. Privately reveals to Karna that he is the Pandavas' eldest brother. Offers him the throne. Karna refuses.", "key_events": ["Krishna's peace mission to Hastinapur", "CRITICAL: Krishna reveals Karna's true identity to Karna privately", "Karna refuses the throne — loyalty to Duryodhana", "Duryodhana refuses all terms"], "parvas_covered": "Udyoga Parva", "runtime_target": 62, "status": "planned"},
    {"id": "S3E02", "season_id": 3, "episode_number": 2, "title_english": "The River", "title_hindi": "Nadi Kinare", "synopsis": "Kunti meets Karna by the river. The most devastating mother-son scene in television history. She asks for his divine armor. He gives it. She promises he will always have five sons.", "key_events": ["CRITICAL: Kunti meets Karna at the river", "CRITICAL: Truth of parentage revealed to Karna by Kunti", "CRITICAL: Karna gives his divine armor to Kunti", "Kunti's promise — he will always have five sons", "Karna asks only to die in single combat with Arjuna"], "parvas_covered": "Udyoga Parva", "runtime_target": 55, "status": "planned"},
    {"id": "S3E03", "season_id": 3, "episode_number": 3, "title_english": "Sanjaya's Mission", "title_hindi": "Sanjay Ka Sandesh", "synopsis": "Sanjaya addresses the Kuru court with the final terms. Dhritarashtra weeps. He cannot stop this. He never could.", "key_events": ["Sanjaya's address to Kuru court", "Dhritarashtra weeps — cannot stop the war", "Vidura's last attempt at reason", "All diplomatic options exhausted"], "parvas_covered": "Udyoga Parva", "runtime_target": 52, "status": "planned"},
    {"id": "S3E04", "season_id": 3, "episode_number": 4, "title_english": "The Armies Assemble", "title_hindi": "Sena Ka Sanghatan", "synopsis": "Both armies assemble at Kurukshetra. 18 days. 4 million warriors. Each side chooses their commander. Alliances confirmed. The night before war.", "key_events": ["Armies assemble at Kurukshetra", "Bhishma appointed Kaurava commander", "Dhrishtadyumna appointed Pandava commander", "Karna forbidden from fighting under Bhishma — his own oath"], "parvas_covered": "Udyoga Parva", "runtime_target": 58, "status": "planned"},
    {"id": "S3E05", "season_id": 3, "episode_number": 5, "title_english": "The Night Before", "title_hindi": "Yuddh Ki Raat", "synopsis": "What each character does alone in the darkness before Kurukshetra. No battle. Pure character. The last night the world is whole.", "key_events": ["Krishna prepares", "Arjuna cannot sleep", "Karna sits alone — knows what is coming", "Duryodhana visits his father", "Draupadi's unbound hair — still waiting", "Bhishma looks at the stars"], "parvas_covered": "Udyoga Parva", "runtime_target": 55, "status": "planned"},
    {"id": "S3E06", "season_id": 3, "episode_number": 6, "title_english": "Conches at Dawn", "title_hindi": "Shankh Naad", "synopsis": "First light at Kurukshetra. Conches blow. Arjuna sees his family on both sides. Drops his bow. The Bhagavad Gita begins.", "key_events": ["Kurukshetra at dawn", "Armies face each other — 4 million warriors", "Arjuna sees family on both sides", "Arjuna drops his bow — Vishada Yoga", "Krishna begins the Gita"], "parvas_covered": "Bhishma Parva", "runtime_target": 60, "status": "planned"},
    {"id": "S3E07", "season_id": 3, "episode_number": 7, "title_english": "The Gita", "title_hindi": "Geeta", "synopsis": "Krishna delivers the Bhagavad Gita. The most dramatic philosophical monologue in television history. A god talking a warrior back from the edge of collapse.", "key_events": ["Full Bhagavad Gita delivered", "Arjuna's crisis of dharma", "Krishna's cosmic perspective", "Arjuna picks up his bow", "War begins"], "parvas_covered": "Bhishma Parva", "runtime_target": 65, "status": "planned"},
    {"id": "S3E08", "season_id": 3, "episode_number": 8, "title_english": "First Blood", "title_hindi": "Pehla Khoon", "synopsis": "Day 1 of the war. The procedural horror of industrialised violence. Both sides fight with honor — for now. The audience must not know which side they are watching.", "key_events": ["Day 1 of Kurukshetra", "Initial formations", "First deaths on both sides", "Bhishma's command — devastating", "Karna watches from the sidelines — his oath prevents him fighting yet"], "parvas_covered": "Bhishma Parva", "runtime_target": 60, "status": "planned"},

    # ── SEASON 4 ──────────────────────────────────────────────────────────────
    {"id": "S4E01", "season_id": 4, "episode_number": 1, "title_english": "Days of Slaughter", "title_hindi": "Sangharsh Ke Din", "synopsis": "Days 2–8 of the war. The rules hold. Bhishma's command is impenetrable. Pandavas cannot break through.", "key_events": ["Days 2–8 of war", "Bhishma's Pitamaha formation", "Pandavas losing ground", "Arjuna reluctant to kill Bhishma"], "parvas_covered": "Bhishma Parva", "runtime_target": 58, "status": "planned"},
    {"id": "S4E02", "season_id": 4, "episode_number": 2, "title_english": "Shikhandi", "title_hindi": "Shikhandi", "synopsis": "Days 9–10. The plan to use Shikhandi. Bhishma falls on Day 10 — a god-king pinned to earth by arrows. Both armies pause.", "key_events": ["Day 9–10", "Shikhandi deployed against Bhishma", "CRITICAL: Bhishma falls — bed of arrows", "Both armies pause — come to pay respects", "Bhishma asks for the right moment to die"], "parvas_covered": "Bhishma Parva", "runtime_target": 62, "status": "planned"},
    {"id": "S4E03", "season_id": 4, "episode_number": 3, "title_english": "Drona Commands", "title_hindi": "Drona Ka Neta", "synopsis": "Days 11–12. Drona takes command. He taught both sides. He will eventually be killed by a lie.", "key_events": ["Drona appointed Kaurava commander", "Days 11–12", "Drona's devastating strategy", "Yudhishthira nearly captured"], "parvas_covered": "Drona Parva", "runtime_target": 55, "status": "planned"},
    {"id": "S4E04", "season_id": 4, "episode_number": 4, "title_english": "The Chakravyuha", "title_hindi": "Chakravyuha", "synopsis": "Day 13. Drona forms the Chakravyuha — the wheel formation only Arjuna and Krishna know how to exit. Abhimanyu knows how to enter but not exit. He goes in alone.", "key_events": ["Day 13 — Chakravyuha formed", "Arjuna drawn away from battlefield", "Abhimanyu enters alone", "Six commanders surround him — against all rules", "CRITICAL: Abhimanyu dies fighting six commanders simultaneously — single sarangi score only"], "parvas_covered": "Drona Parva", "runtime_target": 65, "status": "planned"},
    {"id": "S4E05", "season_id": 4, "episode_number": 5, "title_english": "Arjuna's Vow", "title_hindi": "Arjun Ki Pratigya", "synopsis": "Arjuna learns Abhimanyu is dead. Swears to kill Jayadratha by sunset the next day or die himself. Krishna moves the sun.", "key_events": ["Arjuna learns Abhimanyu's death", "Arjuna's vow — Jayadratha dead by sunset", "Day 14 — Arjuna's rampage", "Krishna moves the sun to trick Jayadratha", "Jayadratha killed"], "parvas_covered": "Drona Parva", "runtime_target": 60, "status": "planned"},
    {"id": "S4E06", "season_id": 4, "episode_number": 6, "title_english": "The Night Battle", "title_hindi": "Raat Ka Yuddha", "synopsis": "Day 14 bleeds into a night battle — the first in the war. The rules of engagement have already been breaking.", "key_events": ["First night battle of the war", "Rules breaking down", "Karna finally enters the battle", "Drona's prowess becomes terrifying"], "parvas_covered": "Drona Parva", "runtime_target": 58, "status": "planned"},
    {"id": "S4E07", "season_id": 4, "episode_number": 7, "title_english": "The Lie That Killed Drona", "title_hindi": "Jhooth Jo Drona Ko Le Gaya", "synopsis": "Day 15. Ashwatthama is rumoured dead. Drona won't believe it unless Yudhishthira confirms it. Yudhishthira must choose between his son's life and his unbroken record of truth.", "key_events": ["Day 15 — Ashwatthama the elephant killed, not the man", "The lie planned around Yudhishthira", "Yudhishthira's truth breaks — he confirms Ashwatthama dead", "Drona lays down his weapons", "Dhrishtadyumna kills Drona — against all rules"], "parvas_covered": "Drona Parva", "runtime_target": 62, "status": "planned"},
    {"id": "S4E08", "season_id": 4, "episode_number": 8, "title_english": "Karna Commands", "title_hindi": "Karna Ka Neta", "synopsis": "Day 16. Karna becomes Kaurava commander. The moment everyone has been building toward. He fights Arjuna. His chariot wheel sinks.", "key_events": ["Day 16 — Karna appointed commander", "Karna vs Arjuna — the showdown", "Karna's chariot wheel sinks into earth", "CRITICAL: Karna steps down unarmed to free it", "Krishna orders Arjuna to shoot — Arjuna hesitates, then fires", "Karna dies. Both sides weep."], "parvas_covered": "Karna Parva", "runtime_target": 68, "status": "planned"},
    {"id": "S4E09", "season_id": 4, "episode_number": 9, "title_english": "Shalya's Day", "title_hindi": "Shalya Ka Din", "synopsis": "Day 17–18. Shalya commands the last Kaurava forces. Yudhishthira kills him. The Kauravas are nearly finished.", "key_events": ["Day 17 — Shalya commands", "Yudhishthira kills Shalya", "Day 18 begins", "Kauravas reduced to Duryodhana"], "parvas_covered": "Shalya Parva", "runtime_target": 55, "status": "planned"},
    {"id": "S4E10", "season_id": 4, "episode_number": 10, "title_english": "The Last Kaurava", "title_hindi": "Antim Kaurava", "synopsis": "Day 18. Duryodhana — the last Kaurava — fights Bhima with a mace. He fights better than he has ever fought. He dies with his thighs broken (against rules) and his dignity intact.", "key_events": ["Day 18 — Duryodhana alone", "Duryodhana vs Bhima — mace fight", "Bhima strikes the thighs — against rules of mace combat", "Duryodhana falls — dying, not defeated in spirit", "Ashwatthama vows revenge", "The war is over. 18 days. 4 million dead."], "parvas_covered": "Shalya Parva", "runtime_target": 65, "status": "planned"},

    # ── SEASON 5 ──────────────────────────────────────────────────────────────
    {"id": "S5E01", "season_id": 5, "episode_number": 1, "title_english": "The Night of Ashwatthama", "title_hindi": "Ashwatthama Ki Raat", "synopsis": "Ashwatthama enters the Pandava camp at night. Kills Draupadi's five sons in their sleep, mistaking them for the Pandavas.", "key_events": ["Ashwatthama's revenge attack at night", "Draupadi's five sons killed in their sleep", "CRITICAL: Do not reveal before Season 5", "Draupadi's grief — the price of war"], "parvas_covered": "Sauptika Parva", "runtime_target": 60, "status": "planned"},
    {"id": "S5E02", "season_id": 5, "episode_number": 2, "title_english": "Ashwatthama Cursed", "title_hindi": "Ashwatthama Ka Shraap", "synopsis": "Arjuna captures Ashwatthama. Draupadi chooses his life over vengeance. Krishna curses Ashwatthama to wander in suffering forever.", "key_events": ["Arjuna pursues Ashwatthama", "Ashwatthama fires Brahmastra at Uttara's womb", "Arjuna's counter", "Draupadi's choice — spare Ashwatthama", "Krishna curses Ashwatthama"], "parvas_covered": "Sauptika Parva", "runtime_target": 55, "status": "planned"},
    {"id": "S5E03", "season_id": 5, "episode_number": 3, "title_english": "Gandhari's Curse", "title_hindi": "Gandhari Ka Shraap", "synopsis": "Gandhari curses Krishna — his entire clan will be destroyed as hers was. Krishna accepts the curse.", "key_events": ["Gandhari confronts Krishna on the battlefield", "Gandhari's curse on Krishna's clan", "Krishna accepts — he knew", "Yudhishthira stands on a field of the dead"], "parvas_covered": "Stri Parva", "runtime_target": 52, "status": "planned"},
    {"id": "S5E04", "season_id": 5, "episode_number": 4, "title_english": "The Women of Kurukshetra", "title_hindi": "Kurukshetra Ki Naariyan", "synopsis": "The women come to collect their dead. Draupadi. Gandhari. Kunti. Three mothers on a field of 18 million bodies.", "key_events": ["Women arrive at Kurukshetra", "Gandhari and Dhritarashtra among the dead", "Kunti reveals Karna to the Pandavas — he was their brother", "Yudhishthira's breakdown", "The cost of winning"], "parvas_covered": "Stri Parva", "runtime_target": 58, "status": "planned"},
    {"id": "S5E05", "season_id": 5, "episode_number": 5, "title_english": "Bhishma's Last Wisdom", "title_hindi": "Bhishma Ka Antim Gyan", "synopsis": "Bhishma still lies on his bed of arrows — waiting for the right astronomical moment. He dispenses all the wisdom he should have used 50 years ago.", "key_events": ["Pandavas visit Bhishma on arrow bed", "Bhishma's Shanti Parva — vast wisdom delivered", "Anushasana Parva — laws of dharma", "The moment comes — Bhishma dies"], "parvas_covered": "Shanti Parva + Anushasana Parva", "runtime_target": 60, "status": "planned"},
    {"id": "S5E06", "season_id": 5, "episode_number": 6, "title_english": "The Crown", "title_hindi": "Rajyabhishek", "synopsis": "Yudhishthira is crowned emperor of Bharatavarsha. It is the most hollow victory in history.", "key_events": ["Yudhishthira's coronation", "Indraprastha restored", "The hollow victory", "Yudhishthira considers renunciation"], "parvas_covered": "Shanti Parva", "runtime_target": 52, "status": "planned"},
    {"id": "S5E07", "season_id": 5, "episode_number": 7, "title_english": "Dhritarashtra's Exile", "title_hindi": "Dhritarashtra Ka Vanvas", "synopsis": "Dhritarashtra, Gandhari, and Kunti leave for the forest. The old generation goes into exile. Kunti chooses to accompany them — and dies in a forest fire.", "key_events": ["Dhritarashtra and Gandhari depart for forest", "Kunti chooses to accompany them", "Kunti, Gandhari, Dhritarashtra — all die in forest fire", "The old generation is gone"], "parvas_covered": "Ashramavasika Parva", "runtime_target": 55, "status": "planned"},
    {"id": "S5E08", "season_id": 5, "episode_number": 8, "title_english": "The Yadava War", "title_hindi": "Yaduvansh Ka Naash", "synopsis": "Krishna's own clan, the Yadavas, destroy themselves fighting each other. Gandhari's curse begins to manifest. Krishna watches.", "key_events": ["Yadavas fight each other at Prabhasa", "Balarama's death", "Krishna's grief watching his people destroy themselves", "The flute goes silent for the first time"], "parvas_covered": "Mausala Parva", "runtime_target": 58, "status": "planned"},
    {"id": "S5E09", "season_id": 5, "episode_number": 9, "title_english": "Krishna", "title_hindi": "Krishna", "synopsis": "Krishna is killed by a hunter's arrow — mistaken for a deer. The god dies as he lived: simply, without spectacle.", "key_events": ["Krishna resting alone in a forest", "Hunter Jara's arrow — mistaken for a deer", "CRITICAL: Krishna's divine form shown for the first time — as he dies", "Krishna's death is quiet, not spectacular", "The world changes"], "parvas_covered": "Mausala Parva", "runtime_target": 55, "status": "planned"},
    {"id": "S5E10", "season_id": 5, "episode_number": 10, "title_english": "Dwarka", "title_hindi": "Dwarka", "synopsis": "Dwarka sinks into the sea. The defining VFX sequence of the series. The flute is permanently silent.", "key_events": ["CRITICAL: Dwarka sinks into the sea — 18% of total VFX budget", "Arjuna watches Dwarka sink", "The survivors of Dwarka become refugees", "The flute permanently silent"], "parvas_covered": "Mausala Parva", "runtime_target": 62, "status": "planned"},

    # ── SEASON 6 ──────────────────────────────────────────────────────────────
    {"id": "S6E01", "season_id": 6, "episode_number": 1, "title_english": "The Long Reign", "title_hindi": "Lambi Rajneeti", "synopsis": "Yudhishthira has been emperor for 36 years. The question that never stopped asking itself: was it worth it?", "key_events": ["36 years of Yudhishthira's rule", "The hollow empire", "Yudhishthira's growing desire to renounce"], "parvas_covered": "Anushasana Parva", "runtime_target": 52, "status": "planned"},
    {"id": "S6E02", "season_id": 6, "episode_number": 2, "title_english": "The Renunciation", "title_hindi": "Sanyaas", "synopsis": "The Pandavas decide to renounce the throne. Parikshit — Abhimanyu's son — is crowned. They prepare for the final journey.", "key_events": ["Pandavas renounce the empire", "Parikshit crowned", "Draupadi joins the final journey", "They give up all possessions"], "parvas_covered": "Mahaprasthanika Parva", "runtime_target": 52, "status": "planned"},
    {"id": "S6E03", "season_id": 6, "episode_number": 3, "title_english": "The Final Road", "title_hindi": "Antim Raah", "synopsis": "The Pandavas and Draupadi begin the Great Journey. One by one they fall — each for a specific spiritual reason. Draupadi falls first.", "key_events": ["The Great Journey begins — toward the Himalayas", "Draupadi falls first — loved Arjuna more than dharma demanded", "Nakula falls — too proud of his beauty", "Sahadeva falls — too proud of his wisdom", "Each fall is a judgment"], "parvas_covered": "Mahaprasthanika Parva", "runtime_target": 55, "status": "planned"},
    {"id": "S6E04", "season_id": 6, "episode_number": 4, "title_english": "Brothers Fall", "title_hindi": "Bhai Girate Hain", "synopsis": "Arjuna and Bhima fall. Only Yudhishthira and a dog remain. The dog has been with them since the beginning.", "key_events": ["Arjuna falls — too proud of his archery", "Bhima falls — ate too much, loved life too much", "Only Yudhishthira and the dog remain", "Indra appears — offers chariot to heaven"], "parvas_covered": "Mahaprasthanika Parva", "runtime_target": 55, "status": "planned"},
    {"id": "S6E05", "season_id": 6, "episode_number": 5, "title_english": "The Dog", "title_hindi": "Woh Kutta", "synopsis": "Indra tells Yudhishthira the dog cannot enter heaven. Yudhishthira refuses to go without the dog. The dog reveals himself as Dharma (Yama) — testing his son one final time.", "key_events": ["Indra's chariot arrives for Yudhishthira", "Yudhishthira refuses to abandon the dog", "The dog reveals himself as Yama/Dharma", "The final test passed", "Yudhishthira enters heaven"], "parvas_covered": "Svargarohanika Parva", "runtime_target": 58, "status": "planned"},
    {"id": "S6E06", "season_id": 6, "episode_number": 6, "title_english": "Heaven", "title_hindi": "Swarg", "synopsis": "Series finale. Heaven, where Yudhishthira finds his cousins feasting. Where he finds Karna. Where the question — What is Dharma? — receives its only possible answer: a silence in which the audience supplies their own.", "key_events": ["Yudhishthira in heaven", "Finds the Kauravas there first — tests his equanimity", "Finds his brothers and Draupadi", "Finds Karna — the final recognition", "FINAL SHOT: The question 'What is Dharma?' — silence. No answer given."], "parvas_covered": "Svargarohanika Parva", "runtime_target": 65, "status": "planned"},
]


def seed_seasons():
    with get_db() as db:
        for data in SEASONS:
            if db.query(Season).filter_by(id=data["id"]).first():
                continue
            db.add(Season(**data))
        logger.success(f"Seeded {len(SEASONS)} seasons.")


def seed_episodes():
    with get_db() as db:
        count = 0
        for data in EPISODES:
            if db.query(Episode).filter_by(id=data["id"]).first():
                continue
            db.add(Episode(**data))
            count += 1
        logger.success(f"Seeded {count} episodes across 7 seasons.")


if __name__ == "__main__":
    seed_seasons()
    seed_episodes()