# CHRONOCAIRN R2.2 — matrice di riscontro dell’audit

Gli identificativi seguono la Master Correction List dell’audit allegato, non numeri di difetti inventati. Lo stato è di implementazione verificata, non validazione umana.

| ID | Rilievo | Stato | Intervento / limite | Sorgente |
|---|---|---|---|---|
| P0.01 | Premi esperienza | IMPLEMENTATO | Chicago e Warden: bande, favori e conseguenze del sistema; nessun premio XP. | adventures/the-chicago-loop.md; wardens-guide/running-the-game.md |
| P0.02 | Loyalty 7–8 | IMPLEMENTATO | Una banda migliorata una volta per settimana; tetto Exceptional; niente bonus Cash cumulativo. | game-systems/loyalty-corruption.md; game-systems/economy.md |
| P0.03 | Loyalty 9–10 | IMPLEMENTATO | +50% alla sola paga base; timing settimanale e sospensione definiti. | game-systems/loyalty-corruption.md |
| P0.04 | Raines e Corruption | IMPLEMENTATO | -1 Loyalty ogni due lavori; nessuna Corruption automatica; soglie e compensi disambiguati. | wardens-guide/creating-enemies.md |
| P0.05 | Esposizione delle reliquie | IMPLEMENTATO | Pericolo Yellow nominato, annunciato, distinto dal contatore; nessun nuovo tracker. | players-guide/temporal-relics.md |
| P0.06 | Uscita da Chicago | IMPLEMENTATO | Solo controlli effettivamente maturati; cronologia e deadline esplicite. | adventures/the-chicago-loop.md |
| P0.07 | Scars | IMPLEMENTATO | Danno dopo Armor come indice, massimo 12, solo HP positivi ridotti esattamente a zero. | players-guide/core-rules.md |
| P0.08 | Debito alla sostituzione | IMPLEMENTATO | Nuovo debito personale iniziale; nessuna eredità automatica; obblighi espliciti separati. | players-guide/core-rules.md; adventures/the-first-four-weeks.md |
| P0.09 | Sette passaggi | IMPLEMENTATO | Numerazione 1–7; rango separato dai sei tracker. | players-guide/character-creation.md |
| P0.10 | Soluzioni approvate a Chicago | IMPLEMENTATO | Opzioni con costi, conseguenze e terze vie; combattimento non classificato come errore autoriale. | adventures/the-chicago-loop.md |
| P1.01 | Attivazione Instability | IMPLEMENTATO | Entrambi i legami almeno 3, distanza massima 2. | game-systems/loyalty-corruption.md |
| P1.02 | Penalità sociale | IMPLEMENTATO | Svantaggio solo ai tiri rischiosi con fazioni/intermediari informati. | game-systems/loyalty-corruption.md |
| P1.03 | Crisi al terzo conteggio | IMPLEMENTATO | Conseguenze e possibilità di rifiuto; nessuna scelta imposta; reset esplicito. | game-systems/loyalty-corruption.md |
| P1.04 | Ordine senza scelta | IMPLEMENTATO | Rifiuto possibile con conseguenze istituzionali e mancato compenso dell’incarico. | adventures/the-first-four-weeks.md |
| P1.05 | Morte prescritta | IMPLEMENTATO | Pericolo letale annunciato e vie di fuga, senza decesso obbligatorio. | adventures/the-first-four-weeks.md |
| P1.06 | Titolo mini-campagna | IMPLEMENTATO | Ten Weeks in Vegas; percorso storico conservato per compatibilità dei link. | adventures/the-first-four-weeks.md |
| P1.07 | Prospetto dieci settimane | IMPLEMENTATO | Dieci righe ricalcolate, bonus e timing inclusi; nessuna spirale economica fittizia. | adventures/the-first-four-weeks.md; reports/r22-ten-week-ledger.json |
| P1.08 | Caricatori e munizioni | IMPLEMENTATO | Stato corrente e scorte separati; costi, slot, ricarica e dado definiti. | players-guide/core-rules.md |
| P1.09 | Informazione di Chen | IMPLEMENTATO | Collasso WIL, accumulo Quirk e danni curabili; nessun limite segreto variabile. | setting/adventure-sites.md |
| P1.10 | Libri del Failed Academic | IMPLEMENTATO | Tre libri in un unico insieme bulky, due slot. | players-guide/character-creation.md |
| P2.01 | Distorsioni causali | IMPLEMENTATO | d12 con indizi osservabili e limiti anti-retcon delle scelte dei PG. | wardens-guide/tables-and-generators.md |
| P2.02 | Generatore missioni | IMPLEMENTATO | Costo economico e interessi incompatibili, con esempio di contabilizzazione. | wardens-guide/tables-and-generators.md |
| P2.03 | Alternativa a Zhou | IMPLEMENTATO | Emergency Clinic Contract: termini e costi, non reddito ripetibile illimitato. | wardens-guide/tables-and-generators.md |
| P2.04 | Compratori stranieri | IMPLEMENTATO | Interessi, limiti e risorse concrete per tre interlocutori indipendenti. | wardens-guide/campaign-management.md |
| P2.05 | Riduzione del testo 7–10% | DIFFERITO | Solo tagli locali di ripetizioni; nessuna quota globale dichiarata o raggiunta. | docs/R22_CHECKPOINT_2026-10-06.md |
| P2.06 | Navigazione PDF | IMPLEMENTATO | Indice cliccabile, 26 capitoli, 299 segnalibri, destinazioni controllate. | scripts/build-pdf.py; reports/r22-pdf-check.json |
| P2.07 | Provenienza repository | IMPLEMENTATO CON RISERVA | URL, commit della diagnostica, data e manifest. La licenza originale degli script richiede dichiarazione autoriale. | reference/monte-carlo-transparency.md |
| P2.08 | Scheda economica separata | IMPLEMENTATO | Modulo A4 distinto dal personaggio: 109 campi, conti non automatizzati. | scripts/build_sheets_r22.py |
| P2.09 | Scheda missione Warden | IMPLEMENTATO | Modulo A4: criteri premio, costi, tempo, pericoli separati, PNG e debrief. | scripts/build_sheets_r22.py |
| P2.10 | Interazioni e casi limite | IMPLEMENTATO | Una pagina A5 canonica con rimandi e ordine delle operazioni. | reference/rules-interactions.md |

## Precisazioni

Scars segue il danno effettivo dopo Armor, non il danno grezzo suggerito in una delle alternative dell’audit. Il termine sociale di Instability è svantaggio ai tiri rischiosi, non il dado d4 di danno impaired. Non è stato aggiunto un tracker Temporal Trace: il costo delle reliquie è un pericolo esplicito. Queste differenze sono intenzionali e documentate.

Rimangono il taglio globale, la precisazione della licenza degli script e le prove umane; lo storico simulatore economico non valida i nuovi benefici Loyalty. Non sostituire questi limiti con una nuova valutazione numerica di pubblicabilità.
