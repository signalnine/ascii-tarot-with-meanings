#!/usr/bin/env python3
"""
Generate vector embeddings for tarot cards using OpenAI's embedding API.
Creates separate embeddings for upright and reversed positions.
"""

import json
import os
from typing import List, Dict
from openai import OpenAI

# Configuration
CARDS_FILE = 'cards.json'
INTERPRETATIONS_FILE = 'interpretations.json'
EMBEDDINGS_OUTPUT_FILE = 'card_embeddings.json'

def load_data():
    """Load cards and interpretations data"""
    with open(CARDS_FILE, 'r') as f:
        cards = json.load(f)

    with open(INTERPRETATIONS_FILE, 'r') as f:
        interpretations = json.load(f)

    return cards, interpretations

def create_card_text(card: Dict, interpretations: Dict, position: str = 'upright') -> str:
    """
    Create comprehensive text representation of a card for embedding.

    Args:
        card: Card data from cards.json
        interpretations: Interpretation data from interpretations.json
        position: 'upright' or 'reversed'

    Returns:
        Combined text for embedding
    """
    card_name = card['name']

    # Start with card name
    parts = [f"Card: {card_name}"]
    parts.append(f"Position: {position}")

    # Add basic meanings from cards.json
    if position == 'upright':
        if 'desc' in card and card['desc']:
            parts.append(f"Basic meaning: {card['desc']}")
    else:
        if 'rdesc' in card and card['rdesc']:
            parts.append(f"Basic meaning: {card['rdesc']}")

    # Add interpretations from all systems
    if card_name in interpretations:
        card_interp = interpretations[card_name]

        # Rider-Waite-Smith Traditional
        if 'rws_traditional' in card_interp:
            rws = card_interp['rws_traditional'].get(position, '')
            if rws:
                parts.append(f"Traditional interpretation: {rws}")

        # Thoth/Crowley
        if 'thoth_crowley' in card_interp:
            thoth = card_interp['thoth_crowley'].get(position, '')
            if thoth:
                parts.append(f"Crowley/Thoth interpretation: {thoth}")

        # Jungian/Psychological
        if 'jungian_psychological' in card_interp:
            jungian = card_interp['jungian_psychological'].get(position, '')
            if jungian:
                parts.append(f"Jungian/psychological interpretation: {jungian}")

        # Modern/Intuitive
        if 'modern_intuitive' in card_interp:
            modern = card_interp['modern_intuitive'].get(position, '')
            if modern:
                parts.append(f"Modern/intuitive interpretation: {modern}")

    return "\n".join(parts)

def generate_embeddings(client: OpenAI, cards: List[Dict], interpretations: Dict) -> List[Dict]:
    """
    Generate embeddings for all cards (both upright and reversed).

    Returns:
        List of embedding records with metadata
    """
    embeddings_data = []

    for card in cards:
        card_name = card['name']
        print(f"Processing: {card_name}")

        # Generate upright embedding
        upright_text = create_card_text(card, interpretations, 'upright')
        print(f"  - Generating upright embedding...")

        try:
            upright_response = client.embeddings.create(
                model="text-embedding-3-small",
                input=upright_text
            )

            upright_embedding = upright_response.data[0].embedding

            embeddings_data.append({
                'card_name': card_name,
                'position': 'upright',
                'text': upright_text,
                'embedding': upright_embedding
            })

        except Exception as e:
            print(f"  ✗ Error generating upright embedding: {e}")

        # Generate reversed embedding
        reversed_text = create_card_text(card, interpretations, 'reversed')
        print(f"  - Generating reversed embedding...")

        try:
            reversed_response = client.embeddings.create(
                model="text-embedding-3-small",
                input=reversed_text
            )

            reversed_embedding = reversed_response.data[0].embedding

            embeddings_data.append({
                'card_name': card_name,
                'position': 'reversed',
                'text': reversed_text,
                'embedding': reversed_embedding
            })

        except Exception as e:
            print(f"  ✗ Error generating reversed embedding: {e}")

    return embeddings_data

def save_embeddings(embeddings_data: List[Dict], output_file: str):
    """Save embeddings to JSON file"""
    with open(output_file, 'w') as f:
        json.dump(embeddings_data, f, indent=2)

    print(f"\n✓ Saved {len(embeddings_data)} embeddings to {output_file}")

def main():
    """Main execution"""
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY='your-key-here'")
        return

    print("=" * 50)
    print("Tarot Card Embedding Generator")
    print("Using OpenAI text-embedding-3-small model")
    print("=" * 50)
    print()

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Load data
    print("Loading card data...")
    cards, interpretations = load_data()
    print(f"✓ Loaded {len(cards)} cards")
    print()

    # Generate embeddings
    print("Generating embeddings...")
    print(f"(Creating {len(cards) * 2} embeddings: upright + reversed)")
    print()
    embeddings_data = generate_embeddings(client, cards, interpretations)

    # Save results
    save_embeddings(embeddings_data, EMBEDDINGS_OUTPUT_FILE)

    print()
    print("=" * 50)
    print("Done!")
    print("=" * 50)

if __name__ == "__main__":
    main()
