# Отчёты по лидам

- `leads_report.py` — выгрузка из Calltouch (звонки, заявки) и Яндекс Метрики (визиты) за период
  с сравнением с предыдущим периодом той же длины. Пишет только агрегаты (без телефонов и ФИО) в `data/`.
- `dashboard/index.html` — страница дашборда «Лиды 100мед» (Artifact типа Data).
- Дашборд: https://claude.ai/artifact/FDyD2BksdjjSBtpqk6W2o1

Запуск (в среде 100MED+calltouch+Imot):

    python3 reports/leads_report.py 2026-11-16 2026-11-22

Лид = уникально-целевой звонок + уникально-целевая заявка (флаги Calltouch).
