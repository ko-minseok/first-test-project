# Email Summary Agent 설정 가이드

이 문서는 Email Summary Agent를 설정하고 사용하는 방법을 설명합니다.

## 개요

Email Summary Agent는 다음 작업을 자동으로 수행합니다:
1. 매일 22:00(KST)에 Microsoft Outlook에서 당일 수신/발신 메일 조회
2. OpenAI GPT를 사용하여 메일 내용 요약
3. 요약된 내용을 GitHub 저장소에 마크다운 파일로 업로드

## 사전 요구사항

- Python 3.11+
- Microsoft 365 계정 (Outlook)
- Azure 구독 (App Registration)
- OpenAI API 키
- GitHub 계정 및 Personal Access Token

---

## 1. Azure AD App Registration 설정

### 1.1 App 등록

1. [Azure Portal](https://portal.azure.com) 접속
2. **Azure Active Directory** > **App registrations** > **New registration**
3. 앱 정보 입력:
   - Name: `Email Summary Agent`
   - Supported account types: `Accounts in this organizational directory only`
4. **Register** 클릭

### 1.2 API 권한 설정

1. 등록된 앱에서 **API permissions** > **Add a permission**
2. **Microsoft Graph** > **Application permissions** 선택
3. 다음 권한 추가:
   - `Mail.Read` - 메일 읽기
   - `Mail.ReadBasic.All` - 기본 메일 정보 읽기
   - `User.Read.All` - 사용자 정보 읽기
4. **Grant admin consent** 클릭 (관리자 동의 필요)

### 1.3 Client Secret 생성

1. **Certificates & secrets** > **New client secret**
2. Description: `email-summary-agent`
3. Expires: 원하는 만료 기간 선택
4. **Add** 클릭 후 **Value** 복사 (⚠️ 한 번만 표시됨!)

### 1.4 필요한 정보 저장

다음 정보를 안전하게 저장:
- **Client ID**: Overview에서 확인
- **Client Secret**: 1.3에서 생성한 값
- **Tenant ID**: Overview에서 확인

---

## 2. OpenAI API 키 발급

1. [OpenAI Platform](https://platform.openai.com) 접속
2. **API Keys** > **Create new secret key**
3. 키 복사 및 안전하게 저장

---

## 3. GitHub Personal Access Token 발급

1. GitHub > **Settings** > **Developer settings** > **Personal access tokens** > **Tokens (classic)**
2. **Generate new token** 클릭
3. 권한 설정:
   - `repo` - 저장소 접근 권한
4. 토큰 생성 및 복사

---

## 4. GitHub Secrets 설정

저장소의 **Settings** > **Secrets and variables** > **Actions** > **New repository secret**에서 다음 시크릿 추가:

| Secret Name | 설명 |
|-------------|------|
| `AZURE_CLIENT_ID` | Azure App Client ID |
| `AZURE_CLIENT_SECRET` | Azure App Client Secret |
| `AZURE_TENANT_ID` | Azure Tenant ID |
| `OPENAI_API_KEY` | OpenAI API 키 |
| `GH_PAT` | GitHub Personal Access Token |
| `USER_EMAIL` | Outlook 사용자 이메일 주소 |

---

## 5. 로컬 실행 (테스트)

### 5.1 환경 설정

```bash
# 저장소 클론
git clone https://github.com/your-username/your-repo.git
cd your-repo

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 5.2 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집하여 실제 값 입력
```

### 5.3 실행

```bash
cd src

# 오늘 메일 요약 (GitHub 업로드)
python main.py --user-email your-email@company.com

# 특정 날짜 메일 요약
python main.py --user-email your-email@company.com --date 2024-01-15

# 로컬에만 저장 (테스트용)
python main.py --user-email your-email@company.com --dry-run
```

---

## 6. GitHub Actions 스케줄

워크플로우는 자동으로 설정되어 있습니다:
- **실행 시간**: 매일 22:00 KST (13:00 UTC)
- **수동 실행**: Actions 탭에서 "Run workflow" 버튼

### 수동 실행 방법

1. GitHub 저장소 > **Actions** 탭
2. **Email Summary Agent** 워크플로우 선택
3. **Run workflow** 클릭
4. (선택) 특정 날짜 입력
5. **Run workflow** 버튼 클릭

---

## 7. 출력 형식

요약은 `summaries/YYYY-MM-DD-email-summary.md` 형식으로 저장됩니다.

### 예시 출력

```markdown
# 📧 이메일 일일 요약 - 2024-01-15

> 생성 시간: 2024-01-15 22:00:00

---

## 📊 통계

- **받은 메일**: 15건
- **보낸 메일**: 8건
- **총 처리**: 23건

---

## 📝 AI 요약

### 오늘의 주요 업무/이슈
1. 프로젝트 A 마일스톤 검토 회의 요청
2. 분기 보고서 제출 마감 안내
...
```

---

## 문제 해결

### Azure 권한 오류

```
Error: Insufficient privileges to complete the operation
```
→ Azure Portal에서 **Grant admin consent** 버튼을 클릭하세요.

### GitHub 업로드 실패

```
Error: 403 Forbidden
```
→ GitHub PAT의 `repo` 권한을 확인하세요.

### 메일을 찾을 수 없음

- 시간대 설정을 확인하세요 (KST vs UTC)
- 사용자 이메일 주소가 올바른지 확인하세요

---

## 보안 주의사항

⚠️ **중요**: 다음 정보는 절대 공개 저장소에 커밋하지 마세요!
- `.env` 파일
- API 키 및 시크릿
- 개인 이메일 주소

`.gitignore`에 민감한 파일이 포함되어 있는지 확인하세요.
