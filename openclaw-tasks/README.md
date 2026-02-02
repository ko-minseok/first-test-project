# OpenClaw Automation Tasks

Minseok의 OpenClaw 자동화 에이전트가 실행하는 Task들입니다.

## 📋 Task 목록

### 1. AI Daily Report
- **스케줄:** 매일 오전 8시 (KST)
- **채널:** Telegram
- **설명:** AI/LLM/Agent 관련 최신 뉴스를 수집하여 리포트 형태로 전송

**수집 항목:**
1. 새로운 LLM 모델 출시 (GPT, Claude, Gemini, Llama, 오픈소스 모델 등)
2. AI Agent 개발 동향 (AutoGPT, LangChain, CrewAI 등)
3. AI 서비스/제품 런칭 (새로운 AI 스타트업, 빅테크 AI 서비스)
4. 주요 AI 연구/논문 (arxiv 등)
5. 주요 LLM 모델 Deprecation/은퇴 일정

**포맷:**
- 각 뉴스 항목에 출처 링크 포함
- Bullet point 형식
- 한국어로 작성

---

## 🔧 기술 스택

- **Platform:** [OpenClaw](https://github.com/openclaw/openclaw)
- **Scheduling:** OpenClaw Cron (Gateway)
- **Data Source:** Web Search / Web Fetch
- **Delivery:** Telegram Bot API

## 📁 파일 구조

```
openclaw-tasks/
├── README.md                 # 이 파일
├── tasks/
│   └── ai-daily-report.json  # AI Daily Report task 설정
└── prompts/
    └── ai-daily-report.md    # 리포트 생성 프롬프트
```

## ⚙️ Task 설정

Task 설정은 OpenClaw Gateway의 cron 시스템을 통해 관리됩니다.
설정 변경이 필요하면 에이전트에게 직접 요청하세요.

---

*Last updated: 2026-02-02*
