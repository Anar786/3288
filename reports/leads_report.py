#!/usr/bin/env python3
"""Отчёт по лидам 100мед: Calltouch (звонки и заявки) + Яндекс Метрика (визиты).

Запуск:  python3 reports/leads_report.py 2026-11-16 2026-11-22
Нужны переменные окружения CALLTOUCH_SITE_ID, CALLTOUCH_TOKEN; доступ к Метрике
даёт прокси среды. Пишет агрегаты (без телефонов и ФИО) в reports/data/*.json.

Лид = уникально-целевой звонок + уникально-целевая заявка (флаги Calltouch
uniqTargetCall / uniqTargetRequest). Сравнение — с периодом той же длины до него.
"""
import collections
import datetime as dt
import json
import os
import sys
import urllib.parse
import urllib.request

CT = "https://api.calltouch.ru/calls-service/RestAPI"
METRIKA = "https://api-metrika.yandex.net/stat/v1/data"
COUNTER = 10180198  # 100med.ru
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

CHANNELS = {
    "geo": "Карты (Яндекс, Google, 2ГИС)",
    "cpc": "Платная реклама", "cpa": "Платная реклама",
    "organic": "SEO",
    "agregatory": "Агрегаторы и каталоги", "referral": "Агрегаторы и каталоги",
    "poligrafiya": "Офлайн-реклама", "outdoor": "Офлайн-реклама",
    "smm": "Соцсети",
}
BRANCHES = [  # фрагмент в source / url -> филиал
    (("lyuber", "luber", "люберц"), "Люберцы"),
    (("lytkarino", "litkarino", "лыткарин", "лыдкарин"), "Лыткарино"),
    (("ramensk", "раменск"), "Раменское"),
    (("uhtomsk", "ukhtomsk"), "Ухтомская"),
    (("kashin", "кашин"), "Кашин"),
    (("kesova", "кесов"), "Кесова Гора"),
]


def get(url):
    with urllib.request.urlopen(url, timeout=120) as r:
        return json.load(r)


def channel(medium):
    return CHANNELS.get(medium or "", "Прямые звонки и без источника")


def branch(*texts):
    t = " ".join(x or "" for x in texts).lower()
    for keys, name in BRANCHES:
        if any(k in t for k in keys):
            return name
    return "Не определён (общий номер)"


def calls(d1, d2):
    site, tok = os.environ["CALLTOUCH_SITE_ID"], os.environ["CALLTOUCH_TOKEN"]
    out, page = [], 1
    while True:
        q = urllib.parse.urlencode(dict(clientApiId=tok, dateFrom=d1.strftime("%d/%m/%Y"),
                                        dateTo=d2.strftime("%d/%m/%Y"), page=page, limit=1000))
        d = get(f"{CT}/{site}/calls-diary/calls?{q}")
        out += d["records"]
        if page >= d["pageTotal"]:
            return out
        page += 1


def requests(d1, d2):
    q = urllib.parse.urlencode(dict(clientApiId=os.environ["CALLTOUCH_TOKEN"],
                                    dateFrom=d1.strftime("%m/%d/%Y"), dateTo=d2.strftime("%m/%d/%Y")))
    return get(f"{CT}/requests/?{q}")


def visits(d1, d2):
    q = urllib.parse.urlencode(dict(ids=COUNTER, metrics="ym:s:visits", dimensions="ym:s:lastTrafficSource",
                                    date1=d1.isoformat(), date2=d2.isoformat(), lang="ru"))
    return {r["dimensions"][0]["name"]: int(r["metrics"][0]) for r in get(f"{METRIKA}?{q}")["data"]}


def leads(d1, d2):
    """Список лидов: dict(date, kind, source, medium, channel, branch) + общие счётчики."""
    rows, c = [], calls(d1, d2)
    for r in c:
        if r["uniqTargetCall"]:
            rows.append(dict(date=dt.datetime.strptime(r["date"][:10], "%d/%m/%Y").date().isoformat(),
                             kind="call", source=r["source"], medium=r["medium"], channel=channel(r["medium"]),
                             branch=branch(r["source"], r["url"], r.get("subPoolName"))))
    for r in requests(d1, d2):
        if r.get("uniqTargetRequest"):
            s = r.get("session") or {}
            rows.append(dict(date=dt.datetime.strptime(r["dateStr"][:10], "%d/%m/%Y").date().isoformat(),
                             kind="request", source=s.get("source") or "(нет данных)", medium=s.get("medium"),
                             channel=channel(s.get("medium")), branch=branch(s.get("source"), s.get("url"))))
    stats = dict(calls_total=len(c), missed=sum(1 for r in c if not r["successful"]))
    return rows, stats


