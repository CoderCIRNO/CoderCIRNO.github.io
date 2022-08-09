# 查看CPU温度

```bash
tmp=`adb shell cat /sys/class/thermal/thermal_zone0/temp`
tmp=`expr $tmp / 1000`
echo "tmp = $tmp"
```
这个命令是在玩工程机的时候发现的。
