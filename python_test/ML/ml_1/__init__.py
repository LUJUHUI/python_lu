"""
 第一步，首先进行语料加载，在这之前，引入所需要的 Python 依赖包，并将全部语料和停用词字典读入内存中

1.1 引入依赖库，有随机数库、jieba 分词、pandas 库等
"""
import jieba
import pandas as pd
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold

"""
 1.2 加载停用词字典，停用词词典为 stopwords.txt 文件，
 可以根据场景自己在该文本里面添加要去除的词（比如冠词、人称、数字等特定词）
"""
# 加载停用词

"""
1 index_col:用作行索引的列编号或者列名，如果给定一个序列则有多个行索引。 如果文件不规则，行尾有分隔符，则可以设定index_col=False
2 quoting:控制csv中的引号常量。
3 sep:指定分隔符。如果不指定参数，则会尝试使用逗号分隔。
4 names:用于结果的列名列表，如果数据文件中没有列标题行，就需要执行header=None。
5 encoding:指定字符集类型，通常指定为'utf-8'
"""
stopwords = pd.read_csv('stopwords.txt', index_col=False, quoting=3, sep='\t', names=['stopword'], encoding='utf-8')
stopwords = stopwords['stopword'].values

"""
 1.3 加载语料，语料是4个已经分好类的 csv 文件，直接用 pandas 加载即可，加载之后
 可以首先删除 nan 行，并提取要分词的 content 列转换为 list 列表.
"""

# 加载语料
husband_df = pd.read_csv("hit_by_husband.csv", encoding='utf-8', sep=",")
wife_df = pd.read_csv("hit_by_wife.csv", encoding='utf-8', sep=",")
daughter_df = pd.read_csv("hit_by_daughter.csv", encoding='utf-8', sep=",")
son_df = pd.read_csv("hit_by_son.csv", encoding='utf-8', sep=",")

# 删除语料的nan行  nan代表有缺失的数据，类似于null、‘’
husband_df.dropna(inplace=True)  # inplace=True：不创建新的对象，直接对原始对象进行修改；inplace=False：对数据进行修改，创建并返回新的对象承载其修改结果。
wife_df.dropna(inplace=True)
daughter_df.dropna(inplace=True)
son_df.dropna(inplace=True)

# 转换
husband = husband_df.segment.values.tolist()
wife = wife_df.segment.values.tolist()
daughter = daughter_df.segment.values.tolist()
son = son_df.segment.values.tolist()

"""
第二步， 分词和去停用词。

2.1 定义分词、去停用词和批量打标签的函数，
函数包含3个参数： 
		content_lines 参数为语料列表；
		sentences 参数为预先定义的 list，用来存储分词并打标签后的结果；
		category参数为标签
"""


# 定义分词和打标签函数preprocess_text
# 参数content_lines即为上面转换的list
# 参数sentences是定义的空list，用来储存打标签之后的数据
# 参数category是类型标签
def preprocess_text(content_lines, sentences, category):
	for line in content_lines:
		try:
			segs = jieba.lcut(line)
			segs = [v for v in segs if not str(v).isdigit()]  # 去数字
			segs = list(filter(lambda x: x.strip(), segs))  # 去左右空格
			segs = list(filter(lambda x: len(x) > 1, segs))  # 长度大于1的字符
			segs = list(filter(lambda x: x not in stopwords, segs))  # 去掉停用词
			sentences.append((" ".join(segs), category))  # 打标签
		except Exception:
			print(line)
			continue


"""
2.2 调用函数、生成训练数据，根据我提供的司法语料数据，
分为报警人被老公打，报警人被老婆打，报警人被儿子打，报警人被女儿打，
标签分别为0、1、2、3，具体如下
"""
sentences = []
preprocess_text(husband, sentences, 0)
preprocess_text(wife, sentences, 1)
preprocess_text(daughter, sentences, 2)
preprocess_text(son, sentences, 3)

"""
2.3 将得到的数据集打散，生成更可靠的训练集分布，避免同类数据分布不均匀
"""
random.shuffle(sentences)

"""
2.4 我们在控制台输出前10条数据
"""
for sentence in sentences[:10]:
	print(sentence[0], sentence[1])  # 0下标是词列表，1是标签

"""
第三步，抽取词向量特征
"""
# 3.1 抽取特征，我们定义文本抽取词袋模型特征

vec = CountVectorizer(
	analyzer='word',  # 按字符'word'标记
	max_features=4000,  # 保持最常见的4000个'word'
)

# 3.2 把语料数据切分，用 sk-learn 对数据切分，分成训练集和测试集
x, y = zip(*sentences)
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1256)

# 3.3 把训练数据转换为词袋模型
vec.fit(x_train)

"""
第四步，分别进行算法建模和模型训练
"""
# 定义朴素贝叶斯模型，然后对训练集进行模型训练，直接使用sklearn中的MultinomialNB
classifier = MultinomialNB()
classifier.fit(vec.transform(x_train), y_train)

"""
第五步， 评估、计算 AUC 值
"""

# 5.1 上面步骤1-4完成了从语料到模型的训练，训练之后，我们要用测试集来计算 AUC值
print(classifier.score(vec.transform(x_test), y_test))  # 0.9952267303102625 但是每次生成的AUC值不是固定的

# 5.2 进行测试集的预测
pre = classifier.predict(vec.transform(x_test))
# print(pre) 打印的结果为二维矩阵

"""
第六步 模型对比
整个模型从语料到训练评估步骤1-5就完成了，接下来我们来看看，改变特征向量模型和训练
模型对结果有什么变化
"""
# 6.1 改变特征向量模型
"""
下面可以把特征做得更强一点，尝试加入抽取 2-gram 和 3-gram 的统计特征，把词库的量放大一点。
"""
vec = CountVectorizer(
	analyzer='word',
	ngram_range=(1, 4),
	max_features=20000,
)
vec.fit(x_train)
# 用朴素贝叶斯算法进行模型训练
classifier = MultinomialNB()
classifier.fit(vec.transform(x_train), y_train)
# 对结果进行评分
print(classifier.score(vec.transform(x_test), y_test))

# 6.2 改变训练模型

# 6.2.1 使用 SVM 训练
svm = SVC(kernel='linear')
svm.fit(vec.transform(x_train), y_train)
print(classifier.score(vec.transform(x_test), y_test))

# 6.2.2 使用决策树、随机森林、XGBoost、神经网络等等


