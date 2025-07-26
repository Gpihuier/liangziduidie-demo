from django.db import models
from django.utils.timezone import now

class BashModel(models.Model):
    id = models.AutoField(primary_key=True)
    create_at = models.DateTimeField('create_at', default=now)
    update_at = models.DateTimeField('update_at', default=now)

class Post(BashModel):
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')

class PostReadCount(BashModel):
    post_id = models.IntegerField('文章ID')
    username = models.CharField('用户名', max_length=30, default='', blank=True)
    read_count = models.IntegerField('阅读量', default=0)
    
