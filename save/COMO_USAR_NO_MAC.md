# Save Atual — Pokémon Brilliant Diamond (PT-BR)

Última sincronização a partir do Windows: **31/10/2026 16:52**

## Arquivos incluídos
- `nn/save/0100000011D90000/00000000000000010000000000000000/SaveData.bin` — Save principal
- `nn/save/0100000011D90000/00000000000000010000000000000000/Backup.bin` — Save de backup automático
- `pc_settings.ini` — Configurações de tela e controles adaptados de teclado
- `save-atual-bdsp.zip` — Pacote compactado pronto para extrair

---

## Como colocar o save no Mac

### Opção 1: Versão nativa `uDPR` compilada para macOS (`Dpr.app`)
No macOS, o Unity lê e grava os saves em `~/Library/Application Support/DefaultCompany/Dpr/`.

Abra o **Terminal** no Mac (dentro da pasta deste repositório) e execute:

```bash
mkdir -p ~/Library/Application\ Support/DefaultCompany/Dpr
cp -R save/nn ~/Library/Application\ Support/DefaultCompany/Dpr/
cp save/pc_settings.ini ~/Library/Application\ Support/DefaultCompany/Dpr/
```

*(Ou pelo **Finder**: aperte `Cmd + Shift + G`, digite `~/Library/Application Support/DefaultCompany/Dpr` e cole a pasta `nn` e o arquivo `pc_settings.ini` lá dentro.)*

### Opção 2: Rodando a build de Windows no Mac (via Boot Camp, CrossOver ou Wine)
- **Boot Camp (Windows nativo no Mac Intel):** cole `nn` e `pc_settings.ini` em `%USERPROFILE%\AppData\LocalLow\DefaultCompany\Dpr\`.
- **CrossOver / Wine:** cole `nn` e `pc_settings.ini` dentro da garrafa (bottle) em `drive_c/users/crossover/AppData/LocalLow/DefaultCompany/Dpr/`.

### Opção 3: Emulador de Switch no Mac (Ryujinx)
Como o `uDPR` salva no formato original do Nintendo Switch, o save também é 100% compatível com o Ryujinx:
1. Clique com o botão direito no jogo no Ryujinx e escolha **Open User Save Directory**.
2. Cole os arquivos `SaveData.bin` e `Backup.bin` diretamente nessa pasta.
