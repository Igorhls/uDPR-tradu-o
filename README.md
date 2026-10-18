# Aplicador de tradução para bundles Unity (MsbtData)
*********** Para instalar, basta extrair na pasta raiz do jogo. **************
Ferramentas para trabalhar com o bundle de localização `english` (UnityFS, Unity 2019.4.27f1) de
**Pokémon Brilliant Diamond / Shining Pearl** (Switch): listar os textos e aplicar uma tradução
já feita sobre o bundle original, mantendo a estrutura que o jogo espera.

> Este repositório contém **apenas ferramentas**. Os arquivos do jogo (bundles `english`) e os
> textos extraídos não estão incluídos. Use os arquivos do seu próprio jogo.

## Requisitos

```bash
pip install -r requirements.txt
```

## Uso

Listar arquivos de texto e exportar CSV:

```bash
python tools/listar_labels.py english labels.csv
```

Aplicar a tradução (`traduzido`) sobre o bundle original e gerar um novo bundle:

```bash
python tools/aplicar_traducao.py english english_pt-br saida_english --relatorio relatorio.md
```

## Como funciona

- O bundle tem 119 arquivos `MsbtData`, cada um com uma lista de labels (`labelDataArray`).
- Os labels são casados **pelo nome**. Para cada um, copia do bundle traduzido: texto
  (`wordDataArray`), estilo (`fontSize`/`maxWidth`) e tags (`tagDataArray`, ex.: variantes de gênero).
- Labels sem tradução, ou com número de trechos diferente, ficam como no original.
- Labels só existentes no traduzido são descartados.
- A compressão original do bundle é mantida.
- Entradas sem nome (slots vazios) são ignoradas.

## Limitações conhecidas

- Testado diretamente no jogo pelo autor das ferramentas: valide no emulador/console.
- `strWidth` não é recalculado; textos longos podem cortar em algumas caixas.
- Se o bundle traduzido tiver espaço extra no início das frases, ele é copiado como está.

## Licença

Código sob licença MIT (ver `LICENSE`).
