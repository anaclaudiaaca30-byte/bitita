from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .crud import create_student, delete_student, get_dashboard, get_students, update_student
from .database import Base, engine, get_db
from .schemas import DashboardItem, StudentCreate, StudentRead, StudentUpdate

BASE_DIR = Path(__file__).resolve().parent.parent

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bitita Web",
    description="Sistema escolar com API, banco de dados e dashboard.",
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/students", response_model=list[StudentRead])
def list_students(db: Session = Depends(get_db)):
    return get_students(db)


@app.post("/api/students", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student_route(student: StudentCreate, db: Session = Depends(get_db)):
    return create_student(db, student)


@app.put("/api/students/{student_id}", response_model=StudentRead)
def update_student_route(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    updated = update_student(db, student_id, student)
    if updated is None:
        raise HTTPException(status_code=404, detail="Estudante não encontrado")
    return updated


@app.delete("/api/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_route(student_id: int, db: Session = Depends(get_db)):
    deleted = delete_student(db, student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Estudante não encontrado")


@app.get("/api/dashboard", response_model=list[DashboardItem])
def dashboard(db: Session = Depends(get_db)):
    return get_dashboard(db)
