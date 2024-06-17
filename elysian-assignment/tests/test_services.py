import pytest
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Person, PersonAdded, PersonRenamed, PersonRemoved
from app.services import add_person, rename_person, remove_person, get_person

def test_add_person(db_session: Session):
    person_data = PersonAdded(
        person_id=uuid.UUID(str(uuid.uuid4())),
        name="Test User",
        timestamp=datetime.now()
    )
    new_person = add_person(db_session, person_data)
    assert new_person.id == str(person_data.person_id)
    assert new_person.name == person_data.name

def test_rename_person(db_session: Session):
    person_id = str(uuid.uuid4())
    person = Person(id=person_id, name="Original Name")
    db_session.add(person)
    db_session.commit()

    person_data = PersonRenamed(
        person_id=uuid.UUID(person_id),
        name="Updated Name",
        timestamp=datetime.now()
    )
    renamed_person = rename_person(db_session, person_data)
    assert renamed_person.name == "Updated Name"

def test_remove_person(db_session: Session):
    person_id = str(uuid.uuid4())
    person = Person(id=person_id, name="Test User")
    db_session.add(person)
    db_session.commit()

    person_data = PersonRemoved(
        person_id=uuid.UUID(person_id),
        timestamp=datetime.now()
    )
    remove_result = remove_person(db_session, person_data)
    assert remove_result is True
    removed_person = db_session.query(Person).filter(Person.id == person_id).first()
    assert removed_person is None

def test_get_person(db_session: Session):
    person_id = str(uuid.uuid4())
    person = Person(id=person_id, name="Test User")
    db_session.add(person)
    db_session.commit()

    retrieved_person = get_person(db_session, person_id)
    assert retrieved_person.id == person_id
    assert retrieved_person.name == "Test User"