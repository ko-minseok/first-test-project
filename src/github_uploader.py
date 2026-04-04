"""
GitHub File Uploader using PyGithub
"""
import os
from datetime import datetime
from typing import Optional
from github import Github, GithubException


class GitHubUploader:
    """GitHub에 파일을 업로드하는 클래스"""

    def __init__(
        self,
        token: Optional[str] = None,
        repo_name: Optional[str] = None
    ):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.repo_name = repo_name or os.getenv("GITHUB_REPO")

        if not self.token:
            raise ValueError("GitHub token is required")
        if not self.repo_name:
            raise ValueError("GitHub repository name is required")

        self.github = Github(self.token)
        self.repo = self.github.get_repo(self.repo_name)

    def upload_summary(
        self,
        content: str,
        date: Optional[str] = None,
        folder: str = "summaries"
    ) -> dict:
        """요약 파일을 GitHub에 업로드

        Args:
            content: 업로드할 마크다운 내용
            date: 파일명에 사용할 날짜 (기본값: 오늘)
            folder: 저장할 폴더 경로

        Returns:
            dict: 업로드 결과 정보
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        file_path = f"{folder}/{date}-email-summary.md"

        try:
            # 기존 파일이 있는지 확인
            existing_file = self._get_file(file_path)

            if existing_file:
                # 파일이 이미 존재하면 업데이트
                result = self._update_file(file_path, content, existing_file)
                action = "updated"
            else:
                # 새 파일 생성
                result = self._create_file(file_path, content)
                action = "created"

            return {
                "success": True,
                "action": action,
                "path": file_path,
                "url": result.content.html_url,
                "sha": result.content.sha
            }

        except GithubException as e:
            return {
                "success": False,
                "error": str(e),
                "path": file_path
            }

    def _get_file(self, path: str):
        """파일이 존재하는지 확인"""
        try:
            return self.repo.get_contents(path)
        except GithubException as e:
            if e.status == 404:
                return None
            raise

    def _create_file(self, path: str, content: str):
        """새 파일 생성"""
        commit_message = f"📧 Add email summary for {path.split('/')[-1].replace('-email-summary.md', '')}"

        return self.repo.create_file(
            path=path,
            message=commit_message,
            content=content,
            branch="main"
        )

    def _update_file(self, path: str, content: str, existing_file):
        """기존 파일 업데이트"""
        commit_message = f"📧 Update email summary for {path.split('/')[-1].replace('-email-summary.md', '')}"

        return self.repo.update_file(
            path=path,
            message=commit_message,
            content=content,
            sha=existing_file.sha,
            branch="main"
        )

    def ensure_folder_exists(self, folder: str = "summaries") -> bool:
        """폴더가 존재하는지 확인하고 없으면 생성"""
        try:
            self.repo.get_contents(folder)
            return True
        except GithubException as e:
            if e.status == 404:
                # README 파일을 생성하여 폴더 생성
                readme_content = """# Email Summaries

이 폴더에는 자동 생성된 이메일 일일 요약이 저장됩니다.

## 구조

- `YYYY-MM-DD-email-summary.md`: 해당 날짜의 이메일 요약

## 자동 생성

이 파일들은 Email Summary Agent에 의해 매일 22:00(KST)에 자동으로 생성됩니다.
"""
                self.repo.create_file(
                    path=f"{folder}/README.md",
                    message="📁 Initialize summaries folder",
                    content=readme_content,
                    branch="main"
                )
                return True
            raise


def upload_to_github(content: str, date: Optional[str] = None) -> dict:
    """GitHub에 요약을 업로드하는 헬퍼 함수"""
    uploader = GitHubUploader()
    uploader.ensure_folder_exists()
    return uploader.upload_summary(content, date)
