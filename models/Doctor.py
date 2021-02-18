import database.db as db
from sqlalchemy import Column, Integer, String, Float 
from sqlalchemy.orm import relationship

class Doctor(db.Base): 
    __tablename__ = 'doctors'

    id = Column('id', Integer, primary_key=True, nullable=False) 
    name = Column('name', String(20), nullable=False) 
    lastname = Column('lastname', String(20), nullable=False) 
    code = Column('lastname', String(20), nullable=False)

    def __init__(self, id, name, lastname, code): 
        self.id = id
        self.name = name
        self.lastname = lastname
        self.code = code

    def __repr__(self):
        return f"{self.id}/{self.name}/{self.lastname}/{self.code}"