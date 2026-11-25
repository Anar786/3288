# Проект 100mednew на claude.ai

Файлы для ручного создания проекта в разделе Projects на claude.ai.

## Как создать

1. Откройте claude.ai → **Projects** → **Create project**.
2. Название: `100mednew`. Описание: «Мультиагентная команда 100мед: SMM, контент, дизайн, разработка, видео, отчёты по лидам».
3. **Project instructions** → вставьте целиком текст из [`project-instructions.md`](project-instructions.md).
4. **Project knowledge** → загрузите файлы из папки [`knowledge/`](knowledge/):
   - `marketing-leads-report.md` — методика отчёта по CPC-лидам (Calltouch + Инфоклиника + iMot).
5. По мере появления добавьте туда же: `brandbook.md`, `prices.md`, `audience.md`, `content-plan.md` и сводки решений.

## Важно

- API-ключи (Calltouch, iMot, Метрика) в проект **не загружаются**. Проект на claude.ai не ходит в API сам — данные прикладываются выгрузками или через подключённые коннекторы.
- Автоматический сбор данных по API остаётся в Claude Code в среде «100MED+calltouch+Imot».
