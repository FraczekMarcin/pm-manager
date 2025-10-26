from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..utils import get_db, get_current_user

router = APIRouter(prefix='/notifications', tags=['notifications'])

@router.get('/', response_model=list[schemas.NotificationOut])
def list_notifications(db: Session = Depends(get_db), user=Depends(get_current_user)):
    notes = db.query(models.Notification).filter(models.Notification.user_id == user.id).order_by(models.Notification.created_at.desc()).all()
    return notes
