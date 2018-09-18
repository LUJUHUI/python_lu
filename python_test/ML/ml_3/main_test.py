import HMM_Model
import HMMSoyoger

soyoger = HMMSoyoger()
soyoger.read_text("kafka.txt")
soyoger.train()

al = soyoger.lcut("如果是p2p模式，当一个消费者消费了以后，其他人就消费不了了。")
print(al)
