# _*_ coding:utf-8 _*_
# author : CuiZhengliang
# name: QA_R Baseline

import random
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import SementicRoleLabeller
from pyltp import NamedEntityRecognizer
from pyltp import Parser


# 分词
def ini_ltp():
	segmentor = Segmentor()  # 初始化实例
	segmentor.load('../../ltp_data_v3.4.0/cws.model')  # 加载模型
	postagger = Postagger()  # 初始化实例
	postagger.load('../../ltp_data_v3.4.0/pos.model')  # 加载模型
	parser = Parser()  # 初始化实例
	parser.load('../../ltp_data_v3.4.0/parser.model')  # 加载模型
	return segmentor, postagger, parser


def release_ltp(segmentor, postagger, parser):
	segmentor.release()
	postagger.release()
	parser.release()


def segmentor_process(segmentor, sentence=' '):
	# segmentor = Segmentor()  # 初始化实例
	# segmentor.load('/usr/local/nlp/ltp_data/cws.model')  # 加载模型
	words = segmentor.segment(sentence)  # 分词
	# 默认可以这样输出
	# print '\t'.join(words)
	# '\t'.join(words)
	# 可以转换成List 输出
	words_list = list(words)
	# segmentor.release()  # 释放模型
	return words_list


def posttagger_process(postagger, words):
	# postagger = Postagger() # 初始化实例
	# postagger.load('/usr/local/nlp/ltp_data/pos.model')  # 加载模型
	postags = postagger.postag(words)  # 词性标注
	'''
	for word,tag in zip(words,postags):
		print word+'/'+tag
	'''
	# postagger.release()  # 释放模型
	return postags


# 依存语义分析
def parse_process(parser, words, postags):
	# parser = Parser() # 初始化实例
	# parser.load('/usr/local/nlp/ltp_data/parser.model')  # 加载模型
	arcs = parser.parse(words, postags)  # 句法分析
	# print "\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs)
	# parser.release()  # 释放模型
	all_num = [(i, arc.relation) for (i, arc) in enumerate(arcs)]
	# all_num = [(arc.head, arc.relation) for  arc in  arcs]
	first_part = []
	index_num = []
	hed_flag = False
	
	for num_i in all_num:
		first_part.append(num_i)
		if num_i[1] == "HED":
			hed_flag = True
			for num_j in first_part[::-1]:
				if num_j[1] == "SBV":
					index_num.append(num_j[0])
					break
			index_num.append(num_i[0])
		if num_i[1] == "VOB" and hed_flag == True:
			index_num.append(num_i[0])
			break
	# list_sentence= [words[i] for i in index_num]
	last_words = ''.join([words[i] for i in index_num])
	return last_words


