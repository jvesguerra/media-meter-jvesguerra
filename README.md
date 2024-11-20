# BACKEND DEV TECHNICAL EXAM

## DESCRIPTION

Python-based API and background service to handle the uploading of medalists from a CSV file and inserting them into a MongoDB database using FastAPI for the API and Python for file processing.

## ASSUMPTION AND DESIGN DECISIONS

1. I modified the original file into a utf-8 encoding csv file.
2. I added more flexibility to the csv files that can be uploaded.
3. In running the python service in background, I opted to use pythonw. I had problems using other process managers such as nssm and pywin32.

## INSTALLATION INSTRUCTION

1. pip install fastapi uvicorn pydantic motor python-dotenv

### Swagger UI

2. Download ZIP file from (https://github.com/swagger-api/swagger-ui)
3. Locate dist and open index.html

### MongoDB

4. Download Mongodb from (https://www.mongodb.com/try/download/community)
5. Add the bin path to the system variables
6. In MongoDB, create a database named 'database'
7. Create a collection named 'medalists'

### Python Background Service

1. pip install pymongo watchdog pandas

## USAGE

In separate terminals:

1. In the api folder, run 'uvicorn app:app --reload'

2. Next, run ' pythonw background.py' in the service folder

3. To trigger the post function, run 'curl.exe -X POST "http://127.0.0.1:8000/upload-csv/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@C:/.../medallists2.csv"'


