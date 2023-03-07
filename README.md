# boone

# 部署
``` bash
mkdirs /etc/boone
vim /etc/boone/config.py
```

``` python
# 调试模式
debug = False
```

``` bash
docker build . -t boone
docker run -d --name boone --restart=always -p 8000:8000 -v /etc/boone/config.py boone
```

