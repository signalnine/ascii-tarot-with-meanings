"""
Tests for validating tarot card data structure and content.
"""

import json
import pytest
import os


@pytest.fixture
def cards_data():
    """Load cards.json data"""
    with open('cards.json', 'r') as f:
        return json.load(f)


@pytest.fixture
def interpretations_data():
    """Load interpretations.json data"""
    with open('interpretations.json', 'r') as f:
        return json.load(f)


class TestCardsDataStructure:
    """Test cards.json structure and completeness"""

    def test_cards_json_exists(self):
        """cards.json file should exist"""
        assert os.path.exists('cards.json'), "cards.json file not found"

    def test_cards_is_list(self, cards_data):
        """cards.json should contain a list"""
        assert isinstance(cards_data, list), "cards.json should be a list"

    def test_has_78_cards(self, cards_data):
        """Should have exactly 78 cards in a standard tarot deck"""
        assert len(cards_data) == 78, f"Expected 78 cards, found {len(cards_data)}"

    def test_all_cards_have_required_fields(self, cards_data):
        """Every card should have all required fields"""
        required_fields = ['name', 'desc', 'rdesc', 'card', 'reversed']

        for card in cards_data:
            for field in required_fields:
                assert field in card, f"Card '{card.get('name', 'Unknown')}' missing field: {field}"

    def test_no_cbd_desc_field(self, cards_data):
        """cbd_desc field should be removed from all cards"""
        for card in cards_data:
            assert 'cbd_desc' not in card, f"Card '{card['name']}' still has cbd_desc field"

    def test_all_names_are_unique(self, cards_data):
        """Card names should be unique"""
        names = [card['name'] for card in cards_data]
        assert len(names) == len(set(names)), "Duplicate card names found"

    def test_all_names_are_non_empty(self, cards_data):
        """All card names should be non-empty strings"""
        for card in cards_data:
            assert card['name'], "Found card with empty name"
            assert isinstance(card['name'], str), f"Card name should be string: {card['name']}"

    def test_all_descriptions_are_non_empty(self, cards_data):
        """All upright descriptions should be non-empty"""
        for card in cards_data:
            assert card['desc'], f"Card '{card['name']}' has empty desc"
            assert isinstance(card['desc'], str), f"Card '{card['name']}' desc should be string"

    def test_all_reversed_descriptions_are_non_empty(self, cards_data):
        """All reversed descriptions should be non-empty"""
        for card in cards_data:
            assert card['rdesc'], f"Card '{card['name']}' has empty rdesc"
            assert isinstance(card['rdesc'], str), f"Card '{card['name']}' rdesc should be string"

    def test_all_cards_have_ascii_art(self, cards_data):
        """All cards should have ASCII art for both positions"""
        for card in cards_data:
            assert card['card'], f"Card '{card['name']}' has empty upright ASCII art"
            assert card['reversed'], f"Card '{card['name']}' has empty reversed ASCII art"
            assert len(card['card']) > 100, f"Card '{card['name']}' ASCII art seems too short"
            assert len(card['reversed']) > 100, f"Card '{card['name']}' reversed ASCII art seems too short"


class TestMajorArcana:
    """Test Major Arcana cards"""

    MAJOR_ARCANA = [
        "The Fool", "The Magician", "The High Priestess", "The Empress",
        "The Emperor", "The Hierophant", "The Lovers", "The Chariot",
        "Strength", "The Hermit", "Wheel of Fortune", "Justice",
        "The Hanged Man", "Death", "Temperance", "The Devil",
        "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"
    ]

    def test_has_all_major_arcana(self, cards_data):
        """Should have all 22 Major Arcana cards"""
        card_names = [card['name'] for card in cards_data]

        for major_card in self.MAJOR_ARCANA:
            assert major_card in card_names, f"Missing Major Arcana card: {major_card}"

    def test_major_arcana_count(self, cards_data):
        """Should have exactly 22 Major Arcana cards"""
        card_names = [card['name'] for card in cards_data]
        major_count = sum(1 for name in card_names if name in self.MAJOR_ARCANA)
        assert major_count == 22, f"Expected 22 Major Arcana cards, found {major_count}"


class TestMinorArcana:
    """Test Minor Arcana cards"""

    SUITS = ['Wands', 'Cups', 'Swords', 'Pentacles']
    RANKS = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
             'Eight', 'Nine', 'Ten', 'Page', 'Knight', 'Queen', 'King']

    def test_has_all_suits(self, cards_data):
        """Should have all four suits"""
        card_names = [card['name'] for card in cards_data]

        for suit in self.SUITS:
            suit_cards = [name for name in card_names if suit in name]
            assert len(suit_cards) == 14, f"Suit '{suit}' should have 14 cards, found {len(suit_cards)}"

    def test_minor_arcana_count(self, cards_data):
        """Should have exactly 56 Minor Arcana cards (4 suits × 14 cards)"""
        card_names = [card['name'] for card in cards_data]

        minor_count = 0
        for suit in self.SUITS:
            minor_count += sum(1 for name in card_names if suit in name)

        assert minor_count == 56, f"Expected 56 Minor Arcana cards, found {minor_count}"


class TestInterpretationsData:
    """Test interpretations.json structure"""

    INTERPRETATION_SYSTEMS = ['rws_traditional', 'thoth_crowley',
                             'jungian_psychological', 'modern_intuitive']

    def test_interpretations_json_exists(self):
        """interpretations.json file should exist"""
        assert os.path.exists('interpretations.json'), "interpretations.json file not found"

    def test_interpretations_is_dict(self, interpretations_data):
        """interpretations.json should be a dictionary"""
        assert isinstance(interpretations_data, dict), "interpretations.json should be a dictionary"

    def test_all_cards_have_interpretations(self, cards_data, interpretations_data):
        """Every card should have interpretation data"""
        card_names = [card['name'] for card in cards_data]

        for card_name in card_names:
            assert card_name in interpretations_data, f"Missing interpretations for: {card_name}"

    def test_all_systems_present(self, interpretations_data):
        """Each card should have all 4 interpretation systems"""
        for card_name, card_interp in interpretations_data.items():
            for system in self.INTERPRETATION_SYSTEMS:
                assert system in card_interp, f"{card_name} missing {system} interpretation"

    def test_upright_and_reversed_present(self, interpretations_data):
        """Each interpretation system should have upright and reversed"""
        for card_name, card_interp in interpretations_data.items():
            for system in self.INTERPRETATION_SYSTEMS:
                system_data = card_interp[system]
                assert 'upright' in system_data, f"{card_name}/{system} missing upright"
                assert 'reversed' in system_data, f"{card_name}/{system} missing reversed"

                # Check they're non-empty strings
                assert system_data['upright'], f"{card_name}/{system} upright is empty"
                assert system_data['reversed'], f"{card_name}/{system} reversed is empty"
                assert isinstance(system_data['upright'], str), f"{card_name}/{system} upright not a string"
                assert isinstance(system_data['reversed'], str), f"{card_name}/{system} reversed not a string"
