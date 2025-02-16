# AI Assessment Agent - FastAPI Backend

## Project Overview
The AI Assessment Agent backend is a FastAPI-based application that powers an innovative platform for automating university admissions interviews for Master's programs in Business and Economics. This backend service orchestrates AI-driven interviews, assessments, and follow-up actions.

## Core Features
- **AI Interview Management**: Handles interview sessions and conversation flow
- **Transcript Processing**: Real-time speech-to-text and interview transcription
- **Assessment Engine**: Analyzes interview responses and generates evaluations
- **Follow-up Actions**: Manages post-interview tasks and scheduling
- **API Integration**: Interfaces with LLMs (Claude) and other external services
- **Data Management**: Secure handling of candidate data and interview records

## Technology Stack
- **Framework**: FastAPI
- **Python Version**: 3.11+
- **Database**: PostgreSQL with SQLAlchemy
- **AI/ML**: Anthropic Claude API
- **Authentication**: JWT-based auth
- **Documentation**: OpenAPI (Swagger UI)

## Getting Started

### Prerequisites
- Python 3.11 or higher
- PostgreSQL
- Virtual environment tool (venv/conda)

### Installation
1. Clone the repository:
```bash
git clone [repository-url]
cd fastapi-backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Running the Application
1. Start the development server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Interview Management
- `POST /api/v1/interviews/`: Create new interview session
- `GET /api/v1/interviews/{interview_id}`: Get interview details
- `POST /api/v1/interviews/{interview_id}/start`: Start interview session
- `POST /api/v1/interviews/{interview_id}/end`: End interview session

### Assessment
- `POST /api/v1/assessments/`: Generate interview assessment
- `GET /api/v1/assessments/{assessment_id}`: Retrieve assessment results

### Follow-up Actions
- `POST /api/v1/actions/schedule`: Schedule follow-up meetings
- `POST /api/v1/actions/notify`: Send notifications

## Project Structure
```
fastapi-backend/
├── app/
│   ├── api/
│   │   └── v1/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   └── services/
├── tests/
├── alembic/
├── requirements.txt
└── README.md
```

## Development Guidelines
- Follow PEP 8 style guide
- Write unit tests for new features
- Document API endpoints using FastAPI's built-in tools
- Use type hints for better code clarity
- Implement error handling and logging

## Testing
Run tests using pytest:
```bash
pytest
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License
[License details]

## Contact
[Contact information]
