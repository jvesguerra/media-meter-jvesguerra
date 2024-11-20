import csv
from io import StringIO
from fastapi import FastAPI, UploadFile, HTTPException, File, Query
from pydantic import BaseModel, ValidationError
from typing import Optional, List
import os
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# MongoDB settings
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "database"
COLLECTION_NAME = "medalists"

# Create an app instance
app = FastAPI(openapi_version="3.1.0", version="1.0.0")

# Allow CORS from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MongoDB client
client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Define Pydantic models

class Medalist(BaseModel):
    medal_date: str
    medal_type: str
    medal_code: float
    name: str
    gender: str
    country_code: str
    country: str
    country_long: str
    nationality: str
    team: str
    team_gender: str
    discipline: str
    event: str
    event_type: str
    url_event: str
    birth_date: str
    code_athlete: int
    code_team: str


# Directory to save uploaded files
UPLOAD_DIR = "storage/app/medalists"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Upload Endpoint
@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    valid_types = ["text/csv", "application/octet-stream"]

    if file.content_type not in valid_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")
    
    # Since the given csv file content type is in octet-stream, I opted to check if the extension csv
    if file.content_type == "application/octet-stream" and not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file extension. Please upload a CSV file.")
    
    # Save the uploaded file to the specified directory
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)
            return JSONResponse(
            status_code=201,
            content={
                "status": "success",
                "message": "CSV file uploaded successfully.",
                "filename": file.filename,
                "file_path": file_path,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

#''' 
class MedalistResponse(BaseModel):
    name: str
    medal_type: str
    gender: str
    country: str
    country_code: str
    nationality: str
    medal_code: Optional[float] = None
    medal_date: Optional[str] = None

class EventStatsResponse(BaseModel):
    discipline: str
    event: str
    event_date: str
    medalists: List[MedalistResponse]

class PaginatedResponse(BaseModel):
    data: List[EventStatsResponse]
    paginate: dict
    
#  Get Event Aggregate Stats Endpoint    
@app.get("/aggregated_stats/event", response_model=PaginatedResponse)
async def get_aggregated_event_stats(page: int = Query(1, ge=1), limit: int = Query(10, le=100)): # Limit of 100 queries
    try:
        result = await get_event_stats(page, limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

async def get_event_stats(page: int = 1, limit: int = 10):
    skip = (page - 1) * limit                                   # used to know how many data to skip
    total_documents = await collection.count_documents({})
    total_pages = (total_documents + limit - 1) // limit

    details = [
        {"$group": {
            "_id": {
                "discipline": "$discipline",
                "event": "$event",
                "event_date": "$medal_date"
            },
            "medalists": {"$push": {
                "name": "$name",
                "medal_type": "$medal_type",
                "gender": "$gender",
                "country": "$country",
                "country_code": "$country_code",
                "nationality": "$nationality",
                "medal_code": "$medal_code",
                "medal_date": "$medal_date"
            }}
        }},
        {"$skip": skip},
        {"$limit": limit}
    ]

    cursor = collection.aggregate(details)
    events = []
    async for event in cursor:
        events.append({
            "discipline": event["_id"]["discipline"],
            "event": event["_id"]["event"],
            "event_date": event["_id"]["event_date"],
            "medalists": event["medalists"]
        })

    pagination = {
        "current_page": page,
        "total_pages": total_pages,
        "next_page": f"/aggregated_stats/event?page={page + 1}" if page < total_pages else None,
        "previous_page": f"/aggregated_stats/event?page={page - 1}" if page > 1 else None
    }

    return {"data": events, "paginate": pagination}
    
#'''
