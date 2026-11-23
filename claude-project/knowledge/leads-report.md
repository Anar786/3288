# Отчёт по CPC-лидам: Calltouch + Инфоклиника + iMot

Перенесено из скила `100med-marketing-leads-report` без изменений по смыслу. Calltouch = источник лида, Инфоклиника = визит и начисления, iMot = разговор и запись. Если журнала Инфоклиники нет, «дошёл» можно брать из сделок Битрикс24 в Calltouch (статус «Приём окончен»), см. definitions.md.

## Общие правила


Create a traceable lead-level report in which Calltouch is the marketing source, Infoclinica proves visits and revenue, and iMot explains calls and booking outcomes.

### Before work

Confirm the reporting period and locate:

- Calltouch lead journal for the period;
- Infoclinica visit journals covering the lead period and the allowed follow-up window;
- access to the connected iMot source or an authorized API key.

Do not place API keys in workbooks, scripts, logs, the skill, or the final response.

Read раздел «Порядок работы» ниже before joining data. Read раздел «Колонки источников» ниже when mapping columns or validating an unfamiliar export. Read раздел «Правила iMot» ниже when retrieving or interpreting iMot data.

### Required outcome

Preserve the original Calltouch rows and add clearly prefixed fields from Infoclinica and iMot. Produce:

- a compact summary of the funnel and revenue;
- one auditable lead-detail table;
- breakdowns by source, campaign, form, landing page, city, and other requested marketing dimensions;
- a separate view of leads not found in visits and/or iMot;
- an audit section with missing phones, duplicate attribution risks, weak iMot matches, and coverage totals.

Use Russian user-facing labels. Keep technical IDs for traceability.

### Non-negotiable definitions

- Normalize Russian phones to 11 digits beginning with `7`.
- Keep every Calltouch row. For unique-lead reporting, default to normalized phone; if phone is absent, use Calltouch client ID, then an explicit row key.
- A shared family phone can represent several patients. Never merge away patient-level evidence; preserve all matched names and visit rows.
- Count a lead as `дошёл` only when an Infoclinica visit on or after the lead date is matched by phone.
- Revenue is `Начислено пациенту + Начислено на организ.` across matched visits, unless the user specifies another definition.
- `Записался` is a booking signal from iMot or another booking source. It is not the same as `дошёл`.
- Treat iMot tags and summaries as automatic analysis. Use transcripts to resolve conflicts or high-impact ambiguous cases.
- Distinguish Calltouch rows, unique leads, calls, patients, visits, and bookings. Never present one as another.

### CPC scope

If the input is not already filtered, include rows where `utm_medium` or the Calltouch medium equals `cpc`, case-insensitively. Preserve the original source and medium values and report excluded row counts. Do not silently classify other paid channels as CPC.

### Privacy

The sources contain personal and medical data. Minimize exposure, keep files in the authorized workspace, and avoid copying full transcripts into summary sheets unless requested. Prefer call IDs and concise summaries in reader-facing outputs.

## Порядок работы


### 1. Inspect sources

Identify actual sheet and column names before processing. Record filenames, period, row counts, and existing filters. Never overwrite source files. The Calltouch lead table remains the report backbone.

### 2. Normalize keys

Normalize phones by removing punctuation and converting Russian 10/11-digit numbers to `7XXXXXXXXXX`. Extract phones from `Телефон`, then `Виджеты: Телефон`, then `Пользовательские данные`. Keep original text and log missing or invalid phones.

Parse Calltouch date and time into one Moscow datetime. Parse visit dates as dates. Keep IDs as text.

### 3. Apply CPC scope

If the file is not already filtered, select rows where `utm_medium` or `Медиум` is exactly `cpc` after trimming and lowercasing. Record rows before filtering, included CPC rows, excluded rows, and blanks requiring review.

### 4. Build unique leads

Default unique key: normalized phone, then `Уникальный ID клиента`, then `row:<source row number>`. Preserve all Calltouch IDs, first and last lead datetime, types, forms, source, medium, UTM fields, landing pages, cities, and target flags. A grouped lead is unique-target when any source row says `Уникально-целевой лид = да`.

Keep original row-level detail. If one phone appears in several campaigns, surface an attribution warning instead of crediting all revenue to every campaign.

### 5. Match Infoclinica

Index visits by normalized phone. A candidate visit must be on or after the first lead date. The default follow-up window ends at the latest supplied visit date; state that cutoff.

Retain source visit row or ID, patient, date, doctor, medical profile, receipt, primary/repeat marker, both charge fields, and total revenue. Count unique leads with visits separately from visit rows.

### 6. Match iMot

