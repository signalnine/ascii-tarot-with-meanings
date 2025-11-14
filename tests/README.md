# Tarot Card Tests

Comprehensive test suite for the ASCII Tarot Card project.

## Test Files

### test_data_validation.py
Tests for data structure and completeness:
- Cards.json structure (78 cards, required fields)
- No cbd_desc field present
- All Major Arcana cards (22 cards)
- All Minor Arcana cards (56 cards, 4 suits)
- Interpretations.json structure (4 systems, upright/reversed)

### test_embeddings.py
Tests for embedding generation:
- Text creation includes all interpretation systems
- Text excludes cbd_desc
- Embeddings file structure (156 entries)
- Each card has upright and reversed
- Correct dimensions (1536 for text-embedding-3-small)
- Consistency between cards and embeddings

### test_search.py
Tests for search functionality:
- Cosine similarity calculation
- Loading embeddings and cards
- Finding similar cards
- Excluding/including self in results
- Results sorted by similarity
- Embedding quality (related cards are similar)

## Running Tests

### Run all tests
```bash
pytest
```

### Run with verbose output
```bash
pytest -v
```

### Run specific test file
```bash
pytest tests/test_data_validation.py
pytest tests/test_embeddings.py
pytest tests/test_search.py
```

### Run specific test class
```bash
pytest tests/test_data_validation.py::TestCardsDataStructure
```

### Run specific test
```bash
pytest tests/test_data_validation.py::TestCardsDataStructure::test_has_78_cards
```

### Show test coverage
```bash
pytest --cov=. --cov-report=html
```

### Run tests that don't require embeddings
```bash
pytest tests/test_data_validation.py -v
```

## Test Requirements

- **Required for all tests**: cards.json, interpretations.json
- **Required for embedding/search tests**: card_embeddings.json

If embeddings haven't been generated yet, those tests will be skipped automatically.

## Expected Results

With all data files present:
- **test_data_validation.py**: All tests should pass
- **test_embeddings.py**: All tests should pass if embeddings exist
- **test_search.py**: All tests should pass if embeddings exist

Total: ~50+ tests
