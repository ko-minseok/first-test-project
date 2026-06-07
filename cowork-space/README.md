# CoWork Space

협업 공간 자동화 에이전트가 실행하는 Task들입니다.

## 📋 Task 목록

### 1. Daily Standup Report
- **스케줄:** 매일 오전 9시 (KST)
- **채널:** Slack
- **설명:** 팀 데일리 스탠드업을 위한 현황 리포트 생성 및 전송

### 2. Weekly Summary
- **스케줄:** 매주 금요일 오후 5시 (KST)
- **채널:** Slack
- **설명:** 한 주간의 작업 요약 및 다음 주 계획 정리

---

## 🔧 기술 스택

- **Platform:** OpenClaw
- **Scheduling:** OpenClaw Cron (Gateway)
- **Delivery:** Slack Bot API

## 📁 파일 구조

```
cowork-space/
├── README.md                     # 이 파일
├── tasks/
│   ├── daily-standup.json        # 데일리 스탠드업 task 설정
│   └── weekly-summary.json       # 주간 요약 task 설정
└── prompts/
    ├── daily-standup.md          # 스탠드업 리포트 프롬프트
    └── weekly-summary.md         # 주간 요약 프롬프트
```

## ⚙️ Task 설정

Task 설정은 OpenClaw Gateway의 cron 시스템을 통해 관리됩니다.
설정 변경이 필요하면 에이전트에게 직접 요청하세요.

---

*Last updated: 2026-06-07*