Retrieve calls by client phone in a bounded window. Follow раздел «Правила iMot».

For phone-call leads, prefer the closest call on the same date: up to 90 seconds `точное`, 10 minutes `близкое`, 30 minutes `слабое`, otherwise `вне окна`.

For form/application leads, search from one day before through seven days after. Prefer calls after the application, then the expected department, then the smallest time difference. Label the offset. Preserve call ID and match quality.

### 7. Derive funnel states

Keep facts and derived states in separate columns:

- `Найден в Инфоклинике` and `Дошёл`;
- `Найден в iMot`;
- `Записался по iMot`: `да`, `нет`, `не определено`;
- `Целевой по iMot`;
- source-supported reason for non-booking/non-arrival;
- final status such as `записался и дошёл`, `записался, не найден визит`, `не записался`, or `нет данных iMot`.

Do not infer `не записался` merely because no visit exists.

### 8. Summary metrics

Calculate Calltouch rows, unique leads, unique-target leads, iMot matches, iMot bookings, leads with visits, visit rows, revenue, lead-to-visit conversion, target-lead-to-visit conversion, booking-to-visit conversion, revenue per lead, and revenue per target lead. Show numerator and denominator for every rate.

### 9. Breakdowns

Use supported dimensions: source, `utm_source`, campaign, keyword, form, landing page, city, lead type, and iMot department/operator/topic/service/result/non-booking reason. Show population size with rates and revenue.

### 10. Audit

Reconcile source rows to the CPC filter, grouped rows to unique leads, matched visits and revenue to supporting details, iMot found/not found to the queried population, and booking classes to iMot matches. Flag duplicate visit attribution, missing phones, ambiguous campaign ownership, weak time matches, and coverage cutoffs. Spot-check exact, weak, and conflicting matches against timestamps and transcripts.

## Колонки источников


Map columns by meaning and preserve original headers.

### Calltouch

Core fields: `ID`, `Вид лида`, `Дата`, `Время`, phone fields, `Название формы`, `Источник`, `Медиум`, `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, landing page, `Город`, tags, `Тип`, `Статус`, `Уникально-целевой лид`, and `Уникальный ID клиента`.

### Infoclinica visit journal

Core fields: `Телефоны`, `Пациент`, `Дата приема`, `Доктор`, `Медпрофиль`, `Начислено пациенту`, `Начислено на организ.`, `№ квитанции`, and `Первичный прием`.

Charges remain numeric. Treat missing charges as zero only during summation; preserve blanks in raw detail.

### iMot

Keep IDs, timestamps, phones, durations, talk/silence time, scores, comments, processing statuses, service links, and all tag arrays: `tags`, `clientTags`, `operatorTags`, `callTags`, `fragmentTags`, `manualTags`, `gptTags`, `integrationTags`, and `dealTags`.

Priority tags: `Отдел`, `Оператор`, `Тип звонка`, `Тема обращения`, `Услуги`/`Услуга`, `Статус лида`, `Статус записи`, `Запись состоялась`, `Результат звонка`, `Причина не записи`, target markers, branch request/booking, objection, transfer, and call group.

Comments can include `Резюме коммуникации`, `Результат звонка`, `Рекомендации для оператора`, and `Резюме записи на приём`.

### Output naming

Use `ct_*` for Calltouch, `ic_*` for Infoclinica, `imot_*` for iMot, `tag_*` for flattened tags, and `audit_*` for warnings. Do not use blank to mean both `нет` and `неизвестно`.

## Правила iMot


Use the connected iMot MCP source when available and discover its real schemas. If direct API use is authorized, read the Bearer token from a secret or environment variable.

### Accounts

`main` is the Люберцы technical cabinet; `lytkarino` is the Лыткарино technical cabinet. Cabinet and physical branch are different dimensions. For a general report search main first, then Lytkarino for unmatched leads or when the campaign/form scope requires it. Record the source cabinet.

### API

Search calls with `POST https://api.imot.io/search_calls/` using date, pagination, `return_call_info=true`, `split_tag_info=true`, and body `[{"key":"client_phone","values":["7XXXXXXXXXX"]}]`.

Get the card with `GET https://api.imot.io/call/{id}?split_tag_info=true`. Get the transcript with `GET https://api.imot.io/call/{id}/stt`; dialogue is in `fragments`, ordered by `begin`.

### Booking

For main/Lyubertsy, `Запись состоялась = Да` is a strong signal. For Lytkarino, also inspect `Запись на прием`. Preserve conflicts.

Normalize to `записался`, `не записался`, or `не определено`. Inspect the value, not merely the presence of a tag name. Do not infer booking from an information request.

### Target status and transcripts

