import time
from django.core.cache import cache
from django.db import transaction
from django.db.models import Sum
from .models import Post, PostReadCount

class ReadCountService:
    def __init__(self, post_id):
        if not Post.objects.filter(pk=post_id).exists():
            raise ValueError("Invalid post_id")
        self.post_id = post_id
        self.total_reads_key = f'post:{post_id}:total_reads'
        self.user_reads_key = f'post:{post_id}:user_reads'
        self.cache_hit_rate_key = 'cache_hit_rate_stats'

    def _delete_cache(self):
        """删除与文章相关的缓存。"""
        cache.delete(self.total_reads_key)
        cache.delete(self.user_reads_key)

    def increment_read_count(self, username):
        """延迟双删"""
        # 第一次删除缓存
        self._delete_cache()

        # 更新数据库
        self._update_db(username)

        # 延迟
        time.sleep(1)

        # 第二次删除缓存
        self._delete_cache()

    def get_read_statistics(self):
        """获取阅读统计信息"""
        self._increment_redis_stats('total_queries')

        # 先从缓存读取
        total_reads = cache.get(self.total_reads_key)
        user_reads = cache.get(self.user_reads_key)

        if total_reads is not None and user_reads is not None:
            self._increment_redis_stats('cache_hits')
            print(f"Cache hit for post {self.post_id}")
            return {
                'total_reads': total_reads,
                'user_reads': user_reads
            }

        # 缓存未命中，从数据库加载并写回缓存
        return self._load_from_db_and_cache()

    def _load_from_db_and_cache(self):
        """从数据库加载数据，并写入缓存。"""
        # 从 PostReadCount 表直接计算总阅读量，以保证数据一致性
        total_reads = PostReadCount.objects.filter(post_id=self.post_id).aggregate(Sum('read_count'))['read_count__sum'] or 0

        # 从数据库获取每个用户的阅读量
        user_read_counts = PostReadCount.objects.filter(post_id=self.post_id)
        user_reads = {prc.username: prc.read_count for prc in user_read_counts}

        # 将数据写入缓存
        cache.set(self.total_reads_key, total_reads, timeout=3600)
        cache.set(self.user_reads_key, user_reads, timeout=3600)

        return {
            'total_reads': total_reads,
            'user_reads': user_reads
        }

    # 在事务中更新数据库
    @transaction.atomic
    def _update_db(self, username):
        """在事务中更新数据库中的阅读计数。"""
        # 更新或创建用户的阅读记录
        read_count_obj, created = PostReadCount.objects.get_or_create(
            post_id=self.post_id,
            username=username,
            defaults={'read_count': 0}
        )
        read_count_obj.read_count += 1
        read_count_obj.save()

        # 更新文章总阅读量
        post = Post.objects.select_for_update().get(pk=self.post_id)
        
        # 重新计算总数以保证一致性
        total_reads = PostReadCount.objects.filter(post_id=self.post_id).aggregate(Sum('read_count'))['read_count__sum'] or 0
        post.read_count = total_reads
        post.save()
        print(f"DB updated for post {self.post_id}. Total reads: {total_reads}")

    def get_cache_hit_rate(self):
        """计算并返回缓存命中率。"""
        stats = cache.get(self.cache_hit_rate_key)
        if not stats or stats.get('total_queries', 0) == 0:
            return 0.0
        
        hit_rate = (stats.get('cache_hits', 0) / stats.get('total_queries', 0)) * 100
        return round(hit_rate, 2)

    def _increment_redis_stats(self, field):
        """递增 Redis 中的统计数据。"""
        stats = cache.get(self.cache_hit_rate_key) or {'total_queries': 0, 'cache_hits': 0}
        stats[field] = stats.get(field, 0) + 1
        cache.set(self.cache_hit_rate_key, stats, timeout=None) # 永久保存