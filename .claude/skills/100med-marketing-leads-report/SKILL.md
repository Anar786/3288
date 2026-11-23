---
name: 100med-marketing-leads-report
description: Build and audit 100med marketing lead reports by joining Calltouch leads, Infoclinica visits and payments, and iMot call analytics. Use for CPC funnel, source/campaign effectiveness, booking, arrival, revenue, unmatched leads, and lead-level Excel reports. Do not use for general call-center performance without marketing leads.
---

# 100med Marketing Leads Report

Create a traceable lead-level report in which Calltouch is the marketing source, Infoclinica proves visits and revenue, and iMot explains calls and booking outcomes.

## Before work

Confirm the reporting period and locate:

- Calltouch lead journal for the period;
- Infoclinica visit journals covering the lead period and the allowed follow-up window;
- access to the connected iMot source or an authorized API key.

Do not place API keys in workbooks, scripts, logs, the skill, or the final response.

Read [references/workflow.md](references/workflow.md) before joining data. Read [references/data-contract.md](references/data-contract.md) when mapping columns or validating an unfamiliar export. Read [references/imot-rules.md](references/imot-rules.md) when retrieving or interpreting iMot data.

## Required outcome

Preserve the original Calltouch rows and add clearly prefixed fields from Infoclinica and iMot. Produce:

- a compact summary of the funnel and revenue;
- one auditable lead-detail table;
- breakdowns by source, campaign, form, landing page, city, and other requested marketing dimensions;
- a separate view of leads not found in visits and/or iMot;
- an audit section with missing phones, duplicate attribution risks, weak iMot matches, and coverage totals.

Use Russian user-facing labels. Keep technical IDs for traceability.

## Non-negotiable definitions

- Normalize Russian phones to 11 digits beginning with `7`.
- Keep every Calltouch row. For unique-lead reporting, default to normalized phone; if phone is absent, use Calltouch client ID, then an explicit row key.
- A shared family phone can represent several patients. Never merge away patient-level evidence; preserve all matched names and visit rows.
- Count a lead as `дошёл` only when an Infoclinica visit on or after the lead date is matched by phone.
- Revenue is `Начислено пациенту + Начислено на организ.` across matched visits, unless the user specifies another definition.
- `Записался` is a booking signal from iMot or another booking source. It is not the same as `дошёл`.
- Treat iMot tags and summaries as automatic analysis. Use transcripts to resolve conflicts or high-impact ambiguous cases.
- Distinguish Calltouch rows, unique leads, calls, patients, visits, and bookings. Never present one as another.

## CPC scope

If the input is not already filtered, include rows where `utm_medium` or the Calltouch medium equals `cpc`, case-insensitively. Preserve the original source and medium values and report excluded row counts. Do not silently classify other paid channels as CPC.

## Privacy

The sources contain personal and medical data. Minimize exposure, keep files in the authorized workspace, and avoid copying full transcripts into summary sheets unless requested. Prefer call IDs and concise summaries in reader-facing outputs.
