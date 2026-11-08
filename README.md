# Ripeti — timer a intervalli per l'allenamento

*Intervalli, senza pensieri.*

Web app (PWA) da palestra: preparazione → serie di round di lavoro con recupero → recupero tra i
cicli → defaticamento, con beep di preavviso 3-2-1. Si installa sulla home screen dell'iPhone
da Safari e si apre a schermo intero, senza App Store e senza account Apple Developer.
Funziona offline dopo il primo caricamento.

> **Stato del progetto:** Fase 0 (setup) completata. Lo scheletro è online su
> **https://mcarame.github.io/gym-timer/** — per ora è solo la pagina di prova: il timer arriva
> dalla Fase 2. Vedi `docs/FASE-0.md` per cosa è stato deciso e perché.

## Requisiti

- iPhone con iOS 16.4 o successivo (serve Screen Wake Lock per tenere lo schermo acceso).
- Il target dichiarato e testato è **iPhone 15 Plus, iOS 26.7.1**.
- Installazione solo da **Safari** (Chrome e Firefox su iOS non offrono "Aggiungi alla home").

## Come si installa su iPhone

1. Apri l'indirizzo dell'app in **Safari**.
2. Tocca il pulsante **Condividi** (il quadrato con la freccia verso l'alto).
3. Scorri e scegli **Aggiungi alla schermata Home**.
4. Conferma con **Aggiungi**. Comparirà l'icona "Ripeti".
5. Apri l'app **dall'icona** (non da Safari): così parte a schermo intero, in standalone.

Dopo il primo avvio l'app resta disponibile anche senza rete.

## Come si usa

*Da completare in Fase 2.* Schema previsto: si sceglie o si crea un preset (round, durata lavoro,
recupero, numero di cicli, preparazione, defaticamento), si avvia, e durante il workout si può
mettere in pausa, saltare un round e aggiungere o togliere un round al volo.

## Sviluppo

```bash
npm install        # una volta sola
npm run dev        # server locale con ricarica automatica
npm test           # test unitari (logica del timer)
npm run build      # build di produzione in dist/
npm run preview    # anteprima della build, come sarà online
```

Stack: Vite + TypeScript, nessun framework, test con Vitest. Le decisioni tecniche e il perché di
ognuna stanno in `docs/DECISIONS.md`.

## Limiti noti (strutturali, non bug)

1. **Niente beep a schermo bloccato.** Quando iOS blocca lo schermo sospende la pagina: i timer e
   i suoni pianificati non partono. Nessuna PWA può suonare a schermo spento.
2. **Lo schermo resta acceso "se possibile".** Il blocco schermo (Wake Lock) viene negato o
   rilasciato dal sistema in risparmio energetico o con batteria quasi scarica.
3. **Vibrazione assente.** `navigator.vibrate` non esiste su iOS: l'app non vibra e non dipende
   dalla vibrazione.
4. **Beep e switch silenzioso / musica di altre app.** Il comportamento dipende dal tipo di
   sessione audio e non è garantito a priori: vedi il limite documentato dopo i test sul
   dispositivo (`docs/DEVICE-NOTES.md`, Fase 3).

## Licenza

MIT — vedi `LICENSE`. Icone, nome e palette sono originali: nessun asset è preso da altre app.
