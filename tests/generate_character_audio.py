"""
Crown of Kaliyug — Character Audio Generator
tests/generate_character_audio.py

Generates full-length Hindi TTS audio samples for all 9 characters
using Edge TTS with emotion-mapped rate/pitch parameters.

Each character gets 2-3 lines covering their defining moments.

Run from project root:
    python tests/generate_character_audio.py

Output: output/audio/character_samples/<character>/<slot_id>.mp3
"""

import asyncio
import os
import sys
import time

# ── Make sure project root is on path ─────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

OUTPUT_DIR = "output/audio/character_samples"

# ──────────────────────────────────────────────────────────────────
# CHARACTER VOICE MAP  (from config/voice_profiles.yaml)
# ──────────────────────────────────────────────────────────────────
VOICES = {
    "arjuna":       "hi-IN-MadhurNeural",
    "karna":        "hi-IN-MadhurNeural",
    "duryodhana":   "hi-IN-MadhurNeural",
    "krishna":      "hi-IN-MadhurNeural",
    "draupadi":     "hi-IN-SwaraNeural",
    "bhishma":      "hi-IN-MadhurNeural",
    "kunti":        "hi-IN-SwaraNeural",
    "shakuni":      "hi-IN-MadhurNeural",
    "yudhishthira": "hi-IN-MadhurNeural",
}

# ──────────────────────────────────────────────────────────────────
# EMOTION TAG → EDGE TTS PARAMS  (from emotion_mapper.py)
# ──────────────────────────────────────────────────────────────────
EMOTION_PARAMS = {
    "[charming]":       {"rate": "+5%",  "pitch": "+2Hz",  "volume": "+5%"},
    "[focused]":        {"rate": "-5%",  "pitch": "+0Hz",  "volume": "+0%"},
    "[grief]":          {"rate": "-20%", "pitch": "-5Hz",  "volume": "-15%"},
    "[formal]":         {"rate": "-10%", "pitch": "+0Hz",  "volume": "+0%"},
    "[warm]":           {"rate": "-5%",  "pitch": "+0Hz",  "volume": "+0%"},
    "[warm_oblique]":   {"rate": "-5%",  "pitch": "+0Hz",  "volume": "+0%"},
    "[generous]":       {"rate": "+0%",  "pitch": "+0Hz",  "volume": "+5%"},
    "[rage]":           {"rate": "+25%", "pitch": "+10Hz", "volume": "+50%"},
    "[private]":        {"rate": "-10%", "pitch": "-2Hz",  "volume": "-10%"},
    "[avuncular]":      {"rate": "-5%",  "pitch": "+0Hz",  "volume": "+0%"},
    "[composed]":       {"rate": "-10%", "pitch": "+0Hz",  "volume": "+0%"},
    "[grief_hidden]":   {"rate": "-15%", "pitch": "-3Hz",  "volume": "-10%"},
    "[verse_mode]":     {"rate": "-20%", "pitch": "-2Hz",  "volume": "+0%"},
    "[battle]":         {"rate": "+5%",  "pitch": "+0Hz",  "volume": "+10%"},
    "[precise]":        {"rate": "-5%",  "pitch": "+0Hz",  "volume": "+0%"},
    "[quiet]":          {"rate": "-20%", "pitch": "-3Hz",  "volume": "-25%"},
    "[solemn]":         {"rate": "-15%", "pitch": "-3Hz",  "volume": "-5%"},
    "[dying]":          {"rate": "-30%", "pitch": "-8Hz",  "volume": "-30%"},
}

def get_params(emotion_tag: str) -> dict:
    return EMOTION_PARAMS.get(emotion_tag, {"rate": "0%", "pitch": "0Hz", "volume": "0%"})


