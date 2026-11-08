# Decisioni tecniche — Ripeti (gym-timer)

Registro delle decisioni prese durante lo sviluppo. Una voce per decisione: contesto, scelta,
motivo, alternative scartate. Le decisioni marcate **DA VALIDARE** dipendono da verifiche che
si possono fare solo sul dispositivo reale.

---

## D-001 — Nome, tagline, identità visiva (Fase 0)

**Decisione:** nome **Ripeti**, tagline *"Intervalli, senza pensieri."*

**Motivo:** è italiano, corto, memorabile, descrive l'azione centrale dell'app (ripetere i round)
e non ha alcuna somiglianza con "Timer Plus" né con altri timer di palestra. Le alternative
"Quaranta" (legherebbe l'app ai 40 secondi, mentre servono durate variabili) e "Sprint Lab"
(nome inflazionato, e il blu elettrico è meno leggibile a distanza del verde acido) sono state
scartate.

## D-002 — Palette (Fase 0)

| Ruolo | HEX | Uso |
|---|---|---|
| Sfondo | `#0B0D0E` | fondo app (nero quasi neutro, non puro, meno affaticante) |
| Superficie | `#14181A` | card, barre, separatori pieni |
| Testo | `#F5F7F5` | numeri e testi principali (contrasto ~18:1 su sfondo) |
| Testo attenuato | `#8B9694` | etichette secondarie |
| Lavoro | `#C6FF3D` | fase di lavoro (verde acido, altissima visibilità) |
| Riposo | `#4DA3FF` | recupero tra round (azzurro, freddo: "rallenta") |
| Preparazione | `#FFB020` | "preparati" / countdown iniziale (ambra, attenzione) |

**Regola d'uso:** il colore identifica la *fase*, non il numero. Il numero del countdown resta
sempre bianco (`#F5F7F5`): è il dato che si guarda a 3 metri e non deve mai perdere contrasto.
Il colore di fase va su etichetta, bordo/alone e barra di avanzamento.

**Motivo:** distinguere lavoro e riposo con due colori percettivamente lontani (verde caldo /
azzurro freddo) permette di capire lo stato con la coda dell'occhio, senza leggere il testo.
Solo tema dark: richiesta esplicita (in palestra, ambiente a luce bassa o media).

## D-003 — Tipografia (Fase 0)

Font di sistema Apple (`-apple-system` / `SF Pro`), **nessun font scaricato**. Numeri del
countdown con `font-variant-numeric: tabular-nums` così le cifre non cambiano larghezza e il
numero non "balla" ogni secondo.

**Motivo:** zero richieste di rete a runtime, zero font da scaricare, resa identica a quella
nativa iOS. Un webfont per un solo numero grande non ripaga il peso e il rischio di FOUT.

## D-004 — Stack: Vite + TypeScript, nessun framework (Fase 0)

**Decisione:** Vite + TypeScript puro + Vitest (test unitari). Framework UI: nessuno.
Playwright (test E2E) verrà aggiunto in **Fase 4**, non prima: scarica browser (~centinaia di MB)
e in Fase 0 non serve a nulla.

**Motivo:** la parte che *deve* essere corretta è la macchina a stati del timer, e per testarla
servono moduli, tipi e un clock finto — non un framework. Preact non aggiunge nulla per ~5
schermate con un solo grande numero. Vanilla senza build avrebbe reso impossibile la Fase 4
(unit test seri sulla logica del tempo).

**Conseguenza pratica:** serve una build. Da ciò deriva D-006 (CI) e il `base` di Vite impostato
su `/gym-timer/` (GitHub Pages serve il sito in sottocartella).

## D-005 — Hosting: GitHub Pages (Fase 0)

**Decisione:** GitHub Pages dal repository, pubblicazione via GitHub Actions.

**Motivo:** stesso posto del codice, HTTPS gratuito, nessun account o servizio aggiuntivo da
mantenere o dismettere, migrazione altrove in pochi minuti se cambiamo idea.

**Limite noto e accettato:** Pages non permette header HTTP personalizzati (niente CSP fatta a
mano, niente `Cache-Control` sul service worker). Se un giorno servissero, si passa a Cloudflare
Pages senza riscrivere l'app.

## D-006 — CI: GitHub Actions (build + test + deploy) (Fase 0)

**Decisione:** una Action a ogni push su `main`: installa → test → build → pubblica su Pages.

**Motivo:** con Vite la build è obbligatoria; mettere test e deploy nello stesso passaggio
impedisce di pubblicare codice non testato. Se un test fallisce, il sito live **non** viene
aggiornato: `main` resta sempre deployabile.

## D-007 — Workflow git: commit diretti su `main` (Fase 0)

**Decisione:** nessuna pull request, nessun branch di sviluppo. Un tag per fase (`fase-0`,
`fase-1`, ...).

**Motivo:** progetto a singolo sviluppatore; le PR aggiungono cerimonia senza valore. La rete di
sicurezza sono i test in CI, non la revisione. Se in futuro servirà sperimentare, si userà un
branch per quella modifica soltanto.

## D-008 — Autenticazione GitHub: PAT in `.git-token` (Fase 0)

**Decisione:** token personale classico (scope `repo` + `workflow`) in `.git-token`, ignorato da
git (`chmod 600`), usato per-comando con `-c credential.helper='' -c http.extraHeader=...`.

**Motivo:** `gh` non è installato e installarlo richiederebbe Homebrew (difficile da
disinstallare, contro la preferenza espressa). Il token **non** viene mai messo nell'URL del
remote: finirebbe in `.git/config` e nella cronologia della shell.

## D-009 — Tipo di sessione audio: `playback` come default, decisione finale sul dispositivo (Fase 0)

**Stato:** implementazione `playback` (come da mandato) + **pannello di debug** con un pulsante
per tipo (`playback`, `transient`, `ambient`).

**Motivo:** su iOS i due obiettivi del mandato sono in tensione:
- `playback` → i beep si sentono con lo switch silenzioso attivo, **ma mette in pausa la musica**
  di altre app (comportamento dichiarato da chi ha implementato un DAW web su iOS);
- `ambient` → si mescola con la musica, **ma viene mutato** dallo switch silenzioso;
- `transient` → mescola, comportamento con lo switch silenzioso **non documentato**.

Nessuna fonte permette di promettere "beep udibili con switch silenzioso ON *e* musica che
continua". La scelta va fatta con una misura sul telefono, non a tavolino.
**DA VALIDARE** sul dispositivo dell'utente.

## D-010 — Modello di timing: deadline assoluta in `Date.now()` (Fase 0)

**Decisione:** nessun conteggio a tick. Si salva `deadline = Date.now() + durata` e a ogni frame
si ricalcola `rimanente = deadline - Date.now()`. Dopo `visibilitychange` → `visible` lo stato
(fase, round, tempo) viene **ricalcolato** dalla deadline, non ripreso da dove era rimasto.
`performance.now()` non si usa. Il delta viene "clampato" per non fidarsi di salti d'orologio.

**Motivo:** iOS sospende la pagina quando lo schermo si blocca o si cambia app: i tick si perdono
in silenzio. La deadline assoluta sopravvive alla sospensione; un contatore no.

## D-011 — Lighthouse: niente "punteggio PWA" (Fase 0)

**Decisione:** in Fase 3 si misurano performance / accessibility / best practices; la
installabilità si verifica a mano con una lista di controlli.

**Motivo:** la categoria PWA è stata **rimossa** da Lighthouse 12 (Chrome 126+; "PWA Category
Removal" nel changelog ufficiale). Promettere un "punteggio PWA" sarebbe stato un requisito
impossibile da consegnare.

## D-012 — Icone generate da script, non disegnate a mano (Fase 0)

**Decisione:** le icone sono prodotte da uno script Python che scrive PNG **senza dipendenze**
(codifica PNG con `zlib`, presente nella libreria standard), partendo da forme geometriche.
Nel repository restano sia lo script sia il sorgente SVG, quindi le icone sono riproducibili e
modificabili.

**Motivo:** su questo Mac non ci sono Homebrew né Pillow; installarli per 4 file PNG sarebbe
spreco. Con uno script nel repo le icone si rigenerano con un comando e non sono "binari
misteriosi" che nessuno sa più rifare.

## D-013 — Limiti accettati come strutturali (Fase 0)

Documentati nel README, non aggirati:

1. **Niente beep a schermo bloccato.** iOS sospende la pagina: `setTimeout`, `requestAnimationFrame`
   e i suoni Web Audio pianificati in anticipo non partono. Non esiste API per suonare da una PWA
   a schermo spento.
2. **`navigator.vibrate` non esiste su iOS** (MDN). Solo feature detection e no-op: nessuna
   funzione dell'app dipende dalla vibrazione.
3. **Wake lock = "best effort".** Lo schermo resta acceso *se* il telefono non è in risparmio
   energetico; il sistema può negare o rilasciare il lock. Promessa onesta, non assoluta.

**Assunzioni da validare** (non verificabili in un giorno):
- una web app installata in home screen non è soggetta alla cancellazione dei dati a 7 giorni
  dell'ITP (coerente con la documentazione WebKit, da confermare empiricamente);
- **DA VALIDARE** la rotazione in standalone su iOS 26.7.1 (vedi D-014).

## D-014 — Landscape: layout ricomposto + fallback interno (Fase 0)

**Decisione:** il layout landscape è progettato a sé (numeri e controlli affiancati, non ruotati).
Se sul dispositivo la rotazione in standalone non avvenisse, l'app offre un comando esplicito per
forzare il layout orizzontale.

**Motivo:** non esiste documentazione affidabile e recente sul comportamento di rotazione delle
web app installate in home screen su iOS 26. **DA VALIDARE** sul dispositivo.
