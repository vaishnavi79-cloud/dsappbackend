from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import joblib

from app.database import SessionLocal, engine
from app import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Canteen Demand Predictor API", version="0.1.0")

# -------- Database Dependency -------- #
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------- Routes ----------- #

@app.post("/add-entry", response_model=schemas.FoodEntryOut, tags=["Canteen"])
def add_entry(entry: schemas.FoodEntryCreate, db: Session = Depends(get_db)):
    db_entry = models.FoodEntry(
        date=entry.date,
        item_name=entry.item_name,
        prepared_qty=entry.prepared_qty,
        consumed_qty=entry.consumed_qty,
        wastage=entry.prepared_qty - entry.consumed_qty
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@app.get("/history", response_model=List[schemas.FoodEntryOut], tags=["Canteen"])
def get_history(db: Session = Depends(get_db)):
    return db.query(models.FoodEntry).all()

@app.get("/wastage-summary", tags=["Analytics"])
def wastage_summary(db: Session = Depends(get_db)):
    total_wastage = db.query(models.FoodEntry).with_entities(
        models.FoodEntry.wastage
    )
    return {
        "total_records": db.query(models.FoodEntry).count(),
        "average_wastage": sum(x[0] for x in total_wastage) / db.query(models.FoodEntry).count()
        if db.query(models.FoodEntry).count() > 0 else 0
    }

@app.get("/predict", tags=["Prediction"])
def predict(item: str, prepared_qty: float):
    try:
        model = joblib.load("model.pkl")
        prediction = model.predict([[prepared_qty]])
        return {"predicted_consumption": prediction[0]}
    except:
        raise HTTPException(status_code=500, detail="Model not trained yet. Add more data.")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=10000, reload=True)
