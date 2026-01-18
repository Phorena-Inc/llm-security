# FastAPI REST API Examples & Patterns

This document shows what FastAPI REST APIs look like with practical examples.

---

## What is FastAPI?

FastAPI is a modern, high-performance Python web framework for building REST APIs:
- **Fast**: Built on Starlette (async) and Pydantic (validation)
- **Auto Documentation**: Generates interactive Swagger/OpenAPI docs
- **Type Safety**: Uses Python type hints for validation
- **Async Support**: Native async/await support

---

## Basic FastAPI Example

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Create FastAPI app
app = FastAPI(
    title="My API",
    description="Example REST API",
    version="1.0.0"
)

# Define request/response models with Pydantic
class UserRequest(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int]
    created_at: str

# GET endpoint
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# GET with path parameter
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": "John Doe"}

# POST endpoint
@app.post("/users", response_model=UserResponse)
def create_user(user: UserRequest):
    # Process request
    return UserResponse(
        id=123,
        name=user.name,
        email=user.email,
        age=user.age,
        created_at="2025-11-06T12:00:00Z"
    )

# GET with query parameters
@app.get("/search")
def search_users(
    q: str,
    limit: int = 10,
    skip: int = 0
):
    return {
        "query": q,
        "limit": limit,
        "skip": skip,
        "results": []
    }

# Error handling
@app.get("/users/{user_id}/profile")
def get_user_profile(user_id: int):
    if user_id < 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID"
        )
    if user_id > 1000:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return {"user_id": user_id, "profile": {}}
```

---

## Running the API

```bash
# Install FastAPI and Uvicorn
pip install fastapi uvicorn

# Run the server
uvicorn main:app --reload

# Server runs at: http://localhost:8000
# Interactive docs: http://localhost:8000/docs
# Alternative docs: http://localhost:8000/redoc
```

---

## Async Endpoints (What We'll Use)

```python
from fastapi import FastAPI
from typing import Dict, List

app = FastAPI()

# Async endpoint (for database queries, etc.)
@app.get("/employees/{email}")
async def get_employee(email: str) -> Dict:
    # Can use await with async functions
    employee = await database.get_employee(email)
    return employee

# Async POST
@app.post("/check-access")
async def check_access(
    employee_email: str,
    resource_id: str,
    classification: str
) -> Dict:
    result = await privacy_api.check_access(
        employee_email=employee_email,
        resource_id=resource_id,
        resource_classification=classification
    )
    return result
```

---

## Request/Response Models (Pydantic)

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum

# Enum for choices
class Classification(str, Enum):
    public = "public"
    internal = "internal"
    confidential = "confidential"
    top_secret = "top_secret"

# Request model with validation
class AccessCheckRequest(BaseModel):
    employee_email: EmailStr  # Validates email format
    resource_id: str = Field(..., min_length=1, max_length=100)
    classification: Classification
    
    class Config:
        # Example for docs
        schema_extra = {
            "example": {
                "employee_email": "john.doe@company.com",
                "resource_id": "RES-001",
                "classification": "confidential"
            }
        }

# Response model
class AccessCheckResponse(BaseModel):
    access_granted: bool
    reason: str
    policy_matched: Optional[str] = None
    confidence: Optional[float] = None
    employee_context: Optional[Dict] = None

# Use in endpoint
@app.post("/check-access", response_model=AccessCheckResponse)
async def check_access(request: AccessCheckRequest):
    result = await privacy_api.check_access(
        employee_email=request.employee_email,
        resource_id=request.resource_id,
        resource_classification=request.classification.value
    )
    return AccessCheckResponse(**result)
```

---

## Error Handling Patterns

```python
from fastapi import FastAPI, HTTPException, status

@app.get("/employees/{email}")
async def get_employee(email: str):
    try:
        employee = await privacy_api.get_employee_context(email)
        
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee not found: {email}"
            )
        
        return employee
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
```

---

## Query Parameters

```python
from typing import Optional
from datetime import date

@app.get("/audit-trail")
async def get_audit_trail(
    employee_email: Optional[str] = None,
    resource_id: Optional[str] = None,
    decision: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 100
):
    """
    GET /audit-trail?employee_email=john@company.com&limit=50
    """
    entries = audit_logger.get_audit_trail(
        employee_email=employee_email,
        resource_id=resource_id,
        decision=decision,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )
    return {"entries": [e.to_dict() for e in entries]}
```

