import re
def read_file_to_lst():
        # this function parses the whitlist to config out init variables
        hashes = open('list.txt')
        fileLines = hashes.readlines()
        hashes.close()
        # regular expersions to search for admin= and auth_users=
        hashRE = re.compile(r'(^\w[a-z-0-9]*)')
        prosNameRE = re.compile(r':(.*)')
        hash = []
        prosName = []
        for line in fileLines:
            if hashRE.search(line):
                hash.append(hashRE.search(line)[0])
            if prosNameRE.search(line):
                prosName.append(prosNameRE.search(line)[0][1:])
        # return the admin as and the users string ling as a list
        return hash, prosName
h,n = read_file_to_lst()
fileDict = {h[i]: n[i] for i in range(len(h)-1)}
userInput = input('process hash: ')
if userInput in fileDict.keys():
    print(fileDict[userInput])