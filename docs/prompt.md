Esegui la sezione "COME INIZIARE" del mandato che segue, alla lettera.
Non iniziare la FASE 0 finché non ti ho dato l'ok.
Prima di tutto, elencami i file presenti nella working directory di questa sessione.

--- MANDATO ---

Sei il lead developer e il project manager tecnico di questo progetto. Lavori con me in italiano.
Io non sono uno sviluppatore: spiegami le cose in linguaggio semplice, senza gergo non spiegato.

# OBIETTIVO
Sviluppare una Progressive Web App (PWA) installabile su iPhone che funzioni come timer da palestra
a intervalli. Tutto in HTML/CSS/JavaScript: nessun account Apple Developer, nessuna build nativa,
nessuna app store. Hosting statico + installazione in home screen da Safari.

Device di riferimento: iPhone 15 Plus, iOS 26.7.1 (il mio).
L'app deve funzionare come web app installata in home screen, aperta in standalone (senza barre Safari).

# RIFERIMENTO UI
Prendi come riferimento funzionale e visivo questa app:
https://apps.apple.com/it/app/timer-plus-timer-per-workout/id1279716547
Leggi la pagina e le recensioni (anche quelle critiche: indicano cosa manca e cosa irrita).
Voglio FEDELTÀ ALTA: stessa struttura di schermate, stessa gerarchia visiva, stessa idea di
numeri giganti leggibili da lontano, stessa logica di colori per fase.
MA: asset originali (icone, illustrazioni, logo, nome dell'app, palette derivata ma non copiata).
Nessun file o grafico preso da quella app. Nessun nome che possa confondersi con "Timer Plus".

# MODALITÀ DI LAVORO (VINCOLANTE)
- Lavori a FASI con GATE. Alla fine di ogni fase ti FERMI, mi mostri un riepilogo in italiano
  semplice (cosa hai fatto, cosa hai deciso, cosa mi serve da te) e aspetti la mia approvazione
  esplicita. Non passi mai alla fase successiva senza un mio "ok".
- Prima di assumere qualcosa, chiedi. Non inventare requisiti.
- Se una decisione è tecnica, presentami 2-3 opzioni con PRO/CONTRO in termini pratici
  (tempo, complessità per me, rischio) + UNA RACCOMANDAZIONE, poi lascia decidere a me.
- Se citi uno strumento o un concetto (CI, service worker, bundler, test E2E...), spiega in 1-2
  frasi a cosa serve e cosa comporta concretamente per me. Non dare per scontato che io sappia.
- Non affermare cose non vere su Safari/iOS. Se non sei sicuro, verifica (MDN, documentazione
  WebKit/Apple) e dimmi la fonte. Preferisci "da verificare sul mio iPhone" a un'affermazione
  inventata.
- Distingui sempre ciò che puoi verificare tu (codice, test, build, Lighthouse) da ciò che
  posso verificare solo io sul device (audio, wake lock, installazione, rotazione, musica).
  Per la seconda categoria scrivi checklist numerate con esito atteso.
- Tieni un registro delle decisioni in `docs/DECISIONS.md` (italiano) e dei requisiti in
  `REQUIREMENTS.md`.
- Ogni fase si chiude con un commit su `main` e un tag (`fase-0`, `fase-1`, `fase-2`...).
- Lavora in modo incrementale: dopo ogni fase l'app deve essere in uno stato funzionante.
- Usa la tua skill `github-auth` (o la skill `github`) per autenticarti e creare il repository.

# FASE 0 — SETUP E DECISIONI TECNICHE (gate)
1) GitHub: crea un repository nuovo, pubblico, sul mio account personale. Nome provvisorio
   `gym-timer` (verrà deciso al punto 2). Licenza MIT. README iniziale.
   Configura GitHub Pages per pubblicare l'app.
   Se serve autenticazione, guidami passo-passo (token o `gh auth login`) spiegandomi cosa sto
   facendo e quali permessi concedere.
   Sposta il file `prompt.txt` (il mio mandato) in `docs/prompt.md` e committalo: serve come
   tracciabilità della specifica di partenza.
2) Brainstorming con me: nome definitivo dell'app, tagline, icona (originale, generata),
   palette colori per le fasi, stile tipografico. Proponimi 3 opzioni con una raccomandazione.
   Preparerai poi le icone nei formati 180x180, 192x192, 512x512 e una maskable.
3) Stack: presentami le opzioni con pro/contro pratici e raccomandane una.
   (a) Vanilla JS, pochi file statici, zero build
   (b) Vite + TypeScript + Preact, con Vitest e Playwright
   (c) Vite + TypeScript senza framework, con Vitest e Playwright
   Considera: tempo di sviluppo, testabilità della logica del timer, semplicità per me,
   facilità di deploy su Pages, peso dell'app.
4) Hosting: GitHub Pages vs Cloudflare Pages vs Netlify. Pro/contro reali per questo progetto
   (HTTPS, dominio, semplicità, cosa succede se cambio idea) + raccomandazione.
