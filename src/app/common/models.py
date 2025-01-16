from django.db import models

from common.shortcuts import transliterate


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    saved = models.DateTimeField(auto_now=True)
    active = models.BooleanField(null=False, default=True)

    class Meta:
        abstract = True


class BaseViewableModel(BaseModel):
    name = models.CharField(
        max_length=200, 
        verbose_name="Название",
        ) 
    slug = models.SlugField(
        blank=True,
        )
    brief = models.TextField(
        blank=True, 
        verbose_name='Краткое описание',
    )
    description = models.TextField(
        blank=True, 
        verbose_name='Описание',
        )
    image = models.ImageField(
        null=True,
        upload_to='img', 
        blank=True, 
        verbose_name="Картинка",
        )
    
    class Meta:
        abstract = True

    def get_display_name(self):
        return self.name
    
    def __str__(self):
        return self.name
    
    
class BaseRelation(BaseModel):
    """Basic model for Many-to-Many relationships"""
    priority = models.IntegerField(
        default=1,
        null=False,
        blank=True,
        verbose_name="Приоритет"
    )

    class Meta:
        abstract = True
        ordering = ('priority', 'pk')

        
def batch_qs(qs:models.QuerySet, batch_size=1000):
    """
    see https://djangosnippets.org/snippets/1170/

    Returns a (start, end, total, queryset) tuple for each batch in the given
    queryset.
    
    Usage:
        # Make sure to order your querset
        article_qs = Article.objects.order_by('id')
        for start, end, total, qs in batch_qs(article_qs):
            print "Now processing %s - %s of %s" % (start + 1, end, total)
            for article in qs:
                print article.body
    """
    total = qs.count()
    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        yield (start, end, total, qs[start:end])