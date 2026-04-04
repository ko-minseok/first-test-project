# Email Summary Agent

매일 Outlook 메일을 자동으로 요약하여 GitHub에 마크다운 파일로 업로드하는 에이전트입니다.

## 기능

- Microsoft Graph API를 통한 Outlook 메일 조회 (수신/발신)
- Anthropic Claude를 활용한 메일 내용 AI 요약
- GitHub 저장소에 자동 업로드
- GitHub Actions를 통한 매일 22:00(KST) 자동 실행

## 아키텍처

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Outlook API   │────▶│  LLM (Claude)   │────▶│  GitHub API     │
│ (Microsoft Graph)│     │   Summarizer    │     │   Uploader      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                       │
         └───────────────────────┴───────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   GitHub Actions        │
                    │   (Daily 22:00 KST)     │
                    └─────────────────────────┘
```

## 프로젝트 구조

```
.
├── src/
│   ├── __init__.py
│   ├── main.py              # 메인 에이전트 스크립트
│   ├── outlook_client.py    # Outlook API 연동
│   ├── summarizer.py        # LLM 요약 모듈
│   └── github_uploader.py   # GitHub 업로드 모듈
├── .github/
│   └── workflows/
│       └── email-summary.yml  # GitHub Actions 워크플로우
├── summaries/               # 요약 파일 저장 폴더
├── requirements.txt
├── .env.example
├── SETUP.md                 # 상세 설정 가이드
└── README.md
```

## 빠른 시작

### 1. 필수 설정

자세한 설정 방법은 [SETUP.md](./SETUP.md)를 참조하세요.

- Azure AD App Registration (Outlook API 접근)
- Anthropic API 키
- GitHub Personal Access Token

### 2. 설치

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
pip install -r requirements.txt
```

### 3. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일 편집
```

### 4. 실행

```bash
cd src
python main.py --user-email your-email@company.com
```

## 사용법

```bash
# 오늘 메일 요약 및 GitHub 업로드
python main.py --user-email user@example.com

# 특정 날짜 메일 요약
python main.py --user-email user@example.com --date 2024-01-15

# 테스트 실행 (로컬 저장만)
python main.py --user-email user@example.com --dry-run
```

## GitHub Actions

- **자동 실행**: 매일 22:00 KST
- **수동 실행**: Actions 탭에서 "Run workflow"

## 출력 예시

```markdown
# 📧 이메일 일일 요약 - 2024-01-15

## 📊 통계
- 받은 메일: 15건
- 보낸 메일: 8건

## 📝 AI 요약
### 오늘의 주요 업무/이슈
1. 프로젝트 A 마일스톤 검토
2. 분기 보고서 마감 안내
...
```

## 기술 스택

- **Python 3.11+**
- **MSAL** - Microsoft 인증 라이브러리
- **Anthropic API** - Claude 모델
- **PyGithub** - GitHub API
- **GitHub Actions** - 스케줄링

## 라이선스

MIT License
