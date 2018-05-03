# ConfigClient 配置管理客户端
manage configuration of services by zookeeper
## 简介
默认使用zk.domain.net获取zookeeper地址列表，zookeeper中配置存储的数据结构可自定义；

## 功能
**本地快照**  客户端会在本地约定目录生成配置快照，用于zookeeper故障容灾；
**动态修改配置** 通过配置管理界面，更改配置，可借由zookeeper的watch 功能实现动态修改配置；
