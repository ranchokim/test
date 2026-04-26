#!/usr/bin/env python3
"""Omnichannel promotion planner for a homepage.

This tool does not send spam or auto-post. It generates a practical plan,
message templates, and a 30-day schedule you can execute across channels.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from textwrap import dedent


@dataclass(frozen=True)
class Channel:
    name: str
    objective: str
    cadence_per_week: int


DEFAULT_CHANNELS: tuple[Channel, ...] = (
    Channel("Instagram", "브랜드 비주얼/짧은 리일로 관심 유도", 4),
    Channel("YouTube Shorts", "짧은 데모 영상으로 제품 이해도 향상", 3),
    Channel("Blog(SEO)", "검색 유입 확보(키워드 콘텐츠)", 2),
    Channel("Email", "기존 잠재고객 전환/재방문 유도", 2),
    Channel("Naver Cafe/Community", "신뢰 기반 후기/질문 대응", 3),
    Channel("X(Twitter)", "실시간 소통/이벤트 확산", 5),
    Channel("Paid Ads", "즉시 트래픽 확보 및 리타겟팅", 7),
)


def build_weekly_plan(url: str, audience: str, tone: str) -> str:
    rows: list[str] = []
    for ch in DEFAULT_CHANNELS:
        rows.append(
            f"- **{ch.name}** ({ch.cadence_per_week}회/주): {ch.objective} | 핵심 메시지: "
            f"'{audience}를 위한 {url}의 가치' ({tone} 톤)"
        )
    return "\n".join(rows)


def day_topic(day_index: int) -> str:
    topics = [
        "문제 공감 + 솔루션 제시",
        "핵심 기능 1가지 데모",
        "고객 후기(또는 예상 사용 시나리오)",
        "비교 콘텐츠(기존 방식 vs pogobox.shop)",
        "FAQ 답변",
        "한정 혜택/이벤트 안내",
        "브랜드 스토리/미션",
    ]
    return topics[day_index % len(topics)]


def create_calendar(start: date, days: int, url: str) -> list[dict[str, str]]:
    channels_cycle = ["Instagram", "YouTube Shorts", "Blog", "Email", "Community", "X", "Paid Ads"]
    calendar: list[dict[str, str]] = []
    for i in range(days):
        when = start + timedelta(days=i)
        channel = channels_cycle[i % len(channels_cycle)]
        topic = day_topic(i)
        cta = f"자세히 보기: {url}"
        calendar.append(
            {
                "date": when.isoformat(),
                "channel": channel,
                "topic": topic,
                "content_hint": f"{topic} 중심으로 15~60초 또는 800~1200자 구성",
                "cta": cta,
            }
        )
    return calendar


def kpi_section(monthly_budget_krw: int) -> str:
    ad = int(monthly_budget_krw * 0.5)
    content = int(monthly_budget_krw * 0.35)
    tool = monthly_budget_krw - ad - content
    return dedent(
        f"""
        ## 예산 가이드 (월 {monthly_budget_krw:,}원)
        - 유료 광고: {ad:,}원 (50%)
        - 콘텐츠 제작: {content:,}원 (35%)
        - 툴/분석: {tool:,}원 (15%)

        ## KPI 제안
        - 방문자수(세션): 주차별 +10~20% 성장
        - 전환율(CVR): 랜딩 페이지 기준 2~5%
        - 이메일 오픈율: 25%+
        - 광고 CTR: 1.5%+
        - CAC(고객획득비용): 매주 하향 추세 확인
        """
    ).strip()


def sample_copy(url: str, tone: str) -> str:
    return dedent(
        f"""
        ## 카피 템플릿
        1) 숏폼 영상 오프닝
        - "아직도 [기존 불편] 때문에 시간 쓰고 있나요?"
        - "{url}에서 {tone} 방식으로 더 빠르게 해결하세요."

        2) 커뮤니티 글
        - "직접 써보니 [구체적 효익]이 가장 좋았습니다."
        - "사용법/팁 정리: {url}"

        3) 이메일 제목
        - "이번 주, [문제]를 줄이는 가장 쉬운 방법"
        - "{url} 신규 가이드 공개 + 한정 혜택"
        """
    ).strip()


def render_markdown(url: str, audience: str, tone: str, budget: int, start: date, days: int) -> str:
    weekly = build_weekly_plan(url, audience, tone)
    calendar = create_calendar(start, days, url)
    cal_lines = [
        f"- {item['date']} | {item['channel']} | {item['topic']} | CTA: {item['cta']}" for item in calendar
    ]

    sections = [
        f"# {url} 옴니채널 홍보 실행안",
        "> 목적: 채널 제한 없이 브랜드 인지 → 유입 → 전환까지 연결되는 실행 중심 플랜",
        "## 1) 채널별 운영 전략",
        weekly,
        "## 2) 30일 운영 캘린더",
        "\n".join(cal_lines),
        kpi_section(budget),
        sample_copy(url, tone),
        "## 실행 원칙",
        "- 무작위 대량 발송(스팸) 대신 타깃 맞춤형 메시지를 사용하세요.",
        "- 모든 채널 성과를 UTM으로 추적하고 주 1회 개선하세요.",
        "- 댓글/문의 응답 SLA(예: 24시간 이내)를 정해 신뢰를 확보하세요.",
    ]
    return "\n\n".join(sections).strip() + "\n"


def write_csv(rows: list[dict[str, str]], output: Path) -> None:
    with output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "channel", "topic", "content_hint", "cta"])
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="pogobox.shop 홍보용 옴니채널 실행안 생성기")
    parser.add_argument("--url", default="https://pogobox.shop", help="홍보할 홈페이지 URL")
    parser.add_argument("--audience", default="온라인에서 더 효율적인 구매/정보 탐색을 원하는 사용자", help="핵심 타깃")
    parser.add_argument("--tone", default="친근하고 신뢰감 있는", help="카피 톤")
    parser.add_argument("--budget", type=int, default=2000000, help="월 예산(원)")
    parser.add_argument("--days", type=int, default=30, help="캘린더 일수")
    parser.add_argument("--start-date", default=date.today().isoformat(), help="시작일(YYYY-MM-DD)")
    parser.add_argument("--out-md", default="promotion_plan.md", help="마크다운 출력 경로")
    parser.add_argument("--out-csv", default="promotion_calendar.csv", help="CSV 출력 경로")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    start = date.fromisoformat(args.start_date)
    md = render_markdown(args.url, args.audience, args.tone, args.budget, start, args.days)
    calendar = create_calendar(start, args.days, args.url)

    out_md = Path(args.out_md)
    out_csv = Path(args.out_csv)
    out_md.write_text(md, encoding="utf-8")
    write_csv(calendar, out_csv)

    print(f"완료: {out_md} / {out_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
