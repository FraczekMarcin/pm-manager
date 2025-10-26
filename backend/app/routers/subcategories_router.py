from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..utils import get_db, get_current_user

router = APIRouter(prefix='/subcategories', tags=['subcategories'])

@router.post('/{project_id}', response_model=schemas.SubcategoryOut)
def add_subcategory(project_id: int, payload: schemas.SubcategoryCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(404, 'Project not found')
    sc = models.Subcategory(project_id=project_id, title=payload.title, details=payload.details, progress=payload.progress, due_date=payload.due_date)
    db.add(sc); db.commit(); db.refresh(sc)
    return sc

@router.patch('/{sub_id}', response_model=schemas.SubcategoryOut)
def update_subcategory(sub_id: int, payload: schemas.SubcategoryCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    sc = db.query(models.Subcategory).filter(models.Subcategory.id == sub_id).first()
    if not sc:
        raise HTTPException(404, 'Not found')
    sc.title = payload.title; sc.details = payload.details
    sc.progress = payload.progress; sc.due_date = payload.due_date
    db.commit(); db.refresh(sc)
    return sc
