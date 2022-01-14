from django.db import models


# Create your models here.
class TestTable(models.Model):
    # id = models.BigAutoField(primary_key=True)
    textfield = models.TextField()  # 속성명 변경 text -> content(내용물)

    class Meta:
        db_table = 'test'
