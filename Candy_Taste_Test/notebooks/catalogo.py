"""Catalogo dei dolci: nome canonico, nomi nei sondaggi 2015/2017, nome FiveThirtyEight e attributi.

Attributi codificati manualmente sulla composizione del prodotto
(cioccolato, frutta/acidulo, menta, arachidi o frutta secca, caramello, liquirizia).
La codifica viene confrontata con FiveThirtyEight nel notebook 01.
"""
import re

#          nome canonico,              chiave 2015,                 chiave 2017,                  FiveThirtyEight,             attributi
CATALOGO = [
    ("100 Grand",                     "100 grand bar",             "100 grand bar",              "100 Grand",                 "cioccolato caramello"),
    ("3 Musketeers",                  "three musketeers",          "three musketeers",           "3 Musketeers",              "cioccolato"),
    ("Mary Janes",                    "anonymous brown globs",     "anonymous brown globs",      None,                        "arachidi"),
    ("Black Jacks",                   "black jacks",               "black jacks",                None,                        "liquirizia"),
    ("Bonkers",                       "bonkers",                   "bonkers the candy",          None,                        "frutta"),
    ("Bottle Caps",                   "bottle caps",               "bottle caps",                None,                        "frutta"),
    ("Box o' Raisins",                "boxo raisins",               "boxoraisins",                None,                        "frutta"),
    ("Butterfinger",                  "butterfinger",              "butterfinger",               "Nestle Butterfinger",       "cioccolato arachidi"),
    ("Cadbury Creme Eggs",            "cadbury creme eggs",        "cadbury creme eggs",         None,                        "cioccolato"),
    ("Candy Corn",                    "candy corn",                "candy corn",                 "Candy Corn",                ""),
    ("Caramellos",                    "caramellos",                "caramellos",                 None,                        "cioccolato caramello"),
    ("Chick-o-Sticks",                "chickosticks",              "chickosticks",               None,                        "arachidi"),
    ("Chiclets",                      "chiclets",                  "chiclets",                   "Chiclets",                  ""),
    ("Circus Peanuts",                "those odd marshmallow",     "those odd marshmallow",      None,                        "frutta"),
    ("Dots",                          "dots",                      "dots",                       "Dots",                      "frutta"),
    ("Fuzzy Peaches",                 "fuzzy peaches",             "fuzzy peaches",              None,                        "frutta"),
    ("Goo Goo Clusters",              "goo goo clusters",          "goo goo clusters",           None,                        "cioccolato arachidi caramello"),
    ("Good N' Plenty",                "good n plenty",             "good n plenty",              None,                        "liquirizia"),
    ("Gum from baseball cards",       "gum from baseball cards",   "gum from baseball cards",    None,                        ""),
    ("Gummy Bears",                   "gummy bears",               "gummy bears",                "Haribo Gold Bears",         "frutta"),
    ("Hard Candy",                    "hard candy",                "hard candy",                 None,                        ""),
    ("Heath Bar",                     "heath bar",                 "heath bar",                  None,                        "cioccolato caramello"),
    ("Hershey's Dark Chocolate",      "dark chocolate hershey",    "hersheys dark chocolate",    "Hershey's Special Dark",    "cioccolato"),
    ("Hershey's Milk Chocolate",      "hersheys milk chocolate",   "hersheys milk chocolate",    "Hershey's Milk Chocolate",  "cioccolato"),
    ("Junior Mints",                  "junior mints",              "junior mints",               "Junior Mints",              "cioccolato menta"),
    ("Kinder Happy Hippo",            "kinder happy hippo",        "kinder happy hippo",         None,                        "cioccolato arachidi"),
    ("Kit Kat",                       "kit kat",                   "kit kat",                    "Kit Kat",                   "cioccolato"),
    ("Laffy Taffy",                   "laffytaffy",                "laffytaffy",                 "Laffy Taffy",               "frutta"),
    ("LemonHeads",                    "lemonheads",                "lemonheads",                 "Lemonhead",                 "frutta"),
    ("Licorice (black)",              "licorice",                  "licorice yes black",         None,                        "liquirizia"),
    ("Licorice (not black)",          "licorice not black",        "licorice not black",         "Twizzlers",                 "frutta"),
    ("Lindt Truffle",                 "lindt truffle",             "lindt truffle",              None,                        "cioccolato"),
    ("Lollipops",                     "lollipops",                 "lollipops",                  None,                        "frutta"),
    ("Mars",                          "mars",                      "mars",                       None,                        "cioccolato caramello"),
    ("Maynards",                      "maynards",                  "maynards",                   None,                        "frutta"),
    ("Milk Duds",                     "milk duds",                 "milk duds",                  "Milk Duds",                 "cioccolato caramello"),
    ("Milky Way",                     "milky way",                 "milky way",                  "Milky Way",                 "cioccolato caramello"),
    ("Mint Juleps",                   "mint juleps",               "mint juleps",                None,                        "menta"),
    ("Mint Kisses",                   "mint kisses",               "mint kisses",                None,                        "menta"),
    ("M&M's",                         "regular mms",               "regular mms",                "M&M's",                     "cioccolato"),
    ("Peanut M&M's",                  "peanut mms",                "peanut mms",                 "Peanut M&Ms",               "cioccolato arachidi"),
    ("Necco Wafers",                  "necco wafers",              "necco wafers",               None,                        ""),
    ("Nerds",                         "nerds",                     "nerds",                      "Nerds",                     "frutta"),
    ("Nestle Crunch",                 "nestle crunch",             "nestle crunch",              "Nestle Crunch",             "cioccolato"),
    ("Now and Later",                 "nownlaters",                "nownlaters",                 "Now & Later",               "frutta"),
    ("Pixy Stix",                     "pixy stix",                 "pixy stix",                  "Pixie Sticks",              "frutta"),
    ("Reese's Peanut Butter Cups",    "reeses peanut butter cups", "reeses peanut butter cups",  "Reese's Peanut Butter cup", "cioccolato arachidi"),
    ("Rolos",                         "rolos",                     "rolos",                      "Rolo",                      "cioccolato caramello"),
    ("Skittles",                      "skittles",                  "skittles",                   "Skittles original",         "frutta"),
    ("Smarties (American)",           "smarties american",         "smarties american",          "Smarties candy",            "frutta"),
    ("Smarties (Commonwealth)",       "smarties commonwealth",     "smarties commonwealth",      "Nestle Smarties",           "cioccolato"),
    ("Snickers",                      "snickers",                  "snickers",                   "Snickers",                  "cioccolato arachidi caramello"),
    ("Starburst",                     "starburst",                 "starburst",                  "Starburst",                 "frutta"),
    ("Swedish Fish",                  "swedish fish",              "swedish fish",               "Swedish Fish",              "frutta"),
    ("Toblerone",                     "tolberone",                 "tolberone",                  None,                        "cioccolato arachidi"),
    ("Twix",                          "twix",                      "twix",                       "Twix",                      "cioccolato caramello"),
    ("York Peppermint Patties",       "york peppermint patties",   "york peppermint patties",    None,                        "cioccolato menta"),
]

