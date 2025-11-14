"""
Tests for tarot card search functionality.
"""

import json
import pytest
import os
import numpy as np
from search_cards import (
    cosine_similarity,
    load_embeddings,
    load_cards,
    find_similar_cards
)


@pytest.fixture
def embeddings_data():
    """Load embeddings data if it exists"""
    if os.path.exists('card_embeddings.json'):
        return load_embeddings()
    return None


@pytest.fixture
def cards_data():
    """Load cards data"""
    return load_cards()


class TestCosineSimilarity:
    """Test cosine similarity calculation"""

    def test_identical_vectors(self):
        """Identical vectors should have similarity of 1.0"""
        vec = [1.0, 2.0, 3.0, 4.0]
        similarity = cosine_similarity(vec, vec)
        assert abs(similarity - 1.0) < 1e-10, "Identical vectors should have similarity 1.0"

    def test_orthogonal_vectors(self):
        """Orthogonal vectors should have similarity of 0.0"""
        vec1 = [1.0, 0.0]
        vec2 = [0.0, 1.0]
        similarity = cosine_similarity(vec1, vec2)
        assert abs(similarity - 0.0) < 1e-10, "Orthogonal vectors should have similarity 0.0"

    def test_opposite_vectors(self):
        """Opposite vectors should have similarity of -1.0"""
        vec1 = [1.0, 2.0, 3.0]
        vec2 = [-1.0, -2.0, -3.0]
        similarity = cosine_similarity(vec1, vec2)
        assert abs(similarity - (-1.0)) < 1e-10, "Opposite vectors should have similarity -1.0"

    def test_similar_vectors(self):
        """Similar vectors should have high positive similarity"""
        vec1 = [1.0, 2.0, 3.0]
        vec2 = [1.1, 2.1, 2.9]
        similarity = cosine_similarity(vec1, vec2)
        assert 0.9 < similarity <= 1.0, f"Similar vectors should have high similarity, got {similarity}"

    def test_zero_vector(self):
        """Zero vector should return 0.0 similarity"""
        vec1 = [0.0, 0.0, 0.0]
        vec2 = [1.0, 2.0, 3.0]
        similarity = cosine_similarity(vec1, vec2)
        assert similarity == 0.0, "Zero vector should have similarity 0.0"

    def test_numpy_conversion(self):
        """Should work with lists (converted to numpy arrays internally)"""
        vec1 = [1.0, 2.0, 3.0]
        vec2 = [4.0, 5.0, 6.0]
        similarity = cosine_similarity(vec1, vec2)
        assert isinstance(similarity, (float, np.floating)), "Should return a float"


class TestLoadFunctions:
    """Test data loading functions"""

    def test_load_embeddings_returns_list(self, embeddings_data):
        """load_embeddings should return a list"""
        if embeddings_data is None:
            pytest.skip("Embeddings file not generated yet")

        assert isinstance(embeddings_data, list), "load_embeddings should return a list"

    def test_load_cards_returns_list(self, cards_data):
        """load_cards should return a list"""
        assert isinstance(cards_data, list), "load_cards should return a list"
        assert len(cards_data) == 78, "Should load 78 cards"

    def test_load_embeddings_file_not_found(self):
        """Should raise FileNotFoundError if embeddings don't exist"""
        # Temporarily rename file if it exists
        embeddings_exists = os.path.exists('card_embeddings.json')
        if embeddings_exists:
            pytest.skip("Embeddings file exists, can't test FileNotFoundError")

        with pytest.raises(FileNotFoundError):
            load_embeddings()


