from fastapi import APIRouter, UploadFile, Form, HTTPException
from pydantic import BaseModel

from env import config
from fast_app.functions.pb import PBFunctions
from web_app.enums import Game

router = APIRouter()


class PostFormData(BaseModel):
    token: str
    uid: int
    game: Game


class PostFormReturnData(BaseModel):
    account_id: str


@router.post("/upload")
async def upload_file(
    file: UploadFile,
    token: str = Form(...),
    uid: int = Form(...),
    game: Game = Form(...),
) -> PostFormReturnData:
    if token != config.pb.token:
        raise HTTPException(status_code=403, detail="Invalid token")
    await PBFunctions.save_file(file, uid, game)
    account_id = await PBFunctions.create_hash(uid, game)
    return PostFormReturnData(account_id=account_id)
