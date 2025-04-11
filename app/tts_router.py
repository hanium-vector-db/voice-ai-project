from fastapi import APIRouter, HTTPException, Form
from app.services.tts_service import text_to_speech
import os

router = APIRouter()

@router.post("/tts/")
async def tts_endpoint(text: str = Form(...)):
    try:
        output_path = os.path.join("uploads", "output.mp3")  # 출력 파일 경로 설정
        result_path = text_to_speech(text, output_path)  # TTS 함수 호출
        return {"message": "TTS processed successfully", "file_path": result_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
