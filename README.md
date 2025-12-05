# Canteen Demand Predictor API

## Setup
cd backend
python -m venv venv
venv\Scripts\activate (Windows) or source venv/bin/activate
pip install -r requirements.txt

## Run
uvicorn app.main:app --reload --port 8000

## Testing
GET http://localhost:8000/history
GET http://localhost:8000/wastage-summary
GET http://localhost:8000/predict?item_name=Rice
