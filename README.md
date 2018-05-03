# ConfigClient 配置管理客户端
manage configuration of services by zookeeper

## 简介
项目背景：python服务治理<br>
公司内所有python服务，统一规范接入配置管理中心；由此通过kazoo实现的配置管理客户端。<br>

## 功能
**本地快照**  客户端会在本地约定目录生成配置快照，用于zookeeper故障容灾；<br>
**动态修改配置** 通过配置管理界面，更改配置，可借由zookeeper的watch 功能实现动态修改配置；<br>
