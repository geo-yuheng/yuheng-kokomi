# Kokomi

一个基于Python的Overpass QL"翻译器"和Overpass查询工具。

A python-based Overpass QL "translator" and Overpass querier.

## 简介

这个工具可以提供比原始QL更友好的查询指令（但本质上仍然基于QL）并且可以执行轻量级的查询工作。它也可以作为QL生成助手。目前，该工具不涉及数据更改操作。

## 文档

详细文档请查看 [docs/README.md](docs/README.md)

## 快速开始

```python
from kokomi import QueryClient
from kokomi.query_builder import QueryBuilder

# 创建查询客户端
client = QueryClient()

# 设置Overpass API端点
client.network_config_set("OSMde")

# 创建查询构建器
query = QueryBuilder("node")
query.key_value("amenity", "=", "restaurant")

# 执行查询
results = client.query(query)

# 处理结果
print(f"找到了 {len(client.directive_dict['node'])} 个节点")
```
