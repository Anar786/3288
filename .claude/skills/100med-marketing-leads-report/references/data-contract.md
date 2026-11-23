# Data contract

Map columns by meaning and preserve original headers.

## Calltouch

Core fields: `ID`, `Вид лида`, `Дата`, `Время`, phone fields, `Название формы`, `Источник`, `Медиум`, `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, landing page, `Город`, tags, `Тип`, `Статус`, `Уникально-целевой лид`, and `Уникальный ID клиента`.

## Infoclinica visit journal

Core fields: `Телефоны`, `Пациент`, `Дата приема`, `Доктор`, `Медпрофиль`, `Начислено пациенту`, `Начислено на организ.`, `№ квитанции`, and `Первичный прием`.

Charges remain numeric. Treat missing charges as zero only during summation; preserve blanks in raw detail.

## iMot

Keep IDs, timestamps, phones, durations, talk/silence time, scores, comments, processing statuses, service links, and all tag arrays: `tags`, `clientTags`, `operatorTags`, `callTags`, `fragmentTags`, `manualTags`, `gptTags`, `integrationTags`, and `dealTags`.

Priority tags: `Отдел`, `Оператор`, `Тип звонка`, `Тема обращения`, `Услуги`/`Услуга`, `Статус лида`, `Статус записи`, `Запись состоялась`, `Результат звонка`, `Причина не записи`, target markers, branch request/booking, objection, transfer, and call group.

Comments can include `Резюме коммуникации`, `Результат звонка`, `Рекомендации для оператора`, and `Резюме записи на приём`.

## Output naming

Use `ct_*` for Calltouch, `ic_*` for Infoclinica, `imot_*` for iMot, `tag_*` for flattened tags, and `audit_*` for warnings. Do not use blank to mean both `нет` and `неизвестно`.

