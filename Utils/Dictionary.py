
class WordDictionary:
    def __init__(self, max_one_hot = None):
        self.one_hot_cnt = 1
        self.max_one_hot = max_one_hot
        self.one_hot_dict: dict[str, int] = {}

    def addWord(self, word):
        self.one_hot_dict[word] = self.one_hot_cnt
        self.one_hot_cnt += 1

    def lookup(self, word):
        if word not in self.one_hot_dict:
            self.addWord(word)
        return self.one_hot_dict[word]

    def isFull(self):
        if self.max_one_hot is None:
            return False
        return self.one_hot_cnt >= self.max_one_hot

    def count(self):
        return self.one_hot_cnt


class PersonDictionary:
    def __init__(self):
        self.dict: dict[int, str] = {}

    def addPerson(self, idx, file):
        self.dict[idx] = file

    def lookup(self, idx):
        return self.dict[idx]