import os
import io
class LastTalk:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        historyfile = os.path.join(cur_dir, 'history.txt')
        self.historydict= self.build_historydict(historyfile)

    '''构造反义词词典'''
    def build_historydict(self, file):
        historydict = {}
        for line in io.open(file,encoding='utf-8'):
            line = line.strip().split(' ')
            wd = line[0]
            historys = line[1].strip().split(';')
            if wd not in historydict:
                historydict[wd] = historys
            else:
                historydict[wd] += historys

        return historydict

    '''根据目标词获取反义词'''
    def get_history(self, word):
        return self.historydict.get(word, 'None')



def demo(user,word):
    handler = LastTalk()
    historys = handler.get_history(word)[0]
    with open('history.txt','r',encoding='utf-8') as f:
        dic=[]
        s=f.read()
    print(s)
    d = eval(s)
    print (d['Age'])

if __name__=="__main__":
    demo("111","nmsl")