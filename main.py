from csv import DictReader

from pylatex import Document, Tabu, MultiColumn, FootnoteText
from pylatex.utils import bold

ZAWODNICY_FILE = "zawodnicy.csv"
KONKURENCJE = (
    "Pistolet Centralnego Zapłonu PCZ",
    "Pistolet Sportowy Bocznego Zapłonu PBZ",
    "Karabin Centralnego Zapłonu KCZ",
    "Karabin Centralnego Zapłonu Optyka KCZO",
    "Karabin sportowy bocznego zapłonu KBZ",
    "Karabin sportowy bocznego zapłonu Optyka KBZO",
    "Strzelba Gładkolufowa SG",
    "Strzelba Gładkolufowa Open SGO",
    "Pistolet Blaszanka PB",
)


def create_table(
    document: Document,
    nazwisko: str,
    imie: str,
    klub: str,
    licencja: str,
    konkurencja: str,
    bron: str,
):
    with document.create(
        Tabu("|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|")
    ) as table:
        table.add_hline()
        table.add_row(
            (
                MultiColumn(size=3, align="|l", data=FootnoteText("Nazwisko")),
                MultiColumn(size=2, align="|l", data=FootnoteText("Imię")),
                MultiColumn(size=4, align="|l", data=FootnoteText("Klub")),
                MultiColumn(size=3, align="|l|", data=FootnoteText("Nr Licencji PZSS")),
            )
        )
        table.add_row(
            (
                MultiColumn(size=3, align="|l", data=bold(nazwisko)),
                MultiColumn(size=2, align="|l", data=bold(imie)),
                MultiColumn(size=4, align="|l", data=bold(klub)),
                MultiColumn(size=3, align="|l|", data=bold(licencja)),
            )
        )
        table.add_hline()
        table.add_row(
            (
                MultiColumn(size=2, align="|l|", data="Konkurencja:"),
                MultiColumn(size=8, align="c|", data=bold(konkurencja)),
                "Broń:",
                bold(bron),
            )
        )
        table.add_hline()
        table.add_row(("Strzały:", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "SUMA"))
        table.add_hline()
        table.add_row("Wynik:", *(11 * [" "]))
        table.add_hline()
        table.add_row((MultiColumn(size=12, align="l", data=""),))
        table.add_row(
            (
                MultiColumn(
                    size=4,
                    align="l",
                    data=FootnoteText("Podpis sędziego stanowiskowego"),
                ),
                MultiColumn(
                    size=5, align="l", data=FootnoteText("Podpis sędziego oceniającego")
                ),
                MultiColumn(size=3, align="l", data=FootnoteText("Podpis zawodnika")),
            )
        )
        table.add_row((MultiColumn(size=12, align="l", data=""),))
        table.add_row((MultiColumn(size=12, align="l", data=""),))

        table.add_hline(1, 3)
        table.add_hline(5, 7)
        table.add_hline(10, 12)
        table.add_row((MultiColumn(size=12, align="l", data=""),))


def parse_line(line: dict):
    for k in KONKURENCJE:
        outdict = {
            "nazwisko": line.get("Nazwisko"),
            "imie": line.get("Imię"),
            "klub": line.get("Klub"),
            "licencja": line.get("Nr Licencji PZSS"),
        }
        bron = line.get(k)
        if not bron:
            continue
        outdict["konkurencja"] = k
        outdict["bron"] = bron
        yield outdict


def read_data(fname=ZAWODNICY_FILE):
    with open(fname) as csvfile:
        reader = DictReader(csvfile)
        for line in reader:
            for res in parse_line(line):
                yield res


if __name__ == "__main__":
    geometry_options = {"margin": "0.3in"}
    doc = Document(geometry_options=geometry_options)
    for comp in read_data():
        create_table(document=doc, **comp)
    doc.generate_pdf("full", clean_tex=False)
