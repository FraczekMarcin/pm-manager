import asyncio, os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base, SessionLocal
from .routers import auth_router, projects_router, subcategories_router, notifications_router, admin_router
from . import models
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)

app = FastAPI(title='PM Manager')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth_router.router)
app.include_router(projects_router.router)
app.include_router(subcategories_router.router)
app.include_router(notifications_router.router)
app.include_router(admin_router.router)

async def deadline_checker():
    while True:
        db = SessionLocal()
        try:
            now = datetime.utcnow()
            threshold = now + timedelta(hours=48)
            subs = db.query(models.Subcategory).filter(models.Subcategory.due_date != None, models.Subcategory.due_date <= threshold, models.Subcategory.notified == False).all()
            for sc in subs:
                note = models.Notification(user_id=sc.project.owner_id, subcategory_id=sc.id, message=f"Deadline '{sc.title}' is approaching: {sc.due_date}")
                db.add(note)
                sc.notified = True
            db.commit()
        except Exception as e:
            print('checker error', e)
        finally:
            db.close()
        await asyncio.sleep(60*60)

@app.on_event('startup')
async def startup_event():
    asyncio.create_task(deadline_checker())

@app.get('/')
def root():
    return {'ok': True}
