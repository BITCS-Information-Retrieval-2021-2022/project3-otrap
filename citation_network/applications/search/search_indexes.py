from haystack import indexes
from .models import Paper

class PaperIndex(indexes.SearchIndex, indexes.Indexable):
    """
    索引数据类
    """
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    def get_model(self):
        return Paper

    def index_queryset(self, using=None):
        return self.get_model().objects.all()