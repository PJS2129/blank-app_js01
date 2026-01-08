"""한국어 헷갈리는 어휘 학습 앱

간단한 플래시카드/퀴즈/리뷰 모드를 제공합니다.
앱 실행: `streamlit run streamlit_app.py`
"""

import streamlit as st
import random
import pandas as pd


# 예제 데이터: 헷갈리는 어휘 항목 목록
# 각 항목은 정답(answer), 오답 후보(distractors), 설명(explanation), 문장(sentence)
BASE_ITEMS = [
    {
        "answer": "되다",
        "distractors": ["돼다", "되어다"],
        "explanation": "표준어는 '되다'입니다. '돼다'는 비표준 표기입니다.",
        "sentence": "일이 잘 ___."  # 빈칸에 들어갈 말
    },
    {
        "answer": "맞히다",
        "distractors": ["맞추다", "맞치다"],
        "explanation": "'맞히다'는 정답을 맞추는 뜻입니다. '맞추다'는 대상을 맞게 조정하거나 맞도리를 하다의 의미가 있습니다.",
        "sentence": "시험에서 정답을 ___." 
    },
    {
        "answer": "맞추다",
        "distractors": ["맞히다", "마추다"],
        "explanation": "'맞추다'는 시계나 목표를 일치시키거나 조정하는 뜻입니다.",
        "sentence": "시계를 시간에 ___." 
    },
    {
        "answer": "안 되다",
        "distractors": ["안되다", "안돼다"],
        "explanation": "부정 표현 '안 되다'는 띄어쓰는 것이 원칙입니다.",
        "sentence": "그렇게 하면 ___." 
    },
    {
        "answer": "이해하다",
        "distractors": ["알아듣다", "알다"],
        "explanation": "'이해하다'는 의미를 완전히 파악하는 것, '알아듣다'는 듣고 해석해 이해하는 상황에 가깝습니다.",
        "sentence": "설명을 잘 ___." 
    },
]


def init_state():
    # session_state 초기화: 퀴즈/스터디 상태 유지
    if "items" not in st.session_state:
        st.session_state.items = BASE_ITEMS.copy()
    if "mode" not in st.session_state:
        st.session_state.mode = "Study"
    if "study_idx" not in st.session_state:
        st.session_state.study_idx = 0
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
    if "quiz_idx" not in st.session_state:
        st.session_state.quiz_idx = 0
    if "score" not in st.session_state:
        st.session_state.score = 0


def make_quiz(items, n=None):
    # 퀴즈용 질문 리스트 생성: (sentence, choices, answer, explanation)
    pool = items.copy()
    random.shuffle(pool)
    if n:
        pool = pool[:n]
    questions = []
    for it in pool:
        choices = [it["answer"]] + it.get("distractors", [])
        # 중복 제거 및 4개 이하로 맞춤
        choices = list(dict.fromkeys(choices))
        random.shuffle(choices)
        questions.append({
            "sentence": it["sentence"],
            "choices": choices,
            "answer": it["answer"],
            "explanation": it["explanation"],
        })
    return questions


def study_mode():
    st.header("Study 모드 — 플래시카드")
    idx = st.session_state.study_idx
    items = st.session_state.items
    item = items[idx]

    # 문장 보여주기(빈칸 포함)
    st.subheader(f"문제 {idx+1} / {len(items)}")
    st.write("문장:", item["sentence"])

    # 정답 숨기기/보기
    if st.button("정답 보기"):
        st.success(f"정답: {item['answer']}")
        st.info(item["explanation"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("이전"):
            st.session_state.study_idx = max(0, idx - 1)
    with col2:
        if st.button("다음"):
            st.session_state.study_idx = min(len(items) - 1, idx + 1)


def quiz_mode():
    st.header("Quiz 모드 — 객관식 테스트")
    if not st.session_state.quiz_questions:
        st.session_state.quiz_questions = make_quiz(st.session_state.items)
        st.session_state.quiz_idx = 0
        st.session_state.score = 0

    qidx = st.session_state.quiz_idx
    questions = st.session_state.quiz_questions
    if qidx >= len(questions):
        st.success(f"퀴즈 완료! 점수: {st.session_state.score} / {len(questions)}")
        if st.button("다시 풀기"):
            st.session_state.quiz_questions = []
        return

    q = questions[qidx]
    st.write("문장:", q["sentence"])  # 빈칸 있는 문장
    choice = st.radio("보기 중에서 고르세요", q["choices"])

    if st.button("제출"):
        if choice == q["answer"]:
            st.success("정답입니다!")
            st.session_state.score += 1
        else:
            st.error(f"오답. 정답은: {q['answer']}")
            st.info(q["explanation"])
        st.session_state.quiz_idx += 1


def review_mode():
    st.header("Review 모드 — 전체 목록 & 검색")
    df = pd.DataFrame(st.session_state.items)
    # 간단한 테이블 표시
    st.dataframe(df[["answer", "sentence", "explanation"]])


def add_custom_item():
    st.sidebar.subheader("새 항목 추가")
    with st.sidebar.form("add_item"):
        ans = st.text_input("정답 (정상 표기)")
        sent = st.text_input("문장 (빈칸은 ___ 로 표기)")
        d1 = st.text_input("오답 후보1")
        d2 = st.text_input("오답 후보2")
        ex = st.text_area("설명")
        sub = st.form_submit_button("추가")
        if sub and ans:
            new = {"answer": ans, "distractors": [c for c in (d1, d2) if c], "explanation": ex, "sentence": sent}
            st.session_state.items.append(new)
            st.sidebar.success("항목이 추가되었습니다")


def main():
    init_state()
    st.title("한국어 헷갈리는 어휘 학습기")
    st.write("모드: Study (플래시카드) / Quiz (객관식) / Review (목록)")

    # 사이드바로 모드 선택
    mode = st.sidebar.radio("모드 선택", ["Study", "Quiz", "Review"])  # 라디오 버튼
    st.session_state.mode = mode

    # 사용자 항목 추가 폼
    add_custom_item()

    if mode == "Study":
        study_mode()
    elif mode == "Quiz":
        quiz_mode()
    elif mode == "Review":
        review_mode()


if __name__ == "__main__":
    main()
