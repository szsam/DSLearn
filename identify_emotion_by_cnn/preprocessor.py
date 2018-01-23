from xml.dom.minidom import parse
import xml.dom.minidom
import jieba
import os

class PreProcessor:

    def __init__(self, texts, punctuation_table_file):
        self.contents = []
        self.polarity = []
        for text in texts:
            contents, polarity = PreProcessor.get_raw_data("datasets" + os.sep + text[0], text[1])
            self.contents += contents
            self.polarity += polarity
        self.punctuation_table = PreProcessor.get_punctuation_table(punctuation_table_file)

    def get_raw_data(file, replace_str):

        """
        操纵DOM树来解析XML文件
        :param file: str XML文件名
        :param replace_str: str 用于过滤话题名称，如:"#彭宇承认撞了南京老太#"
        :return:
        """

        dom_tree = xml.dom.minidom.parse(file)
        sentence_elements = dom_tree.getElementsByTagName("sentence")
        """:type : list[xml.dom.minidom.Element]"""

        sentences = []  #评论内容，用于返回
        polaritys = []  #情感倾向，用于返回

        for sentence_element in sentence_elements:
            sentence = sentence_element.childNodes[0].nodeValue
            """:type : str"""
            sentence = sentence.replace(replace_str, "")

            if sentence_element.hasAttribute('polarity'):
                polarity = sentence_element.getAttribute('polarity')
                if polarity != "NEG" and polarity != "POS": continue # 只接受NEG和POS标签
            else:
                continue

            sentences.append(sentence)
            polaritys.append(polarity)

        return sentences, polaritys

    def get_punctuation_table(file):
        """
        获取符号过滤表
        :param file: str 符号表文件名
        :return: list[str] 符号表
        """
        with open(file, 'r', encoding='utf-8') as f:
            punctuation_table = []
            read_in_string = f.read()
            for c in read_in_string:
                punctuation_table.append(c)

        return punctuation_table

    def perform_chinese_cut(self):

        """
        进行中文分词
        """

        result = [] #用于更新

        #使用jieba中文分词
        for sentence in self.contents:
            result.append(jieba.lcut(sentence))

        self.contents = result

    def perform_punctuation_filtering(self):

        """
        标点符号过滤
        """

        result = [] #用于更新

        zeros = [0 for _ in range(len(self.punctuation_table))]
        punctuation_dict = dict(zip(self.punctuation_table, zeros))

        def helper(x):
            if x not in self.punctuation_table:
                return True
            else:
                punctuation_dict[x] += 1
                return False

        for l in self.contents:
            assert isinstance(l, list)
            l = filter(helper, l)
            result.append(list(l))

        self.contents = result

    def perform_string_to_float(self):
        self.dict1 = self.perform_contents_string_to_float()
        self.dict2 = self.perform_polarity_string_to_float()

    def perform_contents_string_to_float(self):
        cnt = 0
        dictionary = {}
        result = []

        for sl in self.contents:
            nl = []
            for s in sl:
                if s not in dictionary:
                    dictionary[s] = cnt
                    nl.append(cnt)
                    cnt += 1
                else:
                    nl.append(dictionary[s])
            result.append(nl)

        self.contents = result

        return dictionary

    def perform_polarity_string_to_float(self):
        cnt = 0
        dictionary = {}
        result = []
        for s in self.polarity:
            if s not in dictionary:
                dictionary[s] = cnt
                result.append(cnt)
                cnt += 1
            else:
                result.append(dictionary[s])
        self.polarity = result

        return dictionary

    def predict_data(self, string):
        sl = jieba.lcut(string)
        sl = filter(lambda x: x not in self.punctuation_table, sl)
        nl = []
        for s in sl:
            if s in self.dict1:
                nl.append(self.dict1[s])
            else:
                print(Warning("string %s is not in dictionary, default value is 0" % s))
                nl.append(0)
        return nl

    def get_result(self):
        return list(zip(self.contents, self.polarity))

    def show(self):
        """
        显示结果
        :return:
        """
        for i in self.get_result():
            print(i)


def helper(dataset):

    """
    将list[tuple()]->tuple(list[])
    :param dataset:
    :return:
    """

    dataset_x = []
    dataset_y = []

    for d in dataset:
        x, y = d
        dataset_x.append(x)
        dataset_y.append(y)
        del x, y

    return dataset_x, dataset_y


def portion(dataset, valid_portion):

    """
    按照valid_portion的比例将训练集和验证集分离
    :param dataset:
    :param valid_portion:
    :return:
    """

    n = len(dataset)
    pivot = int(n * (1 - valid_portion))
    train = helper(dataset[0:pivot])
    valid = helper(dataset[pivot+1:-1])

    return train, valid


texts = [
    ["fei_jun_jian_e_yi_zhuang_ji_notations.xml", "#菲军舰恶意撞击#"],
    ["feng_kuang_de_da_cong.xml", "#疯狂的大葱#"],
    ["guan_yuan_cai_chan_gong_shi.xml","#官员财产公示#"],
    ["guan_yuan_diao_yan_notations.xml","#官员调研#"],
    ["guo_qi_xia_tao_fa_jiao_yu_zhi_du.xml","#国旗下讨伐教育制度#"],
    ["han_han_fang_zhou_zi_zhi_zheng_notations.xml","#韩寒方舟子之争#"],
    ["jia_he_shang_lou_nv_zi_notations.xml","#假和尚搂女子#"],
    ["jiang_zhuang_zhi_ru_guang_gao.xml","#奖状植入广告#"],
    ["jiu_lin_hou_bao_da_lao_ren.xml","#90后暴打老人#"],
    ["jiu_ling_hou_dang_jiao_shou_notations.xml","#90后当教授#"],
    ["liu_liu_jiao_ban_xiao_san_notations.xml","#六六叫板小三#"],
    ["ming_gu_wu_shi_zhang_fou_ren_nan_jing_da_tu_sha.xml","#名古屋市长否认南京大屠杀#"],
    ["peng_yu_cheng_ren_zhuang_le_nan_jing_lao_tai.xml","#彭宇承认撞了南京老太#"],
    ["pi_xie_guo_dong_notation.xml","#皮鞋果冻#"],
    ["pin_guo_feng_sha_360.xml","#苹果封杀360#"],
    ["san_ya_chun_jie_zai_ke_notations.xml","#三亚春节宰客#"],
    ["shi_yong_you_zhang_jia.xml","#食用油涨价#"],
    ["xi_wan_gong_ren_liu_sheng_cai_bei_kai_chu_notations.xml","#洗碗工留剩菜被开除#"],
    ["xue_lei_feng_bei_diao_yu_zhi_fa.xml","#学雷锋被钓鱼执法#"],
    ["zhong_guo_jiao_shi_shou_ru_quan_qiu_ji_dian_di_notations.xml","#中国教师收入全球几垫底#"]
]

# 获取指定xml文件中的内容,创建符号过滤表
app = PreProcessor(texts, "punctuation_table.txt")


def load_data(valid_portion=0.1):

    # 进行中文分词
    app.perform_chinese_cut()

    # 进行符号过滤
    app.perform_punctuation_filtering()

    # 进行字符串到数值的转换
    app.perform_string_to_float()

    # 进行训练集和验证集的分割
    train, valid = portion(app.get_result(), valid_portion)

    return train, valid

def predict_data(string):
    return app.predict_data(string)
