database_config.yaml ：数据库链接配置，可以写入多个数据库配置

database_connection.py 创建数据库链接的模块，使用方法为
	from database_connection import DataBaseConn
	database_conn = DataBaseConn("数据库名称")
此外database_connection.py中可以根据连接的数据库名定义不同的查询方法，查询函数以后可以在这个类上扩充


database_magager.py 对高频数据库中各个合约的数据表进行管理，使用方法为
	database_mng = DatabaseManager()

	database_mng.upd_contract_list() 自动读取当日从CTP接口获取到的所有合约信息的json文件，如果一个ContractId在json文件中存在但在contract_list表不不存在，
	则会新建这个合约的高频数据表，并将这个ContractId添加到contract_list中

	database_mng.del_contract_list() 如果调用，默认自动删除60天以前生成的数据表, 将contract_list中60天前的合约Isavaiable状态置为0

数据表contract_list:
	ContractId: 记录合约id
	UpdDate: 被添加进该表的日期
	Isavailabe: 数据当前是否存在数据库中，如果是则为1。
	