---
name: personal-finance
description: >
  Personal finance management system using SQLite. Track bank accounts, credit cards,
  income, expenses, investments, bills and recurring payments. Import OFX bank statements
  and PDF credit card invoices. Generate reports, budget vs actual, cashflow projections.
  Set up automated bill reminders via cron. Use when: (1) setting up personal finance tracking,
  (2) importing bank statements (OFX/PDF), (3) categorizing transactions, (4) tracking bills
  and due dates, (5) generating financial reports or summaries, (6) managing credit cards and
  invoices, (7) tracking investments. NOT for: business accounting, tax filing, or stock trading.
---

# Personal Finance Manager

A complete personal finance system built on SQLite. Zero subscription, zero cloud dependency,
full privacy. Your money data stays on your machine.

## Quick Start

1. Run the setup script to create the database:
   ```bash
   python3 scripts/setup_db.py /path/to/financeiro.db
   ```
2. Follow the interactive setup or manually configure accounts (see below)
3. Import your first statement (OFX or PDF)
4. Set up bill reminders via cron

## Database Location

Default: `financeiro/financeiro.db` in the workspace.
All PDFs go in `financeiro/faturas/`, OFX/imports in `financeiro/imports/`.

## Core Concepts

### Accounts (`contas`)
Bank accounts: checking, savings, digital wallets. Each has a type and balance.

### Credit Cards (`cartoes`)
Track cards separately: due date (`dia_vencimento`), closing date (`dia_fechamento`), limit.

### Transactions (`transacoes`)
Every money movement. Positive = income, negative = expense.
- `conta_id` or `cartao_id` — where the money moved
- `categoria_id` — what it was for
- `fitid` — unique OFX ID for deduplication
- `origem` — source: `ofx`, `fatura_pdf`, `manual`
- `parcela_atual/parcela_total` — installment tracking

### Bills (`contas_pagar_receber`)
Upcoming and recurring obligations:
- `tipo`: `pagar` (payable) or `receber` (receivable)
- `recorrente`: 1 = auto-generates next month
- `frequencia`: `mensal`, `semanal`, `anual`, `unica`
- `status`: `pendente`, `pago`, `atrasado`, `cancelado`

### Categories (`categorias`)
Organized by group. See references/categories.md for the default category tree.

### Investments (`investimentos`)
Track pension funds, stocks, fixed income. Fields: type, institution, current value,
applied value, rate, notes.

## Importing Data

### OFX Files (Bank Statements)
```bash
python3 scripts/import_ofx.py /path/to/financeiro.db /path/to/file.ofx --conta-id 1
```
- Auto-deduplicates via `fitid`
- Detects account from OFX ACCTID
- Maps common descriptions to categories

### PDF Credit Card Invoices
Extract text first, then parse:
```bash
pdftotext /path/to/fatura.pdf - | head -100
```
Then insert transactions manually or with the import script:
```bash
python3 scripts/import_fatura_pdf.py /path/to/financeiro.db /path/to/fatura.pdf --cartao-id 1
```

**PDF parsing tips:**
- OCR quality varies — watch for character substitutions (e.g., "õ"→"D", "$9"→"R$")
- Installments appear as "Parcela X de Y" — extract both numbers
- Credits/payments are positive values, purchases are negative
- Always verify totals match the PDF summary

## Bill Reminders (Cron)

Set up a daily cron to alert about upcoming bills:

```
Schedule: 0 8 * * * (daily at 8am)
Session: isolated
```

The cron should:
1. Query `contas_pagar_receber` for bills due in the next 3 days
2. Flag any past-due bills as ATRASADA
3. Send alert via configured channel (Telegram/WhatsApp/etc.)
4. On day 1 of each month, auto-generate recurring bills for the new month

## Reports

### Monthly Summary
```sql
SELECT
  c.grupo, c.nome as categoria,
  SUM(CASE WHEN t.valor < 0 THEN t.valor ELSE 0 END) as despesas,
  SUM(CASE WHEN t.valor > 0 THEN t.valor ELSE 0 END) as receitas
FROM transacoes t
JOIN categorias c ON t.categoria_id = c.id
WHERE t.data BETWEEN '2026-01-01' AND '2026-01-31'
GROUP BY c.grupo, c.nome
ORDER BY despesas ASC;
```

### Credit Card Summary
```sql
SELECT ca.apelido, SUM(ABS(t.valor)) as total
FROM transacoes t
JOIN cartoes ca ON t.cartao_id = ca.id
WHERE t.valor < 0
  AND t.data BETWEEN '2026-01-01' AND '2026-01-31'
GROUP BY ca.apelido;
```

### Upcoming Bills
```sql
SELECT descricao, valor_previsto, data_vencimento,
  CASE WHEN data_vencimento < date('now') THEN '⚠️ ATRASADA'
       WHEN data_vencimento <= date('now', '+3 days') THEN '🔔 EM BREVE'
       ELSE '✅ OK' END as status_alerta
FROM contas_pagar_receber
WHERE tipo = 'pagar' AND status = 'pendente'
ORDER BY data_vencimento;
```

### Investment Portfolio
```sql
SELECT tipo, instituicao, apelido, valor_atual,
  ROUND((valor_atual - valor_aplicado) / valor_aplicado * 100, 2) as rentabilidade_pct
FROM investimentos
ORDER BY valor_atual DESC;
```

## Workflow: Onboarding a New User

1. **Ask about accounts**: Which banks? Checking/savings? Digital wallets?
2. **Ask about credit cards**: Which cards? Due dates? Limits?
3. **Ask about income**: Salary? Freelance? How often?
4. **Ask about fixed expenses**: Rent/mortgage, utilities, subscriptions, insurance
5. **Run setup script** with their answers
6. **Import first statements**: Guide them through OFX download or PDF upload
7. **Set up bill reminders**: Configure cron with their preferred alert time
8. **First report**: Show them a monthly summary to validate data

## Tone & Approach

- Be informal but professional — you're a financial advisor friend, not a bank
- Flag bad financial habits (rotativo credit card debt, missed payments) directly
- Celebrate good decisions (early payoff, investment growth)
- All amounts in the user's local currency (detect from statements)
- When in doubt about a transaction category, ask — don't guess wrong

## File Structure
```
financeiro/
├── financeiro.db          # SQLite database
├── faturas/               # Original PDF invoices
├── imports/               # OFX files and statement screenshots
└── import_ofx.py          # OFX importer (legacy, use scripts/ version)
```

## References
- **Database schema**: See references/schema.sql for the complete CREATE TABLE statements
- **Default categories**: See references/categories.md for the category tree
- **Common queries**: See references/queries.md for useful SQL snippets
