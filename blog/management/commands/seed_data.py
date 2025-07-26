from django.core.management.base import BaseCommand
from blog.models import Post, PostReadCount

class Command(BaseCommand):
    help = 'Seeds the database with test data for posts and read counts.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old data...')
        Post.objects.all().delete()
        PostReadCount.objects.all().delete()

        self.stdout.write('Creating new data...')

        # 创建文章
        post1 = Post.objects.create(title='Django 最佳实践', content='关于 Django 项目的一些最佳实践分享。')
        post2 = Post.objects.create(title='Redis 入门指南', content='本指南将带你快速入门 Redis。')

        # 为文章1创建阅读记录
        PostReadCount.objects.create(post_id=post1.id, username='alice', read_count=5)
        PostReadCount.objects.create(post_id=post1.id, username='bob', read_count=10)

        # 为文章2创建阅读记录
        PostReadCount.objects.create(post_id=post2.id, username='alice', read_count=2)
        PostReadCount.objects.create(post_id=post2.id, username='charlie', read_count=8)
        PostReadCount.objects.create(post_id=post2.id, username='bob', read_count=1)

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.'))