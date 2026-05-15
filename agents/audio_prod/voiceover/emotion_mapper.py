"""
Crown of Kaliyug - Emotion Mapper
A-07 - agents/audio_prod/voiceover/emotion_mapper.py
Maps emotion tags to voice generation parameters.
"""

# Edge TTS SSML rate/pitch per emotion tag
EDGE_TTS_PARAMS = {
    "[whisper]":        {"rate": "-30%", "pitch": "-5Hz",  "volume": "-30%"},
    "[roar]":           {"rate": "+20%", "pitch": "+5Hz",  "volume": "+50%"},
    "[formal]":         {"rate": "-10%", "pitch": "0Hz",   "volume": "+0%"},
    "[sarcastic]":      {"rate": "+5%",  "pitch": "+3Hz",  "volume": "+0%"},
    "[tearful]":        {"rate": "-15%", "pitch": "-3Hz",  "volume": "-10%"},
    "[laughing]":       {"rate": "+10%", "pitch": "+5Hz",  "volume": "+10%"},
    "[laughing-angry]": {"rate": "+15%", "pitch": "+8Hz",  "volume": "+20%"},
    "[verse_mode]":     {"rate": "-20%", "pitch": "-2Hz",  "volume": "+0%"},
    "[warm_oblique]":   {"rate": "-5%",  "pitch": "0Hz",   "volume": "+0%"},
    "[grief]":          {"rate": "-20%", "pitch": "-5Hz",  "volume": "-15%"},
    "[grief_hidden]":   {"rate": "-15%", "pitch": "-3Hz",  "volume": "-10%"},
    "[composed]":       {"rate": "-10%", "pitch": "0Hz",   "volume": "+0%"},
    "[avuncular]":      {"rate": "-5%",  "pitch": "0Hz",   "volume": "+0%"},
    "[dying]":          {"rate": "-30%", "pitch": "-8Hz",  "volume": "-30%"},
    "[ancient]":        {"rate": "-25%", "pitch": "-5Hz",  "volume": "-5%"},
    "[gita]":           {"rate": "-15%", "pitch": "-2Hz",  "volume": "+0%"},
    "[rage]":           {"rate": "+25%", "pitch": "+10Hz", "volume": "+50%"},
    "[precise]":        {"rate": "-5%",  "pitch": "0Hz",   "volume": "+0%"},
    "[quiet]":          {"rate": "-20%", "pitch": "-3Hz",  "volume": "-25%"},
    "[breakdown]":      {"rate": "+10%", "pitch": "+5Hz",  "volume": "+20%"},
    "[focused]":        {"rate": "-5%",  "pitch": "0Hz",   "volume": "+0%"},
    "[warm]":           {"rate": "-5%",  "pitch": "0Hz",   "volume": "+0%"},
    "[generous]":       {"rate": "0%",   "pitch": "0Hz",   "volume": "+5%"},
    "[battle]":         {"rate": "+5%",  "pitch": "0Hz",   "volume": "+10%"},
    "[solemn]":         {"rate": "-15%", "pitch": "-3Hz",  "volume": "-5%"},
    "[vengeance]":      {"rate": "+10%", "pitch": "+5Hz",  "volume": "+15%"},
    "[post_gita]":      {"rate": "-10%", "pitch": "-2Hz",  "volume": "+0%"},
}

# ElevenLabs settings per emotion tag
ELEVENLABS_PARAMS = {
    "[whisper]":        {"stability": 0.95, "similarity_boost": 0.8,  "style": 0.1},
    "[roar]":           {"stability": 0.2,  "similarity_boost": 0.9,  "style": 1.0},
    "[formal]":         {"stability": 0.85, "similarity_boost": 0.85, "style": 0.3},
    "[sarcastic]":      {"stability": 0.5,  "similarity_boost": 0.7,  "style": 0.7},
    "[tearful]":        {"stability": 0.6,  "similarity_boost": 0.9,  "style": 0.5},
    "[laughing]":       {"stability": 0.3,  "similarity_boost": 0.7,  "style": 0.8},
    "[laughing-angry]": {"stability": 0.25, "similarity_boost": 0.85, "style": 0.9},
    "[verse_mode]":     {"stability": 0.9,  "similarity_boost": 0.8,  "style": 0.4},
    "[warm_oblique]":   {"stability": 0.75, "similarity_boost": 0.8,  "style": 0.4},
    "[grief]":          {"stability": 0.7,  "similarity_boost": 0.9,  "style": 0.3},
    "[grief_hidden]":   {"stability": 0.88, "similarity_boost": 0.85, "style": 0.2},
    "[composed]":       {"stability": 0.9,  "similarity_boost": 0.8,  "style": 0.2},
    "[avuncular]":      {"stability": 0.7,  "similarity_boost": 0.75, "style": 0.5},
    "[dying]":          {"stability": 0.85, "similarity_boost": 0.9,  "style": 0.15},
    "[ancient]":        {"stability": 0.95, "similarity_boost": 0.85, "style": 0.1},
    "[gita]":           {"stability": 0.8,  "similarity_boost": 0.9,  "style": 0.35},
    "[rage]":           {"stability": 0.2,  "similarity_boost": 0.85, "style": 0.95},
    "[precise]":        {"stability": 0.9,  "similarity_boost": 0.8,  "style": 0.25},
    "[quiet]":          {"stability": 0.92, "similarity_boost": 0.8,  "style": 0.1},
    "[breakdown]":      {"stability": 0.3,  "similarity_boost": 0.9,  "style": 0.8},
    "[focused]":        {"stability": 0.85, "similarity_boost": 0.8,  "style": 0.3},
    "[warm]":           {"stability": 0.75, "similarity_boost": 0.8,  "style": 0.45},
    "[generous]":       {"stability": 0.7,  "similarity_boost": 0.75, "style": 0.5},
    "[battle]":         {"stability": 0.8,  "similarity_boost": 0.85, "style": 0.4},
    "[vengeance]":      {"stability": 0.6,  "similarity_boost": 0.85, "style": 0.65},
    "[solemn]":         {"stability": 0.88, "similarity_boost": 0.85, "style": 0.2},
    "[post_gita]":      {"stability": 0.82, "similarity_boost": 0.88, "style": 0.28},
}


def get_edge_params(emotion_tag: str) -> dict:
    return EDGE_TTS_PARAMS.get(emotion_tag, {"rate": "0%", "pitch": "0Hz", "volume": "+0%"})


def get_elevenlabs_params(emotion_tag: str) -> dict:
    return ELEVENLABS_PARAMS.get(emotion_tag, {"stability": 0.8, "similarity_boost": 0.8, "style": 0.3})
