# Tarot Card Vector Embeddings & Semantic Search

This project includes vector embeddings for semantic search of tarot cards.

## Overview

Vector embeddings allow you to:
- Search for cards by theme, concept, or feeling (e.g., "new beginnings", "letting go")
- Find cards semantically similar to a given card
- Discover thematic relationships between cards
- Filter searches by interpretation system (Traditional, Crowley, Jungian, Modern)

Each card has **10 embeddings** (2 positions × 5 systems):
- Separate embeddings for upright and reversed positions
- Separate embeddings for each of the 4 interpretation systems
- A combined embedding that includes all systems together
- This allows you to search within a specific tarot tradition or across all traditions

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set OpenAI API Key

```bash
export OPENAI_API_KEY='your-api-key-here'
```

### 3. Generate Embeddings

Run the embedding generation script (this only needs to be done once):

```bash
python generate_embeddings.py
```

This will:
- Process all 78 tarot cards (780 embeddings total: 78 cards × 2 positions × 5 systems)
- Create embeddings for each of the 4 interpretation systems plus a combined version
- Create embeddings using OpenAI's `text-embedding-3-small` model
- Save results to `card_embeddings.json`

**Interpretation Systems:**
- `rws_traditional` - Rider-Waite-Smith (Traditional)
- `thoth_crowley` - Thoth/Crowley (Esoteric)
- `jungian_psychological` - Jungian/Psychological (Archetypes)
- `modern_intuitive` - Modern/Intuitive (Contemporary)
- `combined` - All systems combined (default)

**Note:** This will make API calls to OpenAI and will incur costs (approximately $0.05-0.10 total).

## Usage

The search tool supports both command-line (non-interactive) and interactive modes.

### Command-Line Mode (Recommended)

#### Semantic Search

Search for cards by theme, concept, or feeling:

```bash
# Basic search
python3 search_cards.py "new beginnings"

# More examples
python3 search_cards.py "letting go of the past"
python3 search_cards.py "inner strength and courage"
python3 search_cards.py "confusion and uncertainty"
```

#### Find Similar Cards

Find cards similar to a specific card:

```bash
# Find cards similar to The Fool (upright)
python3 search_cards.py --similar "The Fool"

# Find cards similar to The Tower (reversed)
python3 search_cards.py --similar "The Tower" --reversed

# Get more results (default is 1)
python3 search_cards.py --similar "The Star" --top 5
python3 search_cards.py "love" --top 10

# Include the same card's opposite position in results
python3 search_cards.py --similar "The Fool" --include-same-card --top 5
```

**Note:** By default, the same card (in both upright and reversed positions) is excluded from similar results to show truly different cards. Use `--include-same-card` to include the opposite position.

#### Output Formats

Get results in JSON or YAML format for scripting and integration:

```bash
# JSON output
python3 search_cards.py "new beginnings" --json

# YAML output
python3 search_cards.py --similar "The Tower" --yaml

# Combine with other options
python3 search_cards.py "transformation" --json --top 10
python3 search_cards.py --similar "The Star" --reversed --yaml
```

**JSON output example:**
```json
[
  {
    "card_name": "Eight of Swords",
    "position": "reversed",
    "similarity": 0.3657,
    "meaning": "New beginnings. Freedom from the past bondage."
  },
  {
    "card_name": "Judgement",
    "position": "upright",
    "similarity": 0.3566,
    "meaning": "Radical change, resurrection to a new life..."
  }
]
```

**YAML output example:**
```yaml
- card_name: Eight of Swords
  position: reversed
  similarity: 0.3657
  meaning: New beginnings. Freedom from the past bondage.
- card_name: Judgement
  position: upright
  similarity: 0.3566
  meaning: Radical change, resurrection to a new life...
```

#### System Filtering

Filter results by interpretation system:

```bash
# Search within Traditional (RWS) system only
python3 search_cards.py "new beginnings" --system rws_traditional

# Find similar cards using Crowley/Thoth interpretations
python3 search_cards.py --similar "The Fool" --system thoth_crowley

# Search within Jungian/psychological framework
python3 search_cards.py "shadow work" --system jungian_psychological --top 3

# Modern/intuitive system
python3 search_cards.py "personal growth" --system modern_intuitive

# Combined system (default - uses all interpretations)
python3 search_cards.py "transformation" --system combined
```

**Available Systems:**
- `rws_traditional` - Rider-Waite-Smith (Traditional)
- `thoth_crowley` - Thoth/Crowley (Esoteric)
- `jungian_psychological` - Jungian/Psychological (Archetypes)
- `modern_intuitive` - Modern/Intuitive (Contemporary)
- `combined` - All systems combined (default)

#### Options

```bash
python3 search_cards.py --help

Options:
  -h, --help            Show help message
  --similar CARD, -s    Find cards similar to the specified card
  --reversed, -r        Use reversed position (for --similar mode)
  --include-same-card   Include same card in opposite position in similar results
  --top N, -k N         Number of results to return (default: 1)
  --system SYSTEM       Filter by interpretation system (default: combined)
                        Choices: rws_traditional, thoth_crowley, jungian_psychological,
                                modern_intuitive, combined
  --json                Output results in JSON format
  --yaml                Output results in YAML format
  --interactive, -i     Launch interactive search mode
```

