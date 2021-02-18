import database.db as db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Record(db.Base): 
    __tablename__ = 'records'

    id = Column('id', Integer, primary_key=True, nullable=False) 
    systolic = Column('systolic', Float, nullable=False) 
    diastolic = Column('diastolic', Float, nullable=False) 
    frecuency = Column('frecuency', Float, nullable=False) 
    weight = Column('weight', Float, nullable=False) 
    date = Column('date', DateTime, nullable=False) 
    category = Column('category', String(255), nullable=False) 
    message = Column('message', String(255), nullable=False) 
    patients_id = Column('patients_id', String(15), ForeignKey('patients.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)

    def __init__(self, id, systolic, diastolic, frecuency, weight, date, category, message, patients_id): 
        self.id = id
        self.systolic = systolic
        self.diastolic = diastolic
        self.frecuency = frecuency
        self.weight = weight
        self.date = date
        self.category = category
        self.message = message
        self.patients_id = patients_id

    def __repr__(self):
        return f"<Record {self.id}>"