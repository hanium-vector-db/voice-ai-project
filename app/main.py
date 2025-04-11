from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers.stt_router import router as stt_router # stt_router와 tts_router 임포트
from app.routers.tts_router import router as tts_router  # tts_router 임포트

import os

app = FastAPI()

# CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# STT 라우터
app.include_router(stt_router, prefix="/stt")
app.include_router(tts_router, prefix="/tts")

# 정적 파일 (HTML 프론트엔드)
frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)

# python -m app.main
# uvicorn app.main:app --reload
