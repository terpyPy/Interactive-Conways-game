class objGroup_flags:
    def __init__(self, *flags)->None:
        '''get any flags passed in to constructor and collect them, 
        then set them to modify the constructor of the classes 
        that inherit from this class'''
        # super(objGroup_flags, self).__init__()
        self.flags = [i for i in flags]
        # get any flags passed in to constructor and collect them along with order the flags were passed in
        if len(self.flags) != 0:
            # flagsIn holds a dict of tuple pairs (priority, flag).
            # priority is the order the flags were passed in
            # self.flagsIn = {i: arg for i, arg in enumerate(self.flags)}
            self.printFlags()
        
    def printFlags(self):
        # print the flags in the order they were passed in
       
        for priority in range(self.flags.__len__()):
            # give a debug message for each flag received
            print(f'modifier__priority_- {priority} -__ : {self.flags[priority]}')
        
if __name__ == '__main__':
    x = tuple('test_Mode_'+str(i+i) for i in range(3))
    a,b,c = x
    test = objGroup_flags(a,b,c,c+a)
    test.printFlags()