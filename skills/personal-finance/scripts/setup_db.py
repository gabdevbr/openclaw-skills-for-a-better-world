#!/usr/bin/env python3
"""
Setup the personal finance SQLite database.
Usage: python3 setup_db.py /path/to/financeiro.db
Creates all tables and populates default categories.
"""

import sqlite3
import sys
import os

def get_schema():
    """Read schema from references/schema.sql"""
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'references', 'schema.sql')
    with open(schema_path) as f:
        return f.read()

DEFAULT_CATEGORIES = [
    # (nome, grupo, tipo)
    # Moradia
    ("Aluguel / Financiamento", "Moradia", "despesa"),
    ("Condomínio", "Moradia", "despesa"),
    ("IPTU", "Moradia", "despesa"),
    ("Energia elétrica", "Moradia", "despesa"),
    ("Água", "Moradia", "despesa"),
    ("Gás", "Moradia", "despesa"),
    ("Internet", "Moradia", "despesa"),
    ("Manutenção residencial", "Moradia", "despesa"),
    # Transporte
    ("Combustível", "Transporte", "despesa"),
    ("Financiamento veículo", "Transporte", "despesa"),
    ("Seguro veículo", "Transporte", "despesa"),
    ("IPVA / Licenciamento", "Transporte", "despesa"),
    ("Estacionamento / Pedágio", "Transporte", "despesa"),
    ("Transporte público", "Transporte", "despesa"),
    ("Manutenção veículo", "Transporte", "despesa"),
    ("Aplicativo (Uber/99)", "Transporte", "despesa"),
    # Alimentação
    ("Supermercado", "Alimentação", "despesa"),
    ("Restaurante / Delivery", "Alimentação", "despesa"),
    ("Padaria / Café", "Alimentação", "despesa"),
    ("Lanches", "Alimentação", "despesa"),
    # Saúde
    ("Plano de saúde", "Saúde", "despesa"),
    ("Farmácia", "Saúde", "despesa"),
    ("Consultas médicas", "Saúde", "despesa"),
    ("Exames", "Saúde", "despesa"),
    ("Odontologia", "Saúde", "despesa"),
    # Educação
    ("Escola / Faculdade", "Educação", "despesa"),
    ("Cursos / Livros", "Educação", "despesa"),
    ("Material escolar", "Educação", "despesa"),
    # Lazer
    ("Entretenimento", "Lazer", "despesa"),
    ("Viagens", "Lazer", "despesa"),
    ("Streaming", "Lazer", "despesa"),
    ("Hobbies", "Lazer", "despesa"),
    # Pessoal
    ("Vestuário", "Pessoal", "despesa"),
    ("Beleza / Estética", "Pessoal", "despesa"),
    ("Academia", "Pessoal", "despesa"),
    ("Presentes", "Pessoal", "despesa"),
    # Financeiro
    ("Tarifas bancárias", "Financeiro", "despesa"),
    ("Juros / Multas", "Financeiro", "despesa"),
    ("IOF", "Financeiro", "despesa"),
    ("Seguros", "Financeiro", "despesa"),
    ("Previdência privada", "Financeiro", "despesa"),
    # Compras
    ("Eletrônicos", "Compras", "despesa"),
    ("Casa / Decoração", "Compras", "despesa"),
    ("Marketplace", "Compras", "despesa"),
    # Família
    ("Mesada / Pensão", "Família", "despesa"),
    ("Pet / Veterinário", "Família", "despesa"),
    # Trabalho
    ("Ferramentas / Software", "Trabalho", "despesa"),
    ("Equipamentos", "Trabalho", "despesa"),
    # Igreja / Doações
    ("Dízimo", "Igreja / Doações", "despesa"),
    ("Ofertório", "Igreja / Doações", "despesa"),
    ("Doações", "Igreja / Doações", "despesa"),
    # Outros
    ("Não categorizado", "Outros", "despesa"),
    # Receitas
    ("Salário / Pró-labore", "Receita", "receita"),
    ("Nota fiscal (PJ)", "Receita", "receita"),
    ("Freelance", "Receita", "receita"),
    ("PPR / Bônus", "Receita", "receita"),
    ("Rendimento investimentos", "Receita", "receita"),
    ("Dividendos", "Receita", "receita"),
    ("Aluguel recebido", "Receita", "receita"),
    ("Reembolso", "Receita", "receita"),
    ("Cashback", "Receita", "receita"),
    ("Crédito concedido", "Receita", "receita"),
]

def setup(db_path):
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create tables
    schema = get_schema()
    cur.executescript(schema)

    # Insert default categories (skip if already populated)
    cur.execute("SELECT COUNT(*) FROM categorias")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO categorias (nome, grupo, tipo) VALUES (?, ?, ?)",
            DEFAULT_CATEGORIES
        )
        print(f"[OK] Inserted {len(DEFAULT_CATEGORIES)} default categories")
    else:
        print("[SKIP] Categories already exist")

    conn.commit()
    conn.close()
    print(f"[OK] Database ready at {db_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} /path/to/financeiro.db")
        sys.exit(1)
    setup(sys.argv[1])
