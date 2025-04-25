from fastapi import APIRouter, HTTPException, Depends, Security
from typing import List
from sqlalchemy.orm import Session
from app.schemas import DatasetResponseDTO
from app.auth import get_current_user
from app.models import User
from app.db.dependencies import get_db
from app.models import Dataset
from app.schemas import DatasetDTO

router = APIRouter()


@router.post("/dataset")
async def post_dataset(
    dataset_data: DatasetDTO,
    db: Session = Depends(get_db),
    username: str = Security(get_current_user),
):

    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(
            status_code=404, detail="Could not find user for dataset assignment"
        )

    new_dataset = Dataset(
        name=dataset_data.name,
        user_id=user.id,
        description=dataset_data.description,
    )

    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)

    return {
        "message": f"Dataset {dataset_data.name} created successfully",
        "dataset_id": new_dataset.id,
    }


@router.get("/dataset", response_model=List[DatasetResponseDTO])
async def get_dataset(
    db: Session = Depends(get_db),
    username: str = Security(get_current_user),
):

    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(
            status_code=404, detail="Could not find user to fetch datasets for"
        )

    datasets = db.query(Dataset).filter(Dataset.user_id == user.id).all()

    return datasets
