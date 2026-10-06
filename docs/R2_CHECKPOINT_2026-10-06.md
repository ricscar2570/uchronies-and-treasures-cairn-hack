# CHRONOCAIRN — checkpoint R2.1

**Time-Crime Horror Roleplaying — Riccardo Scaringi**  
Data: 6 ottobre 2026. Stato: **revisione tecnica implementata; validazione umana e pubblicazione ancora aperte**.

## Punto di partenza e perimetro

Il lavoro riprende il commit `32dd003b70a403d19de121f8156bffe009bd38d8` di `ricscar2570/uchronies-and-treasures-cairn-hack`: R1 aveva chiuso l'intervento sull'economia e la sua impaginazione. R2.1 affronta contaminazione, ritmo dei Quirk e divergenze pertinenti fra sito, simulatore e PDF. Non riscrive il resto del gioco né certifica che ogni capitolo sia pronto per la vendita.

## Regole consolidate

La penalità dei Quirk ai soli tiri di contaminazione è ora limitata a **−3**. Un nuovo Quirk richiede **almeno 3 danni finali da un singolo colpo**, dopo protezione e limite a metà WIL corrente arrotondata per eccesso. I danni piccoli non si sommano per questo innesco. Si controlla prima WIL: a zero il personaggio diventa un'eco. Cinque Quirk distinti sono sostenibili; il sesto causa la trasformazione. Un tiro riuscito non infligge danno e non produce mutazioni.

La tuta pesante impedisce il normale innesco dei Quirk nelle zone con d4: il danno massimo, dopo riduzione di 2, è 2. Questo è un beneficio intenzionale della protezione, non immunità: WIL può ancora diminuire fino a zero e il d6 delle zone nere può ancora produrre Quirk. Le cure restituiscono WIL solo al completamento, non a ogni cambio di sessione; non annullano i Quirk o una trasformazione già avvenuta.

**Decisione di design nuova in R2.1, da verificare al tavolo:** il contatore conserva la frazione di intervallo accumulata quando cambia l'intensità della zona. Una breve visita in verde lo sospende. Otto ore ininterrotte di riposo in verde azzerano la frazione residua, senza guarire WIL o Quirk. Il rifugio contaminato a intervallo di dodici ore non equivale a una zona verde. I controlli speciali espressamente previsti da uno scenario sono distinti da quelli periodici.

Esempio: quattro ore in arancione completano due terzi dell'intervallo. Entrando in rosso resta un terzo di tre ore: il primo controllo arriva all'ora complessiva cinque, poi alle ore otto e undici se l'esposizione continua. Entrare, uscire o terminare una sessione non impone di per sé un tiro.

## Misure riproducibili

Sono stati eseguiti **20.000 percorsi sintetici per ciascuno di 12 profili**, per un totale di **240.000 percorsi**. Il rapporto JSON registra semi, ipotesi, distribuzioni, cause di trasformazione e impronte SHA-256 di regole e codice. Nessuna percentuale storica è stata usata come obiettivo di calibrazione.

| Profilo, dieci cicli | Controlli per uscita | Quirk medi su tutti i personaggi iniziali | Trasformazioni in eco |
|---|---:|---:|---:|
| Gialla, quattro ore | 0 | 0,00 | 0,00% |
| Gialla, otto ore | 1 | 1,21 | 0,21% |
| Rossa, sei ore | 2 | 2,33 | 15,01% |
| Rossa, nove ore | 3 | 2,61 | 59,22% |
| Rossa, sei ore, tuta pesante | 2 | 0,00 | 2,14% |
| Gialla, otto ore, senza cure | 1 | 0,83 | 58,54% |

Salvo il profilo senza cure, questi casi assumono **una cura d6 completata dopo ogni uscita sopravvissuta**, medicine disponibili, assenza di Privazione, WIL iniziale 3d6 e un contatore ripartito dopo riposo sicuro. Un ciclo non coincide automaticamente con una settimana o una sessione. Costi, tempi di calendario delle cure, combattimenti, effetti specifici dei Quirk e scelte dei giocatori non sono simulati. La media include anche chi si trasforma prima della fine; il JSON riporta separatamente i sopravvissuti.

La vecchia aspettativa di 3–4 Quirk con esposizione rossa regolare **non è dimostrata**. Aumentare i controlli non basta: nel caso di nove ore il tasso di perdita aumenta molto più del numero medio di Quirk. Perciò non è stata accelerata artificialmente la contaminazione né imposto un primo Quirk a una sessione prestabilita. Una missione breve ben pianificata continua a poter evitare controlli periodici.

## Verifiche effettive

**29 test automatici di regressione superati**: ordine delle operazioni, protezioni, limiti, quinto/sesto Quirk, WIL basso, risultati naturali del d20, cure, orologio fra zone, casi senza controlli, riproducibilità e provenienza del rapporto. Sono test di regole e codice, non partite umane.

Il PDF locale ricostruito comprende **67 pagine A5**. Sono state corrette le tabelle a tutta pagina che finivano in colonne strette; il costruttore ora rifiuta tabelle più larghe del riquadro disponibile. Eliminati salti duplicati che creavano pagine vuote con il solo piè di pagina. Il controllo geometrico non rileva testo fuori pagina né pagine senza corpo, salvo il verso bianco intenzionale di pagina 2. Controllate le anteprime delle pagine e le pagine chiave a maggiore risoluzione. Queste verifiche non equivalgono a un audit tipografico ed editoriale completo.

Tre blocchi del PDF leggono direttamente il Markdown: contaminazione, mini-campagna introduttiva e appendice delle simulazioni. Ciò evita che la mini-campagna stampata conservi bonus cumulativi e inneschi temporali superati rispetto al sorgente R1/R2. Gli altri capitoli incorporati nel generatore rimangono nel perimetro R3.

**Nuove sessioni di playtest umano aggiunte da questo intervento: 0.** Nessun dato sintetico è registrato come osservazione umana. Restano da verificare al tavolo il ritmo percepito, la leggibilità del contatore, il costo reale delle cure e la pressione congiunta di economia e contaminazione.

## Ripresa esatta

Il prossimo blocco è **R3 — coerenza procedurale e fra formati**, non una nuova calibrazione su percentuali desiderate. Iniziare dal confronto dei capitoli ancora incorporati in `scripts/build-pdf.py` con i rispettivi Markdown: combattimento e danno critico, Privazione e recuperi, esempi di downtime, conseguenze istituzionali, descrizioni dei Quirk ed esempi di scenario. Non importare regole da vecchie edizioni italiane o da altri repository senza confronto esplicito.

Prima di chiudere R2 sul piano dell'esperienza, raccogliere osservazioni umane sul tempo reale delle missioni, controlli effettivamente subiti, cure completate, Quirk e perdite. Le evidenze umane esistenti, se presenti altrove, devono essere recuperate e identificate; questo checkpoint non ne presume l'assenza globale e non le sostituisce.

Comandi, dipendenze, rapporto numerico e verifiche sono in `scripts/README.md` e `reports/`. Usare il commit che contiene questo file come punto di ripresa; la cronologia Git distingue il checkpoint sorgente dalla costruzione locale del PDF.
