"""
Email Summary Agent - Main Script
매일 22시에 실행되어 당일 이메일을 요약하고 GitHub에 업로드
"""
import os
import sys
import argparse
from datetime import datetime
from dotenv import load_dotenv

from outlook_client import OutlookClient
from summarizer import EmailSummarizer
from github_uploader import GitHubUploader


def run_agent(user_email: str, target_date: str = None, dry_run: bool = False):
    """이메일 요약 에이전트 실행

    Args:
        user_email: Outlook 사용자 이메일 주소
        target_date: 조회할 날짜 (YYYY-MM-DD 형식, 기본값: 오늘)
        dry_run: True면 GitHub 업로드 없이 로컬에만 저장
    """
    print("=" * 50)
    print("📧 Email Summary Agent 시작")
    print("=" * 50)

    # 날짜 파싱
    if target_date:
        date_obj = datetime.strptime(target_date, "%Y-%m-%d")
    else:
        date_obj = datetime.now()
        target_date = date_obj.strftime("%Y-%m-%d")

    print(f"\n📅 대상 날짜: {target_date}")
    print(f"👤 사용자: {user_email}")

    # Step 1: Outlook에서 이메일 조회
    print("\n[1/3] Outlook에서 이메일 조회 중...")
    try:
        outlook = OutlookClient()
        email_data = outlook.get_emails_for_date(
            user_id=user_email,
            target_date=date_obj
        )
        received_count = len(email_data.get("received", []))
        sent_count = len(email_data.get("sent", []))
        print(f"  ✅ 받은 메일: {received_count}건, 보낸 메일: {sent_count}건")
    except Exception as e:
        print(f"  ❌ Outlook 조회 실패: {e}")
        sys.exit(1)

    # Step 2: LLM으로 요약 생성
    print("\n[2/3] AI로 이메일 요약 생성 중...")
    try:
        summarizer = EmailSummarizer()
        summary_md = summarizer.summarize_emails(email_data)
        print(f"  ✅ 요약 생성 완료 ({len(summary_md)} characters)")
    except Exception as e:
        print(f"  ❌ 요약 생성 실패: {e}")
        sys.exit(1)

    # Step 3: GitHub에 업로드 또는 로컬 저장
    if dry_run:
        print("\n[3/3] 로컬에 파일 저장 중 (dry-run 모드)...")
        local_path = f"summaries/{target_date}-email-summary.md"
        os.makedirs("summaries", exist_ok=True)
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(summary_md)
        print(f"  ✅ 저장 완료: {local_path}")
    else:
        print("\n[3/3] GitHub에 업로드 중...")
        try:
            uploader = GitHubUploader()
            uploader.ensure_folder_exists()
            result = uploader.upload_summary(summary_md, target_date)

            if result["success"]:
                print(f"  ✅ 업로드 완료: {result['action']}")
                print(f"  📎 URL: {result['url']}")
            else:
                print(f"  ❌ 업로드 실패: {result['error']}")
                sys.exit(1)
        except Exception as e:
            print(f"  ❌ GitHub 업로드 실패: {e}")
            sys.exit(1)

    print("\n" + "=" * 50)
    print("✨ Email Summary Agent 완료!")
    print("=" * 50)


def main():
    """CLI 엔트리포인트"""
    # .env 파일 로드
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Outlook 이메일을 요약하여 GitHub에 업로드하는 에이전트"
    )
    parser.add_argument(
        "--user-email",
        "-u",
        required=True,
        help="Outlook 사용자 이메일 주소"
    )
    parser.add_argument(
        "--date",
        "-d",
        default=None,
        help="조회할 날짜 (YYYY-MM-DD 형식, 기본값: 오늘)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="GitHub 업로드 없이 로컬에만 저장"
    )

    args = parser.parse_args()

    # 필수 환경 변수 확인
    required_vars = [
        "AZURE_CLIENT_ID",
        "AZURE_CLIENT_SECRET",
        "AZURE_TENANT_ID",
        "OPENAI_API_KEY"
    ]

    if not args.dry_run:
        required_vars.extend(["GITHUB_TOKEN", "GITHUB_REPO"])

    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"❌ 필수 환경 변수가 설정되지 않았습니다: {', '.join(missing_vars)}")
        print("   .env 파일을 확인하거나 환경 변수를 설정해주세요.")
        sys.exit(1)

    run_agent(
        user_email=args.user_email,
        target_date=args.date,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    main()
