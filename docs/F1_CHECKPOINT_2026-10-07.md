# CHRONOCAIRN — F1: congelamento e preparazione del collaudo

Riccardo Scaringi | Time-Crime Horror Roleplaying | 7 ottobre 2026

## Baseline invariata

Regole: **R2.2.1**, commit `7c688770942db6568815f0c781991f121ea46756`, tree `7a2353c1941b2b7d7e24f382f8559d40cdd36c3c`.
F1 è un checkpoint editoriale di congelamento e preparazione dei test, non una R2.3 né una nuova edizione commerciale. Non è un blocco amministrativo dei rami GitHub.

Nessuna modifica a capitoli, regole, modelli, avventure, generatore del manuale, schede o Omnibus. Il ramo `validation/r221-f1-20261007` conserva separatamente questo stato operativo. Non aggiornare `main`, la release pubblica o il ramo correttivo precedente automaticamente.

Omnibus congelato: `CHRONOCAIRN_OMNIBUS_R2_2_1.pdf`.
SHA-256: `b1039bd585bb65d71d18f010e312f45e079dc6cc6ccc5ba469538ee72cb8eaca`.
92 pagine: 89 A5 e tre schede A4; 304 segnalibri; 72 link; 162 campi compilabili.

## Audit ricevuto: cosa significa

L'audit fornito dall'autore il 7 ottobre 2026 (`Testo incollato(1).txt`) assegna 9,2/10 e non individua nuovi blocchi normativi. Queste sono conclusioni dell'audit ricevuto, non nuova evidenza umana o commerciale. F1 non dichiara un nuovo audit semantico esaustivo.

Precisazioni documentali, senza errata al manuale:

- Il meno prima di clemency era già presente nella R2.2 alla fine della riga precedente; la R2.2.1 ne migliora la leggibilità. Vedere `docs/R221_CORRECTION_MATRIX.md`.
- Le schede separate esistono già in `downloads/`, così come la navigazione dell'Omnibus. Non sono funzionalità mancanti.
- Il vincolo sui rimborsi è stampato: i campi AcroForm non calcolano e non impediscono tecnicamente di digitare importi errati.
- Non introdurre una nuova regola sulle eccedenze dei Certificates: resta il prezzo concordato in unità intere, bundle o Cash, senza arrotondamenti automatici e credito implicito.

## Verifiche F1 eseguite localmente

101 test di regressione esistenti rieseguiti: **101 PASS**. Verificate le 120 voci del manifest dell'archivio R2.2.1. Il manifest F1 nel pacchetto dell'autore protegge 53 file, inclusi i 26 capitoli.

Rieseguiti compilazione, salvataggio, riapertura e reset di tutti i campi nelle tre schede autonome (43, 109, 10) e nell'Omnibus (162), tramite MuPDF e pypdf. Artefatti di gioco invariati byte per byte.

Nuovi PDF di supporto: protocollo italiano di 10 pagine A4 con moduli stampabili e fascicolo riservato del coordinatore di 3 pagine. Tutte le 13 pagine renderizzate con Poppler e ispezionate; nessun testo oltre i bordi rilevato. I nuovi moduli del protocollo sono stampabili, non nuovi AcroForm.

I 240.000 percorsi sintetici appartengono alla diagnostica congelata: non sono stati rieseguiti in F1 e non sono nuova evidenza sul sistema accoppiato economia/fazioni. Le verifiche di questo checkpoint sono locali; non si dichiara un nuovo run CI remoto F1.

## Protocollo proposto

Tre tavoli indipendenti, 4–5 giocatori ciascuno come obiettivo. Ogni tavolo gioca una sessione di The Chicago Loop e quattro incontri di Ten Weeks in Vegas: **15 sessioni pianificate**, per coprire entrambe le avventure senza comprimere la minicampagna.

Chicago e la minicampagna sono coorti separate: creare nuovi Recruit, senza trasferire denaro, Debt, WIL, Quirk o favori. Le quattro sessioni della minicampagna sono un'indicazione di ritmo; registrare il calendario realmente raggiunto e gli eventuali incontri aggiuntivi. Non forzare esiti, contaminazione o scelte per rispettare il piano.

