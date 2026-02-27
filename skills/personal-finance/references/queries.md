# Useful SQL Queries

## Monthly Expense Breakdown
```sql
SELECT c.grupo, c.nome, SUM(t.valor) as total
FROM transacoes t
JOIN categorias c ON t.categoria_id = c.id
WHERE t.valor < 0 AND t.data BETWEEN :start AND :end
GROUP BY c.grupo, c.nome
ORDER BY total ASC;
```

## Top Expenses
```sql
SELECT descricao, valor, data
FROM transacoes
WHERE valor < 0 AND data BETWEEN :start AND :end
ORDER BY valor ASC LIMIT 20;
```

## Income vs Expenses by Month
```sql
SELECT strftime('%Y-%m', data) as mes,
  SUM(CASE WHEN valor > 0 THEN valor ELSE 0 END) as receitas,
  SUM(CASE WHEN valor < 0 THEN ABS(valor) ELSE 0 END) as despesas,
  SUM(valor) as saldo
FROM transacoes
WHERE status = 'realizado'
GROUP BY mes ORDER BY mes;
```

## Credit Card Spending by Card
```sql
SELECT ca.apelido, COUNT(*) as qtd, SUM(ABS(t.valor)) as total
FROM transacoes t
JOIN cartoes ca ON t.cartao_id = ca.id
WHERE t.valor < 0
GROUP BY ca.apelido;
```

## Overdue Bills
```sql
SELECT descricao, valor_previsto, data_vencimento,
  CAST(julianday('now') - julianday(data_vencimento) AS INTEGER) as dias_atraso
FROM contas_pagar_receber
WHERE tipo = 'pagar' AND status = 'pendente'
  AND data_vencimento < date('now')
ORDER BY data_vencimento;
```

## Bills Due Next 7 Days
```sql
SELECT descricao, valor_previsto, data_vencimento
FROM contas_pagar_receber
WHERE tipo = 'pagar' AND status = 'pendente'
  AND data_vencimento BETWEEN date('now') AND date('now', '+7 days')
ORDER BY data_vencimento;
```

## Recurring Bills Monthly Total
```sql
SELECT SUM(valor_previsto) as total_fixo_mensal
FROM contas_pagar_receber
WHERE tipo = 'pagar' AND recorrente = 1 AND status = 'pendente'
  AND data_vencimento BETWEEN date('now', 'start of month') AND date('now', 'start of month', '+1 month', '-1 day');
```

## Uncategorized Transactions
```sql
SELECT id, data, descricao, valor
FROM transacoes
WHERE categoria_id IS NULL OR categoria_id = (SELECT id FROM categorias WHERE nome = 'Não categorizado')
ORDER BY data DESC LIMIT 50;
```

## Investment Portfolio Summary
```sql
SELECT tipo, apelido, instituicao, valor_atual,
  ROUND((valor_atual - valor_aplicado) / valor_aplicado * 100, 2) as rent_pct
FROM investimentos
ORDER BY valor_atual DESC;
```

## Installment Commitments (Future)
```sql
SELECT descricao, parcela_atual, parcela_total, valor,
  (parcela_total - parcela_atual) as parcelas_restantes,
  ABS(valor) * (parcela_total - parcela_atual) as total_restante
FROM transacoes
WHERE parcela_total IS NOT NULL AND parcela_atual < parcela_total
ORDER BY parcela_total - parcela_atual DESC;
```
