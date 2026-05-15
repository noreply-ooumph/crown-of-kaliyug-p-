"""
Crown of Kaliyug — SQLAlchemy ORM Models
Phase 0: Foundation
"""
from sqlalchemy import (
    Column, String, Integer, Boolean, Text, DateTime, 
    ForeignKey, Numeric, Date, JSON
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class Nation(Base):
    __tablename__ = "nations"

    id              = Column(String(50), primary_key=True)
    name            = Column(String(100), nullable=False)
    got_analog      = Column(String(100))
    capital         = Column(String(100))
    ethnicity_ref   = Column(Text)
    aesthetics      = Column(Text)
    color_palette   = Column(String(200))
    music_theme     = Column(String(100))
    notes           = Column(Text)
    created_at      = Column(DateTime, server_default=func.now())

    characters      = relationship("Character", back_populates="nation")


class Character(Base):
    __tablename__ = "characters"

    id                  = Column(String(50), primary_key=True)
    name                = Column(String(100), nullable=False)
    nation_id           = Column(String(50), ForeignKey("nations.id"))
    archetype           = Column(Text)
    arc_summary         = Column(Text)
    voice_profile_path  = Column(String(200))
    hidden_truth        = Column(Text)
    writing_rules       = Column(JSON)
    season_first_appears= Column(Integer, default=1)
    season_dies         = Column(Integer)
    episode_dies        = Column(String(20))
    casting_directive   = Column(Text)
    voice_el_profile_id = Column(String(100))
    avatar_s3_path      = Column(String(500))
    leitmotif_id        = Column(String(100))
    vfx_preset_id       = Column(String(100))
    created_at          = Column(DateTime, server_default=func.now())
    updated_at          = Column(DateTime, server_default=func.now(), onupdate=func.now())

    nation              = relationship("Nation", back_populates="characters")
    continuity_facts    = relationship("ContinuityLog", back_populates="character")


class Season(Base):
    __tablename__ = "seasons"

    id              = Column(Integer, primary_key=True)
    title           = Column(String(200), nullable=False)
    episode_count   = Column(Integer, nullable=False)
    parvas_covered  = Column(String(200))
    tone_reference  = Column(Text)
    thematic_id     = Column(Text)
    status          = Column(String(30), default="planned")

    episodes        = relationship("Episode", back_populates="season")


class Episode(Base):
    __tablename__ = "episodes"

    id              = Column(String(20), primary_key=True)
    season_id       = Column(Integer, ForeignKey("seasons.id"))
    episode_number  = Column(Integer, nullable=False)
    title_english   = Column(String(200), nullable=False)
    title_hindi     = Column(String(200))
    synopsis        = Column(Text)
    key_events      = Column(JSON)
    parvas_covered  = Column(String(200))
    runtime_target  = Column(Integer)
    status          = Column(String(30), default="draft")
    script_s3_path  = Column(String(500))
    created_at      = Column(DateTime, server_default=func.now())
    updated_at      = Column(DateTime, server_default=func.now(), onupdate=func.now())

    season          = relationship("Season", back_populates="episodes")
    scenes          = relationship("Scene", back_populates="episode")
    metrics         = relationship("EpisodeMetric", back_populates="episode")


class Scene(Base):
    __tablename__ = "scenes"

    id                  = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    episode_id          = Column(String(20), ForeignKey("episodes.id"))
    scene_number        = Column(Integer, nullable=False)
    location            = Column(String(200))
    interior_exterior   = Column(String(10))
    time_of_day         = Column(String(20))
    characters_present  = Column(JSON)
    mood                = Column(String(100))
    action_lines        = Column(JSON)
    vfx_required        = Column(JSON)
    sfx_tags            = Column(JSON)
    is_tag_sequence     = Column(Boolean, default=False)
    directors_note      = Column(Text)
    video_s3_path       = Column(String(500))
    audio_s3_path       = Column(String(500))
    created_at          = Column(DateTime, server_default=func.now())

    episode             = relationship("Episode", back_populates="scenes")


class ContinuityLog(Base):
    __tablename__ = "continuity_log"

    id                      = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    episode_id              = Column(String(20), ForeignKey("episodes.id"))
    character_id            = Column(String(50), ForeignKey("characters.id"))
    fact_text               = Column(Text, nullable=False)
    severity                = Column(String(20), default="STANDARD")
    reveal_not_before_season= Column(Integer)
    reveal_not_before_ep    = Column(String(20))
    source                  = Column(String(50), default="series_bible")
    created_at              = Column(DateTime, server_default=func.now())

    character               = relationship("Character", back_populates="continuity_facts")


class AssetsRegistry(Base):
    __tablename__ = "assets_registry"

    id              = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    character_id    = Column(String(50), ForeignKey("characters.id"))
    asset_type      = Column(String(50), nullable=False)
    season_phase    = Column(String(20))
    s3_path         = Column(String(500))
    external_id     = Column(String(200))
    asset_metadata  = Column(JSON)
    created_at      = Column(DateTime, server_default=func.now())


class EpisodeMetric(Base):
    __tablename__ = "episode_metrics"

    id              = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    episode_id      = Column(String(20), ForeignKey("episodes.id"))
    platform        = Column(String(30), nullable=False)
    metric_date     = Column(Date, nullable=False)
    views           = Column(Integer, default=0)
    watch_time_min  = Column(Integer, default=0)
    likes           = Column(Integer, default=0)
    shares          = Column(Integer, default=0)
    comments        = Column(Integer, default=0)
    avg_retention   = Column(Numeric(5, 2))
    created_at      = Column(DateTime, server_default=func.now())

    episode         = relationship("Episode", back_populates="metrics")


class StoryInsight(Base):
    __tablename__ = "story_insights"

    id              = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    generated_for_ep= Column(String(20), ForeignKey("episodes.id"))
    insight_text    = Column(Text, nullable=False)
    character_id    = Column(String(50), ForeignKey("characters.id"))
    insight_type    = Column(String(50))
    data_source     = Column(JSON)
    applied         = Column(Boolean, default=False)
    created_at      = Column(DateTime, server_default=func.now())