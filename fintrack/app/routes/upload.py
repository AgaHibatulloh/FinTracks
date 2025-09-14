from fastapi import APIRouter, UploadFile
import pandas as pd
from app.db import insert_financial_data

router = APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile):
    df = pd.read_csv(file.file)
    # Simpan ke DB
    insert_financial_data(df)
    return {"rows": len(df), "message": "Data uploaded"}