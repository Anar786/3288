# Graph Report - knowledge  (2026-11-23)

## Corpus Check
- Corpus is ~1,438 words - fits in a single context window. You may not need a graph.

## Summary
- 71 nodes · 101 edges · 7 communities
- Extraction: 71% EXTRACTED · 27% INFERRED · 2% AMBIGUOUS · INFERRED: 27 edges (avg confidence: 0.84)
- Token cost: 85,119 input · 0 output

## Community Hubs (Navigation)
- Филиалы и услуги сети
- Брендбук и медреклама
- Прайс и структура базы
- Аудитория и барьеры
- Контент-план и акции
- Путь пациента к операции
- Эстетика и стоматология

## God Nodes (most connected - your core abstractions)
1. `О компании 100мед` - 20 edges
2. `Контент-план декабрь 2026` - 11 edges
3. `Портрет ЦА 100мед` - 8 edges
4. `Лицензии филиалов` - 7 edges
5. `Действующие акции` - 7 edges
6. `Ограничения медрекламы` - 6 edges
7. `Брендбук 100мед` - 5 edges
8. `Прайс-лист 100мед` - 5 edges
9. `База знаний 100мед` - 4 edges
10. `Пациент перед операцией` - 4 edges

## Surprising Connections (you probably didn't know these)
- `brandbook.md` --references--> `Брендбук 100мед`  [INFERRED]
  README.md → brandbook.md
- `audience.md` --references--> `Портрет ЦА 100мед`  [INFERRED]
  README.md → audience.md
- `content-plan.md` --references--> `Контент-план декабрь 2026`  [INFERRED]
  README.md → content-plan.md
- `Что снимает барьеры` --conceptually_related_to--> `Ограничения медрекламы`  [AMBIGUOUS]
  audience.md → brandbook.md
- `prices.md` --references--> `Прайс-лист 100мед`  [INFERRED]
  README.md → prices.md

## Hyperedges (group relationships)
- **Соблюдение требований медрекламы** — brandbook_ограничения_медрекламы, brandbook_дисклеймер_имеются_противопоказания, brandbook_дисклеймер_информационный_характер, brandbook_фз_о_рекламе_ст_24, content_plan_дисклеймер_в_каждом_материале [INFERRED 0.85]
- **Путь пациента перед операцией** — audience_пациент_перед_операцией, company_профессора_и_д_м_н_в_штате, company_полный_цикл_консультация_диагностика_операция, prices_бесплатная_консультация_хирурга [INFERRED 0.75]
- **Филиалы в Тверской области для малых городов** — audience_жители_малых_городов_тверской_области, company_клиника_в_кашине, company_клиника_в_кесовой_горе [INFERRED 0.85]

## Communities (7 total, 0 thin omitted)

### Community 0 - "Филиалы и услуги сети"
Cohesion: 0.17
Nodes (16): Жители малых городов Тверской области, Анализы, Выезд врача на дом и телемедицина, Диагностика, Единый телефон и ЛК, Клиника в Кашине, Клиника в Кесовой Горе, Клиника в Лыткарино (+8 more)

### Community 1 - "Брендбук и медреклама"
Cohesion: 0.15
Nodes (11): WCAG AA, Брендбук 100мед, Дисклеймер Имеются противопоказания, Дисклеймер информационный характер, Запрещённые рекламные формулировки, Позиционирование Стопроцентная медицина, Студия Текарт, ФЗ О рекламе ст. 24 (+3 more)

### Community 2 - "Прайс и структура базы"
Cohesion: 0.18
Nodes (11): Неделя Зима и сосуды, Анализы прайс, Прайс-лист 100мед, Приём врачей, Флеболог к.м.н., Эндоскопические операции, audience.md, brandbook.md (+3 more)

### Community 3 - "Аудитория и барьеры"
Cohesion: 0.24
Nodes (10): Общие барьеры пациентов, Портрет ЦА 100мед, Семья из Подмосковья, Срочная диагностика, Что снимает барьеры, Яндекс.Метрика и Calltouch, Клиника в Люберцах, МРТ 24/7 в Люберцах (+2 more)

### Community 4 - "Контент-план и акции"
Cohesion: 0.24
Nodes (10): Каналы коммуникации, Контент-план декабрь 2026, Неделя Праздничный стол и ЖКТ, Неделя Чекап перед Новым годом, Ритм публикаций, Рубрика Акции месяца, Рубрика Миф или факт, Действующие акции (+2 more)

### Community 5 - "Путь пациента к операции"
Cohesion: 0.33
Nodes (6): Бесплатная консультация хирурга (ценность), Пациент перед операцией, Полный цикл консультация-диагностика-операция, Профессора и д.м.н. в штате, Рубрика Врач рядом, Бесплатная консультация хирурга

### Community 6 - "Эстетика и стоматология"
Cohesion: 0.67
Nodes (3): Эстетика, Пластическая хирургия, косметология, стоматология, Имплантация NorisMedical и циркониевая коронка

## Ambiguous Edges - Review These
- `Что снимает барьеры` → `Ограничения медрекламы`  [AMBIGUOUS]
  audience.md · relation: conceptually_related_to
- `Клиника в Кашине` → `Лицензии филиалов`  [AMBIGUOUS]
  company.md · relation: references

## Knowledge Gaps
- **14 isolated node(s):** `Яндекс.Метрика и Calltouch`, `ФЗ О рекламе ст. 24`, `Запрещённые рекламные формулировки`, `WCAG AA`, `Студия Текарт` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 14 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `О компании 100мед` connect `Филиалы и услуги сети` to `Брендбук и медреклама`, `Аудитория и барьеры`, `Контент-план и акции`, `Путь пациента к операции`, `Эстетика и стоматология`?**
  _High betweenness centrality (0.412) - this node is a cross-community bridge._
- **What connects `Яндекс.Метрика и Calltouch`, `ФЗ О рекламе ст. 24`, `Запрещённые рекламные формулировки` to the rest of the system?**
  _14 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Why does `Контент-план декабрь 2026` connect `Контент-план и акции` to `Брендбук и медреклама`, `Прайс и структура базы`, `Аудитория и барьеры`, `Путь пациента к операции`?**
  _High betweenness centrality (0.281) - this node is a cross-community bridge._
- **Why does `Действующие акции` connect `Контент-план и акции` to `Филиалы и услуги сети`, `Прайс и структура базы`, `Путь пациента к операции`, `Эстетика и стоматология`?**
  _High betweenness centrality (0.156) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Что снимает барьеры` and `Ограничения медрекламы`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Клиника в Кашине` and `Лицензии филиалов`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._