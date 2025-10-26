from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..utils import get_db, get_current_user, get_admin_user

router = APIRouter(prefix='/projects', tags=['projects'])

@router.post('/', response_model=schemas.ProjectOut)
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    p = models.Project(owner_id=user.id, title=payload.title, description=payload.description)
    db.add(p); db.commit(); db.refresh(p)
    return project_to_out(p)

@router.get('/', response_model=list[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(models.Project).filter(models.Project.archived == False).all()
    return [project_to_out(p) for p in projects]

@router.get('/{project_id}', response_model=schemas.ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    p = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not p:
        raise HTTPException(404, 'Not found')
    return project_to_out(p)

@router.delete('/{project_id}')
def delete_project(project_id: int, admin=Depends(get_admin_user), db: Session = Depends(get_db)):
    p = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not p:
        raise HTTPException(404, 'Not found')
    p.archived = True
    db.commit()
    return {'ok': True}

def project_to_out(p):
    return {
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'owner_email': p.owner.email if p.owner else 'unknown',
        'archived': p.archived,
        'subcategories': [{
            'id': s.id, 'title': s.title, 'details': s.details, 'progress': s.progress,
            'due_date': s.due_date.isoformat() if s.due_date else None, 'notified': s.notified
        } for s in p.subcategories]
    }
