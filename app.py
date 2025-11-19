import streamlit as st
from openai import OpenAI

# --- API KEY ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if not api_key:
    print("❌ API 키가 설정되어 있지 않습니다. .env 파일을 확인하세요.")
    exit()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def get_user_input():
    year = input("출생년도?(숫자만): ").strip()
    count = input("이름 생성 개수?: ").strip()
    gender = input("성별(남자/여자): ").strip()
    family_name = input("성 입력: ").strip()
    feeling = input("원하는 이름 느낌: ").strip()

    try:
        count = int(count)
        int(year)
    except ValueError:
        print("⚠ 숫자 입력이 잘못되었습니다.")
        exit()

    if gender not in ["남자", "여자"]:
        print("⚠ 성별은 '남자' 또는 '여자'만 입력해 주세요.")
        exit()

    return year, count, gender, family_name, feeling


def generate_names(year, count, gender, family_name, feeling):
    prompt = (
        f"{year}년도에 유행하던 성 '{family_name}'에 어울리고, "
        f"'{feeling}' 느낌의 {gender} 이름 {count}개를 추천해 주세요.\n"
        "각 이름에는 번호, 한자 뜻, 그리고 사용 비율(또는 인기 순위)를 함께 적어 주세요.\n"
        "아래 형식으로만 출력하세요:\n"
        "1. 이름 (한자 뜻) - 사용 비율: XX%\n"
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "간결하고 형식에 맞게 이름을 추천해 주세요."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    year, count, gender, family_name, feeling = get_user_input()
    result = generate_names(year, count, gender, family_name, feeling)

    print("\n📛 생성된 이름 및 예상 인기 비율:")
    print(result)