Almeno un Warden prepara e conduce senza spiegazioni dell'autore. Tenere le risposte del fascicolo coordinatore separate fino alla fine delle sessioni osservate. Registrare ogni aiuto esterno. I casi procedurali A1–A8 vengono dopo il gioco naturale e NON contano come sessioni di campagna.

Raccogliere: saldi settimanali e ricevute datate, band e timing dei bonus, esposizione e hazard, WIL/Quirk, recuperi effettivamente completati, approcci, offerte reali, dubbi normativi, durata delle chiusure, feedback individuale e prove dei lettori PDF. Zero è un valore osservato; un dato non rilevato rimane sconosciuto.

Tre–quattro settimane sono un obiettivo organizzativo, non date prenotate. Nessun gruppo è stato contattato o reclutato da questo checkpoint.

## Politica del congelamento e criteri di uscita

Riaprire le regole solo per errore dimostrabile, blocco operativo, problema ripetuto in almeno due tavoli o incomprensione grave ricorrente. Un blocker riproducibile può bastare anche da un solo tavolo: non aspettare una seconda sessione danneggiata.

Classificare blocker / major / minor / preference. Chiudere blocker e major prima del copyedit; non inserire varianti per gusto personale. Le correzioni approvate producono una nuova revisione esplicita e i risultati delle revisioni diverse restano separati.

Per la chiusura settimanale: tempo dell'intero tavolo di 4–5 PG, incluse spiegazioni e correzioni, esclusi soltanto pause estranee e debriefing. Dopo la prima sessione, mediana sotto cinque minuti e non più del 25% oltre cinque minuti sono obiettivi qualitativi operativi F1, non proprietà già dimostrate. Conservare tutti i tempi.

Due diversi approcci spontanei al Meridian, decisioni economicamente significative e trasformazione percepita sono osservazioni utili, non eventi da imporre. Copertura insufficiente significa inconclusivo. Tre tavoli non costituiscono un campione statisticamente rappresentativo e non dimostrano domanda o successo commerciale.

## Aperture reali

**Nuove sessioni umane: 0. Test manuali nei lettori reali: 0.** Licenza autonoma degli script ancora da autorizzare dall'autore; nessuna licenza concessa in F1. Proofing madrelingua indipendente, produzione visiva, accessibilità completa, interno Print e prova fisica rimangono aperti.

Il mandato di copyedit è conservativo: numeri, formule, timing, terminologia e may/must/can/cannot non si modificano silenziosamente. Nessun taglio globale del 7–10% viene imposto preventivamente.

Il PDF misto A5/A4 è adatto al lavoro a schermo e al tavolo, non dichiarato un interno POD pronto. Nessuna conformità PDF/UA o prova di stampa dichiarata.

## Materiale consegnato e ripresa

Il pacchetto `CHRONOCAIRN_F1_Collaudo.zip` contiene DA_INVIARE_AI_TAVOLI e SOLO_COORDINATORE. Quest'ultima cartella include risposte, mandato di copyedit, gate, sorgenti Markdown, generatore dei PDF di supporto, manifest F1 e log completo dei test. Non consegnare la cartella riservata al Warden non assistito prima del termine delle osservazioni.

`CHRONOCAIRN_F1_Kit_Tavoli.zip` contiene soltanto Omnibus, schede, protocollo e istruzioni; esclude gli script diagnostici e il fascicolo delle risposte. SHA-256 del kit tavoli: `732cc3ac2d5a79faa37742fe83c16b006abe8515cc81b3d2e017a14617f30682`.

Protocollo PDF SHA-256: `89b3b32553d5d9f0ad1a55c39fb5c24aa91243de85dc3260577c7adee0755fb2`.
Coordinatore PDF SHA-256: `db1731ede18b9fe32fa84ac4078c90f8e738c00eb3bdcda33bd45c62be5bf9a9`.

Questo commit salva lo stato operativo e il riepilogo verifiche; i sorgenti completi del kit e i PDF sono nel pacchetto consegnato nella conversazione, non aggiunti come binari a questo commit. I sorgenti del gioco rimangono integralmente recuperabili dalla baseline.

Prossima attività: distribuire il solo kit tavoli, assegnare coordinamento e tester, raccogliere risultati reali, riunire le issue e applicare la politica di modifica. Non avviare una R2.3 speculativa né trasformare il piano in sessioni già eseguite.
