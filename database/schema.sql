-- Crown of Kaliyug — Story Bible Database Schema
-- Phase 0: Foundation
-- Run: psql -d crown_of_kaliyug -f schema.sql

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ─────────────────────────────────────────────
-- NATIONS
-- ─────────────────────────────────────────────
CREATE TABLE nations (
    id              VARCHAR(50) PRIMARY KEY,    -- e.g. 'kuruvansa'
    name            VARCHAR(100) NOT NULL,
    got_analog      VARCHAR(100),               -- e.g. "King's Landing"
    capital         VARCHAR(100),
    ethnicity_ref   TEXT,                       -- casting reference from Series Bible p.28
    aesthetics      TEXT,                       -- visual style description
    color_palette   VARCHAR(200),               -- e.g. "grey, deep blue, gold"
    music_theme     VARCHAR(100),               -- e.g. "kuru_court_theme"
    notes           TEXT,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────────
-- CHARACTERS
-- ─────────────────────────────────────────────
CREATE TABLE characters (
    id                  VARCHAR(50) PRIMARY KEY,    -- e.g. 'karna'
    name                VARCHAR(100) NOT NULL,
    nation_id           VARCHAR(50) REFERENCES nations(id),
    archetype           TEXT,                       -- e.g. "The Tragic Hero Who Chose the Wrong Side"
    arc_summary         TEXT,                       -- full character arc from bible
    voice_profile_path  VARCHAR(200),               -- path to .md voice rules file
    hidden_truth        TEXT,                       -- the secret Series Bible assigns each character
    writing_rules       TEXT[],                     -- non-negotiable rules for Dialogue Agent
    season_first_appears INTEGER DEFAULT 1,
    season_dies         INTEGER,                    -- NULL if survives
    episode_dies        VARCHAR(20),                -- e.g. 'S4E13' (Abhimanyu)
    casting_directive   TEXT,                       -- ethnicity + age + physical note from bible
    voice_el_profile_id VARCHAR(100),               -- ElevenLabs voice ID (Phase 3)
    avatar_s3_path      VARCHAR(500),               -- S3 path (Phase 2)
    leitmotif_id        VARCHAR(100),               -- music theme ID (Phase 3)
    vfx_preset_id       VARCHAR(100),               -- VFX preset ID (Phase 2)
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────────
-- SEASONS
-- ─────────────────────────────────────────────
CREATE TABLE seasons (
    id              INTEGER PRIMARY KEY,            -- 1–7
    title           VARCHAR(200) NOT NULL,
    episode_count   INTEGER NOT NULL,
    parvas_covered  VARCHAR(200),                   -- e.g. "Adi + Sabha"
    tone_reference  TEXT,                           -- e.g. "Succession meets The Crown"
    thematic_id     TEXT,                           -- e.g. "Succession, Betrayal, The Fall"
    status          VARCHAR(30) DEFAULT 'planned'   -- planned | in_production | complete
);

-- ─────────────────────────────────────────────
-- EPISODES
-- ─────────────────────────────────────────────
CREATE TABLE episodes (
    id              VARCHAR(20) PRIMARY KEY,        -- e.g. 'S1E01'
    season_id       INTEGER REFERENCES seasons(id),
    episode_number  INTEGER NOT NULL,
    title_english   VARCHAR(200) NOT NULL,
    title_hindi     VARCHAR(200),
    synopsis        TEXT,
    key_events      TEXT[],                         -- major plot beats
    parvas_covered  VARCHAR(200),
    runtime_target  INTEGER,                        -- target runtime in minutes
    status          VARCHAR(30) DEFAULT 'draft',    -- draft | locked | produced | published
    script_s3_path  VARCHAR(500),
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────────
-- SCENES
-- ─────────────────────────────────────────────
CREATE TABLE scenes (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    episode_id          VARCHAR(20) REFERENCES episodes(id),
    scene_number        INTEGER NOT NULL,
    location            VARCHAR(200),
    interior_exterior   VARCHAR(10),                -- INT / EXT
    time_of_day         VARCHAR(20),                -- DAY / NIGHT / DAWN / DUSK
    characters_present  VARCHAR(50)[],              -- array of character IDs
    mood                VARCHAR(100),
    action_lines        TEXT[],
    vfx_required        TEXT[],                     -- vfx tags for Phase 2
    sfx_tags            TEXT[],                     -- sfx tags for Phase 3
    is_tag_sequence     BOOLEAN DEFAULT FALSE,       -- TRUE = music only, no dialogue (final 8 min)
    directors_note      TEXT,                       -- from Series Bible
    video_s3_path       VARCHAR(500),               -- Phase 2 output
    audio_s3_path       VARCHAR(500),               -- Phase 3 output
    created_at          TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────────
-- CONTINUITY LOG
-- ─────────────────────────────────────────────
CREATE TABLE continuity_log (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    episode_id              VARCHAR(20) REFERENCES episodes(id),
    character_id            VARCHAR(50) REFERENCES characters(id),
    fact_text               TEXT NOT NULL,          -- the canon fact established
    severity                VARCHAR(20) DEFAULT 'STANDARD', -- CRITICAL | WARNING | STANDARD
    reveal_not_before_season INTEGER,               -- NULL = no restriction
    reveal_not_before_ep    VARCHAR(20),            -- e.g. 'S3E01'
    source                  VARCHAR(50) DEFAULT 'series_bible', -- series_bible | script | derived
    created_at              TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────────
-- ASSETS REGISTRY
-- ─────────────────────────────────────────────
CREATE TABLE assets_registry (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    character_id    VARCHAR(50) REFERENCES characters(id),
    asset_type      VARCHAR(50) NOT NULL,           -- avatar | voice | leitmotif | sfx | vfx_preset
    season_phase    VARCHAR(20),                    -- which season arc this variant is for
    s3_path         VARCHAR(500),
    external_id     VARCHAR(200),                   -- ElevenLabs voice ID / Suno track ID etc.
    asset_metadata  JSONB,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────────
-- EPISODE METRICS (Phase 5)
-- ─────────────────────────────────────────────
CREATE TABLE episode_metrics (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    episode_id      VARCHAR(20) REFERENCES episodes(id),
    platform        VARCHAR(30) NOT NULL,           -- youtube | instagram | twitter
    metric_date     DATE NOT NULL,
    views           INTEGER DEFAULT 0,
    watch_time_min  INTEGER DEFAULT 0,              -- total watch time in minutes
    likes           INTEGER DEFAULT 0,
    shares          INTEGER DEFAULT 0,
    comments        INTEGER DEFAULT 0,
    avg_retention   DECIMAL(5,2),                   -- percentage
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────────
-- STORY INSIGHTS (Phase 5 → Phase 1 feedback)
-- ─────────────────────────────────────────────
CREATE TABLE story_insights (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    generated_for_ep VARCHAR(20) REFERENCES episodes(id),
    insight_text    TEXT NOT NULL,                  -- Claude's recommendation
    character_id    VARCHAR(50) REFERENCES characters(id),
    insight_type    VARCHAR(50),                    -- retention | engagement | viral | character
    data_source     JSONB,                          -- raw metrics that triggered insight
    applied         BOOLEAN DEFAULT FALSE,           -- has Shristi acted on this?
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────────
-- INDEXES
-- ─────────────────────────────────────────────
CREATE INDEX idx_scenes_episode ON scenes(episode_id);
CREATE INDEX idx_continuity_character ON continuity_log(character_id);
CREATE INDEX idx_continuity_episode ON continuity_log(episode_id);
CREATE INDEX idx_metrics_episode ON episode_metrics(episode_id);
CREATE INDEX idx_metrics_platform ON episode_metrics(platform);
CREATE INDEX idx_insights_episode ON story_insights(generated_for_ep);
