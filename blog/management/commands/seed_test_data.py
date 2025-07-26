from django.core.management.base import BaseCommand
from blog.models import Post, PostReadCount

class Command(BaseCommand):
    help = 'Seed test data for posts and read counts'

    def handle(self, *args, **options):
        # 创建测试文章
        post1 = Post.objects.create(title='测试文章1', content='这是测试文章1的内容。')
        post2 = Post.objects.create(title='测试文章2', content='这是测试文章2的内容。')

        # 创建阅读量数据
        PostReadCount.objects.create(post=post1, username='user1', read_count=5)
        PostReadCount.objects.create(post=post1, username='user2', read_count=3)
        PostReadCount.objects.create(post=post2, username='user1', read_count=7)

        self.stdout.write(self.style.SUCCESS('测试数据已成功写入数据库。'))