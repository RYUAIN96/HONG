# 
# python manage.py check

# 1. 회원을 20명 추가하시오.
# ex) 101 102 506 409
# exam_insert
# exam_update
# exam_delete
# exam_select



from django.db import models
from mpmath import clsin

class Table2(models.Model):
    objects = models.Manager() # vs code 오류 제거용

    no        = models.AutoField(primary_key=True)
    name      = models.CharField(max_length=30)
    kor       = models.IntegerField() # 조회수
    eng       = models.IntegerField() # 조회수
    math      = models.IntegerField() # 조회수
    classroom = models.CharField(max_length=3)
    regdate   = models.DateTimeField(auto_now_add=True)
    
