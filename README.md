# How Many Questions Does a Taste Test Need?

![Python](https://img.shields.io/badge/Python-0f2744?style=flat&logo=python&logoColor=7fe3d6)
![pandas](https://img.shields.io/badge/pandas-0f2744?style=flat&logo=pandas&logoColor=7fe3d6)
![scikit-learn](https://img.shields.io/badge/scikit--learn-0f2744?style=flat&logo=scikitlearn&logoColor=7fe3d6)
![SQL](https://img.shields.io/badge/SQL-DuckDB-0f2744?style=flat&logo=duckdb&logoColor=7fe3d6)
![Jupyter](https://img.shields.io/badge/Jupyter-0f2744?style=flat&logo=jupyter&logoColor=7fe3d6)

[Background](#project-background) · [Key Metrics](#key-metrics) · [Summary](#executive-summary) · [Insights](#insights-deep-dive) · [Recommendations](#recommendations) · [Repository](#repository-and-how-to-run)

> Python analysis of **6,255 consumers** rating **57 candies** in two surveys, two years apart. A **12-question** test reaches **90% of the achievable accuracy**. **7 well-chosen questions do the work of ~13 random ones**. The test designed on 2015 data works **unchanged on new respondents in 2017** (40% of taste profiles identified, against 43% in 2015).

<a id="project-background"></a>
## Project Background

A taste test profiles consumers by asking a few quick questions and then recommends products that fit their palate. Every question has a cost: **each extra question loses users, and each question removed makes the profile less precise**. The length of the test and the choice of questions directly affect how many people finish it and how good the recommendations are.

This project uses the *Candy Hierarchy* survey to answer five business questions. In the survey, thousands of people rate Halloween candies as "joy" or "despair".

1. Can consumers be grouped into a few stable, interpretable **taste profiles**?
2. How much does **each extra question** improve the identification of a person's profile, and where does the gain flatten out?
3. **Which** questions are worth asking: taste questions or demographic ones?
4. Can a short test also **recommend products** the person was never asked about?
5. Does a test designed on one survey still work on **new people, two years later**?

The design is **non-circular**. 38 candies define each person's taste profile. The other 19 candies, plus age, are the question pool. So the test has to infer tastes on products it **never asked about**.

<a id="key-metrics"></a>
## Key Metrics

| **12 questions** | **7 ≈ 13** | **0.74 vs 0.63** | **5 of 5** |
|:---:|:---:|:---:|:---:|
| reach 90% of the achievable accuracy | 7 well-chosen questions match ~13 random ones | AUC of direct recommendations vs recommendations via the profile | taste profiles re-emerge from scratch in 2017 (r = 0.93–0.99) |

<a id="executive-summary"></a>
## Executive Summary

[![Taste profiles identified vs number of questions: optimised order vs random order](figures/03_curva_domande_accuratezza.png)](figures/03_curva_domande_accuratezza.png)

| Questions in the test | Profiles identified, 2015 (test set) | Share of achievable gain (CV) | Same test on 2017 respondents |
|---|---|---|---|
| *0 (everyone gets the most common profile)* | *25.7%* | *0%* | *24.8%* |
| 1 | 31.2% | 42% | 29.8% |
| 7 | 39.8% | 74% | 38.2% |
| **12** | **42.6%** | **94%** | **40.3%** |
| 20 (all) | 43.1% | 100% | 40.6% |

*There are 5 taste profiles, so random guessing would score 20%. "Share of achievable gain" is the improvement over 0 questions as a share of the maximum improvement, estimated with repeated cross-validation on the 2015 training set.*

**What this means**

- **Each question helps, but less and less.** The elbow sits between **8 and 12 questions**. From the 8th question on, the test is no longer significantly worse than the full 20-question test (McNemar). At 12 questions it reaches 90% of the achievable gain.
- **Which questions matter as much as how many.** With questions in the optimised order, 7 are enough to reach 40%; with a random order it takes about 13. The best questions **split the audience**, while crowd-pleasers that almost everyone loves add little.
- **Taste questions beat demographics.** Age is worth about as much as a mediocre taste question, and it enters the test only as the 14th question.
- **The result holds on new people.** The 2015 test applied unchanged to 1,676 respondents in 2017 lands within 1–2 points of a model retrained on 2017 data, and its elbow is at 11 questions.

<a id="insights-deep-dive"></a>
## Insights Deep-Dive

### 1. Five stable sensory taste profiles
[Notebook 02](notebooks/02_profili_di_gusto.ipynb)

[![Taste profiles: relative liking by sensory attribute](figures/02_profili_heatmap.png)](figures/02_profili_heatmap.png)

| Profile | Share | Taste |
|---|---|---|
| **#Goloso** (indulgent) | 22% | Classic bars: chocolate with peanuts and caramel; rejects fruity candies |
| **#Vivace** (lively) | 16% | Fruity and sour candies; rejects rich chocolate |
| **#Eccentrico** (eccentric) | 16% | Loves liquorice, the most divisive taste in the catalogue |
| **#Fresco** (fresh) | 26% | Loves mint (York, Junior Mints); dislikes liquorice |
| **#Morbido** (mellow) | 20% | Rejects mint; prefers sweet, round flavours |

Each profile is built on **relative liking** for six sensory attributes: chocolate, fruit, mint, peanuts, caramel and liquorice. "Relative" means liking is measured against the person's own average, so the profiles describe what people prefer, not how generous they are with their ratings. Rating by rating, the candies gave unstable profiles; summarising by attribute fixed that.

5 and 6 profiles are equally stable under bootstrap resampling (mean ARI 0.868 vs 0.878 across three catalogue splits). I chose 5 because it is simpler to communicate and keeps more people in each profile. The profiles also hold up in three checks:
- they show the same pattern on **19 candies never used to build them** (r = 0.93);
- they stay the same when the catalogue is split differently (centroid correlation 0.97);
- they are only weakly linked to age (Cramér's V = 0.12).

### 2. Each question helps, but less and less
[Notebook 03](notebooks/03_valore_delle_domande.ipynb)

Questions are added one at a time, each time picking the one that improves the test the most. The choice is made on the training set only, and the result is measured on about 920 held-out people. Accuracy goes from 26% to 31% with one question, 40% with 7 and 43–44% with 12–14. After that, the last 6 questions add nothing. A gradient boosting model with all questions does not do better (42.2% vs 43.1%), so the plateau comes from the information in the questions, not from the model.

### 3. The best questions split the audience
[Notebook 03](notebooks/03_valore_delle_domande.ipynb)

[![Value of each question on its own](figures/03_valore_singole_domande.png)](figures/03_valore_singole_domande.png)

On their own, **fruity candies** are the most informative questions (Skittles 32%, Nerds 31%), because fruit is the attribute that divides people the most and is the opposite of chocolate. Questions about candies that almost everyone loves are close to useless (Reese's 27%, M&M's 26%): the answer is "joy" for nearly everyone. Age alone reaches 28%.

### 4. A profile is recognised only if the test asks about it
[Notebook 03](notebooks/03_valore_delle_domande.ipynb)

| Profile | Recognised (12 questions) | Defining attribute | Pool questions with that attribute |
|---|---|---|---|
| #Goloso | 64% | chocolate | 8 |
| #Vivace | 43% | fruit | 6 |
| *#Eccentrico* | *26%* | *liquorice* | *1* |
| #Fresco | 52% | mint | 1 |
| *#Morbido* | *20%* | *mint* | *1* |

The profiles driven by liquorice and mint are rarely recognised, because the question pool has only one candy for each of these attributes. #Fresco is the exception: as the most common profile, the model assigns it by default when the answers are inconclusive.

### 5. The profile communicates, a direct model recommends
[Notebook 03](notebooks/03_valore_delle_domande.ipynb)

[![AUC per product: direct model vs recommendations via the profile](figures/03_consigli_auc.png)](figures/03_consigli_auc.png)

For each of the 38 candies never asked about, the test has to tell who will like it from who will not. Recommending by popularity scores an AUC of 0.5, because it tells everyone the same thing. Recommendations deduced from the 5-profile label reach **0.63**. Using the answers directly, with one model per product, reaches **0.74**, and keeps improving with more questions. The label compresses each person into 5 categories and loses individual nuances.

### 6. The optimal length depends on the drop-off per question
[Notebook 03](notebooks/03_valore_delle_domande.ipynb)

[![Correct profiles per 1,000 starters by drop-off rate](figures/03_lunghezza_ottimale.png)](figures/03_lunghezza_ottimale.png)

| Drop-off per question | Optimal length |
|---|---|
| 0% | 20 questions (minimal gain after 12–14) |
| **1%** | **12 questions** |
| **2%** | **6 questions** |
| 5% | 1 question |

The value of a test is modelled as *correct profiles delivered = people who finish × accuracy*. For each question there is a **break-even drop-off** rate, above which removing the question delivers more correct profiles. It is over 20% for the 1st question and 8% for the 3rd, falls to 3–4% around the 10th–12th, and is below 1% from the 15th on. An adaptive test, built as a decision tree, is slightly more efficient up to about 6 questions but plateaus at around 40%.

### 7. The test transfers to new people, two years later
[Notebook 04](notebooks/04_replica_2017.ipynb)

[![2015 test applied unchanged to 2017 respondents](figures/04_curva_trasferimento.png)](figures/04_curva_trasferimento.png)

On the 2017 survey nothing is recalculated: the catalogue split, profile centres, question order and models all come from 2015.
- A segmentation of 2017 run **from scratch** finds the same 5 profiles, with centroid correlations of 0.93–0.99 and almost identical shares.
- 88% of 2017 respondents get the same profile with the 2015 centres and with the new segmentation.
- The 2015 test reaches 40.3% with 12 questions, against 40.6% for a model retrained on 2017.

The 2017 survey adds a "meh" option. Coding it as halfway between joy and despair, rather than as a missing answer, is worth **up to 5 points** of accuracy: a change in answer format needs recalibration.

**Technical details**

```
3 CSV files ──► catalogue & cleaning ──► taste profiles ──► question value ──► replication
(2015, 2017,     (57 candies,             (k-means on 6       (forward selection,   (2015 test applied
 FiveThirtyEight) 4,579 + 1,676 people)    sensory scores)     CIs, McNemar)         unchanged to 2017)
                  notebook 01              notebook 02         notebook 03           notebook 04
```

- **Data quality first:**
  - 95 survey items reduced to 57 real candies present in both years; non-products (cash, Vicodin, pencils), fictional or discontinued candies and generic judgements are excluded with explicit rules;
  - empty rows, 77 duplicate submissions, incomplete ratings (<80%) and straight-liners are removed;
  - age is parsed from free text, and values outside 3–100 are set to "not valid".
- **Name matching across years:** item names are normalised to handle curly apostrophes and a broken encoding in the 2017 file.
- **Sensory coding check:** the manual coding of the six attributes is checked against FiveThirtyEight. It matches 100% on chocolate, caramel and peanuts; the only 2 disagreements, on fruit, are matters of definition.
- **Profiles:** relative liking centred on each person and standardised; the number of profiles is chosen by bootstrap stability (ARI, 50 resamples) across three catalogue splits.
- **Question value:**
  - 80/20 train/test split; forward selection by cross-validated log loss on the training set only;
  - 95% bootstrap confidence intervals (2,000 resamples) and paired McNemar tests;
  - repeated 5×5 cross-validation, and comparison with 30 random question orders;
  - a decision tree as an adaptive test, and gradient boosting as a model check.
- **Robustness:** the whole pipeline is re-run on two other catalogue splits and gives the same curve shape (43–46% at 12 questions).
- **SQL (DuckDB):** joins, aggregations and confidence margins on the long-format ratings (notebook 01).

<a id="recommendations"></a>
## Recommendations

1. **Measure the real drop-off per question first.** It is the number that sets the optimal length: 12 questions at 1% drop-off, 6 at 2%. The model in notebook 03 converts it directly into a recommended test length.
2. **Design the question pool for sensory coverage.** Every attribute that defines a profile needs at least 2–3 questions. Otherwise profiles like #Eccentrico and #Morbido stay invisible.
3. **Ask questions that split the audience,** and test every new question by its marginal gain, with confidence intervals, before adding it to the test.
4. **Keep two tools for two jobs.** Use the taste profile to communicate (a name, a description, a segment for marketing), and a direct model to recommend products.
5. **Recalibrate whenever the answer format changes.** Adding a "neutral" option changed accuracy by up to 5 points depending on how it was coded.

**Limitations:**
- The samples are self-selected (BoingBoing readers) and mostly North American, in a Halloween setting.
- The 2015 scale is binary (joy/despair).
- The drop-off per question is an assumption, not observed data.
- The coding of "meh" was chosen by looking at 2017 results, so the replication numbers are slightly optimistic.
- The profiles describe preferences within this catalogue of 57 candies.

<a id="repository-and-how-to-run"></a>
## Repository and How to Run

```
taste-test-length/
├── data/
│   ├── raw/                              # Candy Hierarchy 2015 and 2017, FiveThirtyEight attributes
│   └── processed/                        # intermediate files, regenerated by the notebooks
├── notebooks/
│   ├── 01_pulizia_dati.ipynb             # catalogue, exclusions, respondent quality, SQL
│   ├── 02_profili_di_gusto.ipynb         # sensory taste profiles, stability, validation
│   ├── 03_valore_delle_domande.ipynb     # question value, optimal order, adaptive test, optimal length
│   ├── 04_replica_2017.ipynb             # replication on 2017 respondents
│   ├── catalogo.py                       # candy catalogue and exclusion rules
│   └── stile_grafici.py                  # shared chart style
├── figures/                              # charts exported by the notebooks
├── requirements.txt
└── README.md
```

```bash
git clone https://github.com/AlessandroCucchi/taste-test-length.git
cd taste-test-length
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd notebooks
jupyter notebook                   # run 01 → 02 → 03 → 04 in order
```

*The notebooks are written in Italian and are saved with their outputs, so they can be read without running them.*

**Data:**
- [Candy Hierarchy](https://www.scq.ubc.ca/?p=4471) 2015 and 2017 by David Ng and Ben Cohen (University of British Columbia, published on BoingBoing): 5,658 and 2,460 survey rows. The 2015 raw file comes from [jennybc/candy](https://github.com/jennybc/candy).
- [FiveThirtyEight Candy Power Ranking](https://github.com/fivethirtyeight/data/tree/master/candy-power-ranking): attributes for 85 candies.

Please check the sources' terms of use before reusing the data.

## Author

**Alessandro Cucchi**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0f2744?style=flat&logo=linkedin&logoColor=7fe3d6)](https://www.linkedin.com/in/alessandrocucchi-)
[![GitHub](https://img.shields.io/badge/GitHub-0f2744?style=flat&logo=github&logoColor=7fe3d6)](https://github.com/AlessandroCucchi)
