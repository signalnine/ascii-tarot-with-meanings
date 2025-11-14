"""
Tests for JSON and YAML output formats in search_cards.py
"""

import json
import pytest
import os
from search_cards import format_results_as_data, display_search_results
from io import StringIO
import sys

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


@pytest.fixture
def sample_results():
    """Sample search results"""
    return [
        ("The Fool", "upright", 0.85),
        ("The Magician", "reversed", 0.72),
        ("The High Priestess", "upright", 0.68)
    ]


@pytest.fixture
def sample_cards():
    """Sample cards data"""
    return [
        {
            "name": "The Fool",
            "desc": "New beginnings, innocence, spontaneity",
            "rdesc": "Folly, failure, madness"
        },
        {
            "name": "The Magician",
            "desc": "Manifestation, resourcefulness, power",
            "rdesc": "Manipulation, poor planning"
        },
        {
            "name": "The High Priestess",
            "desc": "Intuition, sacred knowledge, divine feminine",
            "rdesc": "Hidden agendas, secrets"
        }
    ]


class TestFormatResultsAsData:
    """Test formatting results as structured data"""

    def test_format_basic_structure(self, sample_results, sample_cards):
        """Should format results as list of dictionaries"""
        formatted = format_results_as_data(sample_results, sample_cards)

        assert isinstance(formatted, list), "Should return a list"
        assert len(formatted) == 3, "Should have 3 results"

    def test_format_entry_fields(self, sample_results, sample_cards):
        """Each entry should have required fields"""
        formatted = format_results_as_data(sample_results, sample_cards)

        required_fields = ['card_name', 'position', 'similarity', 'meaning']
        for entry in formatted:
            for field in required_fields:
                assert field in entry, f"Entry missing field: {field}"

    def test_format_upright_meaning(self, sample_results, sample_cards):
        """Should use upright meaning for upright cards"""
        formatted = format_results_as_data(sample_results, sample_cards)

        fool_entry = formatted[0]
        assert fool_entry['card_name'] == "The Fool"
        assert fool_entry['position'] == "upright"
        assert fool_entry['meaning'] == "New beginnings, innocence, spontaneity"

    def test_format_reversed_meaning(self, sample_results, sample_cards):
        """Should use reversed meaning for reversed cards"""
        formatted = format_results_as_data(sample_results, sample_cards)

        magician_entry = formatted[1]
        assert magician_entry['card_name'] == "The Magician"
        assert magician_entry['position'] == "reversed"
        assert magician_entry['meaning'] == "Manipulation, poor planning"

    def test_format_similarity_as_float(self, sample_results, sample_cards):
        """Similarity should be converted to float"""
        formatted = format_results_as_data(sample_results, sample_cards)

        for entry in formatted:
            assert isinstance(entry['similarity'], float), "Similarity should be float"
            assert 0.0 <= entry['similarity'] <= 1.0, "Similarity should be between 0 and 1"

    def test_format_handles_missing_card(self, sample_results, sample_cards):
        """Should skip cards not found in cards data"""
        results_with_missing = sample_results + [("Nonexistent Card", "upright", 0.5)]
        formatted = format_results_as_data(results_with_missing, sample_cards)

        # Should only have 3 entries, skipping the nonexistent card
        assert len(formatted) == 3


class TestJSONOutput:
    """Test JSON output format"""

    def test_json_output_valid(self, sample_results, sample_cards):
        """JSON output should be valid JSON"""
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        display_search_results(sample_results, sample_cards, output_format='json')

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Should be valid JSON
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            pytest.fail("Output is not valid JSON")

        assert isinstance(data, list), "JSON should be a list"
        assert len(data) == 3, "Should have 3 entries"

    def test_json_no_extra_output(self, sample_results, sample_cards):
        """JSON output should not have status messages"""
        captured_output = StringIO()
        sys.stdout = captured_output

        display_search_results(sample_results, sample_cards, output_format='json')

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Should not contain human-readable headers
        assert "SEARCH RESULTS" not in output
        assert "======" not in output
        assert "Similarity:" not in output

    def test_json_structure(self, sample_results, sample_cards):
        """JSON should have correct structure"""
        captured_output = StringIO()
        sys.stdout = captured_output

        display_search_results(sample_results, sample_cards, output_format='json')

        sys.stdout = sys.__stdout__
        data = json.loads(captured_output.getvalue())

        first_entry = data[0]
        assert first_entry['card_name'] == "The Fool"
        assert first_entry['position'] == "upright"
        assert first_entry['similarity'] == 0.85
        assert first_entry['meaning'] == "New beginnings, innocence, spontaneity"


class TestYAMLOutput:
    """Test YAML output format"""

    @pytest.mark.skipif(not YAML_AVAILABLE, reason="pyyaml not installed")
    def test_yaml_output_valid(self, sample_results, sample_cards):
        """YAML output should be valid YAML"""
        captured_output = StringIO()
        sys.stdout = captured_output

        display_search_results(sample_results, sample_cards, output_format='yaml')

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Should be valid YAML
        try:
            data = yaml.safe_load(output)
        except yaml.YAMLError:
            pytest.fail("Output is not valid YAML")

        assert isinstance(data, list), "YAML should parse to a list"
        assert len(data) == 3, "Should have 3 entries"

    @pytest.mark.skipif(not YAML_AVAILABLE, reason="pyyaml not installed")
    def test_yaml_no_extra_output(self, sample_results, sample_cards):
        """YAML output should not have status messages"""
        captured_output = StringIO()
        sys.stdout = captured_output

        display_search_results(sample_results, sample_cards, output_format='yaml')

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Should not contain human-readable headers
        assert "SEARCH RESULTS" not in output
        assert "======" not in output
        assert "Similarity:" not in output

    @pytest.mark.skipif(not YAML_AVAILABLE, reason="pyyaml not installed")
    def test_yaml_structure(self, sample_results, sample_cards):
        """YAML should have correct structure"""
        captured_output = StringIO()
        sys.stdout = captured_output

        display_search_results(sample_results, sample_cards, output_format='yaml')

        sys.stdout = sys.__stdout__
        data = yaml.safe_load(captured_output.getvalue())

        first_entry = data[0]
        assert first_entry['card_name'] == "The Fool"
        assert first_entry['position'] == "upright"
        assert first_entry['similarity'] == 0.85
        assert first_entry['meaning'] == "New beginnings, innocence, spontaneity"


class TestHumanReadableOutput:
    """Test default human-readable output"""

    def test_human_readable_has_headers(self, sample_results, sample_cards):
        """Human-readable output should have formatting"""
        captured_output = StringIO()
        sys.stdout = captured_output

        display_search_results(sample_results, sample_cards, output_format=None)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Should contain human-readable formatting
        assert "SEARCH RESULTS" in output
        assert "======" in output
        assert "Similarity:" in output

    def test_human_readable_card_names(self, sample_results, sample_cards):
        """Should display card names with positions"""
        captured_output = StringIO()
        sys.stdout = captured_output

        display_search_results(sample_results, sample_cards, output_format=None)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert "The Fool (UPRIGHT)" in output
        assert "The Magician (REVERSED)" in output
        assert "The High Priestess (UPRIGHT)" in output

    def test_human_readable_similarity_scores(self, sample_results, sample_cards):
        """Should display similarity scores"""
        captured_output = StringIO()
        sys.stdout = captured_output

        display_search_results(sample_results, sample_cards, output_format=None)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert "0.8500" in output  # The Fool similarity
        assert "0.7200" in output  # The Magician similarity
