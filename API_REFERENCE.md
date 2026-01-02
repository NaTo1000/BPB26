# API Reference

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. In production deployments, implement appropriate authentication mechanisms.

## Response Format

All API responses follow this general structure:

```json
{
  "data": {},
  "error": null,
  "status": "success"
}
```

Errors return:

```json
{
  "detail": "Error message"
}
```

## Endpoints

### Projects

#### Create Project

```http
POST /api/projects
```

**Request Body:**
```json
{
  "name": "string",
  "address": "string",
  "project_type": "string",
  "jurisdiction": "string",
  "metadata": {}
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "string",
  "address": "string",
  "project_type": "string",
  "jurisdiction": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "status": "pending|compliant|non_compliant|needs_review",
  "violations": [],
  "compliance_score": 0.0,
  "metadata": {}
}
```

#### List Projects

```http
GET /api/projects?status=&jurisdiction=
```

**Query Parameters:**
- `status` (optional): Filter by compliance status
- `jurisdiction` (optional): Filter by jurisdiction

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "string",
    ...
  }
]
```

#### Get Project

```http
GET /api/projects/{project_id}
```

**Response:** Same as Create Project response

#### Get Project Summary

```http
GET /api/projects/{project_id}/summary
```

**Response:**
```json
{
  "project_id": "uuid",
  "name": "string",
  "address": "string",
  "status": "string",
  "compliance_score": 0.0,
  "total_violations": 0,
  "violations_by_severity": {
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 0,
    "info": 0
  },
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### Delete Project

```http
DELETE /api/projects/{project_id}
```

**Response:**
```json
{
  "status": "deleted",
  "project_id": "uuid"
}
```

### Compliance

#### Check Compliance

```http
POST /api/compliance/check
```

**Request Body:**
```json
{
  "project_id": "uuid",
  "regulation_ids": ["string"] // optional
}
```

**Response:**
```json
{
  "project_id": "uuid",
  "generated_at": "datetime",
  "overall_status": "compliant|non_compliant|needs_review",
  "compliance_score": 0.0,
  "total_violations": 0,
  "violations_by_severity": {},
  "violations": [
    {
      "id": "uuid",
      "regulation_id": "string",
      "severity": "critical|high|medium|low|info",
      "description": "string",
      "location": "string",
      "detected_at": "datetime",
      "recommendations": ["string"],
      "auto_fixable": false,
      "metadata": {}
    }
  ],
  "applicable_regulations": ["string"],
  "recommendations": ["string"],
  "summary": "string"
}
```

### Regulations

#### Get Regulation

```http
GET /api/regulations/{regulation_id}
```

**Response:**
```json
{
  "id": "string",
  "code": "string",
  "section": "string",
  "title": "string",
  "description": "string",
  "regulation_type": "building_code|fire_safety|electrical|plumbing|structural|accessibility|energy|environmental|zoning",
  "jurisdiction": "string",
  "effective_date": "datetime",
  "version": "string",
  "tags": ["string"],
  "metadata": {}
}
```

#### Search Regulations

```http
GET /api/regulations?query=&jurisdiction=&code=&regulation_type=
```

**Query Parameters:**
- `query` (optional): Search text
- `jurisdiction` (optional): Filter by jurisdiction
- `code` (optional): Filter by code (e.g., "IBC 2021")
- `regulation_type` (optional): Filter by type

**Response:** Array of Regulation objects

#### List Building Codes

```http
GET /api/regulations/codes
```

**Response:**
```json
{
  "codes": ["IBC 2021", "ADA 2010", "NEC 2020", ...]
}
```

#### List Jurisdictions

```http
GET /api/regulations/jurisdictions
```

**Response:**
```json
{
  "jurisdictions": ["International", "United States", ...]
}
```

### AI

#### Analyze Project

```http
POST /api/ai/analyze?project_id={project_id}
```

**Response:**
```json
[
  {
    "id": "uuid",
    "project_id": "uuid",
    "insight_type": "string",
    "title": "string",
    "description": "string",
    "confidence": 0.0,
    "generated_at": "datetime",
    "recommendations": ["string"],
    "metadata": {}
  }
]
```

#### Get Recommendations

```http
POST /api/ai/recommendations?project_id={project_id}
```

**Response:**
```json
{
  "project_id": "uuid",
  "recommendations": ["string"]
}
```

### Statistics

#### Get Platform Statistics

```http
GET /api/statistics
```

**Response:**
```json
{
  "total_projects": 0,
  "projects_by_status": {
    "compliant": 0,
    "non_compliant": 0,
    "needs_review": 0,
    "pending": 0
  },
  "total_violations": 0,
  "average_compliance_score": 0.0
}
```

### Health & Status

#### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

#### Root

```http
GET /
```

**Response:**
```json
{
  "name": "Pinnacle Building Compliance Platform",
  "version": "1.0.0",
  "status": "operational",
  "message": "AI-powered building compliance and regulation management"
}
```

## Error Codes

- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

## Rate Limiting

Currently, no rate limiting is implemented. Production deployments should implement appropriate rate limiting.

## Examples

See [GETTING_STARTED.md](GETTING_STARTED.md) for code examples and integration guides.
