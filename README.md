## API 接口说明

`DNSPod API配置`

```text
# 按照如下修改src/common.py

# 通过到DNSPod官网后去API的ID及Token，例如：
api_id = 'xxxxx'
api_token = 'xxxxxxxxxx'

# 通过get_domain获取域名及DomainID进行修改，例如：
DomainID = {'domainA': '66117180', 'domainB': '65189308', 'domainC': '66094815'}
```

`API启动`

```bash
cd project
python server.py --port=8888 --log_file_prefix=~/god_api.log
```

```text
/api/get_domain # 获取域名列表
/api/get_record # 获取域名的所有A记录
/api/create_record # 创建域名的指定A记录
/api/remove_record # 删除域名的指定A记录
/api/update_record # 更新域名的指定A记录的IP地址
```


* `/api/get_domain`

```shell
curl 'http://127.0.0.1:8888/api/get_domain'
domain: 80ers.com
domain: xinyuanxian.com
domain: yangbanjian.net
domain: zhinang.org
```

* `/api/get_record`

```shell
curl -d 'domain=poolx.io' 'http://127.0.0.1:8888/api/get_record'
A                1.1.1.1                test                 3600
A                2.2.2.2             chenliang               3600
```

* `/api/create_record`

```shell
curl -d 'domain=poolx.io&short_addr=x.x.x.x&a_record=xx' 'http://127.0.0.1:8888/api/create_record'
True:
{ 'errno': 200, 'result': 0,  'errmsg': 'Action completed successful' }

False:
{ 'errno': 500, 'result': 1,  'errmsg': 'Domain record already exists' }
```

* `/api/remove_record`

```shell
curl -d 'domain=xxxx&a_record=xxxx' 'http://127.0.0.1:8888/api/remove_record'
{ 'errno': 200, 'result': 0,  'errmsg': 'Action completed successful' }
```

* `/api/update_record`

```shell
curl -d 'domain=xxxx&short_addr=xxxx&a_record=xxxx' 'http://127.0.0.1:8888/api/update_record'
{ "errno": "0", "result": "200",  "errmsg": "Action completed successful" }
```
