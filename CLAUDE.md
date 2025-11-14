# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Semantic Tarot is a Python-based tarot reading application featuring:
- Interactive CLI for tarot readings with ASCII art cards
- 4 interpretation systems (Traditional/RWS, Crowley/Thoth, Jungian/Psychological, Modern/Intuitive)
- Vector embeddings for semantic card search using OpenAI's embedding API
- Multiple reading spreads (single card, three card, Celtic Cross, etc.)
- Complete 78-card tarot deck (22 Major Arcana + 56 Minor Arcana)

## Core Architecture

### Three Main Components

1. **tarot.py** - Interactive tarot reader
   - Main menu-driven application for performing readings
   - Manages interpretation modes and displays cards with ASCII art
   - Handles reading history and daily card persistence
   - No external dependencies (pure Python stdlib)

2. **search_cards.py** - Semantic search interface
   - Command-line and interactive search using vector embeddings
   - Supports semantic search ("new beginnings") and similarity search
   - System-specific filtering (search within specific interpretation traditions)
   - Multiple output formats (text, JSON, YAML)
   - Requires: openai, numpy, pyyaml

3. **generate_embeddings.py** - Embedding generation
   - One-time script to create vector embeddings
   - Generates 10 embeddings per card (2 positions × 5 systems)
   - Systems: rws_traditional, thoth_crowley, jungian_psychological, modern_intuitive, combined
   - Creates card_embeddings.json (780 embeddings total)

### Data Architecture

**Data Files:**
- `cards.json` - Card definitions with ASCII art and basic meanings
- `interpretations.json` - Four interpretation systems for all 78 cards
- `card_embeddings.json` - Vector embeddings (780 entries: 78 cards × 2 positions × 5 systems)
- `reading_history.json` - Auto-generated user reading history
- `daily_card.json` - Auto-generated daily card persistence

**Interpretation System Design:**
The app uses a multi-perspective approach where each card has interpretations from 4 distinct traditions. The `interpretations.json` structure:
```json
{
  "The Fool": {
    "rws_traditional": {"upright": "...", "reversed": "..."},
    "thoth_crowley": {"upright": "...", "reversed": "..."},
    "jungian_psychological": {"upright": "...", "reversed": "..."},
    "modern_intuitive": {"upright": "...", "reversed": "..."}
  }
}
```

**Embedding System Design:**
Each card has 10 separate embeddings to enable system-specific semantic search:
- 2 positions: upright and reversed
- 5 interpretation systems: 4 traditions + 1 combined
- This allows searching within a specific tradition (e.g., Jungian cards about "shadow") or across all traditions

## Common Commands

### Running the Application

```bash
# Interactive tarot reader (no dependencies)
python3 tarot.py

# Semantic search (requires openai API key)
python3 search_cards.py "new beginnings"
python3 search_cards.py --similar "The Fool"
python3 search_cards.py "shadow work" --system jungian_psychological

# Display ASCII art with search results
python3 search_cards.py "new beginnings" --ascii
python3 search_cards.py --similar "The Fool" --art --top 3

# Generate embeddings (one-time setup, requires OPENAI_API_KEY)
export OPENAI_API_KEY='your-key'
python3 generate_embeddings.py
```

### Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run specific test file
pytest tests/test_search.py

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_search.py::test_search_cards
```

### Development Setup

```bash
# Install dependencies (for semantic search and testing)
pip install -r requirements.txt

# Set OpenAI API key (for embeddings and search)
export OPENAI_API_KEY='your-api-key'
```

## Key Functions Reference

### tarot.py
- `get_interpretation(card_name, is_reversed, mode)` - Fetch interpretation from specific system
- `display_card(card, is_reversed, show_all_interpretations)` - Display card with ASCII art
- `draw_card(allow_reversed)` - Random card draw with optional reversals
- Reading spreads: `single_card_reading()`, `three_card_reading()`, `celtic_cross_reading()`, `horseshoe_reading()`, `yes_no_reading()`, `relationship_reading()`
- `change_interpretation_mode()` - Switch between the 4 interpretation systems
- `compare_interpretations()` - View all 4 perspectives for a card
- `save_reading()` / `view_reading_history()` - Persist and retrieve readings

### search_cards.py
- `search_cards(embeddings, cards_data, interpretations_data, client, query, top_k, system)` - Semantic search by query
- `find_similar_cards(embeddings, card_name, is_reversed, top_k, system, include_same_card)` - Find similar cards
- `display_search_results(results, cards_data, output_format, system, interpretations_data, show_art)` - Display results with optional ASCII art
- `cosine_similarity(vec1, vec2)` - Calculate similarity between embeddings
- `format_results_as_data(results, output_format)` - Convert to JSON/YAML
- `interactive_search()` - Interactive search loop

### generate_embeddings.py
- `create_card_text_for_system(card, interpretations, position, system)` - Generate text for specific system
- `generate_embeddings(client, cards, interpretations)` - Create all 780 embeddings

## Important Constants

```python
# Interpretation system keys
INTERPRETATION_SYSTEMS = {
    'rws_traditional': 'Rider-Waite-Smith (Traditional)',
    'thoth_crowley': 'Thoth/Crowley (Esoteric)',
    'jungian_psychological': 'Jungian/Psychological (Archetypes)',
    'modern_intuitive': 'Modern/Intuitive (Contemporary)'
}

# Embedding systems (includes 'combined' as 5th system)
# Used in search_cards.py and generate_embeddings.py

# Major Arcana card list
MAJOR_ARCANA = ["The Fool", "The Magician", ..., "The World"]  # 22 cards
```

## Working with Embeddings

**System Filtering:**
The embedding system allows searching within specific interpretation traditions. Each card has separate embeddings for each system, so a search for "shadow work" in `jungian_psychological` will prioritize cards with relevant Jungian interpretations.

**Similarity Exclusion:**
By default, `find_similar_cards()` excludes the same card in both positions to show truly different cards. Use `include_same_card=True` to include the opposite position.

**Cost Considerations:**
- Regenerating all embeddings costs ~$0.05-0.10 via OpenAI API
- Search queries cost minimal tokens (~$0.0001 per search)
- Embeddings use `text-embedding-3-small` model (1536 dimensions)

## Testing Notes

- Tests are in `tests/` directory
- `conftest.py` adds parent directory to Python path
- Test files: `test_search.py`, `test_embeddings.py`, `test_output_formats.py`, `test_data_validation.py`
- Tests require all dependencies from requirements.txt
- Some tests may require OPENAI_API_KEY environment variable for embedding generation tests
