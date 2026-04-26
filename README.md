# Pogobox.shop 홍보 프로그램

`promotion_program.py`는 **채널을 가리지 않고** 홈페이지 홍보를 실행할 수 있도록,
아래 결과물을 자동 생성하는 CLI 프로그램입니다.

- 옴니채널 실행안 마크다운 (`promotion_plan.md`)
- 30일 콘텐츠 캘린더 CSV (`promotion_calendar.csv`)

## 사용법

```bash
python3 promotion_program.py \
  --url https://pogobox.shop \
  --audience "가성비와 편리함을 중시하는 온라인 사용자" \
  --tone "간결하고 신뢰감 있는" \
  --budget 3000000 \
  --days 30
```

## 옵션

- `--url`: 홍보 사이트 URL
- `--audience`: 타깃 고객
- `--tone`: 카피 톤
- `--budget`: 월 예산(원)
- `--days`: 운영 캘린더 일수
- `--start-date`: 시작일 (`YYYY-MM-DD`)
- `--out-md`: 마크다운 출력 파일
- `--out-csv`: CSV 출력 파일

## 생성되는 전략 요약

- Instagram / YouTube Shorts / Blog(SEO) / Email / Community / X / Paid Ads
- 주차별 운영 빈도 + KPI + 예산 분배 + 카피 템플릿
- 스팸성 무작위 발송이 아닌 타깃 맞춤 운영 원칙
