-- Personal Finance Database Schema
-- SQLite 3

CREATE TABLE IF NOT EXISTS contas (
  id INTEGER PRIMARY KEY,
  banco TEXT NOT NULL,
  tipo TEXT NOT NULL, -- corrente, poupanca, pagamento, investimento
  titular TEXT NOT NULL,
  apelido TEXT NOT NULL,
  agencia TEXT,
  numero TEXT,
  saldo_inicial REAL DEFAULT 0,
  ativo INTEGER DEFAULT 1,
  criado_em TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS cartoes (
  id INTEGER PRIMARY KEY,
  banco TEXT NOT NULL,
  bandeira TEXT, -- visa, mastercard, elo, amex
  titular TEXT NOT NULL,
  apelido TEXT NOT NULL,
  dia_vencimento INTEGER, -- day of month (1-31)
  dia_fechamento INTEGER, -- closing day
  limite REAL,
  ativo INTEGER DEFAULT 1,
  criado_em TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS categorias (
  id INTEGER PRIMARY KEY,
  nome TEXT NOT NULL,
  grupo TEXT NOT NULL, -- Moradia, Transporte, Alimentação, Saúde, etc.
  tipo TEXT DEFAULT 'despesa', -- despesa, receita, transferencia
  ativo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS transacoes (
  id INTEGER PRIMARY KEY,
  conta_id INTEGER REFERENCES contas(id),
  cartao_id INTEGER REFERENCES cartoes(id),
  data TEXT NOT NULL, -- YYYY-MM-DD
  descricao TEXT NOT NULL,
  descricao_original TEXT, -- as received from OFX/PDF
  valor REAL NOT NULL, -- positive = income, negative = expense
  categoria_id INTEGER REFERENCES categorias(id),
  tipo TEXT NOT NULL, -- debito, credito, pix, ted, boleto, fatura, investimento
  status TEXT DEFAULT 'realizado', -- realizado, previsto, cancelado
  origem TEXT, -- ofx, fatura_pdf, manual
  origem_arquivo TEXT, -- source filename
  fitid TEXT, -- OFX unique ID for deduplication
  hash TEXT, -- hash for PDF deduplication
  parcela_atual INTEGER,
  parcela_total INTEGER,
  notas TEXT,
  criado_em TEXT DEFAULT (datetime('now')),
  atualizado_em TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_transacoes_data ON transacoes(data);
CREATE INDEX IF NOT EXISTS idx_transacoes_fitid ON transacoes(fitid);
CREATE INDEX IF NOT EXISTS idx_transacoes_conta ON transacoes(conta_id);
CREATE INDEX IF NOT EXISTS idx_transacoes_cartao ON transacoes(cartao_id);

CREATE TABLE IF NOT EXISTS contas_pagar_receber (
  id INTEGER PRIMARY KEY,
  descricao TEXT NOT NULL,
  valor_previsto REAL NOT NULL,
  valor_realizado REAL,
  data_vencimento TEXT NOT NULL, -- YYYY-MM-DD
  data_pagamento TEXT,
  tipo TEXT NOT NULL, -- pagar, receber
  recorrente INTEGER DEFAULT 0,
  frequencia TEXT, -- mensal, semanal, anual, unica
  categoria_id INTEGER REFERENCES categorias(id),
  conta_id INTEGER REFERENCES contas(id),
  cartao_id INTEGER REFERENCES cartoes(id),
  transacao_id INTEGER REFERENCES transacoes(id),
  status TEXT DEFAULT 'pendente', -- pendente, pago, atrasado, cancelado
  notas TEXT,
  criado_em TEXT DEFAULT (datetime('now')),
  atualizado_em TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_cpr_vencimento ON contas_pagar_receber(data_vencimento);
CREATE INDEX IF NOT EXISTS idx_cpr_status ON contas_pagar_receber(status);

CREATE TABLE IF NOT EXISTS investimentos (
  id INTEGER PRIMARY KEY,
  tipo TEXT NOT NULL, -- previdencia, cdb, lci, lca, acoes, fii, tesouro, fundo, cripto
  instituicao TEXT NOT NULL,
  apelido TEXT NOT NULL,
  valor_aplicado REAL,
  valor_atual REAL,
  data_aplicacao TEXT,
  data_vencimento TEXT,
  taxa TEXT, -- e.g. "100% CDI", "IPCA+6%"
  notas TEXT,
  criado_em TEXT DEFAULT (datetime('now')),
  atualizado_em TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS saldo_mensal (
  id INTEGER PRIMARY KEY,
  conta_id INTEGER REFERENCES contas(id),
  ano_mes TEXT NOT NULL, -- YYYY-MM
  saldo_final REAL NOT NULL,
  criado_em TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS arquivos_importados (
  id INTEGER PRIMARY KEY,
  nome TEXT NOT NULL,
  tipo TEXT NOT NULL, -- ofx, pdf, csv, print
  hash TEXT,
  transacoes_inseridas INTEGER DEFAULT 0,
  notas TEXT,
  criado_em TEXT DEFAULT (datetime('now'))
);
