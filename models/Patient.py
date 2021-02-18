import database.db as db
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

class Patient(db.Base): 
    __tablename__ = 'patients'

    id = Column('id', Integer, primary_key=True, nullable=False) 
    name = Column('name', String(20), nullable=False) 
    lastname = Column('lastname', String(20), nullable=False) 
    code = Column('lastname', String(20), nullable=False)
    doctors_id = Column('doctors_id', String(15), ForeignKey('doctors.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    doctors = relationship("Doctor", back_populates="patients")

    def __init__(self, id, name, lastname, code, doctors_id): 
        self.id = id
        self.name = name
        self.lastname = lastname
        self.code = code
        self.doctors_id = doctors_id

    def __repr__(self):
        return f"<Patient {self.id}>"