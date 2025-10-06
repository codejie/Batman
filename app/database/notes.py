from sqlalchemy import Column, Integer, String, DateTime, func, select, delete, and_, update, Text
from app.database import TableBase, dbEngine
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import json

class NoteItemTable(TableBase):
  __tablename__ = 'note_items'

  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
  uid = Column(Integer, nullable=False)
  title = Column(String, nullable=False)
  tags = Column(String)  # Stored as a JSON string
  content = Column(Text)
  created = Column(DateTime, default=func.now())
  updated = Column(DateTime, default=func.now(), onupdate=func.now())

class NoteItemModel(BaseModel):
  id: Optional[int] = None
  uid: Optional[int] = None # Changed back to Optional[int]
  title: str
  tags: List[str]
  content: str
  updated: Optional[datetime] = None
  created: Optional[datetime] = None

  class Config:
    orm_mode = True

def create_note(note: NoteItemModel) -> int:
  tags_json = json.dumps(note.tags)
  new_note = NoteItemTable(
      uid=note.uid,
      title=note.title,
      tags=tags_json,
      content=note.content
  )
  return dbEngine.insert_instance(new_note)

def update_note(uid: int, note_id: int, note: NoteItemModel) -> None:
  tags_json = json.dumps(note.tags)
  stmt = update(NoteItemTable).where(
      and_(
          NoteItemTable.id == note_id,
          NoteItemTable.uid == uid
      )
  ).values(
      title=note.title,
      tags=tags_json,
      content=note.content
  )
  dbEngine.execute_stmt(stmt)

def delete_note(uid: int, note_id: int) -> None:
  stmt = delete(NoteItemTable).where(
      and_(
          NoteItemTable.id == note_id,
          NoteItemTable.uid == uid
      )
  )
  dbEngine.execute_stmt(stmt)

def list_notes(uid: int) -> List[NoteItemModel]:
  stmt = select(NoteItemTable).where(NoteItemTable.uid == uid).order_by(NoteItemTable.updated.desc())
  results = dbEngine.select_stmt(stmt)
  
  notes_list = []
  for item in results:
    note_table = item[0]
    notes_list.append(NoteItemModel(
        id=note_table.id,
        uid=note_table.uid,
        title=note_table.title,
        tags=json.loads(note_table.tags) if note_table.tags else [],
        content=note_table.content,
        updated=note_table.updated, # Corrected from updatedAt
        created=note_table.created
    ))
  return notes_list