# ──────────────────────────────────────────────────────────────────
# DIALOGUE LINES  — Real character lines, longer samples
# ──────────────────────────────────────────────────────────────────
DIALOGUE_LINES = [

    # ── ARJUNA ────────────────────────────────────────────────────
    {
        "slot_id":    "arjuna_charming_01",
        "character":  "arjuna",
        "emotion_tag": "[charming]",
        "text": (
            "Acharya Drona ne mujhe sikhaya hai ki lakshya sirf ek hota hai. "
            "Baki sab... sirf andhera hai. "
            "Aaj Maine woh andhera dekha — aur usme ek aur dhanurdhar khada tha."
        ),
    },
    {
        "slot_id":    "arjuna_focused_01",
        "character":  "arjuna",
        "emotion_tag": "[focused]",
        "text": (
            "Yeh dhanush mera haath nahi hai. "
            "Yeh meri aankh hai. "
            "Jab main nishaana lagata hun, toh duniya rukh jaati hai. "
            "Keval woh ek bindu bachta hai — aur main."
        ),
    },
    {
        "slot_id":    "arjuna_grief_01",
        "character":  "arjuna",
        "emotion_tag": "[grief]",
        "text": (
            "Raat bhar main sochta raha. "
            "Pehli baar main chuka. "
            "Sirf ek baar. "
            "Lekin woh ek baar mujhe yaad hai — aur shayad hamesha rahega."
        ),
    },

    # ── KARNA ─────────────────────────────────────────────────────
    {
        "slot_id":    "karna_formal_01",
        "character":  "karna",
        "emotion_tag": "[formal]",
        "text": (
            "Main Kuruvansa ke teesre rajkumar ka apmaan karne nahi aaya. "
            "Main isliye aaya hun kyunki mujhe bataya gaya hai ki Bharatavarsha ke "
            "sabse mahaan dhanurdhar yahan rehte hain. "
            "Main unhe chunauti deta hun — saadar, lekin poori nishtha ke saath."
        ),
    },
    {
        "slot_id":    "karna_warm_01",
        "character":  "karna",
        "emotion_tag": "[warm]",
        "text": (
            "Duryodhana, tumne mujhe woh diya jo kisi ne kabhi nahi diya — "
            "ek naam. Ek jagah. "
            "Main iska bojh jaanta hun, aur main ise kabhi neeche nahi girne dunga."
        ),
    },
    {
        "slot_id":    "karna_grief_01",
        "character":  "karna",
        "emotion_tag": "[grief]",
        "text": (
            "Main jaanta hun yeh yudh galat hai. "
            "Main jaanta hun kaunsi taraf sachhai hai. "
            "Lekin wafadari... wafadari meri sachhai hai. "
            "Aur iske liye main apni jaan de dunga."
        ),
    },

    # ── DURYODHANA ────────────────────────────────────────────────
    {
        "slot_id":    "duryodhana_generous_01",
        "character":  "duryodhana",
        "emotion_tag": "[generous]",
        "text": (
            "Yeh log poochhte hain ki iska kul kya hai, iska janm kahan hua. "
            "Main kehta hun — "
            "aaj se yeh Anga ka raja hai! "
            "Agar sabse bada dhanurdhar hi yeh prashn karta hai, toh main uska uttar deta hun — "
            "is taaj ke saath."
        ),
    },
    {
        "slot_id":    "duryodhana_warm_karna_01",
        "character":  "duryodhana",
        "emotion_tag": "[warm]",
        "text": (
            "Karna, tum mujhe samjhte ho. "
            "Bina kuch maange. Bina kuch chahte. "
            "Duniya mein ek hi aisa insaan hota hai. "
            "Aur woh tum ho."
        ),
    },
    {
        "slot_id":    "duryodhana_rage_01",
        "character":  "duryodhana",
        "emotion_tag": "[rage]",
        "text": (
            "Woh hasee! "
            "Mere mahal mein, mere saamne — woh hasee! "
            "Is apmaan ka jawab hoga. "
            "Main jaanta hun yeh galat hai. "
            "Lekin kuch ghalatiyan hum rok hi nahi sakte."
        ),
    },

    # ── KRISHNA ───────────────────────────────────────────────────
    {
        "slot_id":    "krishna_warm_oblique_01",
        "character":  "krishna",
        "emotion_tag": "[warm_oblique]",
        "text": (
            "Arjuna, tum poochhte ho ki kya sahi hai. "
            "Main poochhunga — sahi kisake liye? "
            "Khud ke liye? Unke liye jo mar jayenge? "
            "Ya unke liye jo bachenge aur yaad rakhenge? "
            "Shayad yeh teen alag jawab hain."
        ),
    },
    {
        "slot_id":    "krishna_solemn_01",
        "character":  "krishna",
        "emotion_tag": "[solemn]",
        "text": (
            "Yeh yudh hoga. "
            "Main yeh nahi rok sakta — na main chahta hun. "
            "Dharma ko apna raasta khud dhundhna padta hai. "
            "Hum sirf unke haath hain jinhone yeh raasta chuna."
        ),
    },

    # ── DRAUPADI ──────────────────────────────────────────────────
    {
        "slot_id":    "draupadi_precise_01",
        "character":  "draupadi",
        "emotion_tag": "[precise]",
        "text": (
            "Mujhe ek prashn ka uttar chahiye. "
            "Sirf ek. "
            "Kya ek aadmi jo khud haar chuka tha, woh mujhe daav par laga sakta tha? "
            "Is sabha mein koi to dharma jaanta hoga."
        ),
    },
    {
        "slot_id":    "draupadi_laughing_angry_01",
        "character":  "draupadi",
        "emotion_tag": "[precise]",
        "text": (
            "Hahaha. "
            "Main hasti hun kyunki rona hote hain unke liye "
            "jinhe koi sunta hai. "
            "Mujhe koi nahi sunta — toh main hasti hun. "
            "Aur yeh hasee... yeh hasee main kabhi nahi bhuloogi."
        ),
    },

    # ── BHISHMA ───────────────────────────────────────────────────
    {
        "slot_id":    "bhishma_formal_01",
        "character":  "bhishma",
        "emotion_tag": "[formal]",
        "text": (
            "Maine pratigya li thi — "
            "is singhasan ki raksha karna. "
            "Chahe singhasan par baithe vyakti layak hon ya nahi. "
            "Yeh mera dharm hai. "
            "Yeh meri zindagi hai. "
            "Aur yeh meri maut hogi."
        ),
    },
    {
        "slot_id":    "bhishma_verse_01",
        "character":  "bhishma",
        "emotion_tag": "[verse_mode]",
        "text": (
            "Jis din main ne apna naam chod diya, "
            "us din mera janam hua. "
            "Jis din yeh yudh khatam hoga, "
            "us din mera ant hoga. "
            "Shantanu ke putra ne apna janam liya dharm ke liye — "
            "aur dharm ke liye hi woh jata hai."
        ),
    },

    # ── KUNTI ─────────────────────────────────────────────────────
    {
        "slot_id":    "kunti_composed_01",
        "character":  "kunti",
        "emotion_tag": "[composed]",
        "text": (
            "Main ek ma hun. "
            "Mera kaam apne beton ki raksha karna tha. "
            "Main ne yeh kiya — "
            "lekin us mein ek aur beta tha "
            "jise main ne raksha nahi ki. "
            "Woh mujhe hamesha yaad rahega."
        ),
    },
    {
        "slot_id":    "kunti_grief_hidden_01",
        "character":  "kunti",
        "emotion_tag": "[grief_hidden]",
        "text": (
            "Jab main ne use arena mein dekha — "
            "woh kavach, woh sone ki chamak — "
            "main jaanti thi. "
            "Lekin main kuch nahi bol sakti thi. "
            "Kuch bhi nahi. "
            "Bas dekha. Aur chup rahi."
        ),
    },

    # ── SHAKUNI ───────────────────────────────────────────────────
    {
        "slot_id":    "shakuni_avuncular_01",
        "character":  "shakuni",
        "emotion_tag": "[avuncular]",
        "text": (
            "Bhaanje, yeh pasa khel nahi hai. "
            "Yeh ek kala hai — jaise teer chalana, jaise raj karna. "
            "Aur main tumhara mama hun. "
            "Kya main tumhare kaam nahi aaunga? "
            "Aao, main tumhe sikhata hun."
        ),
    },
    {
        "slot_id":    "shakuni_private_01",
        "character":  "shakuni",
        "emotion_tag": "[avuncular]",
        "text": (
            "Mere pita ki haddiyon se bane hain yeh pase. "
            "Har baar yeh girate hain, toh woh mujhse poochhte hain — "
            "kya humara badla poora hua? "
            "Abhi nahi. "
            "Lekin hoga."
        ),
    },

    # ── YUDHISHTHIRA ──────────────────────────────────────────────
    {
        "slot_id":    "yudhishthira_formal_01",
        "character":  "yudhishthira",
        "emotion_tag": "[formal]",
        "text": (
            "Dharm ek seedhi lakir nahi hai. "
            "Yeh ek nadi hai — kabhi kabhi tez, kabhi kabhi gehri. "
            "Main ne hamesha iska raasta maana. "
            "Aur main ne hamesha iska dard bhi sahaa."
        ),
    },
    {
        "slot_id":    "yudhishthira_quiet_01",
        "character":  "yudhishthira",
        "emotion_tag": "[quiet]",
        "text": (
            "Main ne daav lagaya. "
            "Apne bhai. "
            "Apni patni. "
            "Main kehta hun ki dharm ne mujhe majboor kiya. "
            "Lekin sach yeh hai ki main dara hua tha. "
            "Aur yeh mujhe hamesha pata tha."
        ),
    },
]


