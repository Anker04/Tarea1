from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from schemas import PersonajeCreate, MisionCreate
import crud

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/personajes")
def crear_personaje(personaje: PersonajeCreate, db: Session = Depends(get_db)):
    return crud.crear_personaje(db, personaje.nombre)

@app.post("/misiones")
def crear_mision(mision: MisionCreate, db: Session = Depends(get_db)):
    return crud.crear_mision(db, mision.descripcion, mision.xp)

@app.post("/personajes/{personaje_id}/misiones/{mision_id}")
def aceptar_mision(personaje_id: int, mision_id: int, db: Session = Depends(get_db)):
    crud.aceptar_mision(db, personaje_id, mision_id)
    return {"mensaje": "Misión encolada"}

@app.post("/personajes/{personaje_id}/completar")
def completar_mision(personaje_id: int, db: Session = Depends(get_db)):
    mision = crud.completar_mision(db, personaje_id)
    if mision:
        return {"mensaje": f"Misión completada: {mision.descripcion}"}
    return {"mensaje": "No hay misiones pendientes"}

@app.get("/personajes/{personaje_id}/misiones")
def listar_misiones(personaje_id: int, db: Session = Depends(get_db)):
    misiones = crud.listar_misiones(db, personaje_id)
    return [{"id": m.id, "descripcion": m.descripcion, "xp": m.xp} for m in misiones]
