import jieba

# 词性标注也叫词类标注。pos tagging是part-of-speech tagging的缩写
import jieba.posseg as psg

# 获取分词结果中词列表的 top n
from collections import Counter

content = "现如今，机器学习和深度学习带动人工智能飞速的发展，" \
          "并在图片处理、语音识别领域取得巨大成功。" \
          "你好你好你好你好你好你好。"

# 1 精确分词：精确模式试图将句子最精确地切开，精确分词也是默认分词
segs_1 = jieba.cut(content, cut_all=False)
print("/".join(segs_1))
print("-*-" * 80)

# 2 全模式分词：把句子中所有的可能是词语的都扫描出来，速度非常快，但不能解决歧义。
segs_2 = jieba.cut(content, cut_all=True)
print("/".join(segs_2))
print("-*-" * 80)

# 3 搜索引擎模式：在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词.
segs_3 = jieba.cut_for_search(content, HMM=True)
print("/".join(segs_3))
print("-*-" * 80)

"""
jieba.cut 以及 jieba.cut_for_search 返回的结构都是一个可迭代的 Generator(生成器），可以使用
for 循环来获得分词后得到的每一个词语（Unicode）。jieba.lcut 对 cut 的结果做了封装，l代表 list，
即返回的结果是一个 list 集合。同样的，用 jieba.lcut_for_search 也直接返回list 集合。
"""
segs_4 = jieba.lcut(content)
print(segs_4)
print("-*-" * 80)

segs_5 = jieba.lcut_for_search(content)
print(segs_5)
print("-*-" * 80)

# jieba 可以很方便地获取中文词性，通过 jieba.posseg 模块实现词性标注。
# 第一种写法
for x in psg.lcut(content):
	print([x.word, x.flag])
print("-*-" * 80)
# 第二种写法
print([(x.word, x.flag) for x in psg.lcut(content)])
print("-*-" * 80)

# 并行分词原理为文本按行分隔后，分配到多个 Python 进程并行分词，最后归并结果。
# jieba.enable_parallel(4)  # 开启并行分词模式，参数为并行进程数
# jieba.disable_parallel()  # 关闭并行分词模式
# print("-*-" * 80)

top_5 = Counter(segs_4).most_common(5)  # 列出出现次数最多的5个元素及其计数，按降序依次排列。如果元素为None，则列出所有元素计数
print(top_5)
print("-*-" * 80)
