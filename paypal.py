import csv, os
from datetime import datetime
import inspect

class Paypal:
    class Fields:
        DATE, TIME, NETTO, CURRENCY, DIRECTION = "Datum", "Uhrzeit", "Netto", "Währung", "Auswirkung auf Guthaben"
        NAME, HINT, ARTICLE = "Name", "Hinweis", "Artikelbezeichnung"

    def __init__(self, infile):
        self.infile, self.rows = infile, []
        with open(infile, newline='', mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.rows.append(row)

    def is_valid(self):
        csv_columns = self.rows[0].keys()
        for key, value in vars(Paypal.Fields).items():
            if not key.startswith("__"): # skip internal
                if value not in csv_columns:
                    return False
        return True

    def transaction_model(self):
        if not self.is_valid():
            return None

        print(f"Input file is a Paypal .csv")
        print(f"Read {len(self.rows)} Paypal transactions.")

        rows, transactions = [], []
        for row in self.rows:
            dt = datetime.strptime(f"{row[Paypal.Fields.DATE]} {row[Paypal.Fields.TIME]}", '%d.%m.%Y %H:%M:%S')
            new_transaction = {
                'name': row[Paypal.Fields.NAME],
                'date': dt.strftime('%Y-%m-%d'),
                'description': row[Paypal.Fields.HINT] if row[Paypal.Fields.HINT] else row[Paypal.Fields.ARTICLE],
                'amount': (row[Paypal.Fields.NETTO][1:] if row[Paypal.Fields.NETTO].startswith("-") else row[Paypal.Fields.NETTO]).replace(',','.'),
                'credit_or_debit': "DBIT" if row[Paypal.Fields.DIRECTION]=="Soll" else "CRDT",
                'currency': row[Paypal.Fields.CURRENCY],
                'dt': dt
            }
            # skip transactions that are directly paid by credit/debit card
            is_paypal_transaction = True
            for idx, transaction in enumerate(transactions):
                if (transaction['dt'] == new_transaction['dt']) and \
                (transaction['amount'] == new_transaction['amount']) and \
                (transaction['credit_or_debit'] == "CRDT" if new_transaction['credit_or_debit']=="DBIT" else "DBIT"):
                    is_paypal_transaction=False
                    transactions.pop(idx)
                    break
            if is_paypal_transaction:
                transactions.append(new_transaction)
        print(f"{len(self.rows)-len(transactions)} transactions were directly paid by bank transfer.")
        print(f"{len(transactions)} transactions remain.")
        return {'transactions': transactions}