class TestFindSimilarCards:
    """Test finding similar cards"""

    def test_find_similar_to_fool(self, embeddings_data):
        """Should find cards similar to The Fool"""
        if embeddings_data is None:
            pytest.skip("Embeddings file not generated yet")

        results = find_similar_cards(
            card_name="The Fool",
            position="upright",
            embeddings_data=embeddings_data,
            top_k=5
        )

        # Should return 5 results (excluding The Fool itself)
        assert len(results) == 5, f"Expected 5 results, got {len(results)}"

        # Each result should be a tuple of (card_name, position, similarity)
        for result in results:
            assert len(result) == 3, "Each result should be a 3-tuple"
            card_name, position, similarity = result
            assert isinstance(card_name, str), "Card name should be a string"
            assert position in ['upright', 'reversed'], f"Invalid position: {position}"
            assert isinstance(similarity, (float, np.floating)), "Similarity should be a float"
            assert -1.0 <= similarity <= 1.0, f"Similarity should be between -1 and 1, got {similarity}"

    def test_find_similar_excludes_same_card(self, embeddings_data):
        """Should exclude the same card (both positions) from results by default"""
        if embeddings_data is None:
            pytest.skip("Embeddings file not generated yet")

        results = find_similar_cards(
            card_name="The Fool",
            position="upright",
            embeddings_data=embeddings_data,
            top_k=10
        )

        # The Fool (both upright and reversed) should not be in results
        for card_name, position, similarity in results:
            assert card_name != "The Fool", \
                f"The Fool ({position}) should be excluded from its own similar cards by default"

    def test_find_similar_includes_same_card(self, embeddings_data):
        """Should include the same card (both positions) when exclude_same_card=False"""
        if embeddings_data is None:
            pytest.skip("Embeddings file not generated yet")

        results = find_similar_cards(
            card_name="The Fool",
            position="upright",
            embeddings_data=embeddings_data,
            top_k=5,
            exclude_same_card=False,
            exclude_self=True
        )

        # First result should be The Fool reversed (highest similarity besides exact match)
        card_name, position, similarity = results[0]
        assert card_name == "The Fool", "First result should be The Fool (reversed)"
        assert position == "reversed", "Should be reversed"
        assert 0.7 < similarity < 1.0, f"Reversed similarity should be high, got {similarity}"

    def test_find_similar_sorted_by_similarity(self, embeddings_data):
        """Results should be sorted by similarity (highest first)"""
        if embeddings_data is None:
            pytest.skip("Embeddings file not generated yet")

        results = find_similar_cards(
            card_name="The Fool",
            position="upright",
            embeddings_data=embeddings_data,
            top_k=10
        )

        # Check that similarities are in descending order
        similarities = [result[2] for result in results]
        assert similarities == sorted(similarities, reverse=True), \
            "Results should be sorted by similarity in descending order"

    def test_find_similar_invalid_card(self, embeddings_data):
        """Should raise ValueError for invalid card"""
        if embeddings_data is None:
            pytest.skip("Embeddings file not generated yet")

        with pytest.raises(ValueError):
            find_similar_cards(
                card_name="Nonexistent Card",
                position="upright",
                embeddings_data=embeddings_data
            )

    def test_find_similar_different_positions(self, embeddings_data):
        """Should handle finding similar cards across positions"""
        if embeddings_data is None:
            pytest.skip("Embeddings file not generated yet")

        upright_results = find_similar_cards(
            card_name="The Fool",
            position="upright",
            embeddings_data=embeddings_data,
            top_k=5
        )

        reversed_results = find_similar_cards(
            card_name="The Fool",
            position="reversed",
            embeddings_data=embeddings_data,
            top_k=5
        )

        # Results should be different for upright vs reversed
        assert upright_results != reversed_results, \
            "Upright and reversed should have different similar cards"


class TestEmbeddingQuality:
    """Test quality and sanity of embeddings"""

    def test_related_cards_are_similar(self, embeddings_data):
        """Related cards should have higher similarity"""
        if embeddings_data is None:
            pytest.skip("Embeddings file not generated yet")

        # The Fool and The Magician are sequential in Major Arcana
        # They should have some similarity (using combined system)
        fool_embedding = None
        magician_embedding = None

        for entry in embeddings_data:
            if (entry['card_name'] == 'The Fool' and
                entry['position'] == 'upright' and
                entry.get('interpretation_system', 'combined') == 'combined'):
                fool_embedding = entry['embedding']
            if (entry['card_name'] == 'The Magician' and
                entry['position'] == 'upright' and
                entry.get('interpretation_system', 'combined') == 'combined'):
                magician_embedding = entry['embedding']

        if fool_embedding and magician_embedding:
            similarity = cosine_similarity(fool_embedding, magician_embedding)
            # They should have some positive similarity (not exact threshold)
            assert similarity > 0, f"Related cards should have positive similarity, got {similarity}"

    def test_upright_vs_reversed_different(self, embeddings_data):
        """Upright and reversed positions should have different embeddings"""
        if embeddings_data is None:
            pytest.skip("Embeddings file not generated yet")

        # Get The Fool upright and reversed (using combined system)
        fool_upright = None
        fool_reversed = None

        for entry in embeddings_data:
            if (entry['card_name'] == 'The Fool' and
                entry.get('interpretation_system', 'combined') == 'combined'):
                if entry['position'] == 'upright':
                    fool_upright = entry['embedding']
                elif entry['position'] == 'reversed':
                    fool_reversed = entry['embedding']

        if fool_upright and fool_reversed:
            similarity = cosine_similarity(fool_upright, fool_reversed)
            # They should be similar but not identical
            assert 0.3 < similarity < 0.99, \
                f"Upright and reversed should be related but distinct, got {similarity}"


class TestSystemFiltering:
    """Test interpretation system filtering"""

    def test_find_similar_with_system_filter(self, embeddings_data):
        """Should find similar cards within specific interpretation system"""
        if embeddings_data is None:
            pytest.skip("Embeddings file not generated yet")

        # Test with traditional system
        results_trad = find_similar_cards(
            card_name="The Fool",
            position="upright",
            embeddings_data=embeddings_data,
            top_k=5,
            system_filter="rws_traditional"
        )

        assert len(results_trad) == 5, f"Expected 5 results, got {len(results_trad)}"

        # Test with Crowley system
        results_crowley = find_similar_cards(
            card_name="The Fool",
            position="upright",
            embeddings_data=embeddings_data,
            top_k=5,
            system_filter="thoth_crowley"
        )

        assert len(results_crowley) == 5, f"Expected 5 results, got {len(results_crowley)}"

        # Results should potentially differ between systems
        # (though not guaranteed - just checking they both work)

    def test_find_similar_combined_system(self, embeddings_data):
        """Should work with combined system (default)"""
        if embeddings_data is None:
            pytest.skip("Embeddings file not generated yet")

        results = find_similar_cards(
            card_name="The Fool",
            position="upright",
            embeddings_data=embeddings_data,
            top_k=5,
            system_filter="combined"
        )

        assert len(results) == 5, f"Expected 5 results, got {len(results)}"
