async-flask-sqlalchemy-postgresql
=================================

异步的数据库连接(postgresql)示例

* 安装所需的插件:

	pip install -r requirements.txt

* 需要在postgresql中创建数据库 test_asyn 

* 运行 python app.py -c 用来创建测试的表；

* 运行 Python app.py 来启动服务器，运行 python client 来测试

结果如下:

localhost:async-flask-sqlalchemy-postgresql sixu05202004$ python client.py
Sending 5 requests for http://localhost:8080/test/postgres/...
	@  5.05s got response [200]
	@  5.05s got response [200]
	@  5.05s got response [200]
	@  5.05s got response [200]
	@  5.05s got response [200]
	=  5.06s TOTAL
SUM TOTAL = 5.06s


注意：
1.config.py 中需要修改测试数据库的用户名和密码，并且可以修改pool_size的数量；
2.python client.py num,比如：python client.py 100可以用来模拟更多的连接；
3.如果python client.py num中得num数大于config.py中的SQLALCHEMY_POOL_SIZE = 100时候，我们会发现有些数据库连接又存在阻塞的情况。
比如，我们把SQLALCHEMY_POOL_SIZE改成10，使用python client.py 30来测试，结果如下:

localhost:async-flask-sqlalchemy-postgresql sixu05202004$ python client.py 30
Sending 30 requests for http://localhost:8080/test/postgres/...
	@  5.07s got response [200]
	@  5.07s got response [200]
	@  5.08s got response [200]
	@  5.09s got response [200]
	@  5.09s got response [200]
	@  5.13s got response [200]
	@  5.12s got response [200]
	@  5.12s got response [200]
	@  5.13s got response [200]
	@  5.19s got response [200]
	@  5.19s got response [200]
	@  5.19s got response [200]
	@  5.19s got response [200]
	@  5.19s got response [200]
	@  5.19s got response [200]
	@  5.19s got response [200]
	@  5.19s got response [200]
	@  5.20s got response [200]
	@  5.20s got response [200]
	@  5.20s got response [200]
	@ 10.14s got response [200]
	@ 10.15s got response [200]
	@ 10.15s got response [200]
	@ 10.24s got response [200]
	@ 10.24s got response [200]
	@ 10.24s got response [200]
	@ 10.24s got response [200]
	@ 10.25s got response [200]
	@ 10.25s got response [200]
	@ 10.26s got response [200]
	= 10.28s TOTAL
SUM TOTAL = 10.28s


这是因为 连接数 》SQLALCHEMY_POOL_SIZE + SQLALCHEMY_MAX_OVERFLOW ，我们可以通过一些设置来避免这种情况（NullPool ），但是实际上 postgresql 规定了最大连接数，这个是无法避免的，因此上述的设置最好不要使用
