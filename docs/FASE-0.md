# Fase 0 — Setup e decisioni tecniche

Data: 8 novembre 2026 · Stato: **completata in attesa di approvazione**

## Cosa è stato fatto

1. **Repository GitHub** `mcarame/gym-timer` — pubblico, licenza MIT, creato dall'utente
   dall'interfaccia web (scelta sua, per non dare a un agente il permesso di creare repository
   a suo nome).
2. **Mandato archiviato:** il testo della specifica iniziale è in `docs/prompt.md`, committato
   così com'era, per tracciabilità.
3. **Stack installato:** Vite + TypeScript + Vitest. Build funzionante, `npm run build` e
   `npm test` verificati (dettagli sotto).
4. **Identità visiva:** nome *Ripeti*, palette a tre colori di fase, icone originali generate da
   script (`scripts/make-icons.py`) nei formati 180, 192, 512 e maskable.
5. **Scheletro dell'app:** `index.html` con tutti i meta tag iOS necessari, gestione safe area
   in CSS, manifest PWA con `display: standalone`.
6. **CI:** Action `.github/workflows/deploy.yml` (type-check → test → build → pubblica su Pages).
7. **Registro decisioni:** `docs/DECISIONS.md` con 14 voci motivate.

## Decisioni prese (dettaglio in `docs/DECISIONS.md`)

| Ambito | Scelta | Perché in una riga |
|---|---|---|
| Nome | **Ripeti** | italiano, corto, descrive l'azione, zero confusione con "Timer Plus" |
| Palette | verde `#C6FF3D` lavoro, azzurro `#4DA3FF` riposo, ambra `#FFB020` preparazione | si distingue la fase con la coda dell'occhio |
| Stack | Vite + TypeScript, nessun framework, Vitest | la logica del tempo va testata con clock finto; un framework non serve |
| Hosting | GitHub Pages | stesso posto del codice, zero servizi extra da mantenere |
| CI | sì, test + build + deploy a ogni push su `main` | se un test fallisce il sito non si aggiorna |
| Git | commit diretti su `main`, un tag per fase | progetto a una persona; la rete di sicurezza sono i test |
| Icone | generate da script Python senza dipendenze | niente Homebrew/Pillow per 4 PNG; icone riproducibili |

## Correzioni al mandato (proposte prima di implementare)

1. **"Lighthouse categoria PWA"** non esiste più: la categoria è stata rimossa in Lighthouse 12.
   Sostituita da performance/accessibility/best practices + controlli di installabilità a mano.
2. **"Beep con switch silenzioso ON e senza mettere in pausa la musica"** non è garantibile con
   una sola impostazione: `playback` buca lo switch ma mette in pausa la musica, `ambient` fa il
   contrario, `transient` non è documentato. Rimandato a un test empirico sul dispositivo.

## Cosa serve dall'utente

- Approvazione della fase.
- In seguito (Fase 2/3): il test del pannello audio sul telefono, per decidere il tipo di sessione
  definitivo.

## Verifiche fatte da me

- `npm run build` completa senza errori.
- `npm test` (Vitest) parte e non trova test: atteso in questa fase.
- Le icone si aprono e sono leggibili a 192px (controllate anche a 512px).
- `manifest.webmanifest` valido come JSON, con 192 + 512 + maskable.

## Verifiche che può fare solo l'utente

Nessuna in questa fase: l'app non è ancora pubblicata. Dalla Fase 3 in poi.