def write(name, rows, meta):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, f"{name}.json"), "w", encoding="utf-8") as f:
        json.dump(dict(rows=rows, meta=meta), f, ensure_ascii=False, indent=1)


def main(a, b):
    d1, d2 = dt.date.fromisoformat(a), dt.date.fromisoformat(b)
    n = (d2 - d1).days + 1
    p1, p2 = d1 - dt.timedelta(days=n), d1 - dt.timedelta(days=1)
    cur, cs = leads(d1, d2)
    prev, ps = leads(p1, p2)
    vc, vp = visits(d1, d2), visits(p1, p2)

    code = open(os.path.abspath(__file__), encoding="utf-8").read()
    meta = [dict(label="leads_report.py", value=code, type="code", lang="python"),
            dict(label="Период", value=f"{d1:%d.%m.%Y}–{d2:%d.%m.%Y}, сравнение с {p1:%d.%m.%Y}–{p2:%d.%m.%Y}"),
            dict(label="Источник", value="Calltouch API (звонки, заявки), Яндекс Метрика (счётчик 100med.ru)"),
            dict(label="Собрано", value=dt.datetime.now().strftime("%d.%m.%Y %H:%M"))]

    def cnt(rows, key=None, kind=None):
        return collections.Counter((r[key] if key else None) for r in rows if kind in (None, r["kind"]))

    write("summary", [
        dict(period="Текущий", start=d1.isoformat(), end=d2.isoformat(), leads=len(cur),
             calls=len([r for r in cur if r["kind"] == "call"]), requests=len([r for r in cur if r["kind"] == "request"]),
             calls_total=cs["calls_total"], missed=cs["missed"], visits=sum(vc.values())),
        dict(period="Предыдущий", start=p1.isoformat(), end=p2.isoformat(), leads=len(prev),
             calls=len([r for r in prev if r["kind"] == "call"]), requests=len([r for r in prev if r["kind"] == "request"]),
             calls_total=ps["calls_total"], missed=ps["missed"], visits=sum(vp.values())),
    ], meta)

    days = [(d1 + dt.timedelta(days=i)).isoformat() for i in range(n)]
    cc, cr = cnt(cur, "date", "call"), cnt(cur, "date", "request")
    write("daily", [dict(date=d, calls=cc[d], requests=cr[d], leads=cc[d] + cr[d]) for d in days], meta)

    def table(key):
        a, b = cnt(cur, key), cnt(prev, key)
        ac, ar = cnt(cur, key, "call"), cnt(cur, key, "request")
        return sorted((dict(name=k, leads=a[k], calls=ac[k], requests=ar[k], leads_prev=b[k])
                       for k in set(a) | set(b)), key=lambda r: (-r["leads"], -r["leads_prev"]))

    write("channels", [dict(channel=r.pop("name"), **r) for r in table("channel")], meta)
    write("branches", [dict(branch=r.pop("name"), **r) for r in table("branch")], meta)

    src = collections.defaultdict(lambda: dict(calls=0, requests=0))
    for r in cur:
        k = (r["source"], r["medium"] or "(none)", r["channel"], r["branch"])
        src[k]["calls" if r["kind"] == "call" else "requests"] += 1
    write("sources", sorted((dict(source=k[0], medium=k[1], channel=k[2], branch=k[3], leads=v["calls"] + v["requests"], **v)
                             for k, v in src.items()), key=lambda r: -r["leads"]), meta)

    write("visits", sorted((dict(traffic=k, visits=vc.get(k, 0), visits_prev=vp.get(k, 0)) for k in set(vc) | set(vp)),
                           key=lambda r: -r["visits"]), meta)
    print(f"leads {len(cur)} (prev {len(prev)}), visits {sum(vc.values())}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
