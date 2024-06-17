from sqlalchemy.orm import Session
from app.models import Person, PersonAdded, PersonRenamed, PersonRemoved
from pydantic import UUID4

def add_person(db: Session, person_data: PersonAdded):
    new_person = Person(id=str(person_data.person_id), name=person_data.name)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person

def rename_person(db: Session, person_data: PersonRenamed):
    person = db.query(Person).filter(Person.id == str(person_data.person_id)).first()
    if not person:
        return False
    
    person.name = person_data.name
    db.commit()
    db.refresh(person)
    return person

def remove_person(db: Session, person_data: PersonRemoved):
    person = db.query(Person).filter(Person.id == str(person_data.person_id)).first()
    if not person:
        return False
    
    db.delete(person)
    db.commit()
    return True

def get_person(db: Session, person_id: UUID4) -> Person:
    return db.query(Person).filter(Person.id == str(person_id)).first()