# 记录所有的名片字典
card_list = []


# 显示菜单
def show_menu():
	print("*" * 50)
	title = "名片管理系统 v1.0"
	print(title.center(45, " ") + "\n")

	fun1 = "[1]：新增名片"
	print(fun1.center(42, " "))
	fun2 = "[2]：显示全部名片信息"
	print(fun2.center(45, " "))
	fun3 = "[3]：查询名片信息"
	print(fun3.center(43, " ") + "\n")
	fun0 = "[0]：退出系统"
	print(fun0.center(42, " "))

	print("*" * 50)


# 新增名片
def new_card():
	print("-" * 50)
	print("新增名片" + "\n")
	# 1.提示用户输入名片信息
	name_str = input("请输入姓名：")
	telphone_str = input("请输入手机号：")
	wechat_str = input("请输入微信号：")
	email_str = input("请输入邮箱：")

	# day2.使用用户输入的信息创建一个名片字典
	card_dic = {"name": name_str,
	            "telphone": telphone_str,
	            "wechat": wechat_str,
	            "email": email_str}

	# 3.将名片字典添加到字典列表中
	card_list.append(card_dic)
	print(card_list)

	# 4.提示用户新增名片成功
	print("新增 %s 名片成功！" % name_str)


# 显示名片
def show_all():
	print("-" * 50)
	print("显示全部名片信息")

	# 判断是否存在记录，如果没有则提示用户添加新的名片记录
	if len(card_list) == 0:
		print("没有记录，请新增名片！")
		return

	for name in ["姓名", "电话", "微信", "邮箱"]:
		print(name, end="\t\t")
	print("")
	print("=" * 50)

	for card_dic in card_list:
		print("%s\t\t%s\t\t%s\t\t%s\t\t" % (card_dic["name"],
		                                    card_dic["telphone"],
		                                    card_dic["wechat"],
		                                    card_dic["email"]))


# 查询名片
def search_card():
	print("-" * 50)
	print("查询名片")

	# 1.提示用户输入搜索的姓名
	find_name = input("请输入要搜索的姓名：")
	for card_dic in card_list:
		if card_dic["name"] == find_name:
			print("姓名\t\t手机号\t\t微信号\t\t邮箱")
			print("=" * 50)
			print("%s\t\t%s\t\t%s\t\t%s\t\t" % (card_dic["name"],
			                                    card_dic["telphone"],
			                                    card_dic["wechat"],
			                                    card_dic["email"]))

			# 针对查找到的信息，进行修改或者删除
			deal_card(card_dic)
			break
	else:
		print("未查询到%s相关信息，请查证后重试!" % find_name)


def deal_card(find_dic):
	"""处理查找到的名片

	:param find_dic: 查找到的名片
	"""
	print(find_dic)
	action_str = input("请选择要执行的操作"
	                   "[1] 修改 [2] 删除 [0] 返回上级菜单")
	if action_str == "1":
		find_dic["name"] = input_card_info(find_dic["name"], "姓名：")
		find_dic["telphone"] = input_card_info(find_dic["telphone"], "手机号：")
		find_dic["wechat"] = input_card_info(find_dic["wechat"], "微信：")
		find_dic["email"] = input_card_info(find_dic["email"], "邮箱：")

		print("修改名片成功！")
	elif action_str == "2":
		card_list.remove(find_dic)
		print("删除名片")


def input_card_info(dic_value, tip_message):
	"""输入名片信息

	:param dic_value: 字典中原有的值
	:param tip_message:输入的提示文字
	:return:如果用户输入内容则直接返回修改后的结果，如果用户没有输入内容，则返回原来的内容
	"""
	# 提示用户输入内容
	result_str = input(tip_message)
	# 针对用户输入的内容进行判断，如果用户输入内容则直接返回修改后的结果
	if len(result_str) > 0:
		return result_str
	# 如果用户没有输入内容，则返回原来的内容
	else:
		return dic_value
