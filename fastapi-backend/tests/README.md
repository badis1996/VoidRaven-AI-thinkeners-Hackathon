# Test Documentation

## Overview
This document describes the automated tests implemented for the AI Assessment Agent's API and database layers. The tests verify the core functionality of our data models, API endpoints, and file handling capabilities.

## Test Configuration
Located in `conftest.py`, the test configuration:
- Creates an async event loop for test execution
- Sets up a dedicated test database
- Manages database sessions with proper cleanup
- Provides test client with dependency overrides
- Ensures test isolation and resource cleanup

## Test Cases

### 1. API Tests (`test_api.py`)

#### Candidate Creation with CV
**Function**: `test_create_candidate`

Tests the creation of a candidate with CV upload:
```python
test_data = {
    "name": "Test Candidate",
    "email": "test@example.com",
    "cv_file": base64_encoded_cv
}
```

**Verifies**:
- Successful candidate creation
- CV file processing
- Response format and status codes
- PDF mime type validation

#### Duplicate Candidate Handling
**Function**: `test_create_duplicate_candidate`

Tests the system's handling of duplicate email addresses:
- Attempts to create candidates with the same email
- Verifies proper error responses
- Ensures database integrity

#### Interview Data Management
**Function**: `test_update_interview_data`

Tests the interview data update process:
- Creates a candidate with CV
- Updates interview information
- Verifies data persistence
- Checks response format

#### Transcript Retrieval
**Functions**: 
- `test_get_transcript`
- `test_get_nonexistent_transcript`

Tests the transcript retrieval functionality:
- Retrieves existing transcripts
- Handles non-existent transcripts
- Verifies response formats
- Validates error handling

### 2. Database Tests (`test_database.py`)

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

### All Tests
```bash
PYTHONPATH=$PYTHONPATH:. pytest -v
```

### Specific Test Files
```bash
# API Tests
PYTHONPATH=$PYTHONPATH:. pytest tests/test_api.py -v

# Database Tests
PYTHONPATH=$PYTHONPATH:. pytest tests/test_database.py -v
```

### Single Test
```bash
PYTHONPATH=$PYTHONPATH:. pytest tests/test_api.py -v -k "test_create_candidate"
```

## Test Coverage
Current coverage for the entire application:
- API Endpoints: 81%
- Models: 100%
- Database operations: 89%
- Configuration: 93%

## Test Resources
- `cvexamples/`: Contains sample CV files for testing
- `conftest.py`: Test configuration and fixtures
- `test_api.py`: API endpoint tests
- `test_database.py`: Database operation tests

## Future Improvements
1. Increase API endpoint coverage
2. Add more CV format validations
3. Implement performance tests
4. Add integration tests with AI services
5. Enhance error scenario coverage

## Future Test Additions
Planned test additions:
1. Update operations for all models
2. Constraint violation tests
3. Bulk operation tests
4. Edge case handling
5. Performance tests for large datasets 