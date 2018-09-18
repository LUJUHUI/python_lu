import jieba
import pandas as pd
import numpy as np
import random
# Scikit learn 也简称 sklearn, 是机器学习领域当中最知名的 python 模块之一. Sklearn 包含了很多种机器学习的方式
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import gensim
from gensim.models import Word2Vec
from sklearn.preprocessing import scale
import multiprocessing
from sklearn.manifold import TSNE

"""
第二步：
		加载停用词字典，停用词词典为 stopwords.txt 文件，
		可以根据场景自己在该文本里面添加要去除的词（比如冠词、人称、数字等特定词）
"""
stopwords = pd.read_csv('stopwords.txt', index_col=False, sep="\t", names=['stopword'], encoding='utf-8', quoting=3)
stopwords = stopwords['stopword'].values

"""
第三步:
		加载语料，语料是4个已经分好类的 csv 文件，直接用 pandas 加载即可，加载之后
		可以首先删除 nan 行，并提取要分词的 content 列转换为 list 列表
"""

# 3.1 加载语料
husband_df = pd.read_csv('hit_by_husband.csv', encoding='utf-8', sep=',')
wife_df = pd.read_csv('hit_by_wife.csv', encoding='utf-8', sep=',')
daughter_df = pd.read_csv('hit_by_daughter.csv', encoding='utf-8', sep=',')
son_df = pd.read_csv('hit_by_son.csv', encoding='utf-8', sep=',')
# 3.2 删除nan行
husband_df.dropna(inplace=True)
wife_df.dropna(inplace=True)
daughter_df.dropna(inplace=True)
son_df.dropna(inplace=True)
# 3.3 转换
husband = husband_df.segment.values.tolist()
wife = wife_df.segment.values.tolist()
daughter = daughter_df.segment.values.tolist()
son = son_df.segment.values.tolist()


def perprocess_text(content_lines, sentences):
	for line in content_lines:
		try:
			segs = jieba.lcut(line)
			segs = [v for v in segs if not str(v).isdigit()]
			segs = list(filter(lambda x: x.strip(), segs))
			segs = list(filter(lambda x: len(x) > 1, segs))
			segs = list(filter(lambda x: x not in stopwords, segs))
			sentences.append(' '.join(segs))
		except Exception:
			print(line)
			continue


# 调用函数、生成训练数据
sentences = []
perprocess_text(husband, sentences)
perprocess_text(wife, sentences)
perprocess_text(daughter, sentences)
perprocess_text(son, sentences)

#  将得到的数据集打散，生成更可靠的训练集分布，避免同类数据分布不均匀
random.shuffle(sentences)

# 在控制台输出前10条数据，观察一下
for sentence in sentences[:10]:
	print(sentence[0], sentence[1])

"""
 第四步:
        抽取词向量特征
"""
# 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5)
# 统计每个词语的tf-idf权值
transformer = TfidfTransformer()
# 第一个fit_transform是计算tf-idf,第二个fit_transform是将文本转为词频矩阵
tfidf = transformer.fit_transform(vectorizer.fit_transform(sentences))
# 获取词袋模型中的所有词语
word = vectorizer.get_feature_names()
# 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
weight = tfidf.toarray()
# 查看特征大小
print('Features length: ' + str(len(word)))

"""
第五步：
		 实战 TF-IDF 的中文文本 K-means 聚类
"""
# 聚类分几簇
numClass = 4
# 这里也可以选择随机初始化init="random"
clf = KMeans(n_clusters=numClass, max_iter=10000, init="k-means++", tol=1e-6, )  # 这里的tol = 1e-6中的 “1e”是数字1，而不是字母"l"
# 降维
pca = PCA(n_components=10)
#  载入N维
TNewData = pca.fit_transform(weight)
s = clf.fit(TNewData)

"""
定义聚类结果可视化函数 plot_cluster(result,newData,numClass) ，该函数包含
3个参数，其中 result 表示聚类拟合的结果集；newData 表示权重 weight 降维的结果，这里
需要降维到2维，即平面可视化；numClass 表示聚类分为几簇，绘制代码第一部分绘制结果
newData，第二部分绘制聚类的中心点
"""


def plot_cluster(result, newData, numClass):
	plt.figure(2)
	Lab = [[] for i in range(numClass)]
	index = 0
	for labi in result:
		Lab[labi].append(index)
		index += 1
		color = ['oy', 'ob', 'og', 'cs', 'ms', 'bs', 'ks', 'ys', 'yv',
		         'mv', 'bv', 'kv', 'gv', 'y^', 'm^', 'b^', 'k^', 'g^'] * 3
		for i in range(numClass):
			x1 = []
			y1 = []
			for ind1 in newData[Lab[i]]:
				# print ind1
				try:
					y1.append(ind1[1])
					x1.append(ind1[0])
				except:
					pass
			plt.plot(x1, y1, color[i])

		# 绘制初始中心点
		x1 = []
		y1 = []
		for ind1 in clf.cluster_centers_:
			try:
				y1.append(ind1[1])
				x1.append(ind1[0])
			except:
				pass
		plt.plot(x1, y1, "rv")  # 绘制中心
		plt.show()


"""
对数据降维到2维，然后获得结果，最后绘制聚类结果图
"""

pca = PCA(n_components=2)  # 输出两维
# 载入N维
newData = pca.fit_transform(weight)
result = list(clf.predict(TNewData))
plot_cluster(result, newData, numClass)

"""
为了更好的表达和获取更具有代表性的信息，在展示（可视化）高维数据时，
更为一般的处理，常常先用 PCA 进行降维，再使用TSNE
"""
newData = PCA(n_components=4).fit_transform(weight)
newData = TSNE(2).fit_transform(newData)
result = list(clf.predict(TNewData))
plot_cluster((result, newData, numClass))