---

## CORS (Cross-Origin Requests)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Dependency Injection

```python
from fastapi import Depends, FastAPI

# Dependency function
async def get_privacy_api():
    return PrivacyFirewallAPI()

# Use in endpoint
@app.post("/check-access")
async def check_access(
    request: AccessCheckRequest,
    api: PrivacyFirewallAPI = Depends(get_privacy_api)
):
    result = await api.check_access(
        employee_email=request.employee_email,
        resource_id=request.resource_id,
        resource_classification=request.classification.value
    )
    return result
```

---

## What We'll Build for Privacy Firewall

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date

app = FastAPI(
    title="AI Privacy Firewall API",
    description="Team B - Organizational Chart Integration",
    version="1.0.0"
)

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class AccessCheckRequest(BaseModel):
    employee_email: EmailStr
    resource_id: str
    classification: str

class AccessCheckResponse(BaseModel):
    access_granted: bool
    reason: str
    policy_matched: Optional[str]
    confidence: Optional[float]
    employee_context: Optional[dict]

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.post("/check-access", response_model=AccessCheckResponse)
async def check_access(request: AccessCheckRequest):
    """
    Check if employee can access a resource
    
    Example:
        POST /check-access
        {
            "employee_email": "john.doe@company.com",
            "resource_id": "RES-001",
            "classification": "confidential"
        }
    """
    pass

@app.get("/employee-context/{email}")
async def get_employee_context(email: str):
    """
    Get organizational context for employee
    
    Example:
        GET /employee-context/john.doe@company.com
    """
    pass

@app.get("/accessible-resources/{email}")
async def get_accessible_resources(
    email: str,
    classification: Optional[str] = Query(None)
):
    """
    Get resources accessible to employee
    
    Example:
        GET /accessible-resources/john.doe@company.com?classification=confidential
    """
    pass

@app.get("/audit-trail")
async def get_audit_trail(
    employee_email: Optional[str] = None,
    resource_id: Optional[str] = None,
    decision: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 100
):
    """
    Get audit trail with filters
    
    Example:
        GET /audit-trail?employee_email=john@company.com&limit=50
    """
    pass

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
```

---

## Interactive Documentation

FastAPI automatically generates interactive API documentation:

**Swagger UI** (http://localhost:8000/docs):
- Try out endpoints directly in browser
- See request/response schemas
- Test with real data

**ReDoc** (http://localhost:8000/redoc):
- Alternative documentation format
- Better for reading/sharing

---

## Testing FastAPI Endpoints

```python
# Using httpx (async HTTP client)
import httpx

async def test_check_access():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/check-access",
            json={
                "employee_email": "john.doe@company.com",
                "resource_id": "RES-001",
                "classification": "confidential"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_granted" in data

# Using curl
curl -X POST http://localhost:8000/check-access \
  -H "Content-Type: application/json" \
  -d '{
    "employee_email": "john.doe@company.com",
    "resource_id": "RES-001",
    "classification": "confidential"
  }'
```

---

## Key FastAPI Features We'll Use

1. ✅ **Automatic validation**: Pydantic models validate requests
2. ✅ **Type safety**: Python type hints catch errors early
3. ✅ **Async support**: Native async/await for database queries
4. ✅ **Auto docs**: Swagger UI for testing
5. ✅ **Error handling**: HTTPException for proper error responses
6. ✅ **Query params**: Optional filters for audit trail
7. ✅ **Path params**: Email/ID in URL path
8. ✅ **Response models**: Consistent response format

---

## Next Steps

Ready to build the actual Privacy Firewall REST API with these patterns!

The API will expose:
1. `POST /check-access` - Main access control endpoint
2. `GET /employee-context/{email}` - Get org context
3. `GET /accessible-resources/{email}` - List accessible resources
4. `GET /resource-viewers/{resource_id}` - Who can access resource
5. `GET /audit-trail` - Query audit logs
6. `GET /health` - Health check

All endpoints will be async, properly validated, and auto-documented.
