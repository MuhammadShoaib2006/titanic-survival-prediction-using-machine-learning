from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json

app = FastAPI()

# ... (your existing Titanic API code remains the same) ...

class PostmanCollectionRequest(BaseModel):
    collection_name: str = "Titanic Survival Predictor"
    base_url: str = "http://localhost:8000"

@app.post("/generate_postman_collection")
async def generate_postman_collection(request: Request, config: PostmanCollectionRequest):
    """Generate Postman collection JSON with all API endpoints"""
    base_url = config.base_url.rstrip("/")
    
    collection = {
        "info": {
            "name": config.collection_name,
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [
            {
                "name": "Predict Survival",
                "request": {
                    "method": "POST",
                    "header": [
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        }
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": json.dumps({
                            "Pclass": 1,
                            "Sex": "male",
                            "Age": 30.0,
                            "SibSp": 0,
                            "Parch": 0,
                            "Fare": 32.0,
                            "Embarked": "S",
                            "Title": "Mr",
                            "HadCabin": False,
                            "FamilySize": 1,
                            "IsAlone": True
                        }, indent=2)
                    },
                    "url": {
                        "raw": f"{base_url}/predict",
                        "protocol": "http",
                        "host": ["localhost"],
                        "port": "8000",
                        "path": ["predict"]
                    }
                }
            },
            {
                "name": "Test Prediction",
                "request": {
                    "method": "POST",
                    "url": {
                        "raw": f"{base_url}/test_prediction",
                        "protocol": "http",
                        "host": ["localhost"],
                        "port": "8000",
                        "path": ["test_prediction"]
                    }
                }
            },
            {
                "name": "Health Check",
                "request": {
                    "method": "GET",
                    "url": {
                        "raw": f"{base_url}/health",
                        "protocol": "http",
                        "host": ["localhost"],
                        "port": "8000",
                        "path": ["health"]
                    }
                }
            },
            {
                "name": "API Documentation",
                "request": {
                    "method": "GET",
                    "url": {
                        "raw": f"{base_url}/docs",
                        "protocol": "http",
                        "host": ["localhost"],
                        "port": "8000",
                        "path": ["docs"]
                    }
                }
            }
        ]
    }
    
    return JSONResponse(content=collection)

@app.get("/generate_postman_urls")
async def generate_postman_urls(request: Request):
    """Generate direct import URL for Postman"""
    base_url = str(request.base_url).rstrip("/")
    return {
        "message": "Use these URLs to import into Postman",
        "direct_import_url": f"https://www.postman.com/collections/import?url={base_url}/generate_postman_collection",
        "collection_json_url": f"{base_url}/generate_postman_collection",
        "usage_instructions": (
            "1. Copy the 'direct_import_url' and paste in Postman's import dialog\n"
            "2. Or download the JSON from 'collection_json_url' and import manually"
        )
    }