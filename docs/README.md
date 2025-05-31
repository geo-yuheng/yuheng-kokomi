# Kokomi

一个基于Python的Overpass QL"翻译器"和Overpass查询工具。

A python-based Overpass QL "translator" and Overpass querier.

## 功能概述

这个工具可以提供比原始QL更友好的查询指令（但本质上仍然基于QL）并且可以执行轻量级的查询工作。它也可以作为QL生成助手。目前，该工具不涉及数据更改操作。

## 文档

+ [→ 开始 · 基本内容](https://github.com/Daredemodaisuki/Kokomi/blob/main/docs/1%20-%20To%20start%20and%20invite%20Kokomi.md)
+ [→ 查询语句基础](https://github.com/Daredemodaisuki/Kokomi/blob/main/docs/2%20-%20QL%20with%20OceanHuedClam.md)
+ [→ 进阶联用与输出](https://github.com/Daredemodaisuki/Kokomi/blob/main/docs/3%20-%20More%20thing%20from%20multiple%20OceanHuedClams.md)

## 应用场景示例

+ 查询地名，创建词库，方便调教输入法
+ 查看某物在某地的数量，进行小统计
+ 简单查询要素，无需学习QL或开启JOSM
+ 其他类似场景

## 已知问题 / TODO

+ <del>手动解析xml不能识别没有tag的节点</del>
+ 潜在的append和extend错误使用问题
+ 需要flag_dict以便在查询后于本地筛选
+ 尚无法实现引用的查询构建器中的多次查询需求

## 如何运行

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

## 改进建议

1. 使用更标准的Python命名约定
2. 使用专门的XML解析库而不是手动解析
3. 添加更完善的错误处理
4. 提供更多的文档和示例
5. 考虑使用类型提示和数据类