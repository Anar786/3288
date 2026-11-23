# iMot rules

Use the connected iMot MCP source when available and discover its real schemas. If direct API use is authorized, read the Bearer token from a secret or environment variable.

## Accounts

`main` is the Люберцы technical cabinet; `lytkarino` is the Лыткарино technical cabinet. Cabinet and physical branch are different dimensions. For a general report search main first, then Lytkarino for unmatched leads or when the campaign/form scope requires it. Record the source cabinet.

## API

Search calls with `POST https://api.imot.io/search_calls/` using date, pagination, `return_call_info=true`, `split_tag_info=true`, and body `[{"key":"client_phone","values":["7XXXXXXXXXX"]}]`.

Get the card with `GET https://api.imot.io/call/{id}?split_tag_info=true`. Get the transcript with `GET https://api.imot.io/call/{id}/stt`; dialogue is in `fragments`, ordered by `begin`.

## Booking

For main/Lyubertsy, `Запись состоялась = Да` is a strong signal. For Lytkarino, also inspect `Запись на прием`. Preserve conflicts.

Normalize to `записался`, `не записался`, or `не определено`. Inspect the value, not merely the presence of a tag name. Do not infer booking from an information request.

## Target status and transcripts

Prefer explicit `Целевой` / `Не целевой`; otherwise use `Тип звонка` or `Целевой/не целевой`. Preserve original and normalized values.

Retrieve transcripts for conflicting tags, weak matches, high-value leads without visits, reasons for non-booking, or requested qualitative analysis. State how many transcripts were reviewed.

