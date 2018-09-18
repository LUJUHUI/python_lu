from HMM_Model import HMM_Model, seg_stop_words


class HMMSoyoger(HMM_Model):
	""""
	第一个方法 init()，构造函数，定义了初始化变量，具体实现如下:
	"""

	def __init__(self, *args, **kwargs):
		super(HMMSoyoger, self).__init__(*args, **kwargs)
		self.states = STATES  # 此处STATES并没有引入jar包
		self.data = None

	"""
	第二个方法 read_txt() ，加载训练语料，读入文件为 txt，并且 UTF-8 编码，防止中文出现乱码，具体实现如下:
	"""

	# 加载语料
	def read_text(self, filename):
		self.data = open(filename, 'r', encoding='utf-8')

	"""
	第三个方法 train()，根据单词生成观测序列和状态序列，并通过父类的 do_train() 方法进行训练，具体实现如下:
	"""

	# 模型训练函数
	def train(self):
		if not self.inited:
			self.setup()

		for line in self.data:
			line = line.strip()
			if not line:
				continue

			# 观测序列
			observes = []
			for i in range(len(line)):
				if line[i] == " ":
					continue
				observes.append(line[i])

			# 状态序列
			words = line.split(" ")

			states = []
			for word in words:
				if word in seg_stop_words:
					continue
				states.extend(HMM_Model.get_tags(word))

			# 开始训练
			if len(observes) >= len(states):
				self.do_train(observes, states)
			else:
				pass

	"""
	第四个方法 lcut()，模型训练好之后，通过该方法进行分词测试，具体实现如下：
	"""

	# 模型分词预测
	def lcut(self, sentence):
		try:
			tags = self.do_predict(sentence)
			return HMM_Model.cut_sent(sentence, tags)
		except:
			return sentence
