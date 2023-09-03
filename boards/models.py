from django.db import models
from common.models import Commonmodel


class Board(Commonmodel):
    pageId = models.AutoField(primary_key=True)

    title = models.CharField(
        max_length=100,
        verbose_name="제목",
    )
    contents = models.TextField(
        max_length=500,
        verbose_name="내용",
    )
    parent_page = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="상위 페이지",
    )

    def __str__(self):
        return self.title
