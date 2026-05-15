import os

def load_character_prompt(character_name):
    """
    Loads the system prompt for a specific character from the prompts directory.
    """
    # Normalize character name
    char_id = character_name.lower().strip()
    path = os.path.join("prompts", f"dialogue_{char_id}.txt")
    
    if not os.path.exists(path):
        # Fallback to a generic prompt or raise error
        raise FileNotFoundError(f"No dialogue prompt found for character '{char_id}' at {path}")
        
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
