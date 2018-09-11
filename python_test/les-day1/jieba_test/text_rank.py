import jieba.analyse

import tf_idf

result = " ".join(jieba.analyse.textrank(tf_idf.sentence, topK=7, withWeight=False, allowPOS=('n', 'v', 'ns', 'vn')))
print(result)  # 天地 不争 圣人 心善 使夫 刍狗 无疵
print("*" * 50)

result = " ".join(jieba.analyse.textrank(tf_idf.sentence, topK=7, withWeight=False, allowPOS=('n', 'v')))
print(result)  # 天地 不争 圣人 心善 使夫 刍狗 动善