# give the answer of template
def give_answer(input_list, postagger, index):
	postags = posttagger_process(postagger, input_list)
	# for word,tag in zip(input_list,postags):
	# print word+'_'+tag
	# sentence_list_1 = ["能", "好好", "VOB|V", "吗?"]
	rand_int = random.randint(1, 10)
	if index == 1:
		# silence
		change_pos = input_list.index("好好") + 1
		if rand_int == 1:
			return "都说可以了!"
		if rand_int == 2:
			return "肯定可以啊!"
		if rand_int == 3:
			return "当然啦!"
		if rand_int == 4:
			return "为啥不能呢？"
		if rand_int == 5:
			return "我不太会呢，以后有机会要学习一下，嘻嘻!"
		# replay
		if rand_int == 6:
			return "我不" + input_list[change_pos] + "了"
		if rand_int == 7:
			return input_list[change_pos] + "好难!"
		if rand_int == 8:
			return "怎么才算好好" + input_list[change_pos] + "?求教啊."
		if rand_int == 9:
			return "之前一直没有好好" + input_list[change_pos] + "吗?"
		# open and turn
		if rand_int == 10:
			return "我不大会啊，" + "你会" + input_list[change_pos] + "吗？"
	# sentence_list_2 = [r 和 r v 过 吗？]
	if index == 2:
		change_pos = input_list.index("过") - 1
		change_pos1 = 0
		for word, tag in zip(input_list, postags):
			if tag == 'c':
				change_pos1 = input_list.index(word)
		# print word+'_'+tag
		# silence
		if rand_int == 1:
			return "是啊！"
		if rand_int == 2:
			return "没有，都很忙！"
		if rand_int == 3:
			return "是个秘密哦!"
		if rand_int == 4:
			return "忘了啊!"
		if rand_int == 5:
			return "大概、也许、可能..."
		# replay
		if rand_int == 6:
			return input_list[change_pos] + "了何止一次，没用"
		if rand_int == 7:
			if input_list[change_pos + 1] == "谁":
				return "跟我"
			elif input_list[change_pos - 1] == "谁":
				return "记不清啊"
			else:
				return input_list[change_pos - 1] + input_list[change_pos] + input_list[change_pos + 1] + input_list[
					change_pos] + "过"
		if rand_int == 8:
			return input_list[change_pos] + "了啊"
		if rand_int == 9:
			return "还没" + input_list[change_pos] + "呢"
		if rand_int == 10:
			return "别管这些了，说说你啊"
	# sentence_list_3 = [听说 你 去 过 美国，去 过 了 吗？]
	if index == 3:
		for word, tag in zip(input_list, postags):
			if tag == 'ns':
				change_pos1 = input_list.index(word)
		# silence
		if rand_int == 1:
			return "当然去过了."
		if rand_int == 2:
			return "还没有"
		if rand_int == 3:
			return "听谁说的,他骗你的,我没去过"
		if rand_int == 4:
			return "不要听说,要相信眼见为实啊！"
		if rand_int == 5:
			return "呵呵，我忘了"
		# replay
		if rand_int == 6:
			return input_list[change_pos1] + "在哪啊?没去过."
		if rand_int == 7:
			return input_list[change_pos1] + "是个好地方"
		if rand_int == 8:
			return "又是" + input_list[change_pos1] + "，去过很多次呢"
		if rand_int == 9:
			return "听谁说的？" + input_list[change_pos1] + "还真不错"
		# open and turn
		if rand_int == 10:
			return "你也对" + input_list[change_pos1] + "感兴趣，啥时候我们一起去？"
	# sentence_list_3 = [你 厉害 吗？]
	if index == 4:
		change_pos = input_list.index("吗") - 1
		# silence
		if rand_int == 1:
			return "有点"
		if rand_int == 2:
			return "当然"
		if rand_int == 3:
			return "你觉得呢？"
		if rand_int == 4:
			return "我自己也不知道啊"
		if rand_int == 5:
			return "必须的"
		if rand_int == 6:
			return "有点" + input_list[change_pos]
		if rand_int == 7:
			return "好" + input_list[change_pos] + "啊"
		if rand_int == 8:
			return "不算" + input_list[change_pos]
		if rand_int == 9:
			return "还好啊，比你" + input_list[change_pos]
		if rand_int == 10:
			return "你我皆" + input_list[change_pos]
	if index == 5:
		change_pos = input_list.index("吗") - 1
		# pre_process
		# if input_list[change_pos] == "命中知识图谱"
		#    return "图谱中人物解释"
		if rand_int == 1:
			return "我只认识自己"
		if rand_int == 2:
			return "熟人,装不认识什么的"
		if rand_int == 3:
			return "朋友认识，我不认识哈。"
		if rand_int == 4:
			return "希望认识"
		if rand_int == 5:
			return "啦啦啦，不认识"
		if rand_int == 6:
			return input_list[change_pos] + ",好像很厉害的样子"
		if rand_int == 7:
			return "也许" + input_list[change_pos] + "认识我，但我不认识他"
		if rand_int == 8:
			return input_list[change_pos] + "，我们一起去打怪！"
		if rand_int == 9:
			return "我想认识的都不认识我，我不想见的却偏偏在我面前晃"
		if rand_int == 10:
			return "你认识吗，介绍给我如何？"
	if index == 6:
		# 1.template                       你有想法吗？   木有
		# 2.template + knowledge graph     你有理想吗？   我的理想[就是]世界和平;  你有姐姐吗？  [有]表姐
		# 3.learning from the reality      你有心吗？ 别以为我不知道你在想什么！; 你有头脑吗？ 教我赚钱
		change_pos = input_list.index("吗") - 1
		# pre_process
		# if input_list[change_pos] == "命中知识图谱"
		#    return "图谱中人物解释"
		if rand_int == 1:
			return "当然"
		if rand_int == 2:
			return "木有"
		if rand_int == 3:
			return "有啊，咋啦？"
		if rand_int == 4:
			return "你说有就有了"
		if rand_int == 5:
			return "也许有，也许没有"
		if rand_int == 6:
			return "有" + input_list[change_pos]
		if rand_int == 7:
			return input_list[change_pos] + ",让我想想..."
		if rand_int == 8:
			return "有的，有的"
		if rand_int == 9:
			return "当我想" + input_list[change_pos] + "的时候就有了，一般没有"
		if rand_int == 10:
			return "你有" + input_list[change_pos] + "吗？我也好奇"


