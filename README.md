# HealthReport

> '#'部分替换成抓包抓到的数据
### 依赖

    schedule
    requests

### 更新内容

* 修复上报成功但返回failed的错误
* 优化异常处理
* 增加功能: 填报失败时推送通知(基于wxpusher)

### 运行脚本

    nohup python3 -u main.py > report.log 2>&1 &
