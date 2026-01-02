# Getting Started with Pinnacle Building Compliance Platform

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/NaTo1000/BPB26.git
cd BPB26
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Or install the package in development mode
pip install -e .
```

## Running the Examples

### Example 1: Basic Usage

```bash
cd examples
python basic_usage.py
```

This example demonstrates:
- Creating a building project
- Running compliance checks
- Generating AI insights
- Getting recommendations

### Example 2: API Server

```bash
# From the project root directory
python run_server.py
```

Then visit:
- http://localhost:8000 - API root
- http://localhost:8000/docs - Interactive API documentation (Swagger)
- http://localhost:8000/redoc - Alternative API documentation (ReDoc)

### Example 3: CLI Tool

```bash
# Create a new project
python -m bpb26.cli create \
  --name "My Building Project" \
  --address "456 Oak Street, Portland, OR" \
  --type "Mixed-Use Development" \
  --jurisdiction "Portland, Oregon"

# List all projects
python -m bpb26.cli list

# Check compliance (use project ID from list command)
python -m bpb26.cli check <project-id>

# Search regulations
python -m bpb26.cli search "accessibility" --jurisdiction "United States"

# Generate AI insights
python -m bpb26.cli analyze <project-id>

# View statistics
python -m bpb26.cli stats
```

## Using the REST API

### Create a Project

```bash
curl -X POST "http://localhost:8000/api/projects" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Building",
    "address": "789 Pine St, Denver, CO",
    "project_type": "Residential",
    "jurisdiction": "Denver, Colorado",
    "metadata": {
      "building_height": 45,
      "floors": 3,
      "square_footage": 5000
    }
  }'
```

### Check Compliance

```bash
curl -X POST "http://localhost:8000/api/compliance/check" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "<project-id-from-previous-step>"
  }'
```

### Search Regulations

```bash
curl "http://localhost:8000/api/regulations?query=fire+safety&jurisdiction=International"
```

### Get AI Insights

```bash
curl -X POST "http://localhost:8000/api/ai/analyze?project_id=<project-id>"
```

## Integration with Your Application

### Python Integration

```python
from bpb26 import ComplianceEngine, ProjectManager, RegulationDatabase, AIAnalyzer

# Initialize components
regulation_db = RegulationDatabase()
compliance_engine = ComplianceEngine(regulation_db=regulation_db)
project_manager = ProjectManager()
ai_analyzer = AIAnalyzer()

# Create and check a project
project = project_manager.create_project(
    name="My Project",
    address="123 Main St",
    project_type="Commercial",
    jurisdiction="Seattle"
)

report = compliance_engine.check_compliance(project)
insights = ai_analyzer.predict_compliance_issues(project)
```

### REST API Integration

Use any HTTP client to integrate with the REST API:

```python
import requests

# Create a project
response = requests.post(
    "http://localhost:8000/api/projects",
    json={
        "name": "My Project",
        "address": "123 Main St",
        "project_type": "Commercial",
        "jurisdiction": "Seattle"
    }
)
project = response.json()

# Check compliance
response = requests.post(
    "http://localhost:8000/api/compliance/check",
    json={"project_id": project["id"]}
)
report = response.json()
```

## Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs to explore all available endpoints
2. **Read the Architecture**: Check [ARCHITECTURE.md](ARCHITECTURE.md) for system design details
3. **Run Tests**: Execute `pytest` to run the test suite
4. **Customize**: Extend the platform with your own regulations and rules

## Troubleshooting

### Import Errors

If you get import errors, make sure you're in the project root directory and have installed the package:

```bash
pip install -e .
```

### Port Already in Use

If port 8000 is already in use, specify a different port:

```bash
uvicorn bpb26.integrations.api:app --host 0.0.0.0 --port 8080
```

### Missing Dependencies

If you encounter missing dependencies, reinstall:

```bash
pip install -r requirements.txt --upgrade
```

## Support

For issues, questions, or feature requests, please open an issue on GitHub.
