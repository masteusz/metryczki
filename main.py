from pylatex import Document, Section, Subsection, Tabular

if __name__ == "__main__":
    geometry_options = {"documentclass": "a4paper", "margin": "0.5in"}
    doc = Document(geometry_options=geometry_options)

    with doc.create(Section("The simple stuff")):
        with doc.create(Subsection("Table of something")):
            with doc.create(Tabular("rc|cl")) as table:
                table.add_hline()
                table.add_row((1, 2, 3, 4))
                table.add_hline(1, 2)
                table.add_empty_row()
                table.add_row((4, 5, 6, 7))

    doc.generate_pdf("full", clean_tex=False)
