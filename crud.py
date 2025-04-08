from sqlalchemy.orm import Session
from models import Personaje, Mision, MisionPersonaje

def crear_personaje(db: Session, nombre: str):
    personaje = Personaje(nombre=nombre)
    db.add(personaje)
    db.commit()
    db.refresh(personaje)
    return personaje

def crear_mision(db: Session, descripcion: str, xp: int):
    mision = Mision(descripcion=descripcion, xp=xp)
    db.add(mision)
    db.commit()
    db.refresh(mision)
    return mision

def aceptar_mision(db: Session, personaje_id: int, mision_id: int):
    personaje = db.query(Personaje).filter(Personaje.id == personaje_id).first()
    orden = len(personaje.misiones_rel)
    db.add(MisionPersonaje(personaje_id=personaje_id, mision_id=mision_id, orden=orden))
    db.commit()

def completar_mision(db: Session, personaje_id: int):
    personaje = db.query(Personaje).filter(Personaje.id == personaje_id).first()
    if personaje.misiones_rel:
        rel = personaje.misiones_rel.pop(0)
        mision = db.query(Mision).filter(Mision.id == rel.mision_id).first()
        personaje.xp += mision.xp
        db.delete(rel)
        db.commit()
        return mision
    return None

def listar_misiones(db: Session, personaje_id: int):
    personaje = db.query(Personaje).filter(Personaje.id == personaje_id).first()
    return [db.query(Mision).get(rel.mision_id) for rel in personaje.misiones_rel]
