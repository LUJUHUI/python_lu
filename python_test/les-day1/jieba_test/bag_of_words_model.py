import jieba
from collections import Counter

# 1 定义停用词、标点符号
punctuaction = [',', '.', '。', '，', ':', '；', '?', '？', '!', '！', '、', ' ']

# 2 定义语料
sentence = "道可道，非常道。名可名，非常名。无名天地之始。有名万物之母。故常无欲以观其妙。常有欲以观其徼。" \
           "此两者同出而异名，同谓之玄。玄之又玄，众妙之门。" \
           "天下皆知美之为美，斯恶矣；皆知善之为善，斯不善已。故有无相生，难易相成，长短相形，高下相" \
           "倾，音声相和，前後相随。是以圣人处无为之事，行不言之教。万物作焉而不辞。生而不有，为而不恃，" \
           "功成而弗居。夫唯弗居，是以不去。" \
           "不尚贤， 使民不争。不贵难得之货，使民不为盗。不见可欲，使民心不乱。是以圣人之治，虚其心，" \
           "实其腹，弱其志，强其骨；常使民无知、无欲，使夫智者不敢为也。为无为，则无不治。" \
           "道冲而用之，或不盈。渊兮似万物之宗。解其纷，和其光，同其尘，湛兮似或存。吾不知谁之子，象帝之先。" \
           "天地不仁，以万物为刍狗。圣人不仁，以百姓为刍狗。天地之间，其犹橐迭乎？虚而不屈，动而愈出" \
           "。多言数穷，不如守中。" \
           "谷神不死是谓玄牝。玄牝之门是谓天地根。绵绵若存，用之不勤。" \
           "天长地久。天地所以能长且久者，以其不自生，故能长生。是以圣人後其身而身先，外其身而身存。" \
           "非以其无私邪！故能成其私。" \
           "上善若水。水善利万物而不争，处众人之所恶，故几於道。居善地，心善渊，与善仁，言善信，正善" \
           "治，事善能，动善时。夫唯不争，故无尤。" \
           "持而盈之不如其己；揣而锐之不可长保；金玉满堂莫之能守；富贵而骄，自遗其咎。功遂身退，天之道。" \
           "载营魄抱一，能无离乎？专气致柔，能如婴儿乎？涤除玄览，能无疵乎？爱国治民，能无为乎？天门" \
           "开阖，能为雌乎？明白四达，能无知乎。"

# 3 分词
seg_1 = [jieba.lcut(con) for con in sentence]
# print(seg_1)

# 4 因为中文语料带有停用词和标点符号，所以需要去停用词和标点符号，这里语料很小，我们直接去标点符号
tokenized = []
for sentence in seg_1:
	words = []
	for word in sentence:
		if word not in punctuaction:
			words.append(word)
	tokenized.append(words)
# print(tokenized)

# 5 求并集
# 第一种写法
# bag_of_words = []
# for item in seg_1:
# 	for x in item:
# 		if x not in punctuaction:
# 			bag_of_words.append(x)
# print(bag_of_words)
# print("-*-" * 60)

# 第二种写法
bag_of_words = [x for item in seg_1 for x in item if x not in punctuaction]

# 6 去重
bag_of_words = list(set(bag_of_words))
print(bag_of_words)
print("*" * 60)

# 7 以上面特征词的顺序，完成词袋化
bag_of_word2vec = []
for sentence in tokenized:
	tokens = [1 if token in sentence else 0 for token in bag_of_words]
	bag_of_word2vec.append(tokens)
print(bag_of_word2vec)
