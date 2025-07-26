# 量子堆栈Python-Django测试题3.0

#### 设计一个博客系统的文章阅读量统计功能

场景描述：
- 当用户访问文章详情页时，统计用户人次、每人对应的阅读次数、总阅读次数。
- 阅读量相关统计数据需实时显示（可以只给一个数据接口，或者简单html展示）
- 需设计缓存更新数据库，数据库异步更新，要保证数据一致性安全，防止数据丢失或错误。
- 系统需监控缓存命中率，redis统计、接口查询命中率百分比。

题目要求：
1. 缓存设计：使用Redis缓存阅读量数据，减少数据库IO。
2. 读写分离：读操作优先访问缓存，写操作异步更新数据库。
3. 缓存命中率：优化缓存策略提高命中率，设计数据最终一致性方案。
4. 异常分级处理：区分缓存/数据库异常级别并降级处理。
5. 面向对象封装：模块化设计，分离缓存操作、数据库操作和异常处理。

附上Django官方链接：https://docs.djangoproje

### 说明

项目搭建和部分写法参考开源项目： https://github.com/liangliangyy/DjangoBlog

缓存一致性参考连接：https://mp.weixin.qq.com/s/h1oi92BbdFdTGtey0wQLLQ

缓存策略：
- 缓存 aside 模式
- 缓存更新策略：延迟双删，确保最终一致性

#### 项目启动

```bash
docker-compose --file ./docker-compose.yml up -d
```

#### 项目访问

- http://localhost:8000/blog/post/<int:post_id>/view/<str:username>/ 访问文章详情页，统计阅读量（http://localhost:8000/blog/post/1/view/wang/）

- http://localhost:8000/blog/post/<int:post_id>/stats/ 访问文章统计页，展示阅读量数据（http://localhost:8000/blog/post/1/stats/）
