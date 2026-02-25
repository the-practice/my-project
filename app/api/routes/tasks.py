"""
Task API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import Task, TaskStatus, TaskPriority

router = APIRouter()


@router.post("/", response_model=Dict[str, Any])
async def create_task(
    title: str,
    description: Optional[str] = None,
    priority: TaskPriority = TaskPriority.MEDIUM,
    db: Session = Depends(get_db)
):
    """
    Create a new task.
    """
    task = Task(
        title=title,
        description=description,
        priority=priority,
        status=TaskStatus.PENDING
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return {
        "status": "success",
        "task_id": task.id,
        "message": "Task created successfully"
    }


@router.get("/", response_model=List[Dict[str, Any]])
async def get_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all tasks with optional filtering.
    """
    query = db.query(Task)
    
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    
    tasks = query.offset(skip).limit(limit).all()
    
    return [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status.value,
            "priority": task.priority.value,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat() if task.updated_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None
        }
        for task in tasks
    ]


@router.get("/{task_id}", response_model=Dict[str, Any])
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Get a specific task by ID.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status.value,
        "priority": task.priority.value,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat() if task.updated_at else None,
        "completed_at": task.completed_at.isoformat() if task.completed_at else None
    }


@router.get("/{task_id}/logs", response_model=List[Dict[str, Any]])
async def get_task_logs(task_id: int, db: Session = Depends(get_db)):
    """
    Get logs for a specific task.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    logs = task.logs
    
    return [
        {
            "id": log.id,
            "level": log.level,
            "message": log.message,
            "created_at": log.created_at.isoformat()
        }
        for log in logs
    ]


@router.post("/{task_id}/execute", response_model=Dict[str, Any])
async def execute_task(task_id: int, db: Session = Depends(get_db)):
    """
    Execute a task.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    if task.status == TaskStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task is already completed"
        )
    
    # TODO: Implement task execution logic
    # This will include:
    # - Task planning
    # - Tool execution
    # - Result recording
    # - Log generation
    
    task.status = TaskStatus.IN_PROGRESS
    db.commit()
    
    return {
        "status": "success",
        "task_id": task.id,
        "message": "Task execution started"
    }


@router.post("/{task_id}/replan", response_model=Dict[str, Any])
async def replan_task(task_id: int, db: Session = Depends(get_db)):
    """
    Force replan a task.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    # TODO: Implement task replanning logic
    # This will include:
    # - Re-evaluating task requirements
    # - Updating task plan
    # - Adjusting execution strategy
    
    return {
        "status": "success",
        "task_id": task.id,
        "message": "Task replanning initiated"
    }
