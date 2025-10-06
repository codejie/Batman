from typing import List, Optional
from fastapi import APIRouter, Depends
from app.database import notes as db
from app.database.notes import NoteItemModel
from app.routers.common import DEFAULT_UID, RequestModel, ResponseModel, verify_token

router: APIRouter = APIRouter(
    prefix="/notes",
    tags=["Notes"],
    dependencies=[Depends(verify_token)]
)

# List Notes
class NoteListResponse(ResponseModel):
    result: List[NoteItemModel] = []

@router.post("/list", response_model=NoteListResponse)
async def list_notes(uid: int = Depends(verify_token)):
    result = db.list_notes(uid=uid)
    return NoteListResponse(result=result)

# Create Note
class NoteCreateRequest(RequestModel):
    title: str
    tags: List[str]
    content: str

class NoteCreateResponse(ResponseModel):
    result: int

@router.post("/create", response_model=NoteCreateResponse)
async def create_note(request: NoteCreateRequest, uid: int = Depends(verify_token)):
    note_model = NoteItemModel(
        uid=uid,
        title=request.title,
        tags=request.tags,
        content=request.content
    )
    note_id = db.create_note(note_model)
    return NoteCreateResponse(result=note_id)

# Update Note
class NoteUpdateRequest(RequestModel):
    id: int
    title: str
    tags: List[str]
    content: str

class NoteUpdateResponse(ResponseModel):
    result: int = 0

@router.post("/update", response_model=NoteUpdateResponse)
async def update_note(request: NoteUpdateRequest, uid: int = Depends(verify_token)):
    note_model = NoteItemModel(
        id=request.id,
        title=request.title,
        tags=request.tags,
        content=request.content
    )
    db.update_note(uid=uid, note_id=request.id, note=note_model)
    return NoteUpdateResponse(result=0)

# Delete Note
class NoteDeleteRequest(RequestModel):
    id: int

class NoteDeleteResponse(ResponseModel):
    result: int = 0

@router.post("/delete", response_model=NoteDeleteResponse)
async def delete_note(request: NoteDeleteRequest, uid: int = Depends(verify_token)):
    db.delete_note(uid=uid, note_id=request.id)
    return NoteDeleteResponse(result=0)