from fastapi import APIRouter, Depends, HTTPException, Security, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Union
from uuid import UUID
from app.models import User
from app.auth import get_current_user
from app.db.dependencies import get_db
from app.models import Dataset, DatasetRow
from app.schemas import DatasetRowCreateDTO, DatasetRowUpdateDTO, DatasetRowResponseDTO
from app.services import StatsService, StatisticalOperation

router = APIRouter()


@router.post("/row")
async def create_row(
    row_data: Union[DatasetRowCreateDTO, List[DatasetRowCreateDTO]] = Body(...),
    db: Session = Depends(get_db),
    user_info: dict = Security(get_current_user),
):
    user_id = user_info["user_id"]

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404, detail="Could not find user by specified user ID"
        )

    if not isinstance(row_data, list):
        row_data = [row_data]

    if not row_data:
        raise HTTPException(status_code=400, detail="No row data supplied")

    if len(row_data) > 100:
        raise HTTPException(
            status_code=400,
            detail="Only a maximum of 100 entries may be persisted at once",
        )

    dataset_id = row_data[0].dataset_id

    dataset = (
        db.query(Dataset)
        .filter(Dataset.id == dataset_id, Dataset.user_id == user_id)
        .first()
    )

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail=f"Dataset {dataset_id} not found or not owned by user",
        )

    new_rows = [
        DatasetRow(dataset_id=row.dataset_id, data=row.data) for row in row_data
    ]

    db.add_all(new_rows)
    db.commit()

    for row in new_rows:
        db.refresh(row)

    entriesRO = [
        DatasetRowResponseDTO(
            id=obj.id,
            dataset_id=obj.dataset_id,
            data=obj.data,
            created_at=obj.created_at,
        )
        for obj in new_rows
    ]

    return {
        "message": f"Created {len(entriesRO)} entries successfully",
        "entries": entriesRO,
    }


@router.get("/row/{dataset_id}")
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


@router.get("/row/opearation/{dataset_id}")
async def calculate_on_data(
    dataset_id: UUID,
    column: str = Query(...),
    operation: str = Query(...),
    # target_column required only for linear regression
    target_column: Optional[str] = Query(None),
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
        .filter(Dataset.id == dataset_id, Dataset.user_id == user_id)
        .first()
    )

    if not dataset:
        raise HTTPException(
            status_code=404, detail="Dataset not found or not owned by user"
        )

    rows = db.query(DatasetRow).filter(DatasetRow.dataset_id == dataset_id).all()
    raw_data = [row.data for row in rows]

    try:
        verified_operation = StatisticalOperation(operation)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid operation '{operation}'",
        )

    if operation == "linear_regression" and not target_column:
        raise HTTPException(
            status_code=400, detail="target_column is required for linear regression"
        )

    if not all(column in row for row in raw_data):
        raise HTTPException(
            status_code=400, detail=f"Column '{column}' does not exist in the dataset"
        )

    try:
        result = StatsService.calculate(
            data=raw_data,
            column=column,
            operation=verified_operation,
            target_column=target_column,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return {"result": result}


@router.put("/row")
async def update_rows(
    row_data: Union[DatasetRowUpdateDTO, List[DatasetRowUpdateDTO]] = Body(...),
    db: Session = Depends(get_db),
    user_info: dict = Security(get_current_user),
):
    user_id = user_info["user_id"]

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404, detail="Could not find user by specified user ID"
        )

    if not isinstance(row_data, list):
        row_data = [row_data]

    if not row_data:
        raise HTTPException(status_code=400, detail="No row data supplied")

    if len(row_data) > 100:
        raise HTTPException(
            status_code=400,
            detail="Only a maximum of 100 entries may be updated at once",
        )

    updated_rows = []

    for item in row_data:
        row = db.query(DatasetRow).filter(DatasetRow.id == item.id).first()

        if not row:
            raise HTTPException(
                status_code=404, detail=f"Row with ID {item.id} not found"
            )

        dataset = (
            db.query(Dataset)
            .filter(Dataset.id == row.dataset_id, Dataset.user_id == user_id)
            .first()
        )

        if not dataset:
            raise HTTPException(
                status_code=403,
                detail=f"Not authorized to modify row with ID {item.id}",
            )

        row.data = item.data

        updated_rows.append(row)

    db.commit()

    for row in updated_rows:
        db.refresh(row)

    entriesRO = [
        DatasetRowResponseDTO(
            id=obj.id,
            dataset_id=obj.dataset_id,
            data=obj.data,
            created_at=obj.created_at,
        )
        for obj in updated_rows
    ]

    return {
        "message": f"Updated {len(entriesRO)} entries successfully",
        "entries": entriesRO,
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
