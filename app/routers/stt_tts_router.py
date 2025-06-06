from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
import logging
from app.services.stt_service import transcribe_audio_file, convert_webm_to_wav
from app.services.processor_service import get_ai_response
from app.services.tts_service import text_to_speech
from fastapi import Form
import uuid


logger = logging.getLogger(__name__)

router = APIRouter()

# 업로드 디렉토리 설정
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

LANGUAGE_TO_VOICE = {
    "한국어": "nova",
    "영어": "alloy",
    "일본어": "shimmer",
    # 필요시 추가
}

@router.post("/")
async def stt_to_tts(
    audio: UploadFile = File(...),
    language: str = Form("한국어"),  # 기본값 한국어, 프론트에서 전달받음
    provider: str = Form("openai"),   # "openai" 또는 "ollama"
    model: str = Form("gpt-4"),       # "gpt-4", "llama3" 등
):
    try:
        logger.info("STT → GPT → TTS 요청 시작")
        # 1. 업로드된 파일 저장
        webm_path = os.path.join(UPLOAD_DIR, audio.filename)
        logger.info(f"업로드된 파일 경로: {webm_path}")
        with open(webm_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        # 2. webm → wav 변환
        wav_path = webm_path.replace(".webm", ".wav")
        convert_webm_to_wav(webm_path, wav_path)
        logger.info(f"webm → wav 변환 완료: {wav_path}")

        # 3. STT 처리
        stt_text = transcribe_audio_file(wav_path)
        logger.info(f"STT 변환 결과: {stt_text}")

        # 4. GPT 처리
        gpt_response = get_ai_response(stt_text, language=language, provider=provider, model=model)
        logger.info(f"GPT 응답 텍스트: {gpt_response}")

        # 5. TTS 처리
        unique_id = str(uuid.uuid4())
        tts_output_path = os.path.join(UPLOAD_DIR, f"{unique_id}.mp3")
        voice = LANGUAGE_TO_VOICE.get(language, "nova")
        text_to_speech(gpt_response, tts_output_path, voice=voice)
        tts_file_url = f"/uploads/{unique_id}.mp3"
        logger.info(f"TTS 출력 파일 생성 완료: {tts_output_path}")

        # HTTP URL로 반환
        logger.info(f"클라이언트에 반환된 TTS 파일 경로: {tts_file_url}")
        return {
            "message": "STT → GPT → TTS 처리 완료",
            "stt_text": stt_text,
            "gpt_response": gpt_response,
            "tts_file_path": tts_file_url
        }
    except Exception as e:
        logger.error(f"에러 발생: {e}")
        raise HTTPException(status_code=500, detail=str(e))