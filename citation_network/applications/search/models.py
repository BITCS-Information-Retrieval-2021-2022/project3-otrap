from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, Completion, Keyword, Text, Integer
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=["localhost"])

class Paper(DocType):
    _id = Text()
    id = Text()
    Title = Text()
    Year = Integer()
    inCitationscount = Integer()
    outCitationscount = Integer()

    class Meta:
        index = "paper"
        doc_type = "article"

if __name__ == "__main__":
    Paper.init()