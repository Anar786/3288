# Workflow

## 1. Inspect sources

Identify actual sheet and column names before processing. Record filenames, period, row counts, and existing filters. Never overwrite source files. The Calltouch lead table remains the report backbone.

## 2. Normalize keys

Normalize phones by removing punctuation and converting Russian 10/11-digit numbers to `7XXXXXXXXXX`. Extract phones from `Телефон`, then `Виджеты: Телефон`, then `Пользовательские данные`. Keep original text and log missing or invalid phones.

Parse Calltouch date and time into one Moscow datetime. Parse visit dates as dates. Keep IDs as text.

## 3. Apply CPC scope

If the file is not already filtered, select rows where `utm_medium` or `Медиум` is exactly `cpc` after trimming and lowercasing. Record rows before filtering, included CPC rows, excluded rows, and blanks requiring review.

## 4. Build unique leads

Default unique key: normalized phone, then `Уникальный ID клиента`, then `row:<source row number>`. Preserve all Calltouch IDs, first and last lead datetime, types, forms, source, medium, UTM fields, landing pages, cities, and target flags. A grouped lead is unique-target when any source row says `Уникально-целевой лид = да`.

Keep original row-level detail. If one phone appears in several campaigns, surface an attribution warning instead of crediting all revenue to every campaign.

## 5. Match Infoclinica

Index visits by normalized phone. A candidate visit must be on or after the first lead date. The default follow-up window ends at the latest supplied visit date; state that cutoff.

Retain source visit row or ID, patient, date, doctor, medical profile, receipt, primary/repeat marker, both charge fields, and total revenue. Count unique leads with visits separately from visit rows.

## 6. Match iMot

Retrieve calls by client phone in a bounded window. Follow [imot-rules.md](imot-rules.md).

For phone-call leads, prefer the closest call on the same date: up to 90 seconds `точное`, 10 minutes `близкое`, 30 minutes `слабое`, otherwise `вне окна`.

For form/application leads, search from one day before through seven days after. Prefer calls after the application, then the expected department, then the smallest time difference. Label the offset. Preserve call ID and match quality.

## 7. Derive funnel states

Keep facts and derived states in separate columns:

- `Найден в Инфоклинике` and `Дошёл`;
- `Найден в iMot`;
- `Записался по iMot`: `да`, `нет`, `не определено`;
- `Целевой по iMot`;
- source-supported reason for non-booking/non-arrival;
- final status such as `записался и дошёл`, `записался, не найден визит`, `не записался`, or `нет данных iMot`.

Do not infer `не записался` merely because no visit exists.

## 8. Summary metrics

Calculate Calltouch rows, unique leads, unique-target leads, iMot matches, iMot bookings, leads with visits, visit rows, revenue, lead-to-visit conversion, target-lead-to-visit conversion, booking-to-visit conversion, revenue per lead, and revenue per target lead. Show numerator and denominator for every rate.

## 9. Breakdowns

Use supported dimensions: source, `utm_source`, campaign, keyword, form, landing page, city, lead type, and iMot department/operator/topic/service/result/non-booking reason. Show population size with rates and revenue.

## 10. Audit

Reconcile source rows to the CPC filter, grouped rows to unique leads, matched visits and revenue to supporting details, iMot found/not found to the queried population, and booking classes to iMot matches. Flag duplicate visit attribution, missing phones, ambiguous campaign ownership, weak time matches, and coverage cutoffs. Spot-check exact, weak, and conflicting matches against timestamps and transcripts.