5) Deploy automatico / CI: spiegami in parole semplici cosa comporta, poi proponi la versione
   minima (es. una GitHub Action che builda e pubblica su Pages a ogni push su `main`).
   Raccomanda se attivarla o no.
6) Workflow git: la mia preferenza è commit diretti su `main`, senza pull request, perché è la
   strada più semplice. Confermami che va bene o spiegami perché no.
Output della fase: repository creato, `docs/DECISIONS.md`, `docs/FASE-0.md` con le decisioni prese.
Poi FERMATI e chiedimi approvazione.

# FASE 1 — REQUISITI (gate)
1) Analizza il riferimento (pagina App Store + recensioni) ed estrai:
   inventario delle schermate, gerarchia visiva, palette, tipografia, pattern di interazione,
   cosa gli utenti apprezzano e cosa criticano.
2) INTERVISTAMI. Fai domande numerate, massimo 8 per volta, con opzioni dove possibile e con la
   tua raccomandazione. Argomenti da coprire (aggiungi ciò che ritieni utile):
   - etichette per i round (es. "burpees") e nome del workout: dentro o fuori?
   - durate diverse per round diversi (es. 30s, 45s, 60s): quanto spingere su questa feature?
   - riposo tra i cicli: come si configura?
   - skip round, pausa/riprendi, +1/-1 round a caldo: comportamento esatto
   - countdown di preparazione ("get ready") e cooldown finale: durata configurabile?
   - come salvare/caricare/eliminare i preset: quanti, con che nome, con che persistenza
   - comportamento audio: quanti beep, in quali momenti, volume, tono, beep di 3-2-1
   - comportamento in portrait e landscape (cosa cambia nel layout)
   - cosa deve succedere se cambio app o blocco lo schermo durante un workout
   - definizione di "prototipo finito" (cosa deve esserci perché io dica "ok, funziona")
   - piano di test: cosa testare in automatico e cosa devo testare io a mano
3) Scrivi `REQUIREMENTS.md`: user stories, criteri di accettazione verificabili, fuori scope,
   assunzioni da validare.
4) Scrivi `docs/UI-SPEC.md`: schermata per schermata, layout, stati (idle, running, paused,
   finished), palette in HEX, dimensioni tipografiche, comportamento in rotazione.
   Fedeltà alta al riferimento, asset originali.
5) Presenta tutto in un riepilogo leggibile e FERMATI.

# FASE 2 — SVILUPPO (gate)
Implementa l'app secondo i requisiti approvati.
VINCOLI TECNICI OBBLIGATORI (derivano da limiti reali di iOS — non aggirarli senza dirmelo):

AUDIO
- Web Audio API. I beep devono essere GENERATI via oscillator: nessun file audio esterno, così
  l'app resta offline e leggerissima.
- Al PRIMISSIMO tap dell'utente (listener su click, `{capture: true, once: true}`) imposta
  `navigator.audioSession.type = 'playback'` e crea/riattiva l'AudioContext.
  È essenziale che avvenga in un gestore di evento utente diretto: NON dentro setTimeout,
  callback di timer o promise differite, altrimenti iOS lo ignora.
- Obiettivo: i beep devono essere udibili anche con lo switch silenzioso attivo e NON devono
  mettere in pausa la musica che sto ascoltando. Verifica empiricamente e documenta l'esito reale.
- Fai feature detection su tutto: se `audioSession` non esiste, l'app non deve rompersi.

TIMING
- Non contare i tick. Salva un timestamp assoluto di fine (Date.now() + durata) e a ogni frame
  ricalcola il tempo rimanente come differenza rispetto a Date.now().
- `performance.now()` non è affidabile per questo: può non avanzare quando il sistema sospende
  la pagina. Usa `Date.now()`.
- Dopo ogni `visibilitychange` verso "visible", riallinea immediatamente lo stato (fase corrente,
  round, tempo rimanente) invece di riprendere da dove eri rimasto.

SCHERMO
- Screen Wake Lock API (`navigator.wakeLock.request('screen')`): attivalo all'avvio del workout,
  rilascialo alla fine e in pausa lunga. Riacquisiscilo su `visibilitychange`.
  Richiede HTTPS e pagina visibile: fai feature detection e gestisci l'errore senza crash.
- Vibrazione: `navigator.vibrate` NON esiste su iOS Safari. Fai feature detection e no-op.
  Non costruire nessuna funzione che dipenda dalla vibrazione.

PWA
- `manifest.json` con nome, short_name, display standalone, start_url, theme_color,
  background_color, icone 192/512 + maskable.
- Meta tag iOS: `apple-mobile-web-app-capable`, `apple-mobile-web-app-status-bar-style`,
  `apple-touch-icon` 180x180, viewport con `viewport-fit=cover`.
- Service worker per l'offline (app shell cache-first, con strategia di aggiornamento sensata).
- Gestione delle safe area (notch / Dynamic Island / home indicator) e del fullscreen.
- Persistenza dei preset in localStorage. Nota: una web app installata in home screen non è
  soggetta alla cancellazione dei dati a 7 giorni che ITP applica ai siti normali.

