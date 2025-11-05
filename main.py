from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from pydantic import BaseModel

app = FastAPI()

print("✅ Database connected successfully!")


# Pydantic model (for input validation)
class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a new task
@app.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(
        title=task.title,
        description=task.description,
        completed=task.completed
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task created", "task": new_task}


# Read all tasks
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks


# Read one task
@app.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# Update a task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = updated_task.title
    task.description = updated_task.description
    task.completed = updated_task.completed
    db.commit()
    db.refresh(task)
    return {"message": "Task updated", "task": task}


# Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}
