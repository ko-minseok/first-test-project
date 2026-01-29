"""
Outlook Mail Client using Microsoft Graph API
"""
import os
from datetime import datetime, timedelta
from typing import Optional
import msal
import requests


class OutlookClient:
    """Microsoft Graph API를 통해 Outlook 메일을 조회하는 클라이언트"""

    GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"
    SCOPES = ["https://graph.microsoft.com/.default"]

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        tenant_id: Optional[str] = None
    ):
        self.client_id = client_id or os.getenv("AZURE_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("AZURE_CLIENT_SECRET")
        self.tenant_id = tenant_id or os.getenv("AZURE_TENANT_ID")
        self._access_token = None

        if not all([self.client_id, self.client_secret, self.tenant_id]):
            raise ValueError("Azure credentials are required")

    def _get_access_token(self) -> str:
        """MSAL을 사용하여 액세스 토큰 획득"""
        if self._access_token:
            return self._access_token

        authority = f"https://login.microsoftonline.com/{self.tenant_id}"

        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=authority,
            client_credential=self.client_secret
        )

        result = app.acquire_token_for_client(scopes=self.SCOPES)

        if "access_token" not in result:
            error_msg = result.get("error_description", "Unknown error")
            raise Exception(f"Failed to acquire token: {error_msg}")

        self._access_token = result["access_token"]
        return self._access_token

    def _make_request(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """Graph API 요청 수행"""
        headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json"
        }

        url = f"{self.GRAPH_API_ENDPOINT}{endpoint}"
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()

        return response.json()

    def get_emails_for_date(
        self,
        user_id: str,
        target_date: Optional[datetime] = None,
        include_sent: bool = True
    ) -> dict:
        """특정 날짜의 수신/발신 메일 조회

        Args:
            user_id: 사용자 이메일 또는 ID
            target_date: 조회할 날짜 (기본값: 오늘)
            include_sent: 발신 메일 포함 여부

        Returns:
            dict: received와 sent 메일 목록
        """
        if target_date is None:
            target_date = datetime.now()

        # 해당 날짜의 시작과 끝 시간 설정
        start_of_day = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        start_iso = start_of_day.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_iso = end_of_day.strftime("%Y-%m-%dT%H:%M:%SZ")

        # 수신 메일 조회 (받은 편지함)
        received_filter = f"receivedDateTime ge {start_iso} and receivedDateTime lt {end_iso}"
        received_emails = self._fetch_emails(
            user_id=user_id,
            folder="inbox",
            filter_query=received_filter
        )

        # 발신 메일 조회 (보낸 편지함)
        sent_emails = []
        if include_sent:
            sent_filter = f"sentDateTime ge {start_iso} and sentDateTime lt {end_iso}"
            sent_emails = self._fetch_emails(
                user_id=user_id,
                folder="sentItems",
                filter_query=sent_filter
            )

        return {
            "date": target_date.strftime("%Y-%m-%d"),
            "received": received_emails,
            "sent": sent_emails
        }

    def _fetch_emails(
        self,
        user_id: str,
        folder: str,
        filter_query: str
    ) -> list:
        """메일 폴더에서 이메일 조회"""
        endpoint = f"/users/{user_id}/mailFolders/{folder}/messages"

        params = {
            "$filter": filter_query,
            "$select": "id,subject,from,toRecipients,receivedDateTime,sentDateTime,bodyPreview,body,importance",
            "$orderby": "receivedDateTime desc",
            "$top": 100
        }

        try:
            result = self._make_request(endpoint, params)
            emails = result.get("value", [])

            return [self._parse_email(email) for email in emails]
        except requests.exceptions.HTTPError as e:
            print(f"Error fetching emails from {folder}: {e}")
            return []

    def _parse_email(self, email: dict) -> dict:
        """이메일 데이터 파싱"""
        from_info = email.get("from", {}).get("emailAddress", {})
        to_recipients = email.get("toRecipients", [])

        return {
            "id": email.get("id"),
            "subject": email.get("subject", "(제목 없음)"),
            "from": {
                "name": from_info.get("name", ""),
                "email": from_info.get("address", "")
            },
            "to": [
                {
                    "name": r.get("emailAddress", {}).get("name", ""),
                    "email": r.get("emailAddress", {}).get("address", "")
                }
                for r in to_recipients
            ],
            "received_at": email.get("receivedDateTime"),
            "sent_at": email.get("sentDateTime"),
            "preview": email.get("bodyPreview", ""),
            "body": email.get("body", {}).get("content", ""),
            "importance": email.get("importance", "normal")
        }


def get_today_emails(user_id: str) -> dict:
    """오늘의 이메일을 조회하는 헬퍼 함수"""
    client = OutlookClient()
    return client.get_emails_for_date(user_id=user_id)
