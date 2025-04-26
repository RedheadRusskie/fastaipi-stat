from fastapi import APIRouter, Depends, HTTPException, Security, Query
from typing import List
from sqlalchemy.orm import Session
from uuid import UUID
from app.models import User
from app.auth import get_current_user
from app.db.dependencies import get_db
from app.models import Dataset, DatasetRow
from app.schemas.dataset_row import DatasetRowDTO

router = APIRouter()


@router.post("/row")
async def create_row(
    row_data: DatasetRowDTO,
    db: Session = Depends(get_db),
    user_info: dict = Security(get_current_user),
):
    user_id = user_info["user_id"]

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404, detail="Could not find user by specified user ID"
        )

    dataset = (
        db.query(Dataset)
        .filter(Dataset.id == row_data.dataset_id, Dataset.user_id == user_id)
        .first()
    )

    if not dataset:
        raise HTTPException(
            status_code=404, detail="Dataset not found or not owned by user"
        )

    new_row = DatasetRow(
        dataset_id=row_data.dataset_id,
        data=row_data.data,
    )

    db.add(new_row)
    db.commit()
    db.refresh(new_row)

    return {
        "message": "Row created successfully",
        "row_id": new_row.id,
    }


@router.get("/row/{dataset_id}", response_model=List[DatasetRowDTO])
async def read_rows(
    dataset_id: UUID,
    db: Session = Depends(get_db),
    user_info: dict = Security(get_current_user),
    limit: int = Query(15, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    user_id = user_info["user_id"]

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404, detail="Could not find user by specified user ID"
        )

    dataset = (
        db.query(Dataset)
        .filter(Dataset.id == dataset_id, Dataset.user_id == user_id)
        .first()
    )

    if not dataset:
        raise HTTPException(
            status_code=404, detail="Dataset not found or not owned by user"
        )

    rows = (
        db.query(DatasetRow)
        .filter(DatasetRow.dataset_id == dataset_id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return rows


@router.put("/row/{row_id}")
async def update_row(
    row_id: UUID,
    row_data: DatasetRowDTO,
    db: Session = Depends(get_db),
    user_info: dict = Security(get_current_user),
):
    user_id = user_info["user_id"]

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404, detail="Could not find user by specified user ID"
        )

    row = db.query(DatasetRow).filter(DatasetRow.id == row_id).first()

    if not row:
        raise HTTPException(
            status_code=404, detail="Row not found with specified row ID"
        )

    dataset = (
        db.query(Dataset)
        .filter(Dataset.id == row.dataset_id, Dataset.user_id == user_id)
        .first()
    )

    if not dataset:
        raise HTTPException(status_code=403, detail="Not authorized to modify this row")

    row.data = row_data.data

    db.commit()
    db.refresh(row)

    return {
        "message": "Row updated successfully",
        "row_id": row.id,
    }


@router.delete("/row/{row_id}")
async def delete_row(
    row_id: UUID,
    db: Session = Depends(get_db),
    user_info: dict = Security(get_current_user),
):
    user_id = user_info["user_id"]

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404, detail="Could not find user by specified user ID"
        )

    row = db.query(DatasetRow).filter(DatasetRow.id == row_id).first()

    if not row:
        raise HTTPException(
            status_code=404, detail="Row not found with specified row ID"
        )

    dataset = (
        db.query(Dataset)
        .filter(Dataset.id == row.dataset_id, Dataset.user_id == user_id)
        .first()
    )

    if not dataset:
        raise HTTPException(status_code=403, detail="Not authorized to delete this row")

    db.delete(row)
    db.commit()

    return {"message": "Row deleted successfully", "row_id": row_id}
