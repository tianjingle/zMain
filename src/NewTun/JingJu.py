class JingJu:
    #名人名言的字典
    files=["C:\\Users\\Administrator\\PycharmProjects\\zMain\\src\\NewTun\\20210627.txt","C:\\Users\\Administrator\\PycharmProjects\\zMain\\src\\NewTun\\20210628.txt"]
    list=[]
    #现在读取到的名言警句的游标
    indexFile="C:\\Users\\Administrator\\PycharmProjects\\zMain\\src\\NewTun\\index"
    index=0
    #警句整理，去除序号和开都的标点符号
    def executeFile(self):
        for file in self.files:
            fo = open(file,"r",encoding='gbk')
            list=[]
            for line in fo.readlines():
                line=line.replace("\n","").strip()
                if line!='':
                    if line.__contains__("."):
                        list.append(line.split('.')[1]+"\n")
                    else:
                        list.append(line+"\n")
            for item in list:
                print(item)
            fo.close()
            f = open(file, "w",encoding='gbk')
            f.writelines(list)
            f.close()

    #从文件中获取一个警句
    def readOneJinju(self):
        for file in self.files:
            fr=open(file,"r",encoding="gbk")
            for line in fr.readlines():
                self.list.append(line)
        #默认的警句
        if len(self.list)==0:
            return '不劳而获是这世界上最大的坏！'

        fi=open(self.indexFile,"r",encoding="utf-8")
        index=fi.readlines()
        if len(index)!=0 and index[0].strip()!='':
            index=int(index[0])
            self.index=int(index)+1
            if self.index>len(self.list):
                self.index=0
        else:
            self.index=0
        fi = open(self.indexFile, "w", encoding="utf-8")
        print(self.list[self.index])
        fi.write(str(self.index))
        fi.close()
        return self.list[self.index]