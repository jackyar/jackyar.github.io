### skynet lua api

https://github.com/cloudwu/skynet/wiki/LuaAPI

- skynet.init(func)
- skynet.start(func)
- skynet.newservice()
- skynet.uniqueservice()

------------------------------------------------------------------------------------------------------------------------------------

- 读取Excel文件



```python
excelData = xlrd.open_workbook(path)
# 读取第一个sheet  
table = excelData.sheets()[0]


names = [v.strip() for v in table.row_values(0)]
types = [v.strip() for v in table.row_values(1)]
keyOrAttru = [v.strip() for v in table.row_values(2)]
desc = [v.strip() for v in table.row_values(3)]
```



wsl --set-version Ubuntu-20.04 2

wsl --list --online

wsl --list --verbose

wsl --set-default-version <Version>

wsl --status
