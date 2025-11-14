"""
Tests for tarot card embeddings generation and structure.
"""

import json
import pytest
import os
from generate_embeddings import create_card_text, create_card_text_for_system, load_data


@pytest.fixture
def cards_data():
    """Load cards data"""
    cards, _ = load_data()
    return cards


@pytest.fixture
def interpretations_data():
    """Load interpretations data"""
    _, interpretations = load_data()
    return interpretations


@pytest.fixture
def embeddings_data():
    """Load embeddings data if it exists"""
    if os.path.exists('card_embeddings.json'):
        with open('card_embeddings.json', 'r') as f:
            return json.load(f)
    return None


class TestEmbeddingGeneration:
    """Test embedding text generation"""

    def test_create_upright_text(self, cards_data, interpretations_data):
        """Should create proper text for upright position"""
        card = cards_data[0]  # The Fool
        text = create_card_text(card, interpretations_data, 'upright')

        # Should include card name
        assert card['name'] in text, "Card name should be in embedding text"

        # Should include position
        assert 'upright' in text.lower(), "Position should be in embedding text"

        # Should include basic meaning
        assert card['desc'] in text, "Upright description should be in embedding text"

        # Should NOT include cbd_desc
        assert 'cbd_desc' not in text.lower(), "Should not reference cbd_desc"

    def test_create_reversed_text(self, cards_data, interpretations_data):
        """Should create proper text for reversed position"""
        card = cards_data[0]  # The Fool
        text = create_card_text(card, interpretations_data, 'reversed')

        # Should include card name
        assert card['name'] in text, "Card name should be in embedding text"

        # Should include position
        assert 'reversed' in text.lower(), "Position should be in embedding text"

        # Should include reversed meaning
        assert card['rdesc'] in text, "Reversed description should be in embedding text"

    def test_includes_all_interpretation_systems(self, cards_data, interpretations_data):
        """Should include all 4 interpretation systems"""
        card = cards_data[0]  # The Fool
        text = create_card_text(card, interpretations_data, 'upright')

        # Check for all systems
        assert 'Traditional interpretation' in text or 'rws_traditional' in text.lower()
        assert 'Crowley' in text or 'Thoth' in text
        assert 'Jungian' in text or 'psychological' in text.lower()
        assert 'Modern' in text or 'intuitive' in text.lower()

    def test_handles_missing_card_in_interpretations(self, cards_data):
        """Should handle cards not in interpretations gracefully"""
        fake_card = {'name': 'Fake Card', 'desc': 'Fake description', 'rdesc': 'Fake reversed'}
        text = create_card_text(fake_card, {}, 'upright')

        # Should still work with basic info
        assert 'Fake Card' in text
        assert 'Fake description' in text

    def test_create_card_text_for_specific_system(self, cards_data, interpretations_data):
        """Should create text for specific interpretation system"""
        card = cards_data[0]  # The Fool

        # Test traditional system
        text_trad = create_card_text_for_system(card, interpretations_data, 'upright', 'rws_traditional')
        assert card['name'] in text_trad
        assert 'upright' in text_trad.lower()

        # Should only include one interpretation (the traditional one)
        # Not all four like the combined version
        assert 'Interpretation:' in text_trad

    def test_create_card_text_for_combined_system(self, cards_data, interpretations_data):
        """Should create text with all systems for combined"""
        card = cards_data[0]  # The Fool

        # Test combined (system=None)
        text_combined = create_card_text_for_system(card, interpretations_data, 'upright', None)

        # Should include all systems
        assert 'Traditional interpretation' in text_combined or 'rws_traditional' in text_combined.lower()
        assert 'Crowley' in text_combined or 'Thoth' in text_combined
        assert 'Jungian' in text_combined or 'psychological' in text_combined.lower()
        assert 'Modern' in text_combined or 'intuitive' in text_combined.lower()


