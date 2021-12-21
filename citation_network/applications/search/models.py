from django.db import models

#这一部分是用elasticsearch-dsl####################
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, Completion, Keyword, Text, Integer, Float
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=["localhost"])

class PaperType(DocType):
    Sid = Text()
    title = Text()
    year = Integer()
    inCitations = Text()
    outCitation = Text()
    inCitationscount = Integer()
    outCitationscount = Integer()
    score = Float()

    class Meta:
        index = "otrap"
        doc_type = "paper"

if __name__ == "__main__":
    PaperType.init()

#############################################

# class Paper(models.Model):
#     Sid = models.CharField(primary_key=True, max_length=40, null=False)
#     title = models.CharField(max_length=100, null=False)
#     year = models.IntegerField(null=False)
#     inCitations = models.CharField(max_length=1000)
#     outCitations = models.CharField(max_length=1000)
#     inCitationscount = models.IntegerField(default=0, null=False)
#     outCitationscount = models.IntegerField(default=0, null=False)
#     score = models.IntegerField(default=0, null=False)