Prefer explicit `Целевой` / `Не целевой`; otherwise use `Тип звонка` or `Целевой/не целевой`. Preserve original and normalized values.

Retrieve transcripts for conflicting tags, weak matches, high-value leads without visits, reasons for non-booking, or requested qualitative analysis. State how many transcripts were reviewed.

## Инструкция для маркетинга (как ставить задачу)


### Что делает отчёт

Отчёт показывает путь маркетингового лида: **Calltouch → разговор и запись в iMot → визит и начисления в Инфоклинике**.

По каждому лиду можно увидеть источник и кампанию, записался ли клиент, дошёл ли он до клиники, сколько было визитов и какую сумму начислили.

### Что нужно подготовить

1. Журнал лидов Calltouch за нужный период.
2. Журнал визитов Инфоклиники за период лидов и последующий период наблюдения. Для лидов за месяц желательно выгрузить визиты минимум ещё за следующий месяц.
3. Указать, нужен весь маркетинг или только CPC.
4. Указать кабинеты iMot: Люберцы, Лыткарино или оба.

Не меняйте названия колонок и не удаляйте строки без телефона: они попадут в список контроля.

### Как использовать скилл

Скил уже установлен в Claude: достаточно описать задачу.

Пример запроса:

```text
Сделай отчёт по скилу 100med-marketing (отчёт по CPC-лидам).
Сделай отчёт по CPC-лидам за сентябрь 2026 года.
Calltouch: <путь к файлу>.
Инфоклиника: <путь к файлу или файлам>.
Проверь оба кабинета iMot.
Нужны сводка, детализация по каждому лиду, конверсия в визит, выручка, разбивка по source/campaign и список лидов, не найденных ни в визитах, ни в iMot.
```

API-ключи нельзя вставлять в запрос, Excel или инструкцию. Доступ к iMot подключается заранее или передаётся через защищённые настройки.

### Основные определения

- **Строка Calltouch** — отдельное обращение в журнале лидов.
- **Уникальный лид** — по умолчанию уникальный нормализованный телефон. Если телефона нет, используется ID клиента Calltouch.
- **Уникально-целевой лид** — хотя бы одна строка лида имеет отметку `Уникально-целевой лид = да`.
- **Записался** — запись подтверждается iMot или другим источником записи.
- **Дошёл** — в Инфоклинике найден визит после даты лида.
- **Выручка** — `Начислено пациенту + Начислено на организ.` по найденным визитам.

Запись и визит — разные этапы. Отсутствие визита не означает, что пациент не записывался: дата приёма может быть позже окончания выгрузки.

### Что должно быть в готовом файле

#### Сводка

- строки Calltouch;
- уникальные и уникально-целевые лиды;
- найденные звонки iMot;
- записавшиеся по iMot;
- лиды с визитом и количество визитов;
- начисления;
- конверсии лид → визит, целевой лид → визит и запись → визит;
- начисления на один лид.

#### Детализация

Для каждого лида сохраняются ID и дата Calltouch, телефон, форма, источник, medium, UTM-кампания, ключевое слово, посадочная страница, город, найденные пациенты и визиты, врачи, услуги, начисления, ID звонка iMot, качество сопоставления, оператор, отдел, целевой статус, тема, результат, причина незаписи, резюме и итог воронки.

#### Списки контроля

- нет корректного телефона;
- не найдено в Инфоклинике;
- не найдено в iMot;
- не найдено ни в одном источнике;
- слабое совпадение звонка по времени;
- один телефон связан с несколькими кампаниями или пациентами;
- запись есть, а визита пока нет.

### Как читать отчёт

Сравнивайте источники и кампании одновременно по количеству лидов, конверсии и начислениям. Высокая конверсия на нескольких лидах не доказывает эффективность кампании.

Для лидов без визита смотрите резюме и причину незаписи iMot. Автоматические теги могут ошибаться, поэтому спорные и финансово значимые случаи проверяются по транскрибации.

### Проверка перед использованием

1. Период Calltouch указан верно.
2. Журнал визитов покрывает достаточный последующий период.
3. Число строк Calltouch совпадает с исходным CPC-фильтром.
4. У каждой конверсии понятны числитель и знаменатель.
5. Визиты и начисления можно проследить до строк Инфоклиники.
6. Для совпадений iMot сохранены ID звонка и качество сопоставления.
7. API-ключи отсутствуют в файле.

### Персональные данные

Отчёт содержит телефоны, ФИО и сведения о посещениях клиники. Его нельзя размещать в общедоступных папках или загружать в сторонние сервисы без разрешённого режима обработки. Для презентаций и внешнего анализа используйте обезличенную копию.
