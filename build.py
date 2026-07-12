#!/usr/bin/env python3
"""FIC 가격·베뉴 경쟁 분석 리포트 빌더.

data/fic_venue_competitors.json 의 공식 출처 기반 경쟁 베뉴 데이터를 읽어
배포용 정적 페이지(_site/index.html)를 만든다.

의존성 없음(파이썬 표준 라이브러리만). 그래서 누구 컴퓨터에서도, GitHub
Actions 에서도 pip 설치 없이 그대로 돈다.
"""
import html
import json
import pathlib
import string

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "data" / "fic_venue_competitors.json"
OUT = ROOT / "_site"


def fmt(value, suffix="") -> str:
    if value is None or value == "":
        return "확인 필요"
    if isinstance(value, int):
        return f"{value:,}{suffix}"
    return f"{html.escape(str(value))}{suffix}"


def esc(value) -> str:
    return html.escape(str(value or ""))


def source_link(row: dict) -> str:
    url = row.get("source_url")
    label = row.get("source") or row.get("evidence") or "출처"
    if not url:
        return esc(label)
    return f"<a href='{esc(url)}' target='_blank' rel='noreferrer'>출처</a>"


def render_named_rows(items: list[dict]) -> str:
    rows = []
    for item in items:
        rows.append(
            "<tr>"
            f"<td><strong>{esc(item['name'])}</strong><br><span class='muted'>{esc(item['role'])}</span></td>"
            f"<td class='num'>{fmt(item.get('capacity'), '명')}</td>"
            f"<td class='num'>{fmt(item.get('area_m2'), 'm²')}</td>"
            f"<td>{esc(item.get('menu_price'))}</td>"
            f"<td>{esc(item.get('mice'))}</td>"
            f"<td>{esc(item.get('wedding'))}</td>"
            f"<td>{esc(item.get('dol'))}</td>"
            f"<td>{esc(item.get('evidence'))}<br>{source_link(item)}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def render_unique_rows(items: list[dict]) -> str:
    rows = []
    for item in sorted(items, key=lambda x: (-x.get("capacity", 0), x["name"])):
        focus = "기준 베뉴" if item["name"] == "Floating Island Convention" else "경쟁사"
        rows.append(
            "<tr>"
            f"<td>{esc(focus)}</td>"
            f"<td><strong>{esc(item['name'])}</strong><br><span class='muted'>{esc(item.get('type'))}</span></td>"
            f"<td class='num'>{fmt(item.get('capacity'), '명')}</td>"
            f"<td class='num'>{fmt(item.get('area_m2'), 'm²')}</td>"
            f"<td>{esc(item.get('source'))}<br>{source_link(item)}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def render_event_analysis(data: dict) -> str:
    items = data["named_competitors"]
    fic = items[0]
    mice_direct = [x for x in items if any(k in x["mice"] for k in ["MICE", "컨벤션", "기업", "리셉션"])]
    wedding_direct = [x for x in items if "웨딩" in x["wedding"] or "혼례" in x["wedding"]]
    dol_direct = [x for x in items if "돌잔치" in x["dol"] or "가족연회" in x["dol"]]
    return f"""
    <section class='cards'>
      <article><h3>MICE 행사</h3><p>판단 기준은 수용인원, 접근성, 공식 MICE 운영 가능성, 유니크 경험성이다. FIC는 {fmt(fic['capacity'], '명')}·{fmt(fic['area_m2'], 'm²')} 기준으로 코엑스·인스파이어·대형 컨벤션과 비교해야 한다. 단, 숙박 연계는 5성급 호텔 대비 보완 과제다.</p><p class='muted'>직접 비교군: {', '.join(esc(x['name']) for x in mice_direct[:7])}</p></article>
      <article><h3>웨딩 행사</h3><p>판단 기준은 메뉴/식음, 홀 분위기, 예식 동선, 사진·상징성이다. FIC는 호텔식 안정성보다 한강 수상 베뉴의 차별성으로 포지셔닝하는 것이 맞다. 호텔 웨딩은 JW 메리어트·신라·롯데·포시즌스·콘래드가 핵심 비교군이다.</p><p class='muted'>직접 비교군: {', '.join(esc(x['name']) for x in wedding_direct[:7])}</p></article>
      <article><h3>돌잔치·가족연회</h3><p>판단 기준은 50~150명대 룸 구성, 식음 단가, 주차, 가족 동선이다. 사용자가 요청한 150석 이상 기준에서는 FIC와 호텔/전통 베뉴가 경쟁하지만, 실제 돌잔치는 소형 룸 상품과 메뉴 가격 확인이 추가로 필요하다.</p><p class='muted'>직접 비교군: {', '.join(esc(x['name']) for x in dol_direct[:7])}</p></article>
    </section>
    """


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    template = string.Template((ROOT / "templates" / "report.html.tmpl").read_text(encoding="utf-8"))
    html_text = template.substitute(
        title=esc(data["project_name"]),
        basis=esc(data["updated_basis"]),
        notes="".join(f"<li>{esc(note)}</li>" for note in data["notes"]),
        named_rows=render_named_rows(data["named_competitors"]),
        unique_rows=render_unique_rows(data["seoul_unique_venues_150_plus"]),
        event_analysis=render_event_analysis(data),
    )
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(html_text, encoding="utf-8")
    print(f"[build] _site/index.html 생성 완료 ({len(html_text.encode('utf-8')):,} bytes)")


if __name__ == "__main__":
    main()
