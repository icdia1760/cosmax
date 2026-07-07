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

# ── 오디가지? 앱 HTML (index.html 내용을 그대로 내장) ─────────────
# localStorage, open-meteo 날씨 API, 네이버 지도 링크만 사용하는
# 완전한 클라이언트 사이드 앱이라 components.html로 그대로 임베드하면 됩니다.
HTML_CONTENT = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>오디가지?</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    color-scheme: light dark;

    /* 메인 컬러 — 세이지 그린 (브랜드 아이덴티티: 로고, 진단 버튼, 헤딩) */
    --sage: #9eb879;
    --sage-deep: #5f7a43;
    --sage-pale: #e8efdc;

    /* 보조 컬러 — 허니 오렌지 (그린과 보색 대비를 이루는 CTA 전용 색) */
    --honey: #f3b15c;
    --honey-deep: #e1963a;

    --cream: #f7f6ea;
    --paper: #fffdf2;
    --ink: #3b3527;
    --ink-soft: #766d52;
    --on-accent: #3a2410;

    --shadow: 0 18px 40px -12px rgba(76, 92, 46, 0.26);
    --shadow-soft: 0 6px 16px -4px rgba(76, 92, 46, 0.16);
  }

  @media (prefers-color-scheme: dark) {
    :root {
      --sage-deep: #bfe3a0;
      --sage-pale: #33402a;
      --cream: #1e2317;
      --paper: #262a1c;
      --ink: #ede8d6;
      --ink-soft: #b7ac8a;

      --shadow: 0 18px 40px -12px rgba(0, 0, 0, 0.55);
      --shadow-soft: 0 6px 16px -4px rgba(0, 0, 0, 0.4);
    }
  }

  :root[data-theme="dark"] {
    --sage-deep: #bfe3a0;
    --sage-pale: #33402a;
    --cream: #1e2317;
    --paper: #262a1c;
    --ink: #ede8d6;
    --ink-soft: #b7ac8a;

    --shadow: 0 18px 40px -12px rgba(0, 0, 0, 0.55);
    --shadow-soft: 0 6px 16px -4px rgba(0, 0, 0, 0.4);
  }

  :root[data-theme="light"] {
    --sage-deep: #5f7a43;
    --sage-pale: #e8efdc;
    --cream: #f7f6ea;
    --paper: #fffdf2;
    --ink: #3b3527;
    --ink-soft: #766d52;

    --shadow: 0 18px 40px -12px rgba(76, 92, 46, 0.26);
    --shadow-soft: 0 6px 16px -4px rgba(76, 92, 46, 0.16);
  }

  * { box-sizing: border-box; }

  html, body {
    margin: 0;
    padding: 0;
    min-height: 100%;
  }

  body {
    font-family: "Noto Sans KR", -apple-system, BlinkMacSystemFont, "Segoe UI", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
    color: var(--ink);
    background: var(--cream);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 32px 16px 48px;
    -webkit-tap-highlight-color: transparent;
    overflow-x: hidden;
  }

  /* ---------- 배경 무드 애니메이션 ---------- */

  .bg-blob {
    position: fixed;
    border-radius: 50%;
    filter: blur(60px);
    pointer-events: none;
    z-index: 0;
  }

  .bg-blob-a {
    width: 380px;
    height: 380px;
    top: -100px;
    left: -110px;
    background: radial-gradient(circle, rgba(158, 184, 121, 0.55), transparent 70%);
    animation: floatA 14s cubic-bezier(0.36, 1.4, 0.64, 1) infinite alternate;
  }

  .bg-blob-b {
    width: 420px;
    height: 420px;
    bottom: -120px;
    right: -120px;
    background: radial-gradient(circle, rgba(243, 177, 92, 0.4), transparent 70%);
    animation: floatB 17s cubic-bezier(0.36, 1.4, 0.64, 1) infinite alternate;
  }

  @keyframes floatA {
    from { transform: translate(0, 0) scale(1); }
    to { transform: translate(55px, 45px) scale(1.22); }
  }

  @keyframes floatB {
    from { transform: translate(0, 0) scale(1); }
    to { transform: translate(-45px, -55px) scale(1.18); }
  }

  .bg-bubble {
    position: fixed;
    bottom: -10vh;
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    filter: blur(1px);
    animation: bubbleRise linear infinite;
  }

  @keyframes bubbleRise {
    0% { transform: translateY(0) scale(0.7); opacity: 0; }
    12% { opacity: 0.6; }
    50% { transform: translateY(-55vh) scale(1.05); }
    88% { opacity: 0.35; }
    100% { transform: translateY(-105vh) scale(0.85); opacity: 0; }
  }

  .bg-icon-bubble {
    position: fixed;
    bottom: -10vh;
    pointer-events: none;
    z-index: 0;
    animation: bubbleRise linear infinite;
  }

  .bg-icon-bubble svg {
    stroke: #c7c2b4;
    fill: none;
    stroke-width: 1.2;
    stroke-linecap: round;
    stroke-linejoin: round;
  }

  @media (prefers-reduced-motion: reduce) {
    .bg-blob, .bg-bubble, .bg-icon-bubble { animation: none; }
    .bg-bubble, .bg-icon-bubble { display: none; }
  }

  .scene {
    position: relative;
    z-index: 1;
    width: 100%;
    max-width: 400px;
  }

  /* ---------- 티켓 카드 ---------- */

  .ticket {
    position: relative;
    background: var(--paper);
    border-radius: 26px;
    box-shadow: var(--shadow);
    overflow: hidden;
  }

  .ticket::before {
    content: "";
    position: absolute;
    inset: 0 0 auto 0;
    height: 14px;
    background-image: radial-gradient(circle at 50% 0%, transparent 7px, var(--cream) 7.5px);
    background-size: 20px 14px;
    background-repeat: repeat-x;
  }

  .ticket-body {
    padding: 30px 26px 26px;
  }

  /* ---------- 화면 전환 ---------- */

  .screen { display: none; }
  .screen.is-active { display: block; animation: screenIn 0.28s ease; }

  @keyframes screenIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
  }

  @media (prefers-reduced-motion: reduce) {
    .screen.is-active { animation: none; }
  }

  /* ---------- 화면 헤더 ---------- */

  .screen-head {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
  }

  .back-btn {
    width: 32px;
    height: 32px;
    border: none;
    border-radius: 50%;
    background: var(--sage-pale);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    flex-shrink: 0;
    padding: 0;
  }

  .back-btn svg {
    width: 16px;
    height: 16px;
    stroke: var(--ink);
    fill: none;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
  }

  .back-btn:focus-visible { outline: 2px solid var(--sage-deep); outline-offset: 2px; }

  .screen-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--ink-soft);
    letter-spacing: 0.03em;
  }

  .progress-dots {
    display: flex;
    gap: 6px;
    margin-left: auto;
  }

  .progress-dots span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--sage-pale);
    transition: background 0.2s ease, transform 0.2s ease;
  }

  .progress-dots span.is-done { background: var(--sage); }
  .progress-dots span.is-active { background: var(--sage-deep); transform: scale(1.3); }

  /* ---------- 로고 / 타이틀 ---------- */

  .brand {
    text-align: center;
  }

  .brand .mark {
    width: 56px;
    height: 56px;
    margin: 0 auto 14px;
    border-radius: 50%;
    background: linear-gradient(150deg, var(--sage), var(--sage-deep));
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: var(--shadow-soft);
  }

  .brand .mark svg {
    width: 28px;
    height: 28px;
    stroke: var(--on-accent);
    fill: none;
    stroke-width: 1.7;
    stroke-linecap: round;
    stroke-linejoin: round;
  }

  .brand h1 {
    margin: 0;
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--sage-deep);
  }

  .brand .tagline {
    margin: 12px auto 0;
    max-width: 240px;
    font-size: 14px;
    line-height: 1.6;
    color: var(--ink-soft);
  }

  .brand .cheers {
    margin: 10px auto 0;
    font-size: 13px;
    color: var(--sage-deep);
  }

  /* ---------- 절취선 ---------- */

  .stub-divider {
    margin: 22px 0;
    border: none;
    border-top: 1.5px dashed var(--sage-pale);
  }

  /* ---------- 날씨 ---------- */

  .weather {
    display: flex;
    align-items: center;
    gap: 14px;
    background: var(--sage-pale);
    border-radius: 18px;
    padding: 14px 16px;
  }

  .weather .w-icon {
    width: 42px;
    height: 42px;
    flex-shrink: 0;
    stroke: var(--sage-deep);
    fill: none;
    stroke-width: 1.5;
    stroke-linecap: round;
    stroke-linejoin: round;
    transition: opacity 0.2s ease;
  }

  .weather .w-info {
    flex: 1;
    min-width: 0;
  }

  .weather .w-location {
    font-size: 11.5px;
    font-weight: 600;
    letter-spacing: 0.04em;
    color: var(--ink-soft);
    text-transform: uppercase;
  }

  .weather .w-main {
    display: flex;
    align-items: baseline;
    gap: 8px;
    margin-top: 2px;
  }

  .weather .w-temp {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 25px;
    font-variant-numeric: tabular-nums;
    color: var(--sage-deep);
  }

  .weather .w-desc {
    font-size: 13.5px;
    font-weight: 500;
    color: var(--ink);
  }

  .weather.is-loading .w-icon { opacity: 0.35; }
  .weather.is-loading .w-temp,
  .weather.is-loading .w-desc { color: var(--ink-soft); }

  /* ---------- 프롬프트 문구 ---------- */

  .prompt-line {
    margin: 22px 0 14px;
    font-size: 13px;
    font-weight: 600;
    color: var(--ink-soft);
    text-align: center;
  }

  /* ---------- 뽑기 옵션 ---------- */

  .pref-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0 0 14px;
    font-size: 12.5px;
    color: var(--ink-soft);
    cursor: pointer;
  }

  .switch {
    position: relative;
    display: inline-flex;
    cursor: pointer;
    flex-shrink: 0;
  }

  .switch input {
    position: absolute;
    width: 1px;
    height: 1px;
    opacity: 0;
  }

  .switch-track {
    width: 38px;
    height: 21px;
    border-radius: 999px;
    background: var(--sage-pale);
    display: flex;
    align-items: center;
    padding: 2px;
    transition: background 0.15s ease;
  }

  .switch-thumb {
    width: 17px;
    height: 17px;
    border-radius: 50%;
    background: var(--paper);
    box-shadow: var(--shadow-soft);
    transition: transform 0.15s ease;
  }

  .switch input:checked + .switch-track { background: var(--sage-deep); }
  .switch input:checked + .switch-track .switch-thumb { transform: translateX(17px); }
  .switch input:focus-visible + .switch-track { outline: 2px solid var(--sage-deep); outline-offset: 2px; }
  .switch-state {
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.04em;
    color: var(--ink-soft);
    width: 24px;
  }

  .switch input:checked ~ .switch-state { color: var(--sage-deep); }

  @media (prefers-reduced-motion: reduce) {
    .switch-track, .switch-thumb { transition: none; }
  }

  /* ---------- 진입 버튼 ---------- */

  .modes {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .mode-btn {
    width: 100%;
    border: none;
    border-radius: 18px;
    padding: 16px 18px;
    text-align: left;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 14px;
    font-family: inherit;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
  }

  .mode-btn:focus-visible {
    outline: 2px solid var(--sage-deep);
    outline-offset: 2px;
  }

  .mode-btn:hover { transform: translateY(-2px); }
  .mode-btn:active { transform: translateY(0); }

  .mode-btn .m-icon {
    width: 30px;
    height: 30px;
    flex-shrink: 0;
    stroke-width: 1.6;
    stroke-linecap: round;
    stroke-linejoin: round;
    fill: none;
  }

  .mode-btn .m-text { flex: 1; }

  .mode-btn .m-title {
    font-size: 15.5px;
    font-weight: 700;
  }

  .mode-btn .m-desc {
    margin-top: 2px;
    font-size: 12px;
    opacity: 0.8;
  }

  .mode-btn.quiz {
    background: var(--sage);
    color: var(--on-accent);
    box-shadow: var(--shadow-soft);
  }

  .mode-btn.quiz .m-icon { stroke: var(--on-accent); }

  .mode-btn.random {
    background: linear-gradient(135deg, var(--sage), var(--sage-deep));
    color: var(--on-accent);
    box-shadow: var(--shadow-soft);
  }

  .mode-btn.random .m-icon { stroke: var(--on-accent); }

  @media (hover: hover) {
    .mode-btn.random:hover .m-icon {
      animation: shake 0.5s ease;
    }
  }

  @keyframes shake {
    0%, 100% { transform: rotate(0); }
    25% { transform: rotate(-12deg); }
    75% { transform: rotate(12deg); }
  }

  @media (prefers-reduced-motion: reduce) {
    .mode-btn, .mode-btn .m-icon { transition: none; animation: none !important; }
  }

  /* ---------- 질문 ---------- */

  .question-title {
    font-size: 18px;
    font-weight: 800;
    color: var(--ink);
    line-height: 1.4;
    margin: 4px 0 18px;
    text-wrap: balance;
  }

  .options {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .option-btn {
    width: 100%;
    border: 1.5px solid var(--sage-pale);
    background: var(--paper);
    color: var(--ink);
    border-radius: 14px;
    padding: 14px 16px;
    font-size: 14.5px;
    font-weight: 600;
    text-align: left;
    cursor: pointer;
    font-family: inherit;
    transition: border-color 0.15s ease, transform 0.15s ease;
  }

  .option-btn:hover { border-color: var(--sage-deep); transform: translateY(-1px); }
  .option-btn:active { transform: translateY(0); }
  .option-btn:focus-visible { outline: 2px solid var(--sage-deep); outline-offset: 2px; }

  @media (prefers-reduced-motion: reduce) {
    .option-btn { transition: none; }
  }

  /* ---------- 결과 ---------- */

  .stamp {
    display: inline-block;
    border: 1.5px solid var(--sage-deep);
    color: var(--sage-deep);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 5px 12px;
    border-radius: 999px;
    transform: rotate(-3deg);
  }

  .result-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 18px;
  }

  .cat-pill {
    background: var(--sage-pale);
    color: var(--sage-deep);
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 999px;
    letter-spacing: 0.03em;
  }

  .result-area {
    font-size: 12.5px;
    color: var(--ink-soft);
  }

  .result-name {
    font-size: 23px;
    font-weight: 800;
    color: var(--sage-deep);
    margin: 8px 0 0;
    line-height: 1.3;
    text-wrap: balance;
  }

  .result-desc {
    font-size: 14px;
    line-height: 1.65;
    color: var(--ink);
    margin: 12px 0 0;
  }

  .result-tip {
    margin-top: 16px;
    border: 1.5px dashed var(--sage-pale);
    border-radius: 14px;
    padding: 12px 14px;
  }

  .result-tip .tip-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: var(--ink-soft);
    text-transform: uppercase;
  }

  .result-tip .tip-text {
    margin-top: 4px;
    font-size: 13px;
    line-height: 1.55;
    color: var(--ink);
  }

  .weather-note {
    margin-top: 14px;
    font-size: 12.5px;
    color: var(--ink-soft);
    line-height: 1.5;
  }

  .result-actions {
    margin-top: 22px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .btn-primary {
    width: 100%;
    border: none;
    border-radius: 16px;
    padding: 15px;
    font-size: 14.5px;
    font-weight: 700;
    color: var(--on-accent);
    background: linear-gradient(135deg, var(--honey), var(--honey-deep));
    cursor: pointer;
    font-family: inherit;
    box-shadow: var(--shadow-soft);
    transition: transform 0.15s ease;
  }

  .btn-primary:hover { transform: translateY(-2px); }
  .btn-primary:active { transform: translateY(0); }
  .btn-primary:focus-visible { outline: 2px solid var(--sage-deep); outline-offset: 2px; }

  .btn-map {
    width: 100%;
    border: 1.5px solid var(--sage-pale);
    border-radius: 16px;
    padding: 13px;
    font-size: 14px;
    font-weight: 700;
    color: var(--sage-deep);
    background: var(--paper);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    text-decoration: none;
    cursor: pointer;
    font-family: inherit;
    transition: border-color 0.15s ease, transform 0.15s ease;
  }

  .btn-map svg {
    width: 16px;
    height: 16px;
    stroke: var(--sage-deep);
    fill: none;
    stroke-width: 1.8;
    stroke-linecap: round;
    stroke-linejoin: round;
  }

  .btn-map:hover { border-color: var(--sage-deep); transform: translateY(-1px); }
  .btn-map:active { transform: translateY(0); }
  .btn-map:focus-visible { outline: 2px solid var(--sage-deep); outline-offset: 2px; }

  @media (prefers-reduced-motion: reduce) {
    .btn-map { transition: none; }
  }

  .btn-ghost {
    width: 100%;
    border: none;
    background: none;
    color: var(--ink-soft);
    font-size: 13px;
    font-weight: 600;
    text-align: center;
    padding: 6px;
    cursor: pointer;
    font-family: inherit;
    text-decoration: underline;
    text-decoration-color: transparent;
    transition: text-decoration-color 0.15s ease;
  }

  .btn-ghost:hover { text-decoration-color: var(--ink-soft); }
  .btn-ghost:focus-visible { outline: 2px solid var(--sage-deep); outline-offset: 2px; }

  @media (prefers-reduced-motion: reduce) {
    .btn-primary { transition: none; }
  }

  /* ---------- 아카이브 ---------- */

  .corner-btn {
    position: absolute;
    top: 14px;
    right: 14px;
    border: none;
    background: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
    cursor: pointer;
    z-index: 2;
    padding: 4px;
    transition: transform 0.15s ease;
  }

  .corner-btn:hover { transform: scale(1.08); }
  .corner-btn:active { transform: scale(0.94); }

  .corner-btn svg {
    width: 20px;
    height: 20px;
    fill: var(--sage-deep);
    stroke: none;
  }

  .corner-btn-label {
    font-size: 9.5px;
    font-weight: 700;
    letter-spacing: 0.02em;
    color: var(--sage-deep);
  }

  .corner-btn:focus-visible { outline: 2px solid var(--sage-deep); outline-offset: 2px; }

  @media (prefers-reduced-motion: reduce) {
    .corner-btn { transition: none; }
  }

  .archive-count {
    margin-left: auto;
    font-size: 12px;
    font-weight: 700;
    color: var(--ink-soft);
    font-variant-numeric: tabular-nums;
  }

  .archive-filter {
    display: flex;
    gap: 6px;
    margin-bottom: 16px;
  }

  .filter-btn {
    flex: 1;
    border: 1.5px solid var(--sage-pale);
    background: var(--paper);
    color: var(--ink-soft);
    font-size: 12.5px;
    font-weight: 700;
    padding: 8px 6px;
    border-radius: 999px;
    cursor: pointer;
    font-family: inherit;
    transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
  }

  .filter-btn:hover:not(.is-active) { border-color: var(--sage-deep); }
  .filter-btn:focus-visible { outline: 2px solid var(--sage-deep); outline-offset: 2px; }

  .filter-btn.is-active { border-color: transparent; }
  .filter-btn[data-filter="all"].is-active { background: var(--ink); color: var(--paper); }
  .filter-btn[data-filter="been"].is-active { background: var(--sage-deep); color: var(--paper); }
  .filter-btn[data-filter="togo"].is-active { background: var(--honey); color: var(--on-accent); }

  @media (prefers-reduced-motion: reduce) {
    .filter-btn { transition: none; }
  }

  .archive-add {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
  }

  .archive-add input[type="text"] {
    flex: 1;
    min-width: 0;
    border: 1.5px solid var(--sage-pale);
    border-radius: 12px;
    padding: 10px 12px;
    font-size: 13.5px;
    font-family: inherit;
    color: var(--ink);
    background: var(--paper);
  }

  .archive-add input[type="text"]::placeholder { color: var(--ink-soft); }
  .archive-add input[type="text"]:focus-visible { outline: 2px solid var(--sage-deep); outline-offset: 1px; }

  .archive-add button {
    border: none;
    border-radius: 12px;
    padding: 10px 16px;
    font-size: 13.5px;
    font-weight: 700;
    color: var(--on-accent);
    background: var(--honey);
    cursor: pointer;
    font-family: inherit;
    white-space: nowrap;
    transition: background 0.15s ease;
  }

  .archive-add button:hover { background: var(--honey-deep); }
  .archive-add button:focus-visible { outline: 2px solid var(--sage-deep); outline-offset: 2px; }

  .archive-list {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
    max-height: 360px;
    overflow-y: auto;
  }

  .archive-item {
    border: 1.5px solid var(--sage-pale);
    border-radius: 14px;
    display: flex;
    align-items: center;
    transition: background 0.15s ease, border-color 0.15s ease;
  }

  .archive-item.is-checked {
    background: var(--sage-pale);
    border-color: transparent;
  }

  .archive-check {
    flex: 1;
    min-width: 0;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    cursor: pointer;
  }

  .archive-check input[type="checkbox"] {
    position: absolute;
    width: 1px;
    height: 1px;
    opacity: 0;
  }

  .check-box {
    width: 20px;
    height: 20px;
    border-radius: 7px;
    border: 1.5px solid var(--sage-pale);
    background: var(--paper);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: background 0.15s ease, border-color 0.15s ease;
  }

  .check-box svg {
    width: 13px;
    height: 13px;
    stroke: var(--paper);
    fill: none;
    stroke-width: 2.4;
    stroke-linecap: round;
    stroke-linejoin: round;
    opacity: 0;
    transition: opacity 0.15s ease;
  }

  .archive-item.is-checked .check-box { background: var(--sage-deep); border-color: var(--sage-deep); }
  .archive-item.is-checked .check-box svg { opacity: 1; }

  .archive-check input:focus-visible + .check-box { outline: 2px solid var(--sage-deep); outline-offset: 2px; }

  .archive-icon {
    width: 32px;
    height: 32px;
    border-radius: 9px;
    background: var(--sage-pale);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .archive-icon svg {
    width: 17px;
    height: 17px;
    stroke: var(--sage-deep);
    fill: none;
    stroke-width: 1.6;
    stroke-linecap: round;
    stroke-linejoin: round;
  }

  .archive-item.is-checked .archive-icon { opacity: 0.55; }

  .archive-text {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
  }

  .archive-name {
    font-size: 13.5px;
    font-weight: 600;
    color: var(--ink);
  }

  .archive-item.is-checked .archive-name {
    text-decoration: line-through;
    color: var(--ink-soft);
  }

  .archive-meta {
    font-size: 11px;
    color: var(--ink-soft);
  }

  .archive-remove {
    border: none;
    background: none;
    width: 32px;
    height: 32px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    margin-right: 6px;
  }

  .archive-remove svg {
    width: 13px;
    height: 13px;
    stroke: var(--ink-soft);
    fill: none;
    stroke-width: 2;
    stroke-linecap: round;
  }

  .archive-remove:hover svg { stroke: var(--sage-deep); }
  .archive-remove:focus-visible { outline: 2px solid var(--sage-deep); outline-offset: 2px; }

  .archive-empty {
    text-align: center;
    font-size: 12.5px;
    color: var(--ink-soft);
    padding: 20px 0;
  }

  .note-textarea {
    width: 100%;
    resize: vertical;
    min-height: 100px;
    border: 1.5px solid var(--sage-pale);
    border-radius: 12px;
    padding: 10px 12px;
    font-family: inherit;
    font-size: 13.5px;
    color: var(--ink);
    background: var(--paper);
  }

  .note-textarea::placeholder { color: var(--ink-soft); }
  .note-textarea:focus-visible { outline: 2px solid var(--sage-deep); outline-offset: 1px; }

  .note-actions {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 10px;
    margin-top: 16px;
  }

  .note-clear-btn {
    border: none;
    background: none;
    color: var(--ink-soft);
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
    padding: 8px;
  }

  .note-clear-btn:hover { color: var(--sage-deep); }
  .note-clear-btn:focus-visible { outline: 2px solid var(--sage-deep); outline-offset: 2px; }

  .note-save-btn {
    border: none;
    border-radius: 12px;
    padding: 10px 18px;
    font-size: 13.5px;
    font-weight: 700;
    color: var(--on-accent);
    background: var(--honey);
    cursor: pointer;
    font-family: inherit;
    transition: background 0.15s ease;
  }

  .note-save-btn:hover { background: var(--honey-deep); }
  .note-save-btn:focus-visible { outline: 2px solid var(--sage-deep); outline-offset: 2px; }

  @media (prefers-reduced-motion: reduce) {
    .note-save-btn { transition: none; }
  }

  .addplace-name-input {
    width: 100%;
    border: 1.5px solid var(--sage-pale);
    border-radius: 12px;
    padding: 10px 12px;
    font-family: inherit;
    font-size: 14px;
    color: var(--ink);
    background: var(--paper);
    margin-bottom: 16px;
  }

  .addplace-name-input::placeholder { color: var(--ink-soft); }
  .addplace-name-input:focus-visible { outline: 2px solid var(--sage-deep); outline-offset: 1px; }

  .addplace-field-label {
    display: block;
    font-size: 12px;
    font-weight: 700;
    color: var(--ink-soft);
    margin-bottom: 8px;
  }

  .icon-picker {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;
    margin-bottom: 16px;
  }

  .icon-option {
    aspect-ratio: 1;
    border: 1.5px solid var(--sage-pale);
    border-radius: 12px;
    background: var(--paper);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    padding: 0;
  }

  .icon-option svg {
    width: 20px;
    height: 20px;
    stroke: var(--sage-deep);
    fill: none;
    stroke-width: 1.6;
    stroke-linecap: round;
    stroke-linejoin: round;
  }

  .icon-option.is-selected { border-color: var(--sage-deep); background: var(--sage-pale); }
  .icon-option:focus-visible { outline: 2px solid var(--sage-deep); outline-offset: 2px; }

  footer.credit {
    margin-top: 20px;
    font-size: 11px;
    color: var(--ink-soft);
    text-align: center;
    opacity: 0.75;
  }

  @media (max-width: 360px) {
    .ticket-body { padding: 26px 20px 22px; }
    .brand h1 { font-size: 24px; }
  }
</style>
</head>
<body>

<div class="bg-blob bg-blob-a" aria-hidden="true"></div>
<div class="bg-blob bg-blob-b" aria-hidden="true"></div>

<div class="bg-bubble" aria-hidden="true" style="left:10%; width:16px; height:16px; background:var(--sage); animation-duration:9s; animation-delay:0s;"></div>
<div class="bg-bubble" aria-hidden="true" style="left:22%; width:10px; height:10px; background:var(--honey); animation-duration:7s; animation-delay:1.2s;"></div>
<div class="bg-bubble" aria-hidden="true" style="left:38%; width:20px; height:20px; background:var(--sage); animation-duration:11s; animation-delay:2.5s;"></div>
<div class="bg-bubble" aria-hidden="true" style="left:55%; width:12px; height:12px; background:var(--honey); animation-duration:8s; animation-delay:0.6s;"></div>
<div class="bg-bubble" aria-hidden="true" style="left:70%; width:18px; height:18px; background:var(--sage); animation-duration:10s; animation-delay:3.4s;"></div>
<div class="bg-bubble" aria-hidden="true" style="left:82%; width:9px; height:9px; background:var(--honey); animation-duration:7.5s; animation-delay:4.1s;"></div>
<div class="bg-bubble" aria-hidden="true" style="left:92%; width:14px; height:14px; background:var(--sage); animation-duration:9.5s; animation-delay:1.8s;"></div>

<div class="bg-icon-bubble" aria-hidden="true" style="left:10%; animation-duration:15s; animation-delay:0.5s;"><svg viewBox="0 0 24 24" style="width:76px; height:76px;"><path d="M5 9h13v3a5 5 0 0 1-5 5H10a5 5 0 0 1-5-5V9Z"/><path d="M18 10h1.5a2 2 0 0 1 0 4H18"/></svg></div>
<div class="bg-icon-bubble" aria-hidden="true" style="left:26%; animation-duration:13s; animation-delay:3.8s;"><svg viewBox="0 0 24 24" style="width:88px; height:88px;"><ellipse cx="9" cy="7" rx="2" ry="3"/><ellipse cx="15" cy="13" rx="2" ry="3"/><ellipse cx="9" cy="19" rx="2" ry="3"/></svg></div>
<div class="bg-icon-bubble" aria-hidden="true" style="left:46%; animation-duration:16s; animation-delay:1.6s;"><svg viewBox="0 0 24 24" style="width:82px; height:82px;"><rect x="4" y="5" width="16" height="13" rx="1.5"/><path d="M4 15l4-4 3 3 5-5 4 4"/><circle cx="9" cy="9" r="1.2"/></svg></div>
<div class="bg-icon-bubble" aria-hidden="true" style="left:64%; animation-duration:14s; animation-delay:5.2s;"><svg viewBox="0 0 24 24" style="width:70px; height:70px;"><path d="M5 4h14l-7 8-7-8Z"/><path d="M12 12v7M9 19h6"/></svg></div>
<div class="bg-icon-bubble" aria-hidden="true" style="left:82%; animation-duration:17s; animation-delay:2.7s;"><svg viewBox="0 0 24 24" style="width:80px; height:80px;"><path d="M15 3a7 7 0 1 0 6 10 7 7 0 0 1-6-10Z"/></svg></div>

<div class="scene">

  <section class="ticket screen is-active" data-screen="home">
    <button class="corner-btn" id="archiveBtn" type="button" aria-label="아카이브">
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M12 20.5s-7.6-4.6-10-9.1C0.6 8.2 1.6 4.4 5 3.4c2.6-0.8 4.9 0.5 7 3.1 2.1-2.6 4.4-3.9 7-3.1 3.4 1 4.4 4.8 3 8-2.4 4.5-10 9.1-10 9.1Z"/>
      </svg>
      <span class="corner-btn-label">아카이브</span>
    </button>
    <div class="ticket-body">

      <div class="brand">
        <div class="mark" aria-hidden="true">
          <svg viewBox="0 0 24 24"><path d="M5 10h13v3a5 5 0 0 1-5 5H10a5 5 0 0 1-5-5v-3Z"/><path d="M18 11h1.5a2 2 0 0 1 0 4H18"/><path d="M8 3.5c-.6.7-.6 1.3 0 2M12 3.5c-.6.7-.6 1.3 0 2"/></svg>
        </div>
        <h1>오디가지?</h1>
        <p class="tagline">당신의 기분과 날씨에 맞춰,<br>나답게 혼자 노는 법을 찾아보아요 :)</p>
        <p class="cheers">당신의 혼놀에 cheers-🍷</p>
      </div>

      <hr class="stub-divider">

      <div class="weather is-loading" id="weather">
        <svg class="w-icon" id="weatherIcon" viewBox="0 0 24 24" aria-hidden="true">
          <circle cx="12" cy="12" r="4"/>
          <path d="M12 3v2M12 19v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M3 12h2M19 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/>
        </svg>
        <div class="w-info">
          <div class="w-location">서울 · 오늘 날씨</div>
          <div class="w-main">
            <span class="w-temp" id="weatherTemp">--°</span>
            <span class="w-desc" id="weatherDesc">불러오는 중</span>
          </div>
        </div>
      </div>

      <p class="prompt-line">오늘은 어떻게 놀아볼까요?</p>

      <label class="pref-row">
        <span class="switch">
          <input type="checkbox" id="excludeVisitedToggle">
          <span class="switch-track"><span class="switch-thumb"></span></span>
          <span class="switch-state" id="excludeVisitedState">OFF</span>
        </span>
        가본 곳 제외하기
      </label>

      <div class="modes">
        <button class="mode-btn quiz" id="quizBtn" type="button">
          <svg class="m-icon" viewBox="0 0 24 24" aria-hidden="true">
            <rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 3.5h6a1 1 0 0 1 1 1V6H8V4.5a1 1 0 0 1 1-1Z"/><path d="M8.5 12.5l2 2 4.5-4.5"/>
          </svg>
          <span class="m-text">
            <span class="m-title">기분 진단하기</span>
            <span class="m-desc">질문 몇 개로 딱 맞는 장소 찾기</span>
          </span>
        </button>

        <button class="mode-btn random" id="randomBtn" type="button">
          <svg class="m-icon" viewBox="0 0 24 24" aria-hidden="true">
            <rect x="4" y="4" width="16" height="16" rx="4"/><circle cx="9" cy="9" r="1.2" fill="currentColor" stroke="none"/><circle cx="15" cy="15" r="1.2" fill="currentColor" stroke="none"/><circle cx="15" cy="9" r="1.2" fill="currentColor" stroke="none"/><circle cx="9" cy="15" r="1.2" fill="currentColor" stroke="none"/>
          </svg>
          <span class="m-text">
            <span class="m-title">랜덤으로 뽑기</span>
            <span class="m-desc">고민은 그만, 오늘의 장소 뽑기</span>
          </span>
        </button>
      </div>

    </div>
  </section>

  <section class="ticket screen" data-screen="quiz">
    <div class="ticket-body">
      <div class="screen-head">
        <button class="back-btn" id="quizBackBtn" type="button" aria-label="뒤로가기">
          <svg viewBox="0 0 24 24"><path d="M15 6l-6 6 6 6"/></svg>
        </button>
        <span class="screen-title">기분 진단</span>
        <div class="progress-dots" id="progressDots"></div>
      </div>
      <h2 class="question-title" id="questionTitle"></h2>
      <div class="options" id="questionOptions"></div>
    </div>
  </section>

  <section class="ticket screen" data-screen="result">
    <div class="ticket-body">
      <div class="screen-head">
        <button class="back-btn" id="resultBackBtn" type="button" aria-label="처음으로">
          <svg viewBox="0 0 24 24"><path d="M15 6l-6 6 6 6"/></svg>
        </button>
        <span class="screen-title" id="resultScreenTitle">결과</span>
      </div>
      <span class="stamp" id="resultStamp">오늘의 뽑기</span>
      <div class="result-meta">
        <span class="cat-pill" id="resultCategory">카페</span>
        <span class="result-area" id="resultArea">서울</span>
      </div>
      <h2 class="result-name" id="resultName">장소 이름</h2>
      <p class="result-desc" id="resultDesc"></p>
      <div class="result-tip">
        <div class="tip-label">혼자 하기 좋은 포인트</div>
        <div class="tip-text" id="resultTip"></div>
      </div>
      <p class="weather-note" id="weatherNote"></p>
      <div class="result-actions">
        <button class="btn-primary" id="retryBtn" type="button">다시 뽑기</button>
        <a class="btn-map" id="mapBtn" href="#" target="_blank" rel="noopener noreferrer">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-6.5-5.2-6.5-10.5A6.5 6.5 0 0 1 12 4a6.5 6.5 0 0 1 6.5 6.5C18.5 15.8 12 21 12 21Z"/><circle cx="12" cy="10.5" r="2.2"/></svg>
          지도에서 보기
        </a>
        <button class="btn-ghost" id="homeFromResultBtn" type="button">처음으로 돌아가기</button>
      </div>
    </div>
  </section>

  <section class="ticket screen" data-screen="archive">
    <div class="ticket-body">
      <div class="screen-head">
        <button class="back-btn" id="archiveBackBtn" type="button" aria-label="처음으로">
          <svg viewBox="0 0 24 24"><path d="M15 6l-6 6 6 6"/></svg>
        </button>
        <span class="screen-title">아카이브</span>
        <span class="archive-count" id="archiveCount"></span>
      </div>

      <div class="archive-filter" id="archiveFilter">
        <button class="filter-btn is-active" type="button" data-filter="all">전체보기</button>
        <button class="filter-btn" type="button" data-filter="been">가본 곳</button>
        <button class="filter-btn" type="button" data-filter="togo">가볼 곳</button>
      </div>

      <div class="archive-add">
        <input type="text" id="archiveInput" placeholder="새로운 장소를 적어보세요" maxlength="40">
        <button type="button" id="archiveAddBtn">추가</button>
      </div>

      <ul class="archive-list" id="archiveList"></ul>
    </div>
  </section>

  <section class="ticket screen" data-screen="addplace">
    <div class="ticket-body">
      <div class="screen-head">
        <button class="back-btn" id="addPlaceBackBtn" type="button" aria-label="아카이브로">
          <svg viewBox="0 0 24 24"><path d="M15 6l-6 6 6 6"/></svg>
        </button>
        <span class="screen-title">새로운 장소</span>
      </div>

      <input type="text" class="addplace-name-input" id="addPlaceNameInput" placeholder="장소 이름" maxlength="40">

      <span class="addplace-field-label">아이콘 선택</span>
      <div class="icon-picker" id="addPlaceIconPicker"></div>

      <span class="addplace-field-label">설명</span>
      <textarea class="note-textarea" id="addPlaceDescInput" placeholder="어떤 곳인지 짧게 설명해보세요" rows="3" maxlength="80"></textarea>

      <div class="note-actions">
        <button type="button" class="note-clear-btn" id="addPlaceCancelBtn">취소</button>
        <button type="button" class="note-save-btn" id="addPlaceSaveBtn">추가하기</button>
      </div>
    </div>
  </section>

  <footer class="credit">오디가지? · 서울 혼자놀기 장소 추천</footer>
</div>

<script>
  const SEOUL = { lat: 37.5665, lon: 126.9780 };
  let currentWeather = null; // { temp, desc, indoorOnly }

  const WEATHER_ICONS = {
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M3 12h2M19 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/>',
    "sun-cloud": '<path d="M8.5 9.5a3.5 3.5 0 1 1 6.6-1.6"/><path d="M6 18h10.5a3.5 3.5 0 0 0 .5-6.96A5 5 0 0 0 7.2 12.1 3 3 0 0 0 6 18Z"/>',
    cloud: '<path d="M6.5 18h10a3.75 3.75 0 0 0 .5-7.47 5.5 5.5 0 0 0-10.65 1.7A3.5 3.5 0 0 0 6.5 18Z"/>',
    "cloud-rain": '<path d="M6.5 15h10a3.75 3.75 0 0 0 .5-7.47 5.5 5.5 0 0 0-10.65 1.7A3.5 3.5 0 0 0 6.5 15Z"/><path d="M9 18.5 8 21M13 18.5l-1 2.5M17 18.5l-1 2.5"/>',
    "cloud-snow": '<path d="M6.5 14h10a3.75 3.75 0 0 0 .5-7.47 5.5 5.5 0 0 0-10.65 1.7A3.5 3.5 0 0 0 6.5 14Z"/><path d="M9 18v.01M9 20.5v.01M13 18v.01M13 20.5v.01M17 18v.01M17 20.5v.01"/>',
    "cloud-bolt": '<path d="M6.5 14h10a3.75 3.75 0 0 0 .5-7.47 5.5 5.5 0 0 0-10.65 1.7A3.5 3.5 0 0 0 6.5 14Z"/><path d="M13 14.5 10 19h3l-1.5 3"/>',
    fog: '<path d="M4 10h14M3 14h16M6 18h11"/>'
  };

  const INDOOR_ONLY_ICONS = ["cloud-rain", "cloud-snow", "cloud-bolt", "fog"];

  function describeWeather(code) {
    if (code === 0) return { icon: "sun", desc: "맑음" };
    if (code === 1 || code === 2) return { icon: "sun-cloud", desc: "대체로 맑음" };
    if (code === 3) return { icon: "cloud", desc: "흐림" };
    if (code === 45 || code === 48) return { icon: "fog", desc: "안개" };
    if ([51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82].includes(code)) return { icon: "cloud-rain", desc: "비" };
    if ([71, 73, 75, 77, 85, 86].includes(code)) return { icon: "cloud-snow", desc: "눈" };
    if ([95, 96, 99].includes(code)) return { icon: "cloud-bolt", desc: "뇌우" };
    return { icon: "cloud", desc: "확인 중" };
  }

  function renderWeather(temp, iconKey, desc) {
    document.getElementById("weather").classList.remove("is-loading");
    document.getElementById("weatherIcon").innerHTML = WEATHER_ICONS[iconKey] || WEATHER_ICONS.cloud;
    document.getElementById("weatherTemp").textContent = `${temp}°`;
    document.getElementById("weatherDesc").textContent = desc;
    currentWeather = { temp, desc, indoorOnly: INDOOR_ONLY_ICONS.includes(iconKey) };
  }

  function renderWeatherFallback() {
    document.getElementById("weather").classList.remove("is-loading");
    document.getElementById("weatherIcon").innerHTML = WEATHER_ICONS.cloud;
    document.getElementById("weatherTemp").textContent = "--°";
    document.getElementById("weatherDesc").textContent = "날씨를 불러오지 못했어요";
    currentWeather = null;
  }

  async function loadWeather() {
    try {
      const url = `https://api.open-meteo.com/v1/forecast?latitude=${SEOUL.lat}&longitude=${SEOUL.lon}&current=temperature_2m,weather_code&timezone=Asia%2FSeoul`;
      const res = await fetch(url);
      if (!res.ok) throw new Error("weather fetch failed");
      const data = await res.json();
      const temp = Math.round(data.current.temperature_2m);
      const { icon, desc } = describeWeather(data.current.weather_code);
      renderWeather(temp, icon, desc);
    } catch (err) {
      renderWeatherFallback();
    }
  }

  /* =========================================================
     장소 데이터 (서울 혼자놀기 스팟)
     ========================================================= */

  const PLACES = [
    { name: "연남동 골목 독립서점", area: "연남동", category: "서점", weather: "indoor",
      mood: ["calm", "create"], vibe: ["quiet", "aesthetic"],
      desc: "책장 사이를 느긋하게 걷다 마음에 드는 문장 하나를 골라오는 재미가 있는 곳이에요.",
      tip: "동네책방답게 사장님이 직접 큐레이션한 코너부터 살펴보세요." },
    { name: "을지로 인쇄소 골목 산책", area: "을지로", category: "산책", weather: "outdoor",
      mood: ["blank", "stimulating"], vibe: ["quiet", "aesthetic"],
      desc: "낡은 간판과 오래된 인쇄소 사이를 걸으며 시간이 멈춘 듯한 골목을 구경하는 코스예요.",
      tip: "골목 안 커피 한 잔 파는 노포도 함께 들러보세요." },
    { name: "성수동 감성 로스터리 카페", area: "성수동", category: "카페", weather: "indoor",
      mood: ["calm", "create"], vibe: ["aesthetic", "peoplewatch"],
      desc: "창가 1인석에 앉아 원두 향과 함께 노트 한 페이지를 채우기 좋은 공간이에요.",
      tip: "평일 오후 시간대가 비교적 여유롭습니다." },
    { name: "망원 한강지구 자전거 산책", area: "망원동", category: "산책", weather: "outdoor",
      mood: ["blank", "stimulating"], vibe: ["lively", "quiet"],
      desc: "강바람을 맞으며 자전거로 달리다 아무 벤치에나 앉아 멍때리기 좋은 곳이에요.",
      tip: "해 질 무렵 노을 각도가 특히 좋아요." },
    { name: "익선동 한옥 디저트 카페", area: "익선동", category: "카페", weather: "indoor",
      mood: ["calm"], vibe: ["peoplewatch", "aesthetic"],
      desc: "좁은 골목 사이 한옥 카페에 숨어 앉아 사람 구경하며 디저트를 즐기는 시간이에요.",
      tip: "평일 낮에 가면 대기 줄이 짧아요." },
    { name: "국립현대미술관 서울관", area: "삼청동", category: "전시", weather: "indoor",
      mood: ["stimulating", "create"], vibe: ["quiet", "aesthetic"],
      desc: "큰 기대 없이 들어갔다가 예상 못한 작품 앞에서 한참 서 있게 되는 곳이에요.",
      tip: "수·토요일 저녁 야간 개장 시간엔 더 여유롭게 볼 수 있어요." },
    { name: "홍대 만화카페", area: "홍대", category: "실내 액티비티", weather: "indoor",
      mood: ["blank"], vibe: ["quiet", "lively"],
      desc: "1인 좌석에 파묻혀 만화책 스무 권을 쌓아두고 하루 종일 뒹굴기 좋은 곳이에요.",
      tip: "라면·간식도 대부분 셀프바로 되어 있어 눈치 볼 필요 없어요." },
    { name: "서촌 도자기 공방 원데이클래스", area: "서촌", category: "공방", weather: "indoor",
      mood: ["create", "calm"], vibe: ["quiet"],
      desc: "흙을 만지는 데 집중하다 보면 어느새 머릿속이 비워지는 원데이 클래스예요.",
      tip: "예약제라 하루 전에는 미리 신청해두는 게 좋아요." },
    { name: "잠실 한강 불빛 야경 산책", area: "잠실", category: "산책", weather: "outdoor",
      mood: ["stimulating", "blank"], vibe: ["lively", "aesthetic"],
      desc: "강 건너 반짝이는 야경을 보며 이어폰 하나 꽂고 걷기 좋은 야간 코스예요.",
      tip: "주말 밤엔 사람이 많아 평일 저녁을 추천해요." },
    { name: "을지로 노포 혼술 골목", area: "을지로", category: "맛집", weather: "indoor",
      mood: ["calm"], vibe: ["peoplewatch", "lively"],
      desc: "허름한 노포 한 켠에 자리 잡고 혼자 한 잔에 하루를 정리하기 좋은 곳이에요.",
      tip: "1인 손님이 많은 동네라 눈치 보지 않아도 돼요." },
    { name: "여의도 한강공원 피크닉", area: "여의도", category: "산책", weather: "outdoor",
      mood: ["blank", "calm"], vibe: ["quiet", "lively"],
      desc: "매트 하나 깔고 앉아 강바람을 맞으며 아무것도 안 하기 좋은 곳이에요.",
      tip: "해 지기 1시간 전쯤 자리를 잡으면 노을까지 볼 수 있어요." },
    { name: "합정 보드게임카페", area: "합정동", category: "실내 액티비티", weather: "indoor",
      mood: ["stimulating"], vibe: ["lively", "peoplewatch"],
      desc: "직원 추천을 받아 혼자서도 즐길 수 있는 보드게임에 빠져보는 시간이에요.",
      tip: "평일 저녁엔 다른 혼자 온 손님과 합석하는 테이블도 운영해요." },
    { name: "서촌 돌담길 산책", area: "서촌", category: "산책", weather: "outdoor",
      mood: ["calm", "create"], vibe: ["quiet", "aesthetic"],
      desc: "고즈넉한 돌담길을 따라 걷다 눈에 띄는 갤러리에 슬쩍 들어가보는 코스예요.",
      tip: "평일 오전이 가장 한적해요." },
    { name: "연희동 독립영화관 조조 상영", area: "연희동", category: "영화", weather: "indoor",
      mood: ["stimulating", "calm"], vibe: ["quiet"],
      desc: "평일 오전, 텅 빈 상영관에 혼자 앉아 마음껏 영화에 몰입하는 시간이에요.",
      tip: "조조 할인 시간대를 노리면 더 여유롭게 볼 수 있어요." },
    { name: "부암동 전망 카페 산책", area: "부암동", category: "산책", weather: "outdoor",
      mood: ["calm", "blank"], vibe: ["quiet", "aesthetic"],
      desc: "인왕산 자락 언덕길을 오르다 전망 좋은 카페에 들어가 서울 시내를 내려다보며 쉬어가는 코스예요.",
      tip: "평일 낮에 가면 카페 창가 자리를 여유롭게 차지할 수 있어요." },
    { name: "문래동 철공소 골목 예술 산책", area: "문래동", category: "산책", weather: "outdoor",
      mood: ["stimulating", "create"], vibe: ["aesthetic", "quiet"],
      desc: "철공소 사이사이 숨어 있는 그래피티와 작은 갤러리를 발견하며 걷는 예술 산책 코스예요.",
      tip: "골목이 복잡하니 지도 앱을 켜두고 천천히 둘러보세요." },
    { name: "노량진 수산시장 혼밥", area: "노량진", category: "맛집", weather: "indoor",
      mood: ["stimulating", "blank"], vibe: ["lively", "peoplewatch"],
      desc: "직접 고른 회를 2층 식당에서 바로 먹을 수 있어 혼자서도 활기찬 한 끼를 즐길 수 있는 곳이에요.",
      tip: "오전 시간대가 비교적 한산하고 흥정하기도 편해요." },
    { name: "서울숲 산책", area: "성수동", category: "산책", weather: "outdoor",
      mood: ["blank", "calm"], vibe: ["quiet", "lively"],
      desc: "넓은 숲길을 따라 걷다 사슴 방사장 앞 벤치에 앉아 멍하니 시간을 흘려보내기 좋은 곳이에요.",
      tip: "가을에는 은행나무길이 특히 예뻐요." },
    { name: "동묘 구제시장 구경", area: "동묘", category: "마켓", weather: "outdoor",
      mood: ["stimulating", "create"], vibe: ["lively", "peoplewatch"],
      desc: "빈티지 옷과 소품이 잔뜩 쌓인 좁은 골목을 뒤지다 보면 시간 가는 줄 모르는 곳이에요.",
      tip: "현금을 챙겨가면 흥정하기 더 편해요." },
    { name: "낙산공원 야경", area: "이화동", category: "야경", weather: "outdoor",
      mood: ["calm", "stimulating"], vibe: ["aesthetic", "quiet"],
      desc: "성곽길을 따라 오르면 도심 야경이 한눈에 펼쳐지는, 사진 찍기 좋은 야간 명소예요.",
      tip: "해 지기 직전에 올라가면 노을과 야경을 함께 볼 수 있어요." },
    { name: "상수동 LP바", area: "상수동", category: "바", weather: "indoor",
      mood: ["calm"], vibe: ["aesthetic", "quiet"],
      desc: "신청곡을 적어 내면 LP로 틀어주는 조용한 바에서 혼자 음악에 잠기기 좋은 곳이에요.",
      tip: "좋아하는 앨범 제목을 미리 메모해가면 신청하기 편해요." },
    { name: "통의동 갤러리 산책", area: "통의동", category: "전시", weather: "indoor",
      mood: ["create", "calm"], vibe: ["quiet", "aesthetic"],
      desc: "작은 한옥·양옥 갤러리들이 모여 있어 가볍게 들어갔다 나오며 여러 전시를 훑어보기 좋은 동네예요.",
      tip: "대부분 무료 관람이라 발길 닿는 대로 들어가 보세요." },
    { name: "종로 코인노래방", area: "종로", category: "실내 액티비티", weather: "indoor",
      mood: ["stimulating"], vibe: ["lively"],
      desc: "좁은 부스에 혼자 들어가 눈치 보지 않고 목청 높여 스트레스를 풀 수 있는 곳이에요.",
      tip: "평일 낮 시간엔 곡당 가격이 더 싼 곳도 많아요." },
    { name: "장충동 대중목욕탕", area: "장충동", category: "사우나", weather: "indoor",
      mood: ["calm", "blank"], vibe: ["quiet"],
      desc: "뜨끈한 탕에 몸을 담그고 아무 생각 없이 시간을 흘려보내며 몸과 마음을 함께 씻어내는 곳이에요.",
      tip: "평일 오전 시간대가 가장 한산해요." },
    { name: "광화문 야외도서관", area: "광화문", category: "독서", weather: "outdoor",
      mood: ["calm", "create"], vibe: ["quiet", "aesthetic"],
      desc: "광화문광장에 마련된 야외 서가에서 책 한 권 골라 그늘 아래 앉아 읽는, 도심 속 여유로운 시간을 보내기 좋은 곳이에요.",
      tip: "책은 무료로 대여 가능하니 편하게 골라 읽고 제자리에 돌려놓으세요." }
  ];

  function weatherNote(place) {
    if (!currentWeather) return "오늘 날씨 정보는 없지만, 이 장소는 언제 가도 좋아요.";
    const kind = place.weather === "indoor" ? "실내" : "야외";
    return `오늘 서울은 ${currentWeather.desc}, ${currentWeather.temp}° — ${kind} 장소라 지금 날씨에도 잘 맞아요.`;
  }

  /* =========================================================
     화면 전환
     ========================================================= */

  function switchScreen(name) {
    document.querySelectorAll(".screen").forEach((el) => {
      el.classList.toggle("is-active", el.dataset.screen === name);
    });
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
  }

  /* =========================================================
     진단형 질문 화면
     ========================================================= */

  const QUESTIONS = [
    { key: "mood", title: "지금 기분에 가장 가까운 건?", options: [
        { label: "차분하게 힐링하고 싶어요", value: "calm" },
        { label: "새로운 자극이 필요해요", value: "stimulating" },
        { label: "아무 생각 없이 멍때리고 싶어요", value: "blank" },
        { label: "뭔가 만들거나 배우고 싶어요", value: "create" }
    ] },
    { key: "vibe", title: "어떤 분위기에 끌리나요?", options: [
        { label: "조용한 곳", value: "quiet" },
        { label: "사람 구경하기 좋은 곳", value: "peoplewatch" },
        { label: "감성 넘치는 곳", value: "aesthetic" },
        { label: "활기찬 곳", value: "lively" }
    ] },
    { key: "place", title: "오늘은 어디서 시간을 보내고 싶어요?", options: [
        { label: "실내가 좋아요", value: "indoor" },
        { label: "밖으로 나가고 싶어요", value: "outdoor" },
        { label: "날씨에 맡길게요", value: "auto" }
    ] }
  ];

  let quizState = { step: 0, answers: {} };

  function renderQuizStep() {
    const q = QUESTIONS[quizState.step];

    document.getElementById("questionTitle").textContent = q.title;

    const optionsWrap = document.getElementById("questionOptions");
    optionsWrap.innerHTML = "";
    q.options.forEach((opt) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "option-btn";
      btn.textContent = opt.label;
      btn.addEventListener("click", () => handleQuizAnswer(q.key, opt.value));
      optionsWrap.appendChild(btn);
    });

    const dotsWrap = document.getElementById("progressDots");
    dotsWrap.innerHTML = "";
    QUESTIONS.forEach((_, i) => {
      const dot = document.createElement("span");
      if (i < quizState.step) dot.classList.add("is-done");
      else if (i === quizState.step) dot.classList.add("is-active");
      dotsWrap.appendChild(dot);
    });
  }

  function handleQuizAnswer(key, value) {
    quizState.answers[key] = value;
    if (quizState.step < QUESTIONS.length - 1) {
      quizState.step += 1;
      renderQuizStep();
    } else {
      showResult(pickByQuiz(quizState.answers), "quiz");
    }
  }

  function startQuiz() {
    quizState = { step: 0, answers: {} };
    renderQuizStep();
    switchScreen("quiz");
  }

  const PREF_KEYS = { excludeVisited: "honplay_exclude_visited" };

  function loadExcludeVisited() {
    return localStorage.getItem(PREF_KEYS.excludeVisited) === "true";
  }

  function saveExcludeVisited(value) {
    localStorage.setItem(PREF_KEYS.excludeVisited, value ? "true" : "false");
  }

  function applyExcludeVisited(pool) {
    if (!loadExcludeVisited()) return pool;
    const visited = new Set(loadVisited());
    const unvisited = pool.filter((p) => !visited.has(p.name));
    return unvisited.length > 0 ? unvisited : pool;
  }

  function pickByQuiz(answers) {
    let indoorPref = null;
    if (answers.place === "indoor") indoorPref = "indoor";
    else if (answers.place === "outdoor") indoorPref = "outdoor";
    else if (currentWeather && currentWeather.indoorOnly) indoorPref = "indoor";

    let pool = indoorPref ? PLACES.filter((p) => p.weather === indoorPref) : PLACES.slice();
    if (pool.length === 0) pool = PLACES.slice();
    pool = applyExcludeVisited(pool);

    const scored = pool.map((p) => ({
      place: p,
      score: (p.mood.includes(answers.mood) ? 2 : 0) + (p.vibe.includes(answers.vibe) ? 1 : 0)
    }));
    const bestScore = Math.max(...scored.map((s) => s.score));
    const top = scored.filter((s) => s.score === bestScore).map((s) => s.place);

    return top[Math.floor(Math.random() * top.length)];
  }

  document.getElementById("quizBackBtn").addEventListener("click", () => {
    if (quizState.step > 0) {
      quizState.step -= 1;
      renderQuizStep();
    } else {
      switchScreen("home");
    }
  });

  /* =========================================================
     랜덤 뽑기 화면
     ========================================================= */

  function drawRandomPlace() {
    let pool = currentWeather && currentWeather.indoorOnly ? PLACES.filter((p) => p.weather === "indoor") : PLACES.slice();
    if (pool.length === 0) pool = PLACES.slice();
    pool = applyExcludeVisited(pool);
    return pool[Math.floor(Math.random() * pool.length)];
  }

  function drawRandom() {
    const finalPlace = drawRandomPlace();
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    switchScreen("result");

    if (reduceMotion) {
      showResult(finalPlace, "random");
      return;
    }

    document.getElementById("resultStamp").textContent = "뽑는 중...";
    document.getElementById("resultCategory").textContent = "";
    document.getElementById("resultArea").textContent = "";
    document.getElementById("resultDesc").textContent = "";
    document.getElementById("resultTip").textContent = "";
    document.getElementById("weatherNote").textContent = "";
    document.getElementById("mapBtn").href = "#";

    const nameEl = document.getElementById("resultName");
    let ticks = 0;
    const maxTicks = 9;
    const timer = setInterval(() => {
      const p = PLACES[Math.floor(Math.random() * PLACES.length)];
      nameEl.textContent = p.name;
      ticks += 1;
      if (ticks >= maxTicks) {
        clearInterval(timer);
        showResult(finalPlace, "random");
      }
    }, 70);
  }

  /* =========================================================
     결과 화면 (진단형 / 랜덤 뽑기 공용)
     ========================================================= */

  function showResult(place, mode) {
    switchScreen("result");

    const label = mode === "quiz" ? "진단 결과" : "오늘의 뽑기";
    document.getElementById("resultStamp").textContent = label;
    document.getElementById("resultScreenTitle").textContent = label;
    document.getElementById("resultCategory").textContent = place.category;
    document.getElementById("resultArea").textContent = place.area;
    document.getElementById("resultName").textContent = place.name;
    document.getElementById("resultDesc").textContent = place.desc;
    document.getElementById("resultTip").textContent = place.tip;
    document.getElementById("weatherNote").textContent = weatherNote(place);
    document.getElementById("mapBtn").href = `https://map.naver.com/p/search/${encodeURIComponent(place.name + " " + place.area)}`;

    const retryBtn = document.getElementById("retryBtn");
    retryBtn.textContent = mode === "quiz" ? "다시 진단하기" : "다시 뽑기";
    retryBtn.onclick = () => (mode === "quiz" ? startQuiz() : drawRandom());
  }

  document.getElementById("resultBackBtn").addEventListener("click", () => switchScreen("home"));
  document.getElementById("homeFromResultBtn").addEventListener("click", () => switchScreen("home"));

  /* =========================================================
     아카이브 (전체 장소 체크리스트)
     ========================================================= */

  const CATEGORY_ICONS = {
    "서점": '<rect x="4" y="16" width="16" height="3" rx="1"/><rect x="5" y="11" width="14" height="3" rx="1"/><rect x="6" y="6" width="12" height="3" rx="1"/>',
    "독서": '<path d="M12 5c-2-1-5-1-8 0v13c3-1 6-1 8 0 2-1 5-1 8 0V5c-3-1-6-1-8 0Z"/><path d="M12 5v13"/>',
    "산책": '<ellipse cx="9" cy="7" rx="2" ry="3"/><ellipse cx="15" cy="13" rx="2" ry="3"/><ellipse cx="9" cy="19" rx="2" ry="3"/>',
    "카페": '<path d="M5 9h13v3a5 5 0 0 1-5 5H10a5 5 0 0 1-5-5V9Z"/><path d="M18 10h1.5a2 2 0 0 1 0 4H18"/>',
    "전시": '<rect x="4" y="5" width="16" height="13" rx="1.5"/><path d="M4 15l4-4 3 3 5-5 4 4"/><circle cx="9" cy="9" r="1.2"/>',
    "실내 액티비티": '<rect x="4" y="4" width="16" height="16" rx="4"/><circle cx="9" cy="9" r="1.1" fill="currentColor" stroke="none"/><circle cx="15" cy="15" r="1.1" fill="currentColor" stroke="none"/><circle cx="15" cy="9" r="1.1" fill="currentColor" stroke="none"/><circle cx="9" cy="15" r="1.1" fill="currentColor" stroke="none"/>',
    "공방": '<path d="M4 20l4-1 9-9-3-3-9 9-1 4Z"/><path d="M14 7l3-3 3 3-3 3"/>',
    "맛집": '<path d="M4 12h16a8 8 0 0 1-16 0Z"/><path d="M9 12V9M15 12V9"/>',
    "영화": '<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18M7 6l2 4M12 6l2 4M17 6l2 4"/>',
    "마켓": '<path d="M6 8h12l-1 12H7L6 8Z"/><path d="M9 8V6a3 3 0 1 1 6 0v2"/>',
    "야경": '<path d="M15 3a7 7 0 1 0 6 10 7 7 0 0 1-6-10Z"/>',
    "바": '<path d="M5 4h14l-7 8-7-8Z"/><path d="M12 12v7M9 19h6"/>',
    "사우나": '<path d="M12 3c2 3 4 5 4 8a4 4 0 1 1-8 0c0-3 2-5 4-8Z"/>'
  };

  const DEFAULT_CATEGORY_ICON = '<path d="M12 3l2.5 6.5L21 10l-5 4 1.5 7-5.5-3.5L6.5 21 8 14 3 10l6.5-.5L12 3Z"/>';

  function categoryIcon(category) {
    return CATEGORY_ICONS[category] || DEFAULT_CATEGORY_ICON;
  }

  const STORAGE_KEYS = { visited: "honplay_visited", custom: "honplay_custom_places" };

  function loadVisited() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEYS.visited)) || []; }
    catch (err) { return []; }
  }

  function saveVisited(ids) {
    localStorage.setItem(STORAGE_KEYS.visited, JSON.stringify(ids));
  }

  function loadCustomPlaces() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEYS.custom)) || []; }
    catch (err) { return []; }
  }

  function saveCustomPlaces(places) {
    localStorage.setItem(STORAGE_KEYS.custom, JSON.stringify(places));
  }

  function toggleVisited(id) {
    const visited = new Set(loadVisited());
    if (visited.has(id)) visited.delete(id);
    else visited.add(id);
    saveVisited([...visited]);
    renderArchive();
  }

  function addCustomPlace(rawName, category, desc) {
    const name = rawName.trim();
    if (!name) return;
    const custom = loadCustomPlaces();
    custom.push({
      id: `custom-${Date.now()}`,
      name,
      area: "",
      category: category || "내가 추가한 곳",
      desc: (desc || "").trim()
    });
    saveCustomPlaces(custom);
    renderArchive();
  }

  function removeCustomPlace(id) {
    saveCustomPlaces(loadCustomPlaces().filter((p) => p.id !== id));
    const visited = new Set(loadVisited());
    visited.delete(id);
    saveVisited([...visited]);
    renderArchive();
  }

  let archiveFilter = "all"; // "all" | "been" | "togo"

  function archiveEmptyMessage() {
    if (archiveFilter === "been") return "아직 다녀온 곳이 없어요.";
    if (archiveFilter === "togo") return "모두 다녀왔어요! 새로운 곳을 추가해보세요.";
    return "아직 담긴 장소가 없어요.";
  }

  function renderArchive() {
    const visited = new Set(loadVisited());
    const combined = [
      ...PLACES.map((p) => ({ id: p.name, name: p.name, area: p.area, category: p.category, desc: "", custom: false })),
      ...loadCustomPlaces().map((p) => ({ id: p.id, name: p.name, area: p.area, category: p.category, desc: p.desc || "", custom: true }))
    ];

    document.getElementById("archiveCount").textContent = `${visited.size}/${combined.length}`;

    const filtered = combined.filter((item) => {
      if (archiveFilter === "been") return visited.has(item.id);
      if (archiveFilter === "togo") return !visited.has(item.id);
      return true;
    });

    const list = document.getElementById("archiveList");
    list.innerHTML = "";

    if (filtered.length === 0) {
      const empty = document.createElement("li");
      empty.className = "archive-empty";
      empty.textContent = archiveEmptyMessage();
      list.appendChild(empty);
      return;
    }

    filtered.forEach((item) => {
      const isChecked = visited.has(item.id);

      const li = document.createElement("li");
      li.className = "archive-item" + (isChecked ? " is-checked" : "");

      const label = document.createElement("label");
      label.className = "archive-check";

      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.checked = isChecked;
      checkbox.addEventListener("change", () => toggleVisited(item.id));

      const box = document.createElement("span");
      box.className = "check-box";
      box.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 13l4 4L19 7"/></svg>';

      const icon = document.createElement("span");
      icon.className = "archive-icon";
      icon.innerHTML = `<svg viewBox="0 0 24 24" aria-hidden="true">${categoryIcon(item.category)}</svg>`;

      const text = document.createElement("span");
      text.className = "archive-text";

      const nameEl = document.createElement("span");
      nameEl.className = "archive-name";
      nameEl.textContent = item.name;

      const metaEl = document.createElement("span");
      metaEl.className = "archive-meta";
      metaEl.textContent = item.desc
        ? item.desc
        : (item.area ? `${item.category} · ${item.area}` : item.category);

      text.appendChild(nameEl);
      text.appendChild(metaEl);

      label.appendChild(checkbox);
      label.appendChild(box);
      label.appendChild(icon);
      label.appendChild(text);
      li.appendChild(label);

      if (item.custom) {
        const removeBtn = document.createElement("button");
        removeBtn.type = "button";
        removeBtn.className = "archive-remove";
        removeBtn.setAttribute("aria-label", "삭제");
        removeBtn.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';
        removeBtn.addEventListener("click", () => removeCustomPlace(item.id));
        li.appendChild(removeBtn);
      }

      list.appendChild(li);
    });
  }

  function setArchiveFilter(name) {
    archiveFilter = name;
    document.querySelectorAll(".filter-btn").forEach((btn) => {
      btn.classList.toggle("is-active", btn.dataset.filter === name);
    });
    renderArchive();
  }

  document.querySelectorAll(".filter-btn").forEach((btn) => {
    btn.addEventListener("click", () => setArchiveFilter(btn.dataset.filter));
  });

  function openArchive() {
    setArchiveFilter("all");
    switchScreen("archive");
  }

  document.getElementById("archiveBtn").addEventListener("click", openArchive);
  document.getElementById("archiveBackBtn").addEventListener("click", () => switchScreen("home"));

  document.getElementById("archiveAddBtn").addEventListener("click", () => {
    const input = document.getElementById("archiveInput");
    openAddPlace(input.value);
    input.value = "";
  });

  document.getElementById("archiveInput").addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      document.getElementById("archiveAddBtn").click();
    }
  });

  /* =========================================================
     장소 추가 화면 (아이콘 · 설명)
     ========================================================= */

  const ADDPLACE_CATEGORIES = Object.keys(CATEGORY_ICONS);
  let selectedAddPlaceCategory = null;

  function renderAddPlaceIconPicker() {
    const wrap = document.getElementById("addPlaceIconPicker");
    wrap.innerHTML = "";
    ADDPLACE_CATEGORIES.forEach((category) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "icon-option" + (selectedAddPlaceCategory === category ? " is-selected" : "");
      btn.setAttribute("aria-label", category);
      btn.title = category;
      btn.innerHTML = `<svg viewBox="0 0 24 24" aria-hidden="true">${categoryIcon(category)}</svg>`;
      btn.addEventListener("click", () => {
        selectedAddPlaceCategory = category;
        renderAddPlaceIconPicker();
      });
      wrap.appendChild(btn);
    });
  }

  function openAddPlace(prefillName) {
    selectedAddPlaceCategory = null;
    document.getElementById("addPlaceNameInput").value = prefillName || "";
    document.getElementById("addPlaceDescInput").value = "";
    renderAddPlaceIconPicker();
    switchScreen("addplace");
    document.getElementById("addPlaceNameInput").focus();
  }

  document.getElementById("addPlaceBackBtn").addEventListener("click", () => switchScreen("archive"));
  document.getElementById("addPlaceCancelBtn").addEventListener("click", () => switchScreen("archive"));

  document.getElementById("addPlaceSaveBtn").addEventListener("click", () => {
    const nameInput = document.getElementById("addPlaceNameInput");
    const name = nameInput.value.trim();
    if (!name) {
      nameInput.focus();
      return;
    }
    const desc = document.getElementById("addPlaceDescInput").value;
    addCustomPlace(name, selectedAddPlaceCategory, desc);
    switchScreen("archive");
  });

  /* =========================================================
     시작
     ========================================================= */

  document.getElementById("quizBtn").addEventListener("click", startQuiz);
  document.getElementById("randomBtn").addEventListener("click", drawRandom);

  const excludeVisitedToggle = document.getElementById("excludeVisitedToggle");
  const excludeVisitedState = document.getElementById("excludeVisitedState");
  if (excludeVisitedToggle && excludeVisitedState) {
    const applyState = (checked) => {
      excludeVisitedToggle.checked = checked;
      excludeVisitedState.textContent = checked ? "ON" : "OFF";
    };
    applyState(loadExcludeVisited());
    excludeVisitedToggle.addEventListener("change", () => {
      saveExcludeVisited(excludeVisitedToggle.checked);
      applyState(excludeVisitedToggle.checked);
    });
  }

  loadWeather();
</script>

</body>
</html>
"""

components.html(
    HTML_CONTENT,
    height=900,
    scrolling=True,
)