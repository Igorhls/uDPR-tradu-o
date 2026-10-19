#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compilador da Tradução Autoral PT-BR de Pokémon Brilliant Diamond (uDPR / Switch).

Aplica:
1. Dicionários oficiais PT-BR (TCG / Pokémon GO / Anime / Mangá) para:
   - 827 Golpes (Moves)
   - 268 Habilidades (Abilities)
   - 25 Naturezas (Natures) e 18 Tipos (Types)
   - 1.623 Itens (+ plurais e formas classificadas), Mantendo nomes clássicos das Bolas especiais e Poké Bola
   - 65 Frutas (Berries), 31 Poffins, 97 Adesivos (Stickers), 32 Itens do Parque Ramanas, 15 Roupas, 631 Itens do Subsolo
   - 218 Cidades, Vilas, Rotas e Locais de Sinnoh (+ formas indiretas "na Cidade de Jubilife", etc.)
   - 112 Falantes (Speakers) e 101 Classes de Treinadores
2. Correção integral de falas híbridas (metade PT, metade EN), textos não traduzidos e remoção de alterações do mod Luminescent Platinum para fidelidade 100% ao Pokémon Brilliant Diamond original.
3. Restauração ortográfica e de acentuação em menus, opções, caixas, batalhas e treinadores.
4. Sincronização automática de termos (cidades, locais, golpes e habilidades) citados dentro dos diálogos e descrições.
5. Recálculo proporcional de `strWidth` em todos os segmentos modificados.
"""

import json
import os
import re
import zipfile
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


ACCENT_FIXES = [
    (r"\bVoce\b", "Você"),
    (r"\bvoce\b", "você"),
    (r"\bVoces\b", "Vocês"),
    (r"\bvoces\b", "vocês"),
    (r"\bPokemon\b", "Pokémon"),
    (r"\bPOKEMON\b", "POKÉMON"),
    (r"\bPokémons\b", "Pokémon"),
    (r"\bpokémons\b", "Pokémon"),
    (r"\bNao\b", "Não"),
    (r"\bnao\b", "não"),
    (r"\bRapido\b", "Rápido"),
    (r"\brapido\b", "rápido"),
    (r"\bAutomatico\b", "Automático"),
    (r"\bautomatico\b", "automático"),
    (r"\bAutomatica\b", "Automática"),
    (r"\bautomatica\b", "automática"),
    (r"\bOPCOES\b", "OPÇÕES"),
    (r"\bOpcoes\b", "Opções"),
    (r"\bopcoes\b", "opções"),
    (r"\bconfiguracoes\b", "configurações"),
    (r"\bConfiguracoes\b", "Configurações"),
    (r"\banimacoes\b", "animações"),
    (r"\bAnimacoes\b", "Animações"),
    (r"\bapos\b", "após"),
    (r"\bApos\b", "Após"),
    (r"\bjapones\b", "japonês"),
    (r"\bGiroscopio\b", "Giroscópio"),
    (r"\bMusica\b", "Música"),
    (r"\bmusica\b", "música"),
    (r"\bpadrao\b", "padrão"),
    (r"\bPadrao\b", "Padrão"),
    (r"\bCamera\b", "Câmera"),
    (r"\bcamera\b", "câmera"),
    (r"\bEscavacao\b", "Escavação"),
    (r"\bescavacao\b", "escavação"),
    (r"\bFosseis\b", "Fósseis"),
    (r"\bfosseis\b", "fósseis"),
    (r"\bFossil\b", "Fóssil"),
    (r"\bfossil\b", "fóssil"),
    (r"\bnecessario\b", "necessário"),
    (r"\bnecessaria\b", "necessária"),
    (r"\btambem\b", "também"),
    (r"\bTambem\b", "Também"),
    (r"\balguem\b", "alguém"),
    (r"\bAlguem\b", "Alguém"),
    (r"\bninguem\b", "ninguém"),
    (r"\bNinguem\b", "Ninguém"),
    (r"\bentao\b", "então"),
    (r"\bEntao\b", "Então"),
    (r"\bestao\b", "estão"),
    (r"\bEstao\b", "Estão"),
    (r"\bsao\b", "são"),
    (r"\bSao\b", "São"),
    (r"\bincrivel\b", "incrível"),
    (r"\bIncrivel\b", "Incrível"),
    (r"\bpossivel\b", "possível"),
    (r"\bPossivel\b", "Possível"),
    (r"\bimpossivel\b", "impossível"),
    (r"\bImpossivel\b", "Impossível"),
    (r"\bfacil\b", "fácil"),
    (r"\bFacil\b", "Fácil"),
    (r"\bdificil\b", "difícil"),
    (r"\bDificil\b", "Difícil"),
    (r"\bproximo\b", "próximo"),
    (r"\bProximo\b", "Próximo"),
    (r"\bproxima\b", "próxima"),
    (r"\bproprio\b", "próprio"),
    (r"\bpropria\b", "própria"),
    (r"\bunico\b", "único"),
    (r"\bunica\b", "única"),
    (r"\bnumero\b", "número"),
    (r"\bNumero\b", "Número"),
    (r"\bnivel\b", "nível"),
    (r"\bNivel\b", "Nível"),
    (r"\bGinasio\b", "Ginásio"),
    (r"\bginasio\b", "ginásio"),
    (r"\bInsignia\b", "Insígnia"),
    (r"\binsignia\b", "insígnia"),
    (r"\bInsignias\b", "Insígnias"),
    (r"\binsignias\b", "insígnias"),
    (r"\bhistoria\b", "história"),
    (r"\bHistoria\b", "História"),
    (r"\bvitoria\b", "vitória"),
    (r"\bVitoria\b", "Vitória"),
    (r"\bvitorias\b", "vitórias"),
    (r"\bexperiencia\b", "experiência"),
    (r"\bforca\b", "força"),
    (r"\bcoracao\b", "coração"),
    (r"\batencao\b", "atenção"),
    (r"\binformacoes\b", "informações"),
    (r"\bcondicoes\b", "condições"),
    (r"\bcampeao\b", "campeão"),
    (r"\bCampeao\b", "Campeão"),
    (r"\bparalizado\b", "paralisado"),
    (r"\bbatalando\b", "batalhando"),
]
COMPILED_ACCENT_FIXES = [(re.compile(pat), repl) for pat, repl in ACCENT_FIXES]

# Correção especial para o menu de Opções (english_ss_option) onde todas as strings perderam acentos
SS_OPTION_OVERRIDE = {
    "SS_option_000": ["Confirmar"],
    "SS_option_001": ["Velocidade do Texto"],
    "SS_option_002": ["Lenta"],
    "SS_option_003": ["Normal"],
    "SS_option_004": ["Rápida"],
    "SS_option_005": [
        "Você pode escolher entre diferentes velocidades",
        "de exibição para controlar a rapidez das mensagens.",
    ],
    "SS_option_006": ["Animações de Batalha"],
    "SS_option_007": ["Ligadas"],
    "SS_option_008": ["Desligadas"],
    "SS_option_009": [
        "Você pode escolher se deseja ver as animações",
        "dos golpes durante as batalhas ou não.",
    ],
    "SS_option_010": ["Estilo de Batalha"],
    "SS_option_011": ["Alternar"],
    "SS_option_012": ["Manter"],
    "SS_option_013": [
        "Você pode escolher se deseja trocar de Pokémon",
        "após um Pokémon adversário ser derrotado ou não.",
    ],
    "SS_option_014": ["Caracteres"],
    "SS_option_015": ["Hiragana"],
    "SS_option_016": ["Kanji"],
    "SS_option_017": [
        "Você pode alterar a forma como o texto",
        "em japonês é exibido.",
    ],
    "SS_option_022": ["Envio para as Caixas"],
    "SS_option_023": ["Manual"],
    "SS_option_024": ["Automático"],
    "SS_option_025": [
        "Você pode enviar Pokémon automaticamente para",
        "as Caixas quando a sua equipe estiver cheia.",
    ],
    "SS_option_026": ["Deseja salvar estas configurações?"],
    "SS_option_027": ["Sim"],
    "SS_option_028": ["Não"],
    "SS_option_029": ["OPÇÕES"],
    "SS_option_030": ["Giroscópio"],
    "SS_option_031": ["Usar"],
    "SS_option_032": ["Não usar"],
    "SS_option_033": [
        "Você pode escolher se deseja usar os controles",
        "de inclinação em determinados locais.",
    ],
    "SS_option_034": ["Salvamento Automático"],
    "SS_option_035": [
        "Você pode escolher se deseja salvar o seu",
        "progresso automaticamente ou não.",
    ],
    "SS_option_040": ["Música de Fundo"],
    "SS_option_041": ["Você pode ajustar o volume da música de fundo."],
    "SS_option_042": ["Efeitos Sonoros"],
    "SS_option_043": ["Você pode ajustar o volume dos efeitos sonoros."],
    "SS_option_044": ["Gritos dos Pokémon"],
    "SS_option_045": ["Você pode ajustar o volume dos gritos dos Pokémon."],
    "SS_option_047": [
        "Deseja restaurar todas as configurações para",
        "os valores padrão?",
    ],
    "SS_option_048": ["Ligado"],
    "SS_option_049": ["Desligado"],
    "SS_option_050": [" Confirmar"],
    "SS_option_051": [" Aplicar e Sair"],
    "SS_option_052": ["Sim"],
    "SS_option_053": ["Não"],
    "SS_option_054": [" Padrão"],
    "SS_option_055": ["Deseja salvar estas configurações?"],
    "SS_option_056": ["As configurações foram salvas.", "", ""],
    "SS_option_061": ["Câmera Vertical"],
    "SS_option_062": ["Normal"],
    "SS_option_063": ["Invertida"],
    "SS_option_064": [
        "Você pode escolher entre normal ou invertida para",
        "o controle vertical da câmera.",
    ],
    "SS_option_065": ["Câmera Horizontal"],
    "SS_option_066": [
        "Você pode escolher entre normal ou invertida para",
        "o controle horizontal da câmera.",
    ],
    "SS_option_067": ["Exibir Apelidos"],
    "SS_option_068": ["Exibir"],
    "SS_option_069": ["Não exibir"],
    "SS_option_070": [
        "Você pode escolher se deseja exibir os",
        "apelidos dos Pokémon em Batalhas por Link.",
    ],
    "SS_option_071": ["Dar Apelidos"],
    "SS_option_072": ["Dar"],
    "SS_option_073": ["Não dar"],
    "SS_option_074": [
        "Você pode escolher se deseja dar um apelido",
        "a um Pokémon quando o capturar ou receber.",
    ],
    "SS_option_077": ["A tentativa falhou. Por favor, tente novamente."],
    "SS_option_079": ["Estilo da Janela"],
    "SS_option_100": ["Você pode alterar o estilo da moldura das janelas."],
    "SS_option_105": ["Tremor na Escavação de Fósseis"],
    "SS_option_106": ["Ativado"],
    "SS_option_107": ["Desativado"],
    "SS_option_108": [
        "Você pode escolher se a tela deve ou não",
        "tremer durante a escavação de Fósseis.",
    ],
}


PLACE_TEXT_SYNC = [
    ("Twinleaf Town", "Vila Twinleaf"),
    ("Sandgem Town", "Vila Sandgem"),
    ("Floaroma Town", "Vila Floaroma"),
    ("Solaceon Town", "Vila Solaceon"),
    ("Celestic Town", "Vila Celestic"),
    ("Jubilife City", "Cidade de Jubilife"),
    ("Canalave City", "Cidade de Canalave"),
    ("Oreburgh City", "Cidade de Oreburgh"),
    ("Eterna City", "Cidade de Eterna"),
    ("Hearthome City", "Cidade de Hearthome"),
    ("Pastoria City", "Cidade de Pastoria"),
    ("Veilstone City", "Cidade de Veilstone"),
    ("Sunyshore City", "Cidade de Sunyshore"),
    ("Snowpoint City", "Cidade de Snowpoint"),
    ("Pokémon League", "Liga Pokémon"),
    ("Mt. Coronet", "Monte Coronet"),
    ("Mount Coronet", "Monte Coronet"),
    ("Spear Pillar", "Pilar de Lança"),
    ("Hall of Origin", "Salão da Origem"),
    ("Lake Verity", "Lago Verity"),
    ("Lake Valor", "Lago Valor"),
    ("Lake Acuity", "Lago Acuity"),
    ("Verity Cavern", "Caverna Verity"),
    ("Valor Cavern", "Caverna Valor"),
    ("Acuity Cavern", "Caverna Acuity"),
    ("Verity Lakefront", "Margem do Lago Verity"),
    ("Valor Lakefront", "Margem do Lago Valor"),
    ("Acuity Lakefront", "Margem do Lago Acuity"),
    ("Eterna Forest", "Floresta de Eterna"),
    ("Old Chateau", "Antigo Palacete"),
    ("Oreburgh Mine", "Mina de Oreburgh"),
    ("Oreburgh Gate", "Portão de Oreburgh"),
    ("Ravaged Path", "Caminho Devastado"),
    ("Floaroma Meadow", "Prado de Floaroma"),
    ("Valley Windworks", "Usina Eólica do Vale"),
    ("Fuego Ironworks", "Siderúrgica Fuego"),
    ("Wayward Cave", "Caverna Desgarrada"),
    ("Solaceon Ruins", "Ruínas de Solaceon"),
    ("Ruin Maniac Cave", "Caverna do Maníaco por Ruínas"),
    ("Maniac Tunnel", "Túnel do Maníaco"),
    ("Great Marsh", "Grande Pântano"),
    ("Hotel Grand Lake", "Hotel Grande Lago"),
    ("Amity Square", "Praça da Amizade"),
    ("Lost Tower", "Torre Perdida"),
    ("Iron Island", "Ilha de Ferro"),
    ("Ilha do Ferro", "Ilha de Ferro"),
    ("Newmoon Island", "Ilha Lua Nova"),
    ("Fullmoon Island", "Ilha Lua Cheia"),
    ("Sendoff Spring", "Fonte da Despedida"),
    ("Turnback Cave", "Caverna do Retorno"),
    ("Snowpoint Temple", "Templo de Snowpoint"),
    ("Victory Road", "Caminho da Vitória"),
    ("Fight Area", "Área de Luta"),
    ("Survival Area", "Área de Sobrevivência"),
    ("Resort Area", "Área de Resort"),
    ("Battle Park", "Parque de Batalha"),
    ("Battle Tower", "Torre de Batalha"),
    ("Stark Mountain", "Montanha Stark"),
    ("Seabreak Path", "Caminho Quebra-Mar"),
    ("Flower Paradise", "Paraíso Florido"),
    ("Ramanas Park", "Parque Ramanas"),
    ("Renegade Park", "Parque Ramanas"),
    ("Parque Renegado", "Parque Ramanas"),
    ("Parque Renegade", "Parque Ramanas"),
    ("Grand Underground", "Grande Subsolo"),
    ("Grande Subterrâneo", "Grande Subsolo"),
    ("Pokétch Company", "Companhia Pokétch"),
    ("Trainers’ School", "Escola de Treinadores"),
    ("Trainers' School", "Escola de Treinadores"),
    ("Mining Museum", "Museu de Mineração"),
    ("Cycle Shop", "Loja de Bicicletas"),
    ("Contest Hall", "Salão de Concursos"),
    ("Pokémon Day Care", "Creche Pokémon"),
    ("Galactic HQ", "Sede da Equipe Galáctica"),
    ("Team Galactic", "Equipe Galáctica"),
    ("Vista Lighthouse", "Farol da Vista"),
    ("Sunyshore Market", "Mercado de Sunyshore"),
    ("Pokémon Mansion", "Mansão Pokémon"),
    ("Footstep House", "Casa das Pegadas"),
    ("Canalave Library", "Biblioteca de Canalave"),
    ("Lavaridge Town", "Vila Lavaridge"),
    ("Shoal Cave", "Caverna dos Baixios"),
    ("Lumiose City", "Cidade de Lumiose"),
    ("Kiloude City", "Cidade de Kiloude"),
    ("Kanto Room", "Sala de Kanto"),
    ("Johto Room", "Sala de Johto"),
    ("Soul Room", "Sala da Alma"),
    ("Rainbow Room", "Sala do Arco-Íris"),
    ("Squall Room", "Sala da Tormenta"),
    ("Oceanic Room", "Sala Oceânica"),
    ("Tectonic Room", "Sala Tectônica"),
    ("Stratospheric Room", "Sala Estratosférica"),
    ("Genome Room", "Sala do Genoma"),
    ("Discovery Room", "Sala da Descoberta"),
    ("Distortion Room", "Sala da Distorção"),
]


def aplicar_fixes_texto(texto: str) -> str:
    if not texto:
        return texto
    for pat, repl in COMPILED_ACCENT_FIXES:
        texto = pat.sub(repl, texto)
    for src, dst in PLACE_TEXT_SYNC:
        if src in texto:
            texto = texto.replace(src, dst)
    # Rotas em inglês ("Route 201" -> "Rota 201")
    texto = re.sub(r"\bRoute (\d{3})\b", r"Rota \1", texto)
    return texto


def compilar_autoral(repo_dir: str) -> None:
    dic_dir = os.path.join(repo_dir, "dicionarios")
    base_bundle = os.path.join(
        repo_dir,
        "extracted_luminescent",
        "Dpr_Data",
        "StreamingAssets",
        "AssetAssistant",
        "Message",
        "english",
    )

    with open(os.path.join(dic_dir, "moves_ptbr.json"), "r", encoding="utf-8") as f:
        moves_pt = json.load(f)
    with open(os.path.join(dic_dir, "abilities_ptbr.json"), "r", encoding="utf-8") as f:
        abilities_pt = json.load(f)
    with open(
        os.path.join(dic_dir, "places_speakers_trainers_ptbr.json"),
        "r",
        encoding="utf-8",
    ) as f:
        pst_pt = json.load(f)
    with open(
        os.path.join(dic_dir, "items_and_misc_ptbr.json"), "r", encoding="utf-8"
    ) as f:
        items_pt = json.load(f)
    with open(
        os.path.join(dic_dir, "dialogue_and_ui_fixes_ptbr.json"), "r", encoding="utf-8"
    ) as f:
        dlg_fixes = json.load(f)

    # Carregar nomes originais de golpes em inglês para sincronizar citações em diálogos/batalhas
    moves_en_path = os.path.join(dic_dir, "moves_en.json")
    if not os.path.isfile(moves_en_path):
        moves_en_path = os.path.join(repo_dir, "work", "inputs", "moves_en.json")
    with open(moves_en_path, "r", encoding="utf-8") as f:
        moves_en = json.load(f)

    move_en_to_pt = {}
    for k, en_name in moves_en.items():
        pt_name = moves_pt.get(k, "")
        if en_name and pt_name and en_name != pt_name and not en_name.startswith("—"):
            move_en_to_pt[en_name] = pt_name

    env = UnityPy.load(base_bundle)

    stats_por_arquivo = {}
    total_labels_modificados = 0

    for obj in env.objects:
        if obj.type.name != "MonoBehaviour":
            continue
        tree = obj.read_typetree()
        fname = tree.get("m_Name", "")
        mod_count = 0

        for ld in tree.get("labelDataArray", []):
            lname = ld.get("labelName", "")
            if not lname:
                continue
            words = ld.get("wordDataArray", [])
            if not words:
                continue
            font_size = ld.get("styleInfo", {}).get("fontSize", 42)
            old_strs = [w.get("str", "") for w in words]
            new_strs = list(old_strs)

            # 1. Dicionários diretos de listas (pst_pt, dlg_fixes, SS_OPTION_OVERRIDE)
            if fname == "english_ss_option" and lname in SS_OPTION_OVERRIDE:
                cand = SS_OPTION_OVERRIDE[lname]
                if len(cand) == len(new_strs):
                    new_strs = list(cand)
            elif fname in pst_pt and lname in pst_pt[fname]:
                cand = pst_pt[fname][lname]
                if isinstance(cand, list) and len(cand) == len(new_strs):
                    new_strs = list(cand)
                elif isinstance(cand, str) and len(new_strs) == 1:
                    new_strs = [cand]
            elif fname in dlg_fixes and lname in dlg_fixes[fname]:
                cand = dlg_fixes[fname][lname]
                if isinstance(cand, list) and len(cand) == len(new_strs):
                    new_strs = list(cand)

            # 2. Golpes e Habilidades
            if fname == "english_ss_wazaname" and lname in moves_pt:
                new_strs[0] = moves_pt[lname]
            elif fname == "english_ss_tokusei" and lname in abilities_pt:
                new_strs[0] = abilities_pt[lname]

            # 3. Itens e Miscelânea
            elif fname in ("english_ss_itemname", "english_ss_itemname_acc"):
                if lname in items_pt.get("english_ss_itemname", {}):
                    new_strs[0] = items_pt["english_ss_itemname"][lname]
            elif fname in (
                "english_ss_itemname_classified",
                "english_ss_itemname_acc_classified",
            ):
                if lname in items_pt.get("english_ss_itemname_classified", {}):
                    new_strs[0] = items_pt["english_ss_itemname_classified"][lname]
                elif lname in items_pt.get("english_ss_itemname", {}):
                    new_strs[0] = items_pt["english_ss_itemname"][lname]
            elif fname in (
                "english_ss_itemname_plural",
                "english_ss_itemname_plural_classified",
            ):
                if lname in items_pt.get("english_ss_itemname_plural", {}):
                    new_strs[0] = items_pt["english_ss_itemname_plural"][lname]
            elif fname == "english_ss_nuts_name":
                if lname in items_pt.get("english_ss_nuts_name", {}):
                    new_strs[0] = items_pt["english_ss_nuts_name"][lname]
            elif fname in ("english_dlp_poffin_name", "english_dlp_poffin_name_acc"):
                if lname in items_pt.get("english_dlp_poffin_name", {}):
                    new_strs[0] = items_pt["english_dlp_poffin_name"][lname]
            elif fname == "english_dlp_poffin_name_plural":
                if lname in items_pt.get("english_dlp_poffin_name_plural", {}):
                    new_strs[0] = items_pt["english_dlp_poffin_name_plural"][lname]
            elif fname == "english_dp_stickers_name":
                if lname in items_pt.get("english_dp_stickers_name", {}):
                    new_strs[0] = items_pt["english_dp_stickers_name"][lname]
            elif fname == "english_dp_stickers_name_plural":
                if lname in items_pt.get("english_dp_stickers_name_plural", {}):
                    new_strs[0] = items_pt["english_dp_stickers_name_plural"][lname]
            elif fname == "english_dlp_park_name":
                if lname in items_pt.get("english_dlp_park_name", {}):
                    new_strs[0] = items_pt["english_dlp_park_name"][lname]
            elif fname == "english_dlp_park_name_plural":
                if lname in items_pt.get("english_dlp_park_name_plural", {}):
                    new_strs[0] = items_pt["english_dlp_park_name_plural"][lname]
            elif fname == "english_ss_fld_dressup_item_name":
                if lname in items_pt.get("english_ss_fld_dressup_item_name", {}):
                    new_strs[0] = items_pt["english_ss_fld_dressup_item_name"][lname]
            elif fname in (
                "english_dp_underground_name",
                "english_dp_underground_name_acc",
                "english_dp_underground_name_classified",
                "english_dp_underground_name_acc_classified",
            ):
                if lname in items_pt.get("english_dp_underground_name", {}):
                    new_strs[0] = items_pt["english_dp_underground_name"][lname]
            elif fname in (
                "english_dp_underground_name_plural",
                "english_dp_underground_name_plural_classified",
            ):
                if lname in items_pt.get("english_dp_underground_name_plural", {}):
                    new_strs[0] = items_pt["english_dp_underground_name_plural"][lname]

            # 4. Em english_ss_btl_attack, traduzir nomes de golpes embutidos ("usou After You!")
            if fname == "english_ss_btl_attack":
                for i, s in enumerate(new_strs):
                    if "usou " in s and s.endswith("!"):
                        prefix, rest = s.split("usou ", 1)
                        mname = rest[:-1].strip()
                        if mname in move_en_to_pt:
                            new_strs[i] = f"{prefix}usou {move_en_to_pt[mname]}!"

            # 5. Passo global de correção de acentos e sincronização de locais/cidades/termos
            for i, s in enumerate(new_strs):
                if s:
                    new_strs[i] = aplicar_fixes_texto(s)
            for i in range(len(new_strs) - 1):
                if new_strs[i].endswith("Parque") and new_strs[i + 1].startswith("Renegado"):
                    new_strs[i + 1] = "Ramanas" + new_strs[i + 1][len("Renegado"):]
                elif new_strs[i].endswith("Renegade") and new_strs[i + 1].startswith("Park"):
                    new_strs[i] = new_strs[i][:-len("Renegade")] + "Parque"
                    new_strs[i + 1] = "Ramanas" + new_strs[i + 1][len("Park"):]

            if new_strs != old_strs:
                mod_count += 1
                total_labels_modificados += 1
                for i, w in enumerate(words):
                    w["str"] = new_strs[i]
                    if w.get("tagIndex", -1) == -1:
                        w["strWidth"] = recalcular_str_width(new_strs[i], font_size)

        if mod_count > 0:
            obj.save_typetree(tree)
        stats_por_arquivo[fname] = mod_count

    out_bundle_dir = os.path.join(
        repo_dir,
        "saida_autoral",
        "Dpr_Data",
        "StreamingAssets",
        "AssetAssistant",
        "Message",
    )
    os.makedirs(out_bundle_dir, exist_ok=True)
    out_bundle_path = os.path.join(out_bundle_dir, "english")
    with open(out_bundle_path, "wb") as f:
        f.write(env.file.save(packer="original"))

    zip_path = os.path.join(repo_dir, "english-ptbr-autoral-v2.0.zip")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(
            out_bundle_path,
            arcname="Dpr_Data/StreamingAssets/AssetAssistant/Message/english",
        )

    relatorio_path = os.path.join(repo_dir, "relatorio_autoral.md")
    with open(relatorio_path, "w", encoding="utf-8") as rf:
        rf.write("# Relatório da Tradução Autoral PT-BR v2.0 (uDPR / BDSP)\n\n")
        rf.write(
            f"- **Total de labels atualizados/traduzidos sobre a base:** {total_labels_modificados}\n"
        )
        rf.write(f"- **Bundle gerado:** `{out_bundle_path}`\n")
        rf.write(f"- **Pacote pronto para extrair no jogo (uDPR):** `{zip_path}`\n\n")
        rf.write("## Arquivos Modificados na Revisão Autoral\n\n")
        rf.write("| Arquivo (`MsbtData`) | Labels Aprimorados |\n")
        rf.write("| :--- | ---: |\n")
        for fn, cnt in sorted(stats_por_arquivo.items()):
            if cnt > 0:
                rf.write(f"| `{fn}` | {cnt} |\n")

    print(f"Compilação concluída com sucesso!")
    print(f"Total de labels aprimorados: {total_labels_modificados}")
    print(f"Bundle salvo em: {out_bundle_path}")
    print(f"ZIP salvo em: {zip_path}")
    print(f"Relatório salvo em: {relatorio_path}")


if __name__ == "__main__":
    base_repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    compilar_autoral(base_repo)
