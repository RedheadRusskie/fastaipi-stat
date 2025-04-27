from fastapi import APIRouter, HTTPException, Depends, Security
from typing import List, Optional, Union
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas import DatasetDTO, DatasetResponseDTO
from app.auth import get_current_user
from app.models import User
from app.db.dependencies import get_db
from app.models import Dataset

router = APIRouter()


@router.post("/dataset")
async def post_dataset(
    dataset_data: DatasetDTO,
    db: Session = Depends(get_db),
    user_info: dict = Security(get_current_user),
):
    user_id = user_info["user_id"]

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404, detail="Could not find user by specified user ID"
        )

    new_dataset = Dataset(
        name=dataset_data.name,
        user_id=user_id,
        description=dataset_data.description,
    )

    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)

    return {
        "message": f"Dataset {dataset_data.name} created successfully",
        "dataset_id": new_dataset.id,
    }


@router.get(
    "/dataset", response_model=Union[DatasetResponseDTO, List[DatasetResponseDTO]]
)
async def get_dataset(
    dataset_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    user_info: dict = Security(get_current_user),
):
    user_id = user_info["user_id"]

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404, detail="Could not find user by specified user ID"
        )

    if dataset_id is not None:
        dataset = (
            db.query(Dataset)
            .filter(Dataset.id == dataset_id, Dataset.user_id == user_id)
            .first()
        )

        if dataset is None:
            raise HTTPException(
                status_code=404, detail="Could not find dataset with supplied ID"
            )

        return dataset

    datasets = db.query(Dataset).filter(Dataset.user_id == user_id).all()

    return datasets


@router.delete("/dataset/{dataset_id}")
async def delete_dataset(
    dataset_id: UUID,
    db: Session = Depends(get_db),
    user_info: dict = Security(get_current_user),
):
    user_id = user_info["user_id"]

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404, detail="Could not find user by specified user ID"
        )

    dataset_entry = (
        db.query(Dataset)
        .filter(
            Dataset.id == dataset_id,
            Dataset.user_id == user_id,
        )
        .first()
    )

    if dataset_entry is None:
        raise HTTPException(
            status_code=404, detail="Could not find dataset with supplied ID"
        )

    db.delete(dataset_entry)
    db.commit()

    return {"message": "Dataset of ID removed successfully", "dataset_id": dataset_id}
