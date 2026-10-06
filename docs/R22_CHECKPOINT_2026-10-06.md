# CHRONOCAIRN — checkpoint R2.2

**Time-Crime Horror Roleplaying — Riccardo Scaringi**  
6 ottobre 2026. **Consolidamento procedurale implementato; non una certificazione di pubblicazione.**

## Base, perimetro e stato

Base esatta: `ricscar2570/uchronies-and-treasures-cairn-hack`, R2.1, commit `d4b13099c8b530b0d717396df72c5f41aa9e197b`.
Ramo di consegna previsto: `development/r22-procedural-20261006`. Il commit effettivo della consegna è registrato in `SOURCE_COMMIT.txt` nell'archivio; questo documento non inventa un hash futuro. Non aggiornare `main` né la release pubblica automaticamente.

Il nuovo audit allegato dall'autore è stato usato come lista R2.2 al posto di limitarsi al precedente piano R3. I dieci interventi P0 e i dieci P1 sono implementati nei sorgenti e nella nuova costruzione PDF. Nove interventi P2 hanno un'implementazione; il taglio editoriale globale del 7–10% resta differito. La matrice puntuale è `docs/R22_CORRECTION_MATRIX.md`. Implementato non significa dimostrato al tavolo.

## Cambiamenti normativi

**Ricompense.** Rimossi premi in un sistema di esperienza inesistente. Una missione riceve una sola indennità e una sola banda. Loyalty 7+ alza di un gradino una banda ammissibile una volta per settimana, fino a Exceptional; non aggiunge $200. Loyalty 9+ aumenta del 50% soltanto la paga base. Il beneficio di missione usa Loyalty prima della ricompensa; la paga usa rango/Loyalty all'inizio della settimana. Instability sospende i benefici speciali economici, non la normale paga né le cure prioritarie per chi ha davvero Loyalty 7+.

**Instability.** Occorrono Loyalty e Corruption entrambe almeno 3, distanti al massimo 2. Lo svantaggio riguarda soltanto tiri sociali rischiosi con interlocutori informati delle fazioni interessate. Non trasforma ogni conversazione in un tiro. Tre chiusure settimanali consecutive instabili producono una crisi, non la scelta del personaggio da parte del Warden. Rifiuto, negoziato o terza via restano possibili con conseguenze dichiarate. La penalità pendente della tabella di sospetto riguarda il successivo tiro WIL di sospetto, non il d20 della tabella né la contaminazione.

**Raines.** Ogni due incarichi completati: -1 Loyalty; nessuna Corruption automatica, che resta il rapporto con Zhou. Alla terza missione il rapporto viene scoperto; la pressione si applica al successivo incarico della Divisione. Il 40% è calcolato sulle bande pubblicate non modificate dai benefici personali. Una scorta già presente non viene duplicata.

**Danno e Scars.** Il danno dopo Armor che porta HP positivi esattamente a zero individua la riga della tabella Scars, massimo 12. Nessun d12 di selezione. L'eccedenza infligge danno STR e richiede il tiro sulla STR già ridotta; non innesca anche una Scar. Corretti esempio di danno critico, iniziativa iniziale e copertura. La contaminazione conserva la propria protezione e la propria procedura separate.

**Munizioni.** Caricatore corrente pronto/scarso/vuoto, più ricariche di scorta. Dopo uno scontro a fuoco intenso: 1 svuota il corrente; 2 lo segna scarso, o lo svuota se era già scarso; 3–6 non cambia nulla. Un'arma caricata spara anche con zero scorte. Ricaricare il vuoto consuma una scorta. Una costa $50; due occupano uno slot. Il tiro non cancella retroattivamente colpi sparati.

**Contabilità personale.** Il sostituto ricomincia con i normali valori iniziali, inclusi $500 Debt, non con il debito personale del morto. Obblighi di squadra effettivamente concordati restano documentati, ma non creano automaticamente un nuovo debitore. I tre libri del Failed Academic formano un unico oggetto bulky da due slot. I sei tracker sono separati dal rango.

**Reliquie.** Eliminata l'unità di esposizione indefinita, senza introdurre un ulteriore tracker. L'autenticazione non schermata di Zhou è un pericolo esplicito, annunciato: un controllo Yellow per chi maneggia direttamente l'oggetto. Non modifica il contatore periodico. La vendita dà +1 Corruption per transazione; la conversione dei certificati è una transazione distinta. Questa è una scelta nuova da playtestare, non una correzione matematica obbligata.

## Scenari e strumenti

Chicago conserva sito, PNG e problema centrale, ma non impone combattimento, morte, mutazione o soluzione approvata. Le ricompense usano criteri dichiarati e una sola banda. I controlli seguono il tempo effettivo; uscire non ne aggiunge uno. Orange→Red all'ora quattro conserva la frazione e porta i controlli alle ore cinque e otto. L'implosione ha un termine iniziale di otto ore; solo la manipolazione non schermata annunciata può accorciarlo. La tuta standard è la dotazione introduttiva, senza togliere una tuta migliore a chi la possiede.

