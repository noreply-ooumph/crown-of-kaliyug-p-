import re
from loguru import logger

# Valid tags from character prompts
VALID_TAGS = [
    "[formal]", "[warm]", "[grief]", "[battle]", "[generous]", "[rage]", 
    "[private]", "[dying]", "[verse_mode]", "[ancient]", "[avuncular]", 
    "[laughing]", "[vengeance]", "[quiet]", "[breakdown]", "[warm_oblique]", 
    "[solemn]", "[gita]", "[precise]", "[laughing-angry]", "[charming]", 
    "[focused]", "[post_gita]", "[composed]", "[grief_hidden]"
]

def validate_tag(tag):
    """
    Ensures the tag is wrapped in brackets and is one of the valid tags.
    Returns [formal] as default if invalid.
    """
    if not tag:
        return "[formal]"
    
    tag_str = str(tag).strip()
    
    # Ensure brackets
    if not tag_str.startswith("["):
        tag_str = f"[{tag_str}"
    if not tag_str.endswith("]"):
        tag_str = f"{tag_str}]"
    
    tag_lower = tag_str.lower()
    if tag_lower in VALID_TAGS:
        return tag_lower
    
    # Check for common variants
    if tag_lower == "[roar]": return "[rage]"
    if tag_lower == "[whisper]": return "[quiet]"
    
    return "[formal]"

def get_voice_settings(tag):
    """
    Returns ElevenLabs-style voice settings based on the emotion tag.
    """
    tag = validate_tag(tag)
    
    # Default settings
    settings = {
        "stability": 0.75, 
        "similarity_boost": 0.75, 
        "style": 0.0, 
        "use_speaker_boost": True
    }
    
    if tag in ["[rage]", "[laughing-angry]", "[roar]"]:
        settings["stability"] = 0.4
        settings["style"] = 0.5
    elif tag in ["[quiet]", "[grief_hidden]", "[whisper]"]:
        settings["stability"] = 0.95
    elif tag in ["[formal]", "[ancient]", "[verse_mode]"]:
        settings["stability"] = 0.85
    elif tag in ["[charming]", "[warm]", "[avuncular]"]:
        settings["stability"] = 0.65
        
    return settings

def extract_tag_from_line(line_text):
    """
    Extracts emotion tag from text like 'Hello world. [warm]'
    Returns (cleaned_text, tag)
    """
    if not line_text:
        return "", "[formal]"
        
    # Look for [tag] at the end of the line
    match = re.search(r"(\[[\w-]+\])\s*$", line_text.strip())
    if match:
        tag = match.group(1)
        text = line_text.replace(tag, "").strip()
        return text, validate_tag(tag)
    
    return line_text.strip(), "[formal]"
