import pickle
import json

STARTS = {"B", "E", "M", "S"}
EPS = 0.0001
# 定义停顿标点
seg_stop_words = {" ", "，", "。", "“", "”", '“', "？", "！", "：", "《",
                  "》", "、", "；", "·", "‘ ", "’", "──", ",", ".", "?", "!", "`", "~",
                  "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "[", "]",
                  "{", "}", '"', "'", "<", ">", "\\", "|" "\r", "\n", "\t"}


class HMM_Model:
	"""
	第一个方法 __init__() 是一种特殊的方法，被称为类的构造函数或初始化方法，当创建了
    这个类的实例时就会调用该方法，其中定义了数据结构和初始变量，实现如下:
	"""

	def __init__(self):
		# trans_mat ：状态转移矩阵， trans_mat[state1][state2] 表示训练集中由 state1 转移到 state2 的次数
		self.trans_mat = {}
		# emit_mat ：观测矩阵， emit_mat[state][char] 表示训练集中单字 char 被标注为state 的次数
		self.emit_mat = {}
		# init_vec : 初始状态分布向量， init_vec[state] 表示状态 state 在训练集中出现的次数
		self.init_vec = {}
		# state_count ：状态统计向量， state_count[state] 表示状态 state 出现的次数
		self.state_count = {}
		# word_set ：词集合，包含所有单词
		self.states = {}
		self.inited = False

	"""
	第二个方法 setup()，初始化第一个方法中的数据结构,实现如下:
	"""

	# 初始化
	def setup(self):
		for state in self.states:
			self.trans_mat[state] = {}
			for target in self.states:
				self.trans_mat[state][target] = 0.0
			self.emit_mat[state] = {}
			self.init_vec[state] = 0
			self.state_count[state] = 0
		self.inited = True

	"""
	第三个方法 save()，用来保存训练好的模型，filename 指定模型名称，默认模型名称为
	hmm.json，这里提供两种格式的保存类型，JSON 或者 pickle 格式，通过参数 code 来决
	定，code 的值为 code='json' 或者 code = 'pickle' ，默认为 code='json' ，具体实现
	如下:
	"""

	# 模型保存
	def save(self, filename='hmm.json', code='json'):
		fw = open(filename, 'w', encoding='utf-8')
		data = {
			"trans_mat": self.trans_mat,
			"emit_mat": self.emit_mat,
			"init_vec": self.init_vec,
			"state_count": self.state_count
		}
		if code == "json":
			txt = json.dumps(data)
			txt = txt.encode('utf-8').decode('unicode-escape')
			fw.write(txt)
		elif code == "pickle":
			pickle.dumps(data, fw)
		fw.close()

	"""
	第四个方法 load()，与第三个 save() 方法对应，用来加载模型，filename 指定模型名称，
	默认模型名称为 hmm.json，这里提供两种格式的保存类型，JSON 或者 pickle 格式，通过参数 code 来决定，
	code 的值为 code='json' 或者 code = 'pickle' ，默认为code='json' ，具体实现如下：
	"""

	# 模型加载
	def load(self, filename="hmm.json", code="json"):
		fr = open(filename, 'r', encoding='utf-8')
		if code == 'json':
			txt = fr.read()
			model = json.loads(txt)
		elif code == 'pickle':
			model = pickle.load(fr)
		self.trans_mat = model["trans_mat"]
		self.emit_mat = model["emit_mat"]
		self.init_vec = model["init_vec"]
		self.state_count = model["state_count"]
		self.inited = True
		fr.close()

	"""
	第五个方法 do_train() ，用来训练模型，因为使用的标注数据集， 因此可以使用更简单的
	监督学习算法，训练函数输入观测序列和状态序列进行训练， 依次更新各矩阵数据。类中维
	护的模型参数均为频数而非频率， 这样的设计使得模型可以进行在线训练，使得模型随时都
	可以接受新的训练数据继续训练，不会丢失前次训练的结果。具体实现如下:
	"""

	# 模型训练
	def do_train(self, observes, states):
		if not self.inited:
			self.setup()
		for i in range(len(states)):
			if i == 0:
				self.init_vec[states[0]] += 1
				self.state_count[states[0]] += 1
			else:
				self.trans_mat[states[i - 1]][states[i]] += 1
				self.state_count[states[i]] += 1
				if object[i] not in self.emit_mat[states[i]]:
					self.emit_mat[states[i]][observes[i]] = 1
				else:
					self.emit_mat[states[i]][observes[i]] += 1

	"""
	第六个方法 get_prob() ，在进行预测前，需将数据结构的频数转换为频率，具体实现如下:
	"""

	# HMM训练
	def get_prob(self):
		init_vec = {}
		trans_mat = {}
		emit_mat = {}
		default = max(self.state_count.values())
		for key in self.init_vec:
			if self.state_count != 0:
				init_vec[key] = float(self.init_vec[key]) / self.state_count[key]
			else:
				init_vec[key] = float(self.init_vec[key]) / default

		for key1 in self.trans_mat:
			trans_mat[key1] = {}
			for key2 in self.trans_mat[key1]:
				if self.trans_mat[key1] != 0:
					trans_mat[key1][key2] = float(self.trans_mat[key1][key2]) / self.state_count[key1]
				else:
					trans_mat[key1][key2] = float(self.trans_mat[key1][key2]) / default

		for key1 in self.emit_mat:
			emit_mat[key1] = {}
			for key2 in self.emit_mat[key1]:
				if self.state_count[key1] != 0:
					emit_mat[key1][key2] = float(self.emit_mat[key1][key2]) / self.state_count[key1]
				else:
					emit_mat[key1][key2] = float(self.emit_mat[key1][key2]) / default
		return init_vec, trans_mat, emit_mat

	"""
	第七个方法 do_predict() ，预测采用 Viterbi 算法求得最优路径， 具体实现如下：
	"""

	# 模型预测
	def do_predict(self, sequence):
		tab = [{}]
		path = {}
		init_vec, trans_mat, emit_mat = self.get_prob()

		# 初始化
		for state in self.states:
			tab[0][state] = init_vec[state] * emit_mat[state].get(sequence[0], EPS)
			path[state] = [state]

		# 创建动态搜索表
		for t in range(1, len(sequence)):
			tab.append({})
			new_path = {}
			for state1 in self.states:
				items = []
				for state2 in self.states:
					if tab[t - 1][state2] == 0:
						continue
					prob = tab[t - 1][state2] * trans_mat[state2].get(state1, EPS) * emit_mat[state1].get(sequence(t),
					                                                                                      EPS)
					items.append(prob, state2)
					best = max(items)
					tab[t][state1] = best[0]
					new_path[state1] = path[best[1]] + [state1]
					path = new_path
		# 搜索最优路径
		prob, state = max([(tab[len(sequence) - 1][state], state) for state in self.states])
		return path(state)

	"""
	1 定义一个工具函数对输入的训练语料中的每个词进行标注，
	  因为训练数据是空格隔开的，可以进行转态标注，该方法用在训练数据的标注，具体实现如下:
	"""

	def get_tags(src):
		tags = []
		if len(src) == 1:
			tags = ['S']
		elif len(src) == 2:
			tags = ['B', 'E']
		else:
			m_num = len(src) - 2
			tags.append('B')
			tags.extend(['M'] * m_num)
			tags.append('S')
		return tags

	"""
	2 定义一个工具函数根据预测得到的标注序列将输入的句子分割为词语列表，
	  也就是预测得到的状态序列，解析成一个 list 列表进行返回，具体实现如下：
	"""

	def cut_sent(src, tags):
		word_list = []
		start = -1
		started = False

		if len(tags) != len(src):
			return None
		if tags[-1] not in ['B', 'E']:
			if tags[-2] in ['B', 'E']:
				tags[-1] = 'B'
			else:
				tags[-1] = 'E'
		for i in range(len(tags)):
			if tags[i] == 'S':
				if started:
					started = False
					word_list.append(src[start:i])
				word_list.append(src[i])
			elif tags[i] == 'B':
				if started:
					word_list.append(src[start:i])
				start = i
				started = True
			elif tags[i] == 'E':
				started = False
				word = src[start:i + 1]
				word_list.append(word)
			elif tags[i] == 'M':
				continue
		return word_list
