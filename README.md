TITLE

Backend Dev Technical Exam

DESCRIPTION

Python-based API and background service to handle the uploading of medalists from a CSV file and inserting them into a MongoDB database using FastAPI for the API and Python for file processing.

INSTALLATION INSTRUCTION

1. pip install fastapi uvicorn pydantic motor python-dotenv

Swagger UI

2. Download ZIP file from (https://github.com/swagger-api/swagger-ui)
3. Locate dist and open index.html

MONGODB

4. Download Mongodb from (https://www.mongodb.com/try/download/community)
5. Add the bin path to the system variables
6. In MongoDB, create a database named 'database'
7. Create a collection named 'medalists'

FOR PYTHON BACKGROUND SERVICE

1. pip install pymongo watchdog pandas

USAGE

In separate terminals:

1. In the api folder, run 'uvicorn app:app --reload'

2. Next, run 'python background.py' in the service folder

3. To trigger the post function, run 'curl.exe -X POST "http://127.0.0.1:8000/upload-csv/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@C:/Users/Bruu/Desktop/MEDIAMETER-TECHNICAL-EXAM/medallists2.csv"'

pip install pywin32
python background.py install
python background.py start
python background.py status
python background.py stop
python background.py remove
