# Интеграции и доступы

Все ключи хранятся в переменных окружения облачной среды (Claude Code: настройки проекта → Cloud environment → шестерёнка у среды → Environment variables). Значения в скиле не хранятся. Новые переменные видны только в новых сессиях.

## Переменные окружения

| Переменная | Что это |
|---|---|
| `CALLTOUCH_TOKEN` | API-ключ Calltouch (clientApiId) |
| `CALLTOUCH_SITE_ID` | ID сайта Calltouch, только цифры |
| `IMOT_TOKEN` | iMot, кабинет **Люберцы** (main), ~1,49 млн записей с марта 2024 |
| `IMOT_TOKEN_LYTKARINO` | iMot, кабинет **Лыткарино**, ~0,5 млн записей |
| `YANDEX_TOKEN` | OAuth-токен Яндекса (Метрика работает; Директ проверить не удалось) |

## Разрешённые домены (Network access → Allowed domains)

- `api.calltouch.ru`
- `imot.io`, `*.imot.io` (API: `api.imot.io`)
- `api-metrika.yandex.net`
- `api.direct.yandex.com`: нужен для Директа, на старом аккаунте был закрыт прокси. Добавь, если нужны данные Директа по API.
- Галочку «Allow package managers» оставить (нужны pip-пакеты для Excel/PowerPoint).

## Calltouch

База: `https://api.calltouch.ru/calls-service/RestAPI/`

- Звонки: `GET {base}{SITE_ID}/calls-diary/calls?clientApiId=$CALLTOUCH_TOKEN&dateFrom=dd/mm/yyyy&dateTo=dd/mm/yyyy&page=N&limit=1000`. Ответ: `page`, `pageTotal`, `recordsTotal`, `records`. Объём: ~40–57 тыс. звонков в месяц.
- Заявки (формы): `GET {base}requests/?clientApiId=$CALLTOUCH_TOKEN&dateFrom=mm/dd/yyyy&dateTo=mm/dd/yyyy`. Ответ: список. Внимание: формат даты здесь месяц/день.
- Сделки (сюда приходят сделки Битрикс24): `GET {base}{SITE_ID}/orders-diary/orders?clientApiId=$CALLTOUCH_TOKEN&dateFrom=dd/mm/yyyy&dateTo=dd/mm/yyyy`. Поля: `orderId`, `orderStatus`, `createdDate`, `completedDate`, `completedAmount`, `client`, `orderContacts`, `funnel`, `service` и др. Статус «Приём окончен» = пациент дошёл. Ответ ограничен 1000 строк, выгружай по дням.
- Перед большой выгрузкой проверь формат дат на одном дне.

## iMot

- Авторизация: `Authorization: Bearer $IMOT_TOKEN` (или `$IMOT_TOKEN_LYTKARINO`).
- Поиск: `POST https://api.imot.io/search_calls/` с параметрами даты, пагинации, `return_call_info=true`, `split_tag_info=true`, тело `[{"key":"client_phone","values":["7XXXXXXXXXX"]}]`.
- Карточка: `GET https://api.imot.io/call/{id}?split_tag_info=true`.
- Расшифровка: `GET https://api.imot.io/call/{id}/stt`, реплики в `fragments`, сортировать по `begin`.
- Кабинет ≠ физический филиал. Сначала ищи в Люберцах, потом в Лыткарино для ненайденных. Записывай, из какого кабинета запись.
- Подробные правила тегов: [leads-report.md](leads-report.md).

## Яндекс Метрика

- `GET https://api-metrika.yandex.net/management/v1/counters` с заголовком `Authorization: OAuth $YANDEX_TOKEN`.
- Счётчики: `10180198` (100med.ru), `74510380` (yandex.ru/maps).
- Отчёты: `https://api-metrika.yandex.net/stat/v1/data?ids=10180198&metrics=...&dimensions=...&date1=...&date2=...`.

## Яндекс Директ

- `https://api.direct.yandex.com/json/v5/...` с `Authorization: Bearer $YANDEX_TOKEN`. Если домен закрыт, работай по отчёту Ingate (xlsx) и меткам utm в Calltouch.

## Инфоклиника

API нет. Пользователь присылает журнал визитов в Excel (колонки: Телефоны, Пациент, Дата приема, Доктор, Медпрофиль, Начислено пациенту, Начислено на организ., № квитанции, Первичный прием).

## Быстрая проверка подключения (только чтение, значения не выводить)

```bash
for v in CALLTOUCH_TOKEN CALLTOUCH_SITE_ID IMOT_TOKEN IMOT_TOKEN_LYTKARINO YANDEX_TOKEN; do
  [ -n "${!v}" ] && echo "$v: есть" || echo "$v: НЕТ"; done
curl -s -o /dev/null -w "calltouch %{http_code}\n" "https://api.calltouch.ru/calls-service/RestAPI/$CALLTOUCH_SITE_ID/calls-diary/calls?clientApiId=$CALLTOUCH_TOKEN&dateFrom=01/11/2026&dateTo=01/11/2026&page=1&limit=1"
curl -s -o /dev/null -w "metrika %{http_code}\n" -H "Authorization: OAuth $YANDEX_TOKEN" https://api-metrika.yandex.net/management/v1/counters
```

Ответ 403 от прокси означает, что домен не добавлен в Allowed domains; 401 означает неверный токен.
