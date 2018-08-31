#! /usr/bin/python3
import cards_tools

# 无限循环，由用户决定何时退出系统
while True:
	# 显示系统功能菜单
	cards_tools.show_menu()
	user_input = input("请选择想要执行的操作：")
	print("你选择的操作是 [%s]" % user_input)

	# 1,day2,3针对名片操作
	if user_input in ["1", "2", "3"]:
		# 新增名片
		if user_input == "1":
			cards_tools.new_card()
		# 显示全部名片信息
		elif user_input == "2":
			cards_tools.show_all()
		# 查询名片
		elif user_input == "3":
			cards_tools.search_card()

	# “0”退出系统
	elif user_input == "0":
		print("感谢使用---名片管理系统，期待您的下次使用!")
		break
	# 输入内容错误，提醒用户重新输入
	else:
		print("您输入了错误的选项，请重试!")
