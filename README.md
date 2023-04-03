# 410自动实验系统（v2.0）

--2023.3.29，ljc

### 版本记录

* v4.0（开发中）：支持思仪1465信号发生器
* v3.0（完成待测试）：支持恒誉激光300mm实心转盘的其他采样方式
* v2.0（主分支）：计划支持基于200mm转台的圆环旋转连续序列采样
* v1.2（旧版本）：文档版本，文档拆分为开发文档和快速上手文档
* v1.1（旧版本）：优化版本，采用更简洁的参数配置方法，支持txt、csv、xlsx数据保存格式，更友好的命令行交互
* v1.0（旧版本）：整合200mm电机转盘，实现圆环旋转跨步序列采样
* v0.1（旧版本）：arduino驱动小步进电机，实现中心旋转跨步序列采样



## 警告！

* 系统控制的机械结构具有一定危险性，所搭载的实验器材贵重，使用不当很有可能会造成人员受伤或设备损坏。运行前要着重关注旋转角度、速度、加速度等参数配置的正确性。新手和重要版本更新时请认真阅读系统文档，初次使用请在他人指导下进行实验。
* 有任何疑问不要莽，先找作者咨询！！！



## 系统文档

2.0版本增加序列采样受众较少，时间原因暂不更新配套文档，先拿1.2的将就看，之后有时间一起补。

新版本同样支持原采样方案，细节略有改动，如有问题请联系我。

普通用户：请参考[快速上手](./doc/QuickStart.md)

开发者：请参考[开发手册](./doc/Development.md)



