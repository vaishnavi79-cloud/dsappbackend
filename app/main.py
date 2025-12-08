from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal, engine, Base
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from prophet import Prophet
from datetime import timedelta

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Canteen Demand Predictor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/add-entry", response_model=schemas.FoodEntryOut)
def add_entry(entry: schemas.FoodEntryCreate, db: Session = Depends(get_db)):
    wastage = max(0.0, entry.prepared_qty - entry.consumed_qty)
    db_entry = models.FoodEntry(
        date=entry.date,
        item_name=entry.item_name,
        prepared_qty=entry.prepared_qty,
        consumed_qty=entry.consumed_qty,
        wastage=wastage
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@app.get("/history", response_model=list[schemas.FoodEntryOut])
def history(item_name: str | None = None, db: Session = Depends(get_db)):
    q = db.query(models.FoodEntry)
    if item_name:
        q = q.filter(models.FoodEntry.item_name == item_name)
    return q.order_by(models.FoodEntry.date.desc()).all()

@app.get("/wastage-summary")
def wastage_summary(db: Session = Depends(get_db)):
    q = db.query(models.FoodEntry).all()
    if not q:
        return {"message": "no data"}
    df = pd.DataFrame([{"date": r.date, "item": r.item_name, "wastage": r.wastage} for r in q])
    return {
        "total_wastage": float(df["wastage"].sum()),
        "by_item": df.groupby("item")["wastage"].sum().to_dict()
    }

@app.get("/predict")
def predict(item_name: str | None = None, days: int = 1, db: Session = Depends(get_db)):
    q = db.query(models.FoodEntry)
    if item_name:
        q = q.filter(models.FoodEntry.item_name == item_name)
    rows = q.order_by(models.FoodEntry.date).all()

    if not rows:
        raise HTTPException(status_code=404, detail="No data found for this item")

    if len(rows) < 10:
        avg = sum([r.consumed_qty for r in rows]) / len(rows)
        return {
            "prediction": [
                {"ds": (rows[-1].date + timedelta(days=i)), "yhat": round(avg, 2)}
                for i in range(1, days + 1)
            ],
            "note": "Used average due to insufficient data"
        }

    df = pd.DataFrame([{"ds": r.date, "y": r.consumed_qty} for r in rows])
    df = df.groupby("ds").sum().reset_index()

    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    result = forecast[["ds", "yhat"]].tail(days).to_dict(orient="records")
    for r in result:
        r["yhat"] = round(float(r["yhat"]), 2)
    return {"prediction": result}
