import pathlib

import streamlit as st
import streamlit.components.v1 as components

# ── 기본 페이지 설정 ─────────────────────────────────────────
st.set_page_config(
    page_title="오디가지?",
    page_icon="🍽️",
    layout="centered",
)

# Streamlit 기본 여백/헤더를 최대한 걷어내서
# 순수 웹앱처럼 보이게 만들어요.
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
            max-width: 100%;
        }
        iframe {
            display: block;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── index.html 로드 & 렌더링 ─────────────────────────────────
HTML_PATH = pathlib.Path(__file__).parent / "index.html"
html_content = HTML_PATH.read_text(encoding="utf-8")

# 이 앱은 localStorage, open-meteo 날씨 API, 네이버 지도 링크만 사용하는
# 완전한 클라이언트 사이드 앱이라 components.html로 그대로 임베드하면 됩니다.
components.html(
    html_content,
    height=900,
    scrolling=True,
)
