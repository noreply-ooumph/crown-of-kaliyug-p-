"""
Crown of Kaliyug — Frame Composer
Phase 2 · agents/visual_prod/video/frame_composer.py

Handles multi-character scenes — composites multiple avatars.
For demo: primary character Ken Burns + secondary smaller overlay.
"""
import os
import numpy as np
from pathlib import Path
from loguru import logger


def compose_multi_character_frame(
    primary_avatar: str,
    secondary_avatars: list,
    frame_size: tuple = (1920, 1080),
) -> np.ndarray:
    """
    Composes a frame with primary character full-frame
    and secondary characters as smaller overlays.
    """
    try:
        from PIL import Image
        frame = Image.open(primary_avatar).convert("RGB").resize(frame_size, Image.LANCZOS)
        frame_arr = np.array(frame)

        # Add secondary characters as smaller overlays (bottom corners)
        for i, sec_path in enumerate(secondary_avatars[:2]):
            if not os.path.exists(sec_path):
                continue
            sec = Image.open(sec_path).convert("RGB")
            thumb_size = (320, 480)
            sec_thumb = sec.resize(thumb_size, Image.LANCZOS)
            x = frame_size[0] - thumb_size[0] - 20 - (i * (thumb_size[0] + 10))
            y = frame_size[1] - thumb_size[1] - 20
            frame.paste(sec_thumb, (x, y))

        return np.array(frame)
    except Exception as e:
        logger.error(f"[FrameComposer] Failed: {e}")
        return np.zeros((frame_size[1], frame_size[0], 3), dtype=np.uint8)
