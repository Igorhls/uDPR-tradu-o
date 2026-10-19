#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lista todos os arquivos MsbtData e seus labels de um bundle UnityFS (Message/english)
e exporta para um arquivo CSV.

Uso:
    python tools/listar_labels.py <caminho_bundle_english> <saida.csv>
"""

import argparse
import csv
import os
import sys
import UnityPy


def listar_labels(bundle_path: str, csv_path: str) -> None:
    if not os.path.isfile(bundle_path):
        raise FileNotFoundError(f"Bundle não encontrado: {bundle_path}")

    env = UnityPy.load(bundle_path)
    rows = []

    for obj in env.objects:
        if obj.type.name != "MonoBehaviour":
            continue
        tree = obj.read_typetree()
        msbt_name = tree.get("m_Name", "")
        labels = tree.get("labelDataArray", [])
        for ld in labels:
            label_name = ld.get("labelName", "")
            if not label_name:
                continue
            words = [w.get("str", "") for w in ld.get("wordDataArray", [])]
            full_text = " | ".join(words)
            style = ld.get("styleInfo", {})
            rows.append({
                "arquivo": msbt_name,
                "labelIndex": ld.get("labelIndex", -1),
                "labelName": label_name,
                "segmentos": len(words),
                "tags": len(ld.get("tagDataArray", [])),
                "fontSize": style.get("fontSize", -1),
                "maxWidth": style.get("maxWidth", -1),
                "texto": full_text,
            })

    rows.sort(key=lambda r: (r["arquivo"], r["labelIndex"]))

    os.makedirs(os.path.dirname(os.path.abspath(csv_path)), exist_ok=True)
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "arquivo",
                "labelIndex",
                "labelName",
                "segmentos",
                "tags",
                "fontSize",
                "maxWidth",
                "texto",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Exportados {len(rows)} labels para: {csv_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exporta os labels de um bundle MsbtData (UnityFS) para CSV."
    )
    parser.add_argument("bundle", help="Caminho para o bundle english (UnityFS)")
    parser.add_argument("csv_out", help="Caminho para o arquivo CSV de saída")
    args = parser.parse_args()
    listar_labels(args.bundle, args.csv_out)


if __name__ == "__main__":
    main()
