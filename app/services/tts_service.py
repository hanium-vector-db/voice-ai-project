from google.cloud import texttospeech

# Google TTS 클라이언트 초기화
client = texttospeech.TextToSpeechClient()

def text_to_speech(text, output_path):
    synthesis_input = texttospeech.SynthesisInput(text=text)  # 입력 텍스트 설정
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",  # 한국어로 설정
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3  # 오디오 파일 형식 설정
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_path, "wb") as out:  # 파일을 이진 모드로 열기
        out.write(response.audio_content)  # 응답의 오디오 내용을 파일에 쓰기
    return output_path

# 실행 코드
output_path = "C:\\Users\\user\\Documents\\tts_output2.mp3"
text = "안녕하세요 말하기 테스트 입니다"
result_path = text_to_speech(text, output_path)
print(f"Audio file saved to {result_path}")