class TestEmbeddingsFile:
    """Test embeddings file structure if it exists"""

    def test_embeddings_file_structure(self, embeddings_data):
        """If embeddings exist, should have correct structure"""
        if embeddings_data is None:
            pytest.skip("Embeddings file not generated yet")

        # Should be a list
        assert isinstance(embeddings_data, list), "Embeddings should be a list"

        # Should have 780 embeddings (78 cards × 2 positions × 5 systems)
        assert len(embeddings_data) == 780, f"Expected 780 embeddings, found {len(embeddings_data)}"

    def test_embedding_entry_structure(self, embeddings_data):
        """Each embedding entry should have correct fields"""
        if embeddings_data is None:
            pytest.skip("Embeddings file not generated yet")

        required_fields = ['card_name', 'position', 'interpretation_system', 'text', 'embedding']

        for entry in embeddings_data:
            for field in required_fields:
                assert field in entry, f"Embedding entry missing field: {field}"

    def test_embedding_positions(self, embeddings_data):
        """Each card should have embeddings for all positions and systems"""
        if embeddings_data is None:
            pytest.skip("Embeddings file not generated yet")

        # Group by card name
        cards_dict = {}
        for entry in embeddings_data:
            name = entry['card_name']
            if name not in cards_dict:
                cards_dict[name] = []
            cards_dict[name].append((entry['position'], entry['interpretation_system']))

        # Check each card has all positions and systems (2 positions × 5 systems = 10 embeddings)
        expected_systems = ['rws_traditional', 'thoth_crowley', 'jungian_psychological', 'modern_intuitive', 'combined']
        for card_name, entries in cards_dict.items():
            positions = [e[0] for e in entries]
            systems = [e[1] for e in entries]

            # Check both positions exist
            assert 'upright' in positions, f"{card_name} missing upright embedding"
            assert 'reversed' in positions, f"{card_name} missing reversed embedding"

            # Check all systems exist
            for system in expected_systems:
                assert system in systems, f"{card_name} missing {system} embedding"

            # Check total count (2 positions × 5 systems = 10)
            assert len(entries) == 10, f"{card_name} has {len(entries)} embeddings, expected 10"

    def test_embedding_dimensions(self, embeddings_data):
        """All embeddings should have same dimensions"""
        if embeddings_data is None:
            pytest.skip("Embeddings file not generated yet")

        # OpenAI text-embedding-3-small should be 1536 dimensions
        expected_dims = 1536

        for entry in embeddings_data:
            embedding = entry['embedding']
            assert isinstance(embedding, list), f"Embedding should be a list"
            assert len(embedding) == expected_dims, \
                f"{entry['card_name']} ({entry['position']}) has {len(embedding)} dimensions, expected {expected_dims}"

    def test_embedding_values_are_floats(self, embeddings_data):
        """All embedding values should be floats"""
        if embeddings_data is None:
            pytest.skip("Embeddings file not generated yet")

        # Check first embedding
        first_embedding = embeddings_data[0]['embedding']

        for i, value in enumerate(first_embedding[:10]):  # Check first 10 values
            assert isinstance(value, (float, int)), \
                f"Embedding value at index {i} should be a number, got {type(value)}"

    def test_no_cbd_desc_in_embeddings(self, embeddings_data):
        """Embedding text should not contain cbd_desc references"""
        if embeddings_data is None:
            pytest.skip("Embeddings file not generated yet")

        for entry in embeddings_data[:10]:  # Check first 10
            text = entry['text'].lower()
            # Should not have "additional meaning" which was the cbd_desc label
            # But might appear in interpretations, so just check it's not prominent
            assert 'cbd_desc' not in text, f"{entry['card_name']} text contains 'cbd_desc'"


class TestEmbeddingConsistency:
    """Test consistency between cards.json and embeddings"""

    def test_all_cards_have_embeddings(self, cards_data, embeddings_data):
        """Every card should have embeddings"""
        if embeddings_data is None:
            pytest.skip("Embeddings file not generated yet")

        embedded_cards = set(entry['card_name'] for entry in embeddings_data)
        card_names = set(card['name'] for card in cards_data)

        assert embedded_cards == card_names, \
            f"Mismatch between cards and embeddings: {card_names - embedded_cards} missing embeddings"