UI
- Solo tema dark.
- Portrait e landscape entrambi curati (in landscape il layout deve essere ripensato, non
  semplicemente ruotato).
- Numeri del countdown giganteschi, leggibili a 2-3 metri di distanza.
- Touch target >= 44px, contrasto alto, feedback visivo immediato sui tap.
- Testi in italiano.
- Nessuna dipendenza di rete a runtime.

Deliverable: app funzionante in locale, `README.md` in italiano (cos'è, come si installa su
iPhone passo-passo, come si usa, limiti noti), `docs/ARCHITECTURE.md` (com'è organizzato il codice,
dove sta la logica del timer, come si aggiunge una funzione).
Poi FERMATI e chiedimi approvazione.

# FASE 3 — PROTOTIPO (gate)
- Pubblica l'app all'URL live e verificane l'accessibilità.
- Verifica tu: build pulita, service worker attivo, Lighthouse (categoria PWA/performance),
  nessun errore in console, funzionamento offline.
- Consegna una CHECKLIST DI TEST MANUALE numerata, da fare io sul mio iPhone, con: passi,
  esito atteso, cosa fare se non torna. Copri almeno: installazione in home screen, apertura
  standalone, beep con switch silenzioso ON, beep sopra la musica, wake lock (schermo non si
  spegne), rotazione portrait/landscape, blocco schermo durante il workout, cambio app e ritorno,
  riallineamento del timer, salvataggio e ricarica di un preset, funzionamento offline.
- Registra i risultati reali in `docs/DEVICE-NOTES.md` quando te li riporto.
- FERMATI e aspetta che io provi e ti riporti l'esito.

# FASE 4 — TEST (gate)
- Unit test sulla logica pura del timer: macchina a stati, calcolo delle fasi, sequenza
  preparazione/work/rest/rest-tra-cicli/cooldown, durate variabili per round, gestione dei
  limiti (0 round, 1 round, durata 0, preset corrotto). Usa un clock finto per testare il
  tempo senza aspettare davvero.
- Test E2E del flusso principale con clock finto (se lo stack scelto lo consente).
- Checklist manuale su device reale (già fatta in Fase 3): consolida i risultati.
- Scrivi `docs/TEST-PLAN.md` con cosa è coperto e cosa no.
- Correggi i bug trovati, uno per commit, con messaggio in inglese.
- FERMATI e mostrami i risultati.

# DEFINITION OF DONE (v1)
- Installabile in home screen e avviabile in standalone su iPhone 15 Plus / iOS 26.7.1.
- Workout completo: preparazione -> (work -> rest) x round -> rest tra cicli -> ... -> cooldown,
  con beep 3-2-1 prima di ogni transizione.
- Pausa/riprendi, skip round, +1/-1 round a caldo.
- Durate variabili per singolo round.
- Preset salvabili, caricabili, rinominabili, eliminabili (localStorage).
- Funziona offline dopo il primo caricamento.
- Lo schermo non si spegne durante il workout.
- Beep udibili con switch silenzioso attivo e sopra la musica (best effort, documentato).
- Solo dark, portrait + landscape, UI in italiano.
- README + documentazione completi in italiano.
- Test automatici verdi.
- Limiti noti documentati esplicitamente nel README.

# FUORI SCOPE v1 (non implementare, ma non precluderli)
- Guida vocale / sintesi vocale
- Cronologia e statistiche dei workout
- Stopwatch
- Notifiche push e backend
- Timer che suona a schermo spento (limite strutturale delle PWA su iOS: documentalo, non aggirarlo
  con hack non documentati)
- Vibrazione (non supportata su iOS)
- App Store, TestFlight, Capacitor, Expo, build native, account Apple Developer
- Accessibilità VoiceOver avanzata
- Account utente, cloud sync, multi-dispositivo
- Supporto nativo Android/desktop (non richiesto, ma non romperlo)

# CONVENZIONI
- Codice, nomi di variabili e funzioni, commenti nel codice, messaggi di commit, issue: INGLESE.
- Conversazione con me, README e documentazione in `docs/`: ITALIANO.
- Commit con Conventional Commits (feat:, fix:, docs:, test:, chore:).
- Nessun asset, icona, nome o grafico copiato da app di terze parti.

# COME INIZIARE
1) Confermami in poche righe che hai capito il progetto, il modo di lavorare a fasi e i vincoli.
2) Elencami le cose su cui hai dei dubbi o che secondo te non stanno in piedi tecnicamente
   su iOS 26.7.1, PRIMA di implementarle.
3) Presentami il piano dettagliato della FASE 0 e le domande di brainstorming.
4) Aspetta il mio "ok" prima di procedere.

Se durante una fase scopri che qualcosa scritto qui è tecnicamente sbagliato o irrealizzabile,
segnalamelo subito e proponi l'alternativa: non implementare male qualcosa in silenzio.