class word_filter():
    def __init__(self):
        self.dic = set()
        self.read_dic()

    def extract_verb(self, l):
        verb_list = []
        for i in l:
            if i[1].startswith("V"):
                verb_list.append(i[0])
        return verb_list

    def add_to_dic(self, l):
        for item in l:
            self.dic.add(item)
        return

    def save_dic(self):
        file = open("uresearcher_app/static/other/word_filter", "w")
        for item in list(self.dic):
            file.write(item + "\n")

    def read_dic(self):

        file = open("uresearcher_app/static/other/word_filter", "r")
        for x in file:
            self.dic.add(x.strip())
        file.close()
        return self.dic

    def isValid(self, input):
        if input in self.dic:
            return False
        # if last 3 word is ing
        if input[-3:] == "ing":
            return False

        return True
