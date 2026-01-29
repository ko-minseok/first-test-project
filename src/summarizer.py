"""
Email Summarizer using LLM (OpenAI)
"""
import os
from datetime import datetime
from typing import Optional
from openai import OpenAI


class EmailSummarizer:
    """LLM을 사용하여 이메일을 요약하는 클래스"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model

        if not self.api_key:
            raise ValueError("OpenAI API key is required")

        self.client = OpenAI(api_key=self.api_key)

    def summarize_emails(self, email_data: dict) -> str:
        """이메일 데이터를 요약하여 마크다운 형식으로 반환

        Args:
            email_data: outlook_client에서 반환된 이메일 데이터

        Returns:
            str: 마크다운 형식의 요약문
        """
        date = email_data.get("date", datetime.now().strftime("%Y-%m-%d"))
        received = email_data.get("received", [])
        sent = email_data.get("sent", [])

        if not received and not sent:
            return self._generate_empty_summary(date)

        # 이메일 내용을 프롬프트용 텍스트로 변환
        email_text = self._format_emails_for_prompt(received, sent)

        # LLM으로 요약 생성
        summary = self._call_llm(email_text, date)

        # 마크다운 문서 생성
        return self._format_markdown(date, received, sent, summary)

    def _format_emails_for_prompt(self, received: list, sent: list) -> str:
        """이메일을 프롬프트용 텍스트로 변환"""
        lines = []

        if received:
            lines.append("=== 받은 메일 ===")
            for i, email in enumerate(received, 1):
                lines.append(f"\n[받은 메일 {i}]")
                lines.append(f"보낸 사람: {email['from']['name']} <{email['from']['email']}>")
                lines.append(f"제목: {email['subject']}")
                lines.append(f"중요도: {email['importance']}")
                lines.append(f"내용 미리보기: {email['preview'][:500]}...")

        if sent:
            lines.append("\n\n=== 보낸 메일 ===")
            for i, email in enumerate(sent, 1):
                lines.append(f"\n[보낸 메일 {i}]")
                to_list = ", ".join([f"{r['name']} <{r['email']}>" for r in email['to']])
                lines.append(f"받는 사람: {to_list}")
                lines.append(f"제목: {email['subject']}")
                lines.append(f"내용 미리보기: {email['preview'][:500]}...")

        return "\n".join(lines)

    def _call_llm(self, email_text: str, date: str) -> str:
        """LLM API를 호출하여 요약 생성"""
        system_prompt = """당신은 이메일 요약 전문가입니다.
주어진 이메일들을 분석하여 다음 형식으로 요약해주세요:

1. 오늘의 주요 업무/이슈 (가장 중요한 내용 3-5개)
2. 처리가 필요한 항목 (액션 아이템)
3. 주요 연락처 및 미팅 관련 내용
4. 기타 참고사항

요약은 한국어로 작성하고, 핵심 내용만 간결하게 정리해주세요.
개인정보나 민감한 정보는 [비공개]로 마스킹해주세요."""

        user_prompt = f"""다음은 {date}에 수신 및 발신한 이메일 목록입니다.
이 내용을 분석하여 하루 업무 요약을 작성해주세요.

{email_text}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )

        return response.choices[0].message.content

    def _format_markdown(
        self,
        date: str,
        received: list,
        sent: list,
        summary: str
    ) -> str:
        """마크다운 문서 생성"""
        lines = [
            f"# 📧 이메일 일일 요약 - {date}",
            "",
            f"> 생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
            "## 📊 통계",
            "",
            f"- **받은 메일**: {len(received)}건",
            f"- **보낸 메일**: {len(sent)}건",
            f"- **총 처리**: {len(received) + len(sent)}건",
            "",
            "---",
            "",
            "## 📝 AI 요약",
            "",
            summary,
            "",
            "---",
            "",
            "## 📬 받은 메일 목록",
            ""
        ]

        if received:
            for email in received:
                importance_icon = "🔴" if email['importance'] == 'high' else "⚪"
                lines.append(f"- {importance_icon} **{email['subject']}**")
                lines.append(f"  - 보낸 사람: {email['from']['name']}")
                lines.append(f"  - 시간: {email['received_at']}")
                lines.append("")
        else:
            lines.append("- 받은 메일이 없습니다.")
            lines.append("")

        lines.extend([
            "---",
            "",
            "## 📤 보낸 메일 목록",
            ""
        ])

        if sent:
            for email in sent:
                to_names = ", ".join([r['name'] or r['email'] for r in email['to']])
                lines.append(f"- **{email['subject']}**")
                lines.append(f"  - 받는 사람: {to_names}")
                lines.append(f"  - 시간: {email['sent_at']}")
                lines.append("")
        else:
            lines.append("- 보낸 메일이 없습니다.")
            lines.append("")

        lines.extend([
            "---",
            "",
            "*이 문서는 Email Summary Agent에 의해 자동 생성되었습니다.*"
        ])

        return "\n".join(lines)

    def _generate_empty_summary(self, date: str) -> str:
        """메일이 없을 때의 요약문 생성"""
        return f"""# 📧 이메일 일일 요약 - {date}

> 생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 통계

- **받은 메일**: 0건
- **보낸 메일**: 0건

---

## 📝 요약

오늘은 수신 및 발신된 메일이 없습니다.

---

*이 문서는 Email Summary Agent에 의해 자동 생성되었습니다.*
"""


def summarize_today_emails(email_data: dict) -> str:
    """오늘의 이메일을 요약하는 헬퍼 함수"""
    summarizer = EmailSummarizer()
    return summarizer.summarize_emails(email_data)
