from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..utils import get_db, get_admin_user
import os, io
import pandas as pd

router = APIRouter(prefix='/admin', tags=['admin'])

@router.post('/create_user')
def create_user(u: schemas.UserCreate, admin=Depends(get_admin_user), db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == u.email).first()
    if existing:
        raise HTTPException(400, 'exists')
    user = models.User(email=u.email, hashed_password=auth.get_password_hash(u.password), is_admin=u.is_admin)
    db.add(user); db.commit(); db.refresh(user)
    return {'id': user.id, 'email': user.email}

@router.get('/backup')
def backup(admin=Depends(get_admin_user)):
    db_path = './data/app.db'
    if not os.path.exists(db_path):
        raise HTTPException(404, 'db not found')
    return {'path': db_path}

@router.get('/export_excel')
def export_excel(admin=Depends(get_admin_user), db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()
    rows = []
    for p in projects:
        for s in p.subcategories:
            rows.append({
                'project_id': p.id,
                'project_title': p.title,
                'owner_email': p.owner.email if p.owner else '',
                'subcategory_id': s.id,
                'subcategory_title': s.title,
                'progress': s.progress,
                'due_date': s.due_date
            })
    df = pd.DataFrame(rows)
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='projects')
    out.seek(0)
    return Response(content=out.read(), media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers={
        'Content-Disposition': 'attachment; filename="projects_export.xlsx"'
    })
