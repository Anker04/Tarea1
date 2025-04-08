from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy

from database import Base

class MisionPersonaje(Base):
    __tablename__ = "misiones_personajes"
    id = Column(Integer, primary_key=True, index=True)
    personaje_id = Column(Integer, ForeignKey("personajes.id"))
    mision_id = Column(Integer, ForeignKey("misiones.id"))
    orden = Column(Integer)  # Para mantener FIFO

class Personaje(Base):
    __tablename__ = "personajes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    xp = Column(Integer, default=0)
    misiones_rel = relationship("MisionPersonaje", order_by="MisionPersonaje.orden", cascade="all, delete-orphan")
    misiones = association_proxy("misiones_rel", "mision")

class Mision(Base):
    __tablename__ = "misiones"
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String)
    xp = Column(Integer)
