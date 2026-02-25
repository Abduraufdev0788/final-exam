from django.db import models


class Category(models.Model):
    name = models.CharField()
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    icon = models.CharField(blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order_num = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['order_num', 'name']
