from fastapi import FastAPI, Depends, HTTPException
from pydantic import UUID4, ValidationError
from sqlalchemy.orm import Session
from app.db import get_db
from app.services import add_person, rename_person, remove_person, get_person
from app.models import PersonAdded, PersonRenamed, PersonRemoved, WebhookPayload, GetNameResponse

app = FastAPI(
    title="Elysian Insurance Services - Claim Conductor Phonebook Integration",
    description="Service that handles incoming webhook notifications from a phonebook, manages internal state, and allows querying for current user names.",
    version="1.0.0",
)

@app.post("/accept_webhook", responses={
    200: {"description": "Webhook processed successfully"},
    400: {"description": "Invalid input"},
    404: {"description": "Person not found"},
    500: {"description": "Server error"}
})
def accept_webhook(payload: WebhookPayload, db: Session = Depends(get_db)):
    try:
        if payload.payload_type == "PersonAdded":
            person_data = PersonAdded(**payload.payload_content)
            add_person(db, person_data)
        elif payload.payload_type == "PersonRenamed":
            person_data = PersonRenamed(**payload.payload_content)
            if not rename_person(db, person_data):
                raise HTTPException(status_code=404, detail="Person not found")
        elif payload.payload_type == "PersonRemoved":
            person_data = PersonRemoved(**payload.payload_content)
            if not remove_person(db, person_data):
                raise HTTPException(status_code=404, detail="Person not found")
        else:
            raise HTTPException(status_code=400, detail="Invalid input")
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid input")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Server error: {str(e)}')

    return {"detail": "Webhook processed successfully"}

@app.get("/get_name", response_model=GetNameResponse, responses={
    200: {"description": "Name fetched successfully"},
    400: {"description": "Invalid UUID format"},
    404: {"description": "Person not found"},
    500: {"description": "Server error"}
})
async def get_name(person_id: UUID4, db: Session = Depends(get_db)):
    try:
        person = get_person(db, person_id)
        if not person:
            raise HTTPException(status_code=404, detail="Person not found")
        return {"name": person.name}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Server error")