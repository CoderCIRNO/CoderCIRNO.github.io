# 切换Python版本

```bash
function _switch_python_version()
{
    flag=`ls -l /usr/bin/python | grep -c "python2.7"`
    if (($flag == 1))
    then
        echo "python2.7 now, switching..."
        sudo ln -sf /usr/bin/python3.6 /usr/bin/python
        echo "switched to python3.6!"
    else
        echo "python3.6 now, switching..."
        sudo ln -sf /usr/bin/python2.7 /usr/bin/python
        echo "switched to python2.7!"
    fi
}
```

如果当前是2.7，切换到3.6;

如果是3.6，则切换到2.7