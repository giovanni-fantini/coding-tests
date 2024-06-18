import os
import openai
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import UUID4
from app.models import Person, PersonAdded, PersonRenamed, PersonRemoved

openai.api_key = os.getenv('OPENAI_API_KEY')

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

def translate_nl_to_sql(nl_query: str) -> str:
    system_message = """
    Given the following SQL table, your job is to write safe queries given a user's request. \n
    Ensure that no dangerous operations can be performed on the database (like SQL injection or deletion of records). \n
        CREATE TABLE people (
        id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255)
    )
    WITH SYSTEM VERSIONING
    """
    user_message = f'For the following question, write a SQL query with placeholders for parameters and provide the parameters separate in JSON: {nl_query}'
    message = [
    {
      "role": "system",
      "content": system_message
    },
    {
      "role": "user",
      "content": user_message
    }
    ]
    return openai.Completion.create(
            model="gpt-3.5-turbo",
            messages = message,
            temperature = 0,
            max_tokens=256  # Adjust based on your requirements
        )

# def execute_sql_query(db: Session, query_template: str, params: dict):
#     try:
#         result = db.execute(query_template, params)
#         db.commit()

#         # Fetch and format result rows
#         rows = result.fetchall()
#         return '\n'.join([str(row) for row in rows])
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise Exception(f"SQL execution error: {str(e)}")