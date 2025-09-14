from fastapi import APIRouter, Query
from sqlalchemy import select
from app.db import engine, finance_table
import numpy as np
import json
from app.utils import get_embedding

router = APIRouter()

@router.get("/ask")
async def ask_question(q: str = Query(...)):
    query_emb = get_embedding(q)

    with engine.begin() as conn:
        rows = conn.execute(select(finance_table)).fetchall()

    # hitung cosine similarity sederhana
    sims = []
    for r in rows:
        emb = json.loads(r.embedding) if r.embedding else [0]
        sim = np.dot(query_emb, emb) / (np.linalg.norm(query_emb) * np.linalg.norm(emb))
        sims.append((sim, r))

    # ambil row paling mirip
    best = sorted(sims, key=lambda x: x[0], reverse=True)[0][1]
    return {"best_match": dict(best._mapping)}