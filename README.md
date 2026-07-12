# FIC 가격·베뉴 경쟁 분석 리포트

FIC 세빛섬 플로팅아일랜드를 기준으로 서울 유니크베뉴와 4~5성급 호텔 경쟁사를 비교하는 정적 웹 리포트입니다.

## 분석 범위

- 기준 베뉴: FIC 세빛섬 플로팅아일랜드 / Floating Island Convention
- 전체 경쟁군: 서울관광재단 Seoul MICE Alliance Unique Venue Search 기준, 서울의 150석 이상 유니크베뉴 전체
- 보조 출처: 한국관광공사 K-MICE 코리아 유니크베뉴
- 지정 경쟁사: JW 메리어트 호텔 서울 반포, 신라호텔, 코엑스, 인스파이어, 한국의집, 삼청각, 이랜드크루즈, 콘래드호텔, 롯데호텔, 포시즌스 호텔
- 예외 포함: 한국의집과 이랜드크루즈는 서울관광재단 수용인원 기준 150석 미만이지만, 지정 경쟁사이므로 전체 경쟁군 표에도 포함
- 분석 축: 메뉴가격, 홀/공간 사이즈, 수용인원, MICE 행사, 웨딩 행사, 돌잔치·가족연회 적합성

## 무엇이 들어 있나

```
fic-price-report/
├─ build.py                         리포트 생성기 (표준 라이브러리만, 의존성 없음)
├─ templates/report.html.tmpl        리포트 HTML 틀
├─ data/
│  ├─ fic_venue_competitors.json     FIC 경쟁 베뉴 분석 데이터
│  └─ mid.json                       원본 스타터 예시 데이터(보존)
├─ sources.md                        데이터 출처와 확인 한계
└─ .github/workflows/
   ├─ check.yml                      PR 마다 도는 자동 검문
   └─ deploy.yml                     main 에 합쳐지면 GitHub Pages 로 배포
```

## 직접 해보기

```bash
python3 build.py
open _site/index.html
```

## 데이터 해석 원칙

메뉴가격은 공식 웹페이지에 공개된 정가만 숫자로 넣습니다. 현재 다수 호텔·베뉴는 메뉴 단가를 공개하지 않고 별도 문의 방식으로 운영하므로, 추정 가격을 넣지 않고 “공식 공개 단가 확인 필요”로 표시했습니다.

## 배포를 켜는 법

저장소 Settings → Pages → Source 를 GitHub Actions 로 바꾸면, 이후 main 에 변경이 합쳐질 때마다 리포트가 자동으로 다시 배포됩니다.
