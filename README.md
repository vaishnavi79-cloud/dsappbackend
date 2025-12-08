# Canteen Demand Predictor API

## Setup
cd backend
python -m venv venv
venv\Scripts\activate (Windows) or source venv/bin/activate
pip install -r requirements.txt

## Run
uvicorn app.main:app --reload --port 8000

## Testing
GET https://dsappbackend.onrender.com/history
GET https://dsappbackend.onrender.com/wastage-summary
GET https://dsappbackend.onrender.com/predict