ATTRIBUTI = ["cioccolato", "frutta", "menta", "arachidi", "caramello", "liquirizia"]

# Voci escluse dal catalogo, con il motivo (documentato nel notebook 01)
ESCLUSI = {
    "non è un dolce": ["cash", "dental paraphenalia", "generic brand acetaminophen", "glow sticks",
                        "broken glow stick", "creepy religious comics", "hugs", "lapel pins", "pencils",
                        "peterson brand sidewalk chalk", "vicodin"],
    "cibo non dolce o non da Halloween": ["healthy fruit", "kale smoothie", "minibags of chips", "spotted dick",
                                           "trail mix", "white bread", "whole wheat anything"],
    "dolce inventato o fuori commercio": ["joyjoy", "sweetums", "senior mints", "reggie jackson bar"],
    "categoria generica o giudizio, non un prodotto": ["any fullsized candy bar", "candy that is clearly just",
                                                       "vials of pure high fructose", "jolly rancher bad flavor",
                                                       "jolly ranchers good flavor", "seasalt flavored stuff"],
}


def chiave(testo):
    """Normalizza un nome: minuscolo, solo lettere/numeri/spazi (gestisce apostrofi tipografici e codifiche rotte)."""
    t = str(testo).lower()
    t = re.sub(r"[^a-z0-9 ]", "", t.replace("\t", " "))
    return re.sub(r"\s+", " ", t).strip()


def trova_colonna(colonne, prefisso_chiave):
    """Trova l'unica colonna la cui chiave normalizzata inizia con il prefisso dato."""
    esatte = [c for c in colonne if chiave(c) == prefisso_chiave]
    if len(esatte) == 1:
        return esatte[0]
    trovate = [c for c in colonne if chiave(c).startswith(prefisso_chiave)]
    if len(trovate) != 1:
        raise ValueError(f"'{prefisso_chiave}': trovate {len(trovate)} colonne {trovate[:3]}")
    return trovate[0]
