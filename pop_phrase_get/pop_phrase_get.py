import re

#   extract useful information from raw_file1
def pop_phrase_get1():
    p1 = "<tr id=\".+?\">"
    pattern1 = re.compile(p1)
    f = open('raw_file1', 'r', encoding='UTF-8')
    lines = f.readlines()
    pop_phrases = []
    for i in lines:
        all = pattern1.findall(i)
        for j in all:
            pop_phrases.append((j.encode('utf-8').decode('utf-8-sig'))[8:-2] + '\n')
    f2 = open('common_pop_phrase', 'a+', encoding='UTF-8')
    f2.writelines(pop_phrases)
    f.close()
    f2.close()

#   extract useful information from raw_file2
def pop_phrase_get2():
    p1 = "[0-9]{1,3} {1,3}.+? "
    pattern1 = re.compile(p1)
    f = open('raw_file2', 'r', encoding='UTF-8')
    lines = f.readlines()
    pop_phrases = []
    for i in lines:
        all = pattern1.findall(i)
        for j in all:
            pop_phrases.append((j.encode('utf-8').decode('utf-8-sig'))[4:-1] + '\n')
    f2 = open('common_pop_phrase', 'a+', encoding='UTF-8')
    f2.writelines(pop_phrases)
    f.close()
    f2.close()

#   extract useful information from raw_file3
def pop_phrase_get3():
    f = open('raw_file3', 'r', encoding='UTF-8')
    lines = f.readlines()
    f.close()
    f2 = open('common_pop_phrase', 'a+', encoding='UTF-8')
    f2.writelines(lines)
    f2.close()

#  To remove the duplicate popular phrases.
def remove_duplicate():
    f = open('common_pop_phrase', 'r', encoding='UTF-8')
    lines = list(set(f.readlines()))
    f.close()
    f2 = open('common_pop_phrase', 'w', encoding='UTF-8')
    f2.writelines(lines)
    f2.close()

if __name__ == '__main__':
    pop_phrase_get1()
#    pop_phrase_get2()
    pop_phrase_get3()
    remove_duplicate()