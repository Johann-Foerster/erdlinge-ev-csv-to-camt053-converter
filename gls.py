import csv
from datetime import datetime
import inspect

class GLS:
    class Fields:
        DATE, AMOUNT, CURRENCY, NAME, PURPOSE = "Buchungstag", "Betrag", "Waehrung", "Name Zahlungsbeteiligter", "Verwendungszweck"

    def __init__(self, infile):
        self.infile, self.rows = infile, []
        with open(infile, newline='', mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                self.rows.append(row)

    def is_valid(self):
        csv_columns = self.rows[0].keys()
        unmatched_columns = []
        for key, value in vars(GLS.Fields).items():
            if not key.startswith("__"): # skip internal
                if value not in csv_columns:
                    return False
        return True

    def transaction_model(self):
        if not self.is_valid():
            return None

        print(f"{self.infile} columns match GLS .csv style.")
        print(f"Read {len(self.rows)} GLS transactions from {self.infile}.")

        rows, transactions = [], []
        for row in self.rows:
            dt = datetime.strptime(f"{row[GLS.Fields.DATE]}", '%d.%m.%Y')
            new_transaction = {
                'name': row[GLS.Fields.NAME],
                'date': dt.strftime('%Y-%m-%d'),
                'description': row[GLS.Fields.PURPOSE],
                'amount': (row[GLS.Fields.AMOUNT][1:] if row[GLS.Fields.AMOUNT].startswith("-") else row[GLS.Fields.AMOUNT]).replace(',','.'),
                'credit_or_debit': "DBIT" if row[GLS.Fields.AMOUNT].startswith("-") else "CRDT",
                'currency': row[GLS.Fields.CURRENCY],
                'dt': dt
            }
            transactions.append(new_transaction)
        return {'transactions': transactions}
