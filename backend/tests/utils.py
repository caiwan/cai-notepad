import csv
import os, io


def from_csv(*args):
    with open(os.path.join(*args), encoding="utf-8") as f:
        text = f.read()
        stream = io.BytesIO(text.encode("utf-8"))
        reader = csv.DictReader(io.StringIO(text), delimiter=",")
        items = [item for item in reader]
        return (stream, items)
    pass