# return dictionary{key_word: index_of_line_number1,...,index_of_line_numberN}
def create_reverse_index():
	reverse_dict = {}  # a empty dictionary.
	# n = 100
	file_r = open("templet/askModel.txt")
	file_lines = file_r.readlines()
	row = 0
	for lines in file_lines[1:]:
		whole_line = lines.strip()
		number_of_keyword = whole_line.split(";")[0]
		whole_line = whole_line.split(";")[0].split()
		# information = raw_input()
		#
		# line_words = information.split()
		# split the information inputed into lines by '/n'
		reverse_dict[row + 1] = number_of_keyword
		for word in whole_line:  # Judge every word in every lines .
			# If the word appear first time .
			if word not in reverse_dict:
				item = set()  # set up a new set .
				item.add(row + 1)  # now rows
				reverse_dict[word] = item  # Add now rows into keys(item).
			
			# THe word have appeared before .
			else:
				reverse_dict[word].add(row + 1)  # Add now rows into keys(item).
		row += 1
	return reverse_dict


def get_index(input_sentence, segmentor, postagger, parser, reverse_dict):
	# print dictionary    we can get the information dictionary.
	# input_sentence="能好好说话吗？"
	sentence_list = segmentor_process(segmentor, sentence=input_sentence)
	list_index = []
	for key_word in sentence_list:
		if key_word in reverse_dict:
			list_index.append(reverse_dict[key_word])
	index = ()
	flag_first = 0
	for index_set in list_index:
		if flag_first == 0:
			index = index_set
			flag_first = 1
		else:
			index = index.intersection(index_set)
	last_index = 0
	for index_ in list(index):
		if reverse_dict[index_] == len(list_index):
			last_index = index_
	if last_index != 0:
		# return sentence_list, list(index)[random.randint(1,len_index)-1]
		return sentence_list, last_index
	else:
		return sentence_list, None


# create_reverse_index()


def frequency_template_model():
	segmentor, postagger, parser = ini_ltp()
	reverse_dict = create_reverse_index()
	flag_input = True
	while flag_input:
		input_sentence = input()
		if input_sentence == "":
			print("无输入,输入q退出")
			continue
		if input_sentence == "q":
			flag_input = False
			continue
		word_list, index = get_index(input_sentence, segmentor, postagger, parser, reverse_dict)
		if index != None:
			print(give_answer(word_list, postagger, index))
		else:
			print("next step!")
	release_ltp(segmentor, postagger, parser)


frequency_template_model()
