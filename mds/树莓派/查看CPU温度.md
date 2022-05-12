# 查看CPU温度

```bash
tmp=`adb shell cat /sys/class/thermal/thermal_zone0/temp`
tmp=`expr $tmp / 1000`
echo "tmp = $tmp"
```


