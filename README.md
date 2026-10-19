# Tradução Autoral PT-BR v2.0 — Pokémon Brilliant Diamond (uDPR / Switch)

Ferramentas, dicionários oficiais e compilador do bundle de localização `english` (`UnityFS`, Unity `2019.4.27f1`) de **Pokémon Brilliant Diamond** para a versão nativa de PC (**uDPR**) e Switch/Emuladores.

---

## 📦 Instalação Rápida (uDPR / PC)

1. Basta extrair o arquivo **`english-ptbr-autoral-v2.0.zip`** (ou copiar a pasta `Dpr_Data` de dentro de `saida_autoral/`) na pasta raiz onde está o seu `Dpr.exe`, substituindo o arquivo `Dpr_Data/StreamingAssets/AssetAssistant/Message/english`.
2. **Para Ryujinx / Switch:** Copie o arquivo `saida_autoral/Dpr_Data/StreamingAssets/AssetAssistant/Message/english` para a pasta de mods do jogo em `romfs/Data/StreamingAssets/AssetAssistant/Message/english`.

---

## ✨ Diferenciais da Versão Autoral v2.0

- **Cidades, Vilas, Rotas e Locais de Sinnoh (100% PT-BR Oficial):** Padrão oficial do Anime/Mangá/TCG (*Cidade de Jubilife*, *Vila Twinleaf*, *Monte Coronet*, *Lago Verity*, *Pilar de Lança*, *Parque Ramanas*, *Grande Subsolo*, *Liga Pokémon*, *Rota 201* a *Rota 230*), incluindo todas as preposições no sumário dos Pokémon (*"na Vila Twinleaf"*, *"no Monte Coronet"*).
- **827 Golpes (Moves), 268 Habilidades (Abilities) e 25 Naturezas (Natures):** Todos traduzidos segundo a terminologia oficial em Português Brasileiro (**Pokémon TCG**, **Pokémon GO**, **Anime**, **Pokémon UNITE**).
- **1.623 Itens, 65 Frutas, 31 Poffins, 97 Adesivos e 631 Itens do Subsolo:** Traduzidos segundo o TCG/Anime/GO (*Poção*, *Doce Raro*, *Compartilhador de Exp.*, *Orbe da Vida*, *Pedra do Trovão*, *Esfera Vermelha P/G*, *Estátua de Lucario*), mantendo os nomes clássicos das bolas especiais (*Master Ball*, *Ultra Ball*, *Great Ball*, etc.) e *Poké Bola*.
- **Personagens e Classes de Treinadores:** Nomes oficiais preservados (*Rowan*, *Dawn*, *Lucas*, *Barry*, *Cynthia*, *Cyrus*), com títulos, familiares e classes 100% traduzidos e revisados (*Mãe*, *Palavras da Mãe*, *Recruta Galáctico*, *Piqueniqueira*, *Treinador Ás*, *Líder de Ginásio*).
- **Fidelidade 100% ao Brilliant Diamond Original:** Removidas todas as alterações intrusivas de texto do mod *Luminescent Platinum* (como menções a *Renegade Park*, Eevee na casa da mãe, MTs infinitas, relógio floral no Ginásio de Eterna, troca de Snorunt em vez de Buizel e avisos de *"base mod"* na tela inicial).
- **Zero Frases Híbridas e Acentuação Completa:** Corrigidos os mais de 1.100 textos que estavam metade em português e metade em inglês, restaurados todos os acentos ausentes nos menus de Opções e Caixas, e recalculado proporcionalmente o `strWidth` de todas as entradas.

---

## 🛠️ Ferramentas e Compilação

### Requisitos

```bash
pip install -r requirements.txt
```

### Recompilar a Tradução Autoral a partir dos Dicionários

```bash
python tools/compilar_autoral.py
```

Gera automaticamente:
- `saida_autoral/Dpr_Data/StreamingAssets/AssetAssistant/Message/english`
- `english-ptbr-autoral-v2.0.zip`
- `relatorio_autoral.md`

### Outros Utilitários

Listar arquivos `MsbtData` e exportar todos os 42.557 labels para CSV:

```bash
python tools/listar_labels.py <caminho_bundle_english> labels.csv
```

Aplicar um bundle traduzido sobre outro bundle original:

```bash
python tools/aplicar_traducao.py <bundle_original> <bundle_traduzido> <bundle_saida> --relatorio relatorio.md
```

---

## 📂 Estrutura de Dicionários (`dicionarios/`)

- `moves_ptbr.json`: 827 golpes em PT-BR oficial.
- `abilities_ptbr.json`: 268 habilidades em PT-BR oficial.
- `places_speakers_trainers_ptbr.json`: Locais de Sinnoh, falantes, classes de treinadores, naturezas e tipos.
- `items_and_misc_ptbr.json`: Itens (singular, plural e classificados), frutas, poffins, adesivos, roupas, Parque Ramanas e Subsolo.
- `dialogue_and_ui_fixes_ptbr.json`: Correções de diálogos híbridos, textos de rede/TV/acompanhante e fidelidade de história ao Brilliant Diamond.

## Licença

Código e ferramentas sob licença MIT (ver `LICENSE`).