La mini-campagna è **Ten Weeks in Vegas**: quattro sessioni reali, dieci settimane fittizie. Il percorso del file precedente resta invariato per non rompere i collegamenti del sito. Ordini e pericoli hanno conseguenze, non esiti obbligatori. Il prospetto arriva alla settimana dieci e applica i benefici Loyalty espliciti.

Sono stati aggiunti una tabella d12 di distorsioni causali, costo economico e interessi incompatibili al generatore di missioni, un contratto clinico indipendente da Zhou, ruoli concreti di compratori stranieri e una pagina di interazioni/casi limite. Il tempo può complicare la causalità, ma non riscrive in segreto le decisioni, il denaro già registrato o le convinzioni del personaggio.

## Evidenza economica: che cosa cambia davvero

L'esempio dichiarato, senza rimborsi volontari né accordi con Zhou, termina alla settimana dieci con **Cash $1.270 e Debt $987**. Contiene solo sei missioni riuscite: niente promozione anticipata. L'onestà può dare respiro economico con Loyalty elevata; non è corretto mantenere una spirale obbligatoria falsando le entrate. Il debito continua ad accumulare interessi perché l'esempio non effettua rimborsi, non perché il denaro disponibile venga ignorato dalla regola.

Lo script storico `economy_sim.py` non implementa questi benefici di fazione: i suoi 100.000 casi e le sue percentuali sono ora esplicitamente presentati come diagnostica R1, non come validazione R2.2. I nuovi test verificano il calcolo dichiarato e i casi limite, non un'intera campagna simulata con decisioni umane.

## Verifiche e artefatti

- **78 test automatici superati** nella verifica locale: 29 precedenti più 49 nuovi. Il test di collegamento PDF è stato adattato al manifest canonico, senza rimuovere i controlli di contaminazione. Il test di compilazione PDF conserva la pagina del modulo durante la modifica del campo; il precedente errore riguardava l'oggetto di test, non un modulo incompleto.
- **240.000 percorsi sintetici di contaminazione rieseguiti**, 12 profili da 20.000, seed 42026: JSON identico a R2.1. I quattro file congelati di regole/dati/simulatori corrispondono alla base. Non sono nuove prove di campagna o playtest umani.
- **88 pagine A5**, 26 capitoli canonici, **299 segnalibri**, indice cliccabile e **57 collegamenti**. Nessun testo fuori pagina, nessun collegamento interno con destinazione invalida; pagina due bianca intenzionale. Tutti i 26 hash dei sorgenti coincidono con quelli della costruzione.
- **Tre schede A4 autonome compilabili:** personaggio 43 campi, contabilità 109, missione del Warden 10; **162 campi totali**. Verificata compilazione, salvataggio e riapertura di un campo campione, non ogni combinazione possibile di lettore PDF.
- Render Poppler di tutte le pagine esaminati in contact sheet; controlli ravvicinati su tabelle, procedure e moduli. Corrette tabelle in colonne improprie, indice su una sola pagina e righe isolate. Questa è una verifica visiva di sviluppo, non conformità tipografica, PDF/UA o approvazione POD.

La crescita da 67 a 88 pagine deriva soprattutto dalla sostituzione dei capitoli incorporati/abbreviati con il corpus Markdown completo, oltre ai nuovi strumenti. La dimensione del corpo non è stata ridotta: 8 pt. I due formati non sono più due edizioni normative parallele. Non è stata eseguita una riduzione editoriale globale del testo.

Le prove remote, quando eseguite, sono documentate dall'esito GitHub Actions e dall'archivio costruito sul commit effettivo; questo file non anticipa il loro risultato.

## Aperture reali e punto di ripresa

1. **Licenza degli script:** il testo dichiara CC BY-SA 4.0, ma il LICENSE principale riguarda il tema GPLv3. Occorre una dichiarazione autoriale distinta e compatibile per il codice originale; nessuna licenza è stata inventata o cambiata per conto dell'autore.
2. **Editing:** riduzione prudente delle ripetizioni, controllo linguistico madrelingua, artwork/mappe e layout commerciale definitivo. Gli schemi testuali dei siti sono conservati, non sostituiti da nuove mappe illustrate.
3. **Evidenza umana e campagna:** nessuna nuova sessione umana aggiunta (0). Verificare Instability, munizioni, bonus Loyalty, autenticazione delle reliquie, cure realmente completate, agency degli scenari e pressione congiunta. Recuperare le eventuali prove umane già esistenti prima di giudicarne l'assenza complessiva.
4. **R3.1:** proseguire dalle interazioni residue dei singoli Quirk e dalle eccezioni mediche/istituzionali; costruire poi un modello accoppiato economia/fazioni/calendario solo dopo aver fissato tutte le assunzioni. Non riutilizzare statistiche R1 come R2.2 né calibrare sui vecchi risultati desiderati.

La parte R3 di eliminazione delle copie incorporate nel generatore è completata. Non occorre ripeterla da zero: ripartire da `_data/manual-chapters.json`, `docs/R22_CORRECTION_MATRIX.md`, `reference/rules-interactions.md` e dai test. Lo stato è **R2.2 PROCEDURAL CONSOLIDATION**, non «10/10», non un manuale certificato per la vendita.
