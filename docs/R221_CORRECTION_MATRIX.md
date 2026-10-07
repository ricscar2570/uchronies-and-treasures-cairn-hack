# R2.2.1 — verifica e disposizione dell'audit

Base effettiva: Omnibus R2.2 allegato (91 pagine, SHA-256 registrato nel rapporto tecnico) e sorgenti R2.2 al commit `d2126ff54bf097bdba1085df7bfb8315c1952a71`.

| ID audit finale | Verifica indipendente e intervento | Stato |
|---|---|---|
| 1 — meno nella formula Debt | Il meno è presente nei sorgenti E nel PDF originale, alla fine della riga prima di `clemency`. Rilievo matematico non confermato. Formula riformattata su due righe esplicite; sottrazioni e motore numerico invariati. | LEGGIBILITÀ CORRETTA |
| 2 — Meridian roof | Rimosso il check automatico dal tetto. Per i piani 25–26: pericolo nominato, segnalato, protezioni ordinarie, fase quieta/alternativa, attesa conteggiata. Non introdotto in segreto nella one-shot Chicago. | CORRETTO; chiarimento hazard da provare al tavolo |
| 3 — iniziativa rapida | DEX riuscito dà un turno di apertura; poi nemici, tutti i PG, alternanza. Il fallimento ritarda, non cancella il turno successivo. | CORRETTO |
| 4 — game over | Il sabotaggio può portare al licenziamento, non all'eliminazione automatica del PG. Conseguenze e possibili strade indipendenti esplicitate. | CORRETTO |
| 5 — End Cash | Disponibilità e limite al rimborso espliciti; doppio zero floor come difesa della formula. Un rimborso impossibile è rifiutato, NON usato per cancellare Debt gratuitamente. | CORRETTO |
| 6 — titolo combattimento | `Telegraph the Cost of Combat`. | CORRETTO |
| 7 — approccio preferito | Eliminata la formulazione `the way the scene goes wrong` e la presunzione di un combattimento da evitare. Motivi dei PNG e conseguenze non cambiano per sostenere un piano preferito. | CORRETTO |
| 8 — reddito legittimo | Via onesta possibile, ma stretta e incerta; eliminata l'inevitabilità. | CORRETTO |
| 9 — Echo / Corruption | Corrosione temporale distinta dal rapporto con Zhou; nessuna trasformazione dovuta soltanto a Corruption 10. | CORRETTO |
| 10 — Certificates | Scelta esplicita R2.2.1: soltanto unità intere. Prezzo concordato prima, bundle o pagamento Cash per acquisti minori, niente arrotondamento automatico o credito invisibile. Non presentata come regola già dimostrata della R2.2. | DEFINITO; da playtestare |
| 11 — mission pay | Ricevuta datata al pagamento immediato o alla chiusura. Entrata accreditata una sola volta; distinto il saldo corrente dalla ricostruzione su un foglio con Cash di apertura. | CORRETTO |
| 12 — licenza script | Inventario e ambito delle dichiarazioni documentati in `LICENSING_SCOPE.md`. Nessuna nuova licenza applicata unilateralmente. | APERTO: decisione autore |
| 13 — proofing madrelingua | Eseguito controllo editoriale dei passaggi toccati; non è una revisione madrelingua indipendente. | APERTO |
| 14 — moduli | Verifica strutturale, tutti i campi, salvataggio/riapertura/reset e rendering documentati nel rapporto. Non equivale a test manuale in Acrobat, Firefox, Preview o mobile. | TECNICO; collaudo lettori da completare |
| 15 — segnalibri/navigazione | Già presenti nella R2.2: 304 segnalibri e 72 link. Conservati e ricostruiti con destinazioni dinamiche; non dichiarati erroneamente assenti. | VERIFICATO E CONSERVATO |

## Altri residui rapidi corretti nello stesso perimetro

Nel Cheat Sheet: STR del tiro critico già ridotta; recupero WIL distinto dal recupero ordinario e con durata corretta di tre giorni a Loyalty 7+; intervalli di tutte le zone al posto dell'ambiguo `standard = 6h`; eliminata la promessa di `one page`, non vera nell'edizione compilata. Riparata la posizione del banner di sviluppo che interrompeva il front matter del README.

## Non fatto e non dichiarato

Nessun taglio globale del 7–10%, nuova ambientazione, nuovo sottosistema, playtest umano, simulazione accoppiata dell'economia, certificazione di stampa o PDF/UA. Il motore delle simulazioni e l'esempio numerico di dieci settimane non sono stati ricalibrati.
