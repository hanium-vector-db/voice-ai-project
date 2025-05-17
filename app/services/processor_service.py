import openai
from dotenv import load_dotenv
import os
import requests
import json  # json 모듈 추가

load_dotenv()  # .env 파일 불러오기
openai.api_key = os.getenv("OPENAI_API_KEY")

#텍스트 입력 → GPT 응답 받기
def get_gpt_response(user_input, language="한국어", model="gpt-4"):
    response = openai.ChatCompletion.create(
        model=model,  # ← 여기서 model 파라미터 사용
        messages=[
            {"role": "system",
             "content": f"당신은 친절하고 공손한 음성 비서입니다. 모든 답변을 '{language}'로 해주세요. 모르는 질문이나 이상한 말에는 '{language}'로 '죄송해요, 이해하지 못했어요. 다시 한번 더 말씀해주시겠어요?'라고 대답하세요."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.8
    )
    reply = response.choices[0].message['content']
    return reply

def get_ollama_response(user_input, language="한국어", model="exaone3.5:7.8b"):
    url = "http://localhost:11434/api/chat"
    if language == "영어":
        system_prompt = "You are a kind and polite voice assistant. Always answer in English."
    elif language == "일본어":
        system_prompt = "あなたは親切で丁寧な音声アシスタントです。必ず日本語で答えてください。"
    else:
        system_prompt = "당신은 친절하고 공손한 음성 비서입니다. 모든 답변을 한국어로 해주세요."
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    }
    response = requests.post(url, json=payload, stream=True)
    if response.status_code != 200:
        print("❌ Ollama 요청 실패!")
        print("📄 응답 본문:", response.text)
        raise Exception(f"Ollama 요청 실패: {response.status_code}")

    # 스트리밍 응답에서 각 줄의 content를 합침
    contents = []
    for line in response.iter_lines(decode_unicode=True):
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            if "message" in data and "content" in data["message"]:
                contents.append(data["message"]["content"])
        except Exception as e:
            print("⚠️ JSON 파싱 실패!", e)
            print("📄 응답 라인:", line)
    return "".join(contents)


def get_ai_response(user_input, language="한국어", provider="openai", model="gpt-4"):
    if provider == "ollama":
        return get_ollama_response(user_input, language=language, model=model)
    else:
        return get_gpt_response(user_input, language=language, model=model)

print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")

# #기본 테스트
# if __name__ == "__main__":
#     stt_output = "졸업할 수 있겠지?"
#     answer = get_gpt_response(stt_output)
#     print("🙋 나:" , stt_output)
#     print("🤖 GPT 응답:", answer)
#     print("-" * 40)

# #여러 문장을 한꺼번에 테스트
# questions = [
#     "안녕, 반가워.",
#     "오늘 할 일 추천해줘!",
#     "오늘 서울에서 벚꽃 보러갈 만한 곳이 어디 있을까?",
#     "서울에서 10000원으로 장보고 싶은데 어떤 걸 구매할까?",
# ]

# for q in questions:
#     print(f"🙋 사용자: {q}")
#     print(f"🤖 나만의 음성 비서: {get_gpt_response(q)}")
#     print("-" * 40)