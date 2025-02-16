# Database Tests Documentation

## Overview
This document describes the automated tests implemented for the AI Assessment Agent's database layer. The tests verify the core functionality of our data models and their relationships.

## Test Configuration
Located in `conftest.py`, the test configuration:
- Creates an async event loop for test execution
- Resets the database before each test
- Provides a clean database session with transaction rollback
- Ensures test isolation

## Test Cases

### 1. Candidate Creation Test
**File**: `test_database.py`
**Function**: `test_create_candidate`

Tests the creation of a candidate with basic information:
```python
candidate = Candidate(
    id=uuid.uuid4(),
    name="Test Candidate",
    email="test@example.com",
    cv_data={"education": "Master's in Computer Science"}
)
```

**Verifies**:
- Successful candidate creation
- Correct storage of all fields
- UUID generation
- JSON data storage (cv_data)

### 2. Interview with Questions Test
**File**: `test_database.py`
**Function**: `test_create_interview_with_questions`

Tests the creation of an interview with associated questions:
1. Creates a candidate
2. Creates an interview linked to the candidate
3. Adds multiple questions to the interview

**Verifies**:
- Interview creation with candidate association
- Multiple question creation
- Relationship integrity between models
- Proper storage of interview transcript

### 3. Cascade Delete Test
**File**: `test_database.py`
**Function**: `test_cascade_delete`

Tests the deletion cascade from candidate to related records:
1. Creates a candidate
2. Creates an interview for the candidate
3. Adds a question to the interview
4. Deletes the candidate
5. Verifies cascade deletion

**Verifies**:
- Proper cascade deletion setup
- Removal of related interviews
- Removal of related questions
- Database integrity after deletion

## Running the Tests

To run all database tests:
```bash
pytest tests/test_database.py -v
```

To run a specific test:
```bash
pytest tests/test_database.py -v -k "test_create_candidate"
```

## Test Coverage
Current coverage for database-related code:
- Models: 100%
- Database operations: 79%
- Configuration: 96%

## Future Test Additions
Planned test additions:
1. Update operations for all models
2. Constraint violation tests
3. Bulk operation tests
4. Edge case handling
5. Performance tests for large datasets 