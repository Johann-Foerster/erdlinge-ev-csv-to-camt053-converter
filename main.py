import os, sys, jinja2
from paypal import Paypal
from gls import GLS
from pathlib import Path

def main(argv, arc):
    if (arc != 2):
        raise Exception("Usage:\n> python main.py <<your-paypal.csv>>")
    infile = argv[1]
    if not os.path.exists(infile):
        raise Exception(f"{infile} does not exist.")
    if not Path(infile).suffix.lower() == ".csv":
        raise Exception(f"{infile} is not a .csv")

    model = Paypal(infile).transaction_model()
    if model == None:
        model = GLS(infile).transaction_model()
    if model == None:
        raise Exception(f"{infile} could not be interpreted as Paypal or GLS")

    templateLoader = jinja2.FileSystemLoader(searchpath="./template")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template("camt.053.xml.j2")
    
    out_xml = template.render(model)
    outfile = f"{os.path.dirname(infile)}/{Path(infile).stem}.xml"
    print(f"Writing {len(model['transactions'])} transactions to {outfile}...")
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(out_xml)
    print(f"Success")

if __name__ == "__main__":
    main(sys.argv, len(sys.argv))
