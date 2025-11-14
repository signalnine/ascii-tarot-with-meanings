# ASCII Tarot Reader

A comprehensive interactive tarot reading application featuring beautiful ASCII art cards with detailed interpretations.

<img src='cards.gif' />

## Features

### 📖 Multiple Reading Types
- **Single Card Reading** - Quick one-card draw for daily guidance
- **Three Card Reading** - Past, Present, Future spread
- **Celtic Cross** - Traditional 10-card spread for in-depth readings
- **Horseshoe Spread** - 7-card spread for focused questions
- **Yes/No Reading** - Simple binary answer to your question
- **Relationship Reading** - 5-card spread for relationship insights
- **Daily Card** - Get a consistent card for the entire day

### 🔮 Card Features
- **Reversed Cards** - Cards can appear upright or reversed with different meanings
- **Full Interpretations** - Each card includes multiple interpretation contexts
- **ASCII Art** - Beautiful ASCII artwork for each card
- **Major & Minor Arcana** - Complete tarot deck with all traditional cards

### 🔍 Search & Browse
- **Search by Name** - Find any card by its exact name
- **Keyword Search** - Search through all card descriptions
- **List All Cards** - View complete deck organized by arcana
- **Filter by Arcana** - View only Major or Minor Arcana cards

### 📚 Reading History
- **Save Readings** - Save any reading to your personal history
- **View History** - Review your last 10 saved readings
- **Timestamped Records** - Each reading is saved with date and time

## Usage

Run the interactive menu:

```bash
python3 tarot.py
```

Follow the on-screen menu to:
1. Choose a reading type
2. View your cards with interpretations
3. Save readings to history
4. Search and explore the deck

## Data Files

The application uses:
- `cards.json` - Complete tarot deck data with ASCII art
- `reading_history.json` - Your saved readings (auto-generated)
- `daily_card.json` - Daily card persistence (auto-generated)

## Example

```python
import json
from tarot import draw_card, display_card, search_card

# Draw a random card
card, is_reversed = draw_card()
display_card(card, is_reversed)

# Search for a specific card
search_card('The High Priestess')
```

## Requirements

- Python 3.6+
- No external dependencies required

## Card Structure

Each card in the JSON deck includes:
- `name` - Card name
- `desc` - Upright meaning
- `rdesc` - Reversed meaning
- `cbd_desc` - Additional interpretation context
- `card` - ASCII art (upright)
- `reversed` - ASCII art (reversed)