# ──────────────────────────────────────────────────────────────────
# ASYNC GENERATOR
# ──────────────────────────────────────────────────────────────────
async def generate_line(entry: dict) -> tuple:
    """Generate one TTS line and save to file. Returns (slot_id, success, size)."""
    try:
        import edge_tts
    except ImportError:
        print("  [ERROR] edge-tts not installed. Run: pip install edge-tts")
        return (entry["slot_id"], False, 0)

    character  = entry["character"]
    slot_id    = entry["slot_id"]
    text       = entry["text"]
    emotion    = entry["emotion_tag"]
    voice      = VOICES.get(character, "hi-IN-MadhurNeural")
    params     = get_params(emotion)

    out_dir = os.path.join(OUTPUT_DIR, character)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{slot_id}.mp3")

    try:
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=params["rate"],
            pitch=params["pitch"],
            volume=params["volume"],
        )
        await communicate.save(out_path)
        size = os.path.getsize(out_path)
        return (slot_id, True, size)
    except Exception as e:
        print(f"  [FAIL] {slot_id} -> {e}")
        return (slot_id, False, 0)


async def run_all():
    print("\n" + "=" * 60)
    print("  Crown of Kaliyug — Character Audio Generator")
    print("  Generating TTS samples for 9 characters...")
    print("=" * 60)

    tasks   = [generate_line(entry) for entry in DIALOGUE_LINES]
    results = await asyncio.gather(*tasks)

    # ── Summary ───────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  RESULTS")
    print("=" * 60)

    passed = 0
    failed = 0
    current_char = None

    for slot_id, success, size in sorted(results, key=lambda r: r[0]):
        char = slot_id.split("_")[0]
        if char != current_char:
            print(f"\n  [{char.upper()}]")
            current_char = char
        if success:
            duration_est = round(size / 6000, 1)  # rough MP3 estimate
            print(f"    [OK]  {slot_id}.mp3  ({size:,} bytes, ~{duration_est}s)")
            passed += 1
        else:
            print(f"    [--]  {slot_id}  FAILED")
            failed += 1

    print("\n" + "=" * 60)
    print(f"  {passed} generated  |  {failed} failed")
    print(f"  Output: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 60 + "\n")


# ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    start = time.time()
    asyncio.run(run_all())
    elapsed = round(time.time() - start, 1)
    print(f"  Completed in {elapsed}s\n")
