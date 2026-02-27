#!/usr/bin/env python3
"""
Import OFX bank statements into the personal finance database.
Usage: python3 import_ofx.py /path/to/financeiro.db /path/to/file.ofx [--conta-id N] [--cartao-id N]

Deduplicates via fitid. Supports checking accounts and credit cards.
"""

import sqlite3
import sys
import re
import hashlib
from datetime import datetime

def parse_ofx(filepath):
    """Simple OFX parser — handles OFX 1.x (SGML) format."""
    with open(filepath, encoding='latin-1') as f:
        content = f.read()

    transactions = []
    acctid = None

    # Extract account ID
    m = re.search(r'<ACCTID>([^<\s]+)', content)
    if m:
        acctid = m.group(1).strip()

    # Extract transactions
    for block in re.findall(r'<STMTTRN>(.*?)</STMTTRN>', content, re.DOTALL):
        tx = {}
        for tag in ['TRNTYPE', 'DTPOSTED', 'TRNAMT', 'FITID', 'MEMO', 'NAME', 'CHECKNUM']:
            m = re.search(rf'<{tag}>([^<\n]+)', block)
            if m:
                tx[tag] = m.group(1).strip()

        if 'DTPOSTED' in tx and 'TRNAMT' in tx:
            # Parse date (YYYYMMDD or YYYYMMDDHHMMSS)
            dt = tx['DTPOSTED'][:8]
            tx['date'] = f"{dt[:4]}-{dt[4:6]}-{dt[6:8]}"
            tx['amount'] = float(tx['TRNAMT'].replace(',', '.'))
            tx['description'] = tx.get('MEMO') or tx.get('NAME') or 'Sem descrição'
            tx['fitid'] = tx.get('FITID', '')
            tx['trntype'] = tx.get('TRNTYPE', 'OTHER')
            transactions.append(tx)

    return transactions, acctid

def import_ofx(db_path, ofx_path, conta_id=None, cartao_id=None):
    transactions, acctid = parse_ofx(ofx_path)
    if not transactions:
        print("[WARN] No transactions found in OFX file")
        return

    print(f"[INFO] Found {len(transactions)} transactions, ACCTID: {acctid}")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    inserted = 0
    skipped = 0
    filename = ofx_path.split('/')[-1]

    for tx in transactions:
        # Check for duplicate
        if tx['fitid']:
            cur.execute("SELECT id FROM transacoes WHERE fitid = ?", (tx['fitid'],))
            if cur.fetchone():
                skipped += 1
                continue

        tipo = 'credito' if tx['amount'] > 0 else 'debito'

        cur.execute("""
            INSERT INTO transacoes (conta_id, cartao_id, data, descricao, descricao_original,
                valor, tipo, origem, origem_arquivo, fitid, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'ofx', ?, ?, 'realizado')
        """, (
            conta_id, cartao_id, tx['date'], tx['description'], tx['description'],
            tx['amount'], tipo, filename, tx['fitid']
        ))
        inserted += 1

    # Log import
    file_hash = hashlib.md5(open(ofx_path, 'rb').read()).hexdigest()
    cur.execute("""
        INSERT INTO arquivos_importados (nome, tipo, hash, transacoes_inseridas)
        VALUES (?, 'ofx', ?, ?)
    """, (filename, file_hash, inserted))

    conn.commit()
    conn.close()
    print(f"[OK] Inserted: {inserted}, Skipped (duplicates): {skipped}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <db_path> <ofx_path> [--conta-id N] [--cartao-id N]")
        sys.exit(1)

    db_path = sys.argv[1]
    ofx_path = sys.argv[2]
    conta_id = None
    cartao_id = None

    for i, arg in enumerate(sys.argv):
        if arg == '--conta-id' and i + 1 < len(sys.argv):
            conta_id = int(sys.argv[i + 1])
        if arg == '--cartao-id' and i + 1 < len(sys.argv):
            cartao_id = int(sys.argv[i + 1])

    import_ofx(db_path, ofx_path, conta_id, cartao_id)
