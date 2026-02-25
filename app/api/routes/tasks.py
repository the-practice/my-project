"""
Task API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.database import get_db
from app.models import Task, TaskState

router = APIRouter()


@router.post("/", response_model=Dict[str, Any])
async def create_task(
    goal: str,
    user_id: str,
    metadata_json: Optional[Dict[str, Any]] = None,
    db: Session = Depends(get_db)
):
    """
    Create a new task.
    """
    task = Task(
        goal=goal,
        user_id=user_id,
        state=TaskState.INIT.value,
        metadata_json=metadata_json
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "status": "success",
        "task_id": str(task.id),
        "message": "Task created successfully"
    }


@router.get("/", response_model=List[Dict[str, Any]])
async def get_tasks(
    state: Optional[str] = None,
    user_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all tasks with optional filtering by state and user.
    """
    query = db.query(Task)

    if state:
        query = query.filter(Task.state == state)
    if user_id:
        query = query.filter(Task.user_id == user_id)

    tasks = query.offset(skip).limit(limit).all()

    return [
        {
            "id": str(task.id),
            "user_id": str(task.user_id),
            "goal": task.goal,
            "state": task.state,
            "metadata_json": task.metadata_json,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None,
        }
        for task in tasks
    ]


@router.get("/{task_id}", response_model=Dict[str, Any])
async def get_task(task_id: str, db: Session = Depends(get_db)):
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
        "id": str(task.id),
        "user_id": str(task.user_id),
        "goal": task.goal,
        "state": task.state,
        "metadata_json": task.metadata_json,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "updated_at": task.updated_at.isoformat() if task.updated_at else None,
    }


@router.get("/{task_id}/logs", response_model=List[Dict[str, Any]])
async def get_task_logs(task_id: str, db: Session = Depends(get_db)):
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
            "id": str(log.id),
            "event_type": log.event_type,
            "payload_json": log.payload_json,
            "timestamp": log.timestamp.isoformat() if log.timestamp else None
        }
        for log in logs
    ]


@router.post("/{task_id}/execute", response_model=Dict[str, Any])
async def execute_task(task_id: str, db: Session = Depends(get_db)):
    """
    Execute a task.
    """
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    if task.state == TaskState.COMPLETED.value:
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

    task.state = TaskState.CALL_IN_PROGRESS.value
    db.commit()

    return {
        "status": "success",
        "task_id": str(task.id),
        "message": "Task execution started"
    }


@router.post("/{task_id}/replan", response_model=Dict[str, Any])
async def replan_task(task_id: str, db: Session = Depends(get_db)):
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

    task.state = TaskState.INIT.value
    db.commit()

    return {
        "status": "success",
        "task_id": str(task.id),
        "message": "Task replanning initiated"
    }
