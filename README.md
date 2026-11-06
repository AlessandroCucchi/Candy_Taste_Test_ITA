# Quante domande servono davvero? Progettare un Taste Test con i dati

Un test del gusto deve capire i gusti di una persona con poche domande: **ogni domanda in più fa perdere utenti, ogni domanda in meno rende il profilo meno preciso**. Questo progetto misura su dati reali quanto vale ogni domanda, quali domande scegliere e dove si trova la lunghezza ottimale. Il risultato viene poi verificato su persone nuove, due anni dopo.

## Dati

- **Candy Hierarchy 2015**: 5.658 righe, 4.579 rispondenti utilizzabili. Per ogni dolce di Halloween si indica "gioia" o "delusione". Sondaggio di D. Ng e B. Cohen (University of British Columbia / BoingBoing).
- **Candy Hierarchy 2017**: 2.460 righe, 1.676 utilizzabili. Stessa struttura, con l'opzione "indifferente".
- **FiveThirtyEight Candy Power Ranking**: attributi dei dolci, usati per controllare la codifica sensoriale.

## Disegno

- **Catalogo:** 57 dolci comuni ai due anni, ciascuno codificato per 6 attributi sensoriali (cioccolato, frutta, menta, arachidi, caramello, liquirizia).
- **Divisione non circolare:** 38 dolci definiscono il profilo di gusto; gli altri 19, più l'età, sono il serbatoio di 20 domande del test. Il test deve quindi indovinare il gusto su prodotti che **non ha chiesto**.
- **Scoperta sul 2015, replica sul 2017** senza ricalcolare nulla.

## Risultati principali

| | #Carattere indovinato (5 profili) |
|---|---|
| Nessuna domanda | 26% |
| 1 domanda | 31% |
| 7 domande scelte bene | 40% (con domande scelte a caso ne servono circa 13) |
| **12 domande** | **43%**, il 90% del guadagno possibile |
| 20 domande | 43% |
| Replica 2017, 12 domande, test del 2015 senza modifiche | 40% |

1. **5 #Caratteri sensoriali stabili:** #Goloso, #Vivace, #Eccentrico, #Fresco, #Morbido. Generalizzano a dolci mai usati per costruirli e riemergono da zero nel 2017, con correlazione tra i centri di 0,93–0,99.
2. **Il gomito cade tra 8 e 12 domande**, quasi nello stesso punto nel 2015 e nel 2017 (12 e 11 domande).
3. **Quali domande conta quanto quante:** scegliendo bene, servono circa metà delle domande. Le domande utili dividono il pubblico; quelle su dolci amati da tutti servono a poco.
4. **Le domande di gusto battono quelle demografiche.** L'età vale quanto una domanda di gusto mediocre ed entra nel test solo come 14ª.
5. **Un profilo si riconosce solo se il test lo "interroga":** i profili legati a menta e liquirizia sono riconosciuti poco, perché il serbatoio ha una sola domanda su ciascuno di questi attributi.
6. **Il #Carattere comunica, il modello diretto consiglia.** Per raccomandare prodotti, usare le risposte direttamente dà un'AUC di 0,74, contro 0,63 passando dal profilo.
7. **La lunghezza ottimale dipende dall'abbandono per domanda:** 12 domande con l'1%, 6 con il 2%.
8. **Il formato della risposta conta:** codificare "indifferente" in modo sensato vale fino a 5 punti di accuratezza.

## Struttura

```
notebooks/
  01_pulizia_dati.ipynb          catalogo, esclusioni, qualità dei rispondenti, età, SQL (DuckDB)
  02_profili_di_gusto.ipynb      divisione del catalogo, profili sensoriali, stabilità, validazione
  03_valore_delle_domande.ipynb  curva domande-accuratezza, ordine ottimale vs casuale, adattivo,
                                 consigli (AUC), lunghezza ottimale, robustezza
  04_replica_2017.ipynb          stessi profili? stesso test? su persone nuove
  catalogo.py                    catalogo dei dolci e regole di esclusione
  stile_grafici.py               stile grafico condiviso
data/raw/                        dati originali
data/processed/                  output intermedi (rigenerati dai notebook)
figures/                         grafici esportati
```

I notebook vanno eseguiti in ordine dalla cartella `notebooks/`. Sono già salvati con gli output, quindi si leggono anche senza eseguirli.

## Metodo in breve

- **Pulizia:**
  - esclusione esplicita delle voci che non sono prodotti (oggetti, scherzi, dolci inventati o fuori commercio);
  - rimozione di righe vuote, invii duplicati, valutazioni incomplete (<80%) e straight-liner;
  - normalizzazione dei nomi tra gli anni (apostrofi, errori di codifica);
  - età da testo libero, con una regola prudente; è l'unica domanda non legata al gusto che tengo.
- **Profili:** gradimento relativo per attributo, centrato sulla persona e standardizzato; k-means; numero di profili scelto per stabilità al bootstrap (ARI) su più divisioni del catalogo.
- **Valore delle domande:**
  - train/test 80/20;
  - forward selection con log loss in CV solo sul train;
  - IC bootstrap al 95% e test di McNemar appaiato;
  - CV ripetuta 5×5;
  - confronto con 30 ordini casuali;
  - albero decisionale come test adattivo;
  - gradient boosting come controllo del modello.
- **Decisione:** #Caratteri corretti = completamenti × accuratezza, con sensibilità al tasso di abbandono e abbandono di pareggio per ogni domanda.

## Limiti

- Campione nordamericano e auto-selezionato, contesto Halloween.
- Scala binaria nel 2015.
- L'abbandono per domanda è un'ipotesi, non un dato osservato.
- Nella replica la codifica di "indifferente" è stata scelta guardando il 2017, quindi quei numeri sono leggermente ottimistici.

## Ambiente

Python 3.11+, vedi `requirements.txt`.
