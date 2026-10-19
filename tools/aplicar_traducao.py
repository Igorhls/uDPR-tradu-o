#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplica uma tradução sobre o bundle original `english` (UnityFS, Unity 2019.4.27f1)
de Pokémon Brilliant Diamond / Shining Pearl, recalculando `strWidth` proporcionalmente
e gerando um relatório opcional em Markdown.

Uso:
    python tools/aplicar_traducao.py <bundle_original> <bundle_traduzido> <bundle_saida> [--relatorio relatorio.md]
"""

import argparse
import os
import UnityPy


def recalcular_str_width(texto: str, font_size: int) -> float:
    if not texto:
        return 0.0
     escala = (font_size if font_size > 0 else 42) / 42.0
    largura = 0.0
    for ch in texto:
        if ch in "ilI1|!.,:;'`´":
            largura += 6.2
        elif ch in "mwMW@#%&":
            largura += 18.5
        elif ch in "ABCDEFGHJKLNOPQRSTUVXYZÇÃÕÁÉÍÓÚÂÊÔÀÜ":
            largura += 14.8
        elif ch == " ":
            largura += 7.5
        else:
            largura += 12.2
    return round(largura * escala, 4)


def aplicar_traducao(
    orig_path: str,
    trad_path: str,
    out_path: str,
    relatorio_path: str | None = None,
) -> None:
    env_orig = UnityPy.load(orig_path)
    env_trad = UnityPy.load(trad_path)

    trad_map: dict[str, dict[str, dict]] = {}
    for obj in env_trad.objects:
        if obj.type.name != "MonoBehaviour":
            continue
        tree = obj.read_typetree()
        name = tree.get("m_Name", "")
        labels = {}
        for ld in tree.get("labelDataArray", []):
            lname = ld.get("labelName", "")
            if lname:
                labels[lname] = ld
        trad_map[name] = labels

    stats = []
    total_aplicados = 0
    total_mantidos = 0

    for obj in env_orig.objects:
        if obj.type.name != "MonoBehaviour":
            continue
        tree = obj.read_typetree()
        name = tree.get("m_Name", "")
        t_labels = trad_map.get(name, {})
        aplicados_arq = 0
        mantidos_arq = 0

        for ld in tree.get("labelDataArray", []):
            lname = ld.get("labelName", "")
            if not lname or lname not in t_labels:
                mantidos_arq += 1
                continue

            tld = t_labels[lname]
            w_orig = ld.get("wordDataArray", [])
            w_trad = tld.get("wordDataArray", [])
            if len(w_orig) != len(w_trad):
                mantidos_arq += 1
                continue

            font_size = ld.get("styleInfo", {}).get("fontSize", 42)
            for i, w in enumerate(w_orig):
                novo_str = w_trad[i].get("str", "")
                w["str"] = novo_str
                if w.get("tagIndex", -1) == -1:
                    w["strWidth"] = recalcular_str_width(novo_str, font_size)

            if "styleInfo" in tld and "styleInfo" in ld:
                ld["styleInfo"]["fontSize"] = tld["styleInfo"].get(
                    "fontSize", ld["styleInfo"]["fontSize"]
                )
                ld["styleInfo"]["maxWidth"] = tld["styleInfo"].get(
                    "maxWidth", ld["styleInfo"]["maxWidth"]
                )
            if "tagDataArray" in tld and len(tld["tagDataArray"]) == len(
                ld.get("tagDataArray", [])
            ):
                ld["tagDataArray"] = tld["tagDataArray"]

            aplicados_arq += 1

        obj.save_typetree(tree)
        total_aplicados += aplicados_arq
        total_mantidos += mantidos_arq
        stats.append((name, aplicados_arq, mantidos_arq))

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(env_orig.file.save(packer="original"))

    print(
        f"Bundle salvo em: {out_path} ({total_aplicados} labels aplicados, {total_mantidos} mantidos)"
    )

    if relatorio_path:
        os.makedirs(os.path.dirname(os.path.abspath(relatorio_path)), exist_ok=True)
        with open(relatorio_path, "w", encoding="utf-8") as rf:
            rf.write("# Relatório de Aplicação de Tradução\n\n")
            rf.write(f"- **Labels traduzidos aplicados:** {total_aplicados}\n")
            rf.write(f"- **Labels mantidos do original:** {total_mantidos}\n\n")
            rf.write("| Arquivo (`MsbtData`) | Aplicados | Mantidos |\n")
            rf.write("| :--- | ---: | ---: |\n")
            for name, ap, ma in sorted(stats):
                rf.write(f"| `{name}` | {ap} | {ma} |\n")
        print(f"Relatório salvo em: {relatorio_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Aplica um bundle traduzido sobre o bundle original english."
    )
    parser.add_argument("original", help="Caminho para o bundle english original")
    parser.add_argument("traduzido", help="Caminho para o bundle english traduzido")
    parser.add_argument("saida", help="Caminho para o bundle english de saída")
    parser.add_argument(
        "--relatorio", help="Caminho opcional para salvar relatório Markdown"
    )
    args = parser.parse_args()
    aplicar_traducao(args.original, args.traduzido, args.saida, args.relatorio)


if __name__ == "__main__":
    main()
