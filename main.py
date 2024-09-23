from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Car
from schema import CarlistValidate
from typing import List
app = FastAPI(title='car ')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/create/', response_model=CarlistValidate)
def create_car(car: CarlistValidate, db: Session = Depends(get_db)):
    db_car = Car(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


@app.get('/cars/', response_model=List[CarlistValidate])
def read_cars(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cars = db.query(Car).offset(skip).limit(limit).all()
    return cars


@app.get('/cars/{car_id}', response_model=CarlistValidate)
def read_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail='not fount')
    else:
        return car


@app.put('/cars/update/{car_id}', response_model=CarlistValidate)
def update_car(car_id: int, car: CarlistValidate, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == car_id).first()

    if db_car is None:
        raise HTTPException(status_code=404, detail='not found')

    for key, value in car.dict().items():
        setattr(db_car, key, value)

    db.commit()
    db.refresh(db_car)
    return db_car


@app.delete('/cars/delete/{car_id}', response_model=CarlistValidate)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == car_id).first()

    if db_car is None:
        raise HTTPException(status_code=404, detail='not found')

    db.delete(db_car)
    db.commit()
    return db_car


