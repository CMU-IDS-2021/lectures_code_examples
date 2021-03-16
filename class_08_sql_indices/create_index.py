import pandas as pd

# from whoosh.filedb.filestore import FileStorage
from whoosh.filedb.filestore import RamStorage, FileStorage
from whoosh.fields import *
from whoosh.index import create_in
from whoosh.qparser import QueryParser

__authors__ = "Hendrik Strobelt"

storage = FileStorage("index")
schema = Schema(title=TEXT(stored=True), abstract=TEXT(stored=True))

# index = create_in("index", schema)
index = storage.create_index(schema)

data = pd.read_csv("vis_papers_2020.csv")
abstractNull = data.Abstract.isnull()
with index.writer() as w:
    # anti-pattern but well...
    for idx, _ in data.iterrows():
        title = data.Title[idx]
        abstract = "" if abstractNull[idx] else data.Abstract[idx]
        w.add_document(title=title,
                       abstract=abstract)

with index.searcher() as s:
    q = QueryParser("asbtract", index.schema).parse("Seq2Seq")
    results = s.search(q)
    print(results)
