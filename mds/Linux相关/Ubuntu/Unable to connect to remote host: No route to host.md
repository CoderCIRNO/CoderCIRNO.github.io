# Unable to connect to remote host: No route to host

## 检查iptables是不是有防火墙的设置

```bash
 iptables -L INPUT --line-numbers
# 结果如下
7    REJECT     all  --  anywhere             anywhere             reject-with icmp-host-prohibited
```

## 删除记录

```bash
iptables -D INPUT 7
```
