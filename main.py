import os, sys, jinja2
from pathlib import Path

def to_transaction_model(infile):
    return {'transactions': [
                {'name': 'Elizabetha', 'description':'stuff1', 'amount': '100.00', 'currency': 'EUR', 'credit_or_debit': 'CRDT', 'date': '2023-02-24'},
                {'name': 'George', 'description':'stuff2', 'amount': '100.00', 'currency': 'EUR', 'credit_or_debit': 'DBIT', 'date': '2023-02-24'}
            ]} # placeholder

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
