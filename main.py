import os, sys, jinja2, csv
from pathlib import Path
from datetime import datetime

DATE, TIME, NETTO, CURRENCY, DIRECTION = "Datum", "Uhrzeit", "Netto", "Währung", "Auswirkung auf Guthaben"
NAME, HINT, ARTICLE = "Name", "Hinweis", "Artikelbezeichnung"

def to_transaction_model(infile):
    rows, transactions = [], []
    with open(infile, newline='', mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    for row in rows:
        dt = datetime.strptime(f"{row[DATE]} {row[TIME]}", '%d.%m.%Y %H:%M:%S')
        transactions.append({'name': row[NAME],
                             'date': dt.strftime('%Y-%m-%d'),
                             'description': row[HINT] if row[HINT] else row[ARTICLE],
                             'amount': row[NETTO][1:] if row[NETTO].startswith("-") else row[NETTO],
                             'credit_or_debit': "CRDT" if row[DIRECTION]=="SOLL" else "DBIT",
                             'currency': row[CURRENCY],
                             'dt': dt
                            })
    return {'transactions': transactions}

def main(argv, arc):
    if (arc != 2):
        raise Exception("Usage:\n> python main.py <<your-paypal.csv>>")
    infile = argv[1]
    if not os.path.exists(infile):
        raise Exception(f"{infile} does not exist.")
    if not Path(infile).suffix == ".csv":
        raise Exception(f"{infile} is not a .csv")
    model = to_transaction_model(infile)

    templateLoader = jinja2.FileSystemLoader(searchpath="./template")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template("camt.053.xml.j2")
    
    out_xml = template.render(model)
    outfile = f"{os.path.dirname(infile)}/{Path(infile).stem}.xml"
    print(f"Writing {outfile}...")
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(out_xml)
    print(f"Success")

if __name__ == "__main__":
    main(sys.argv, len(sys.argv))
