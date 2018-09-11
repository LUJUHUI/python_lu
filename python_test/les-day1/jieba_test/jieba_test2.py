import jieba

# 自定义添加词和字典
txt = "铁甲网是中国最大的工程机械交易权威前平台。" \
      "就像世界大V5一样骄傲而自豪"
jieba.add_word("铁甲网")
print(jieba.lcut(txt))
print("-*-" * 80)

# 如果要添加很多个词，一个个添加效率就不够高了，
# 这时候可以定义一个文件，然后通过 load_userdict() 函数，加载自定义词典
jieba.load_userdict('user_dic.txt')
print(jieba.lcut(txt))
print("-*-" * 80)