### Interactive Search Mode

Launch the interactive interface:

```bash
python3 search_cards.py --interactive
# or just:
python3 search_cards.py
```

In interactive mode, you can:
- Enter search queries directly
- Use `/similar <card name>` to find similar cards
- Use `/quit` to exit

## Example Searches

### By Theme
- `"new beginnings"` → Eight of Swords (reversed), Judgement, Ace of Pentacles
- `"love and relationships"` → The Lovers, Two of Cups, Ace of Cups
- `"difficult choices"` → Two of Swords, The Lovers (reversed), Seven of Cups

### By Feeling
- `"hopeful and optimistic"` → The Star, The Sun, Three of Cups
- `"anxious and worried"` → Nine of Swords, The Moon, Five of Pentacles
- `"powerful and confident"` → The Emperor, Strength, King of Wands

### By Concept
- `"transformation and change"` → Death, The Tower, Judgement
- `"wisdom and intuition"` → The High Priestess, The Hermit, King of Cups
- `"material success"` → Ten of Pentacles, Four of Wands, Ace of Pentacles

## Real-World Usage Examples

### Example 1: Finding Guidance for a Specific Situation

```bash
# You're starting a new job and want guidance
python3 search_cards.py "new opportunities and growth" --top 3

# Output: Ace of Wands, The Fool, Three of Wands
```

### Example 2: Exploring Card Relationships

```bash
# Understand what cards are thematically similar to Death
python3 search_cards.py --similar "Death" --top 5

# Output: Ten of Swords, The Tower, Judgement, etc.
# (Notice The Tower is similar - both represent sudden transformation)
```

### Example 3: Scripting and Automation

```bash
# Save search results to a file
python3 search_cards.py "inner peace" --json > peace_cards.json

# Parse with jq to get just card names
python3 search_cards.py "strength" --json --top 3 | jq '.[].card_name'

# Use in a shell script
CARD=$(python3 search_cards.py "wisdom" --json | jq -r '.[0].card_name')
echo "Today's wisdom card: $CARD"
```

### Example 4: Comparing Search Results

```bash
# Find cards for different emotional states
python3 search_cards.py "anxiety" --yaml > anxiety.yaml
python3 search_cards.py "peace" --yaml > peace.yaml

# Compare what cards appear for opposite states
```

### Example 5: Comparing Interpretation Systems

```bash
# Find cards related to "shadow" in Jungian framework
python3 search_cards.py "shadow self" --system jungian_psychological --top 3

# Compare with Traditional interpretation
python3 search_cards.py "shadow self" --system rws_traditional --top 3

# See how Crowley/Thoth system interprets the same theme
python3 search_cards.py "shadow self" --system thoth_crowley --top 3

# Different systems may emphasize different cards for the same concept
```

### Example 6: Building a Custom Application

```python
import json
import subprocess

def get_card_for_theme(theme, system='combined'):
    """Get the top card for a given theme"""
    result = subprocess.run(
        ['python3', 'search_cards.py', theme, '--json', '--system', system],
        capture_output=True,
        text=True
    )
    cards = json.loads(result.stdout)
    return cards[0] if cards else None

# Use in your application
card = get_card_for_theme("new beginnings", system='jungian_psychological')
print(f"Card: {card['card_name']} ({card['position']})")
print(f"Meaning: {card['meaning']}")
print(f"Similarity: {card['similarity']:.2f}")
```

## Technical Details

### Embedding Model
- **Model:** OpenAI `text-embedding-3-small`
- **Dimensions:** 1536
- **Cost:** ~$0.02 per 1 million tokens

### Similarity Metric
- **Method:** Cosine similarity
- **Range:** -1 to 1 (1 = most similar, -1 = most dissimilar)
- **Typical scores:** 0.5-0.9 for related cards

### Data Structure

Each embedding in `card_embeddings.json` contains:
```json
{
  "card_name": "The Fool",
  "position": "upright",
  "interpretation_system": "combined",
  "text": "Combined text used for embedding...",
  "embedding": [0.123, -0.456, ...]
}
```

The file contains 780 embeddings total:
- 78 cards × 2 positions (upright/reversed) × 5 systems = 780 embeddings
- Systems: `rws_traditional`, `thoth_crowley`, `jungian_psychological`, `modern_intuitive`, `combined`

## Files

- `generate_embeddings.py` - Script to generate embeddings
- `search_cards.py` - Interactive search interface
- `card_embeddings.json` - Generated embeddings (created after running generate_embeddings.py)
- `requirements.txt` - Python dependencies

## Future Enhancements

Possible additions:
- Integration with the main `tarot.py` app
- Batch search capabilities
- Visualization of card relationships
- Export to vector databases (Pinecone, Weaviate, etc.)
- Fine-tuning on tarot-specific corpus
