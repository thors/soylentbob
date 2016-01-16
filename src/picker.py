import os,re,random,time


def readFile(filename):
    f = open(filename,"r")
    lines = f.readlines()
    f.close()
    i = 0
    while i < len(lines):
        if lines[i].find("#") == 0:
            del lines[i]
        else:
            i = i + 1
    return lines
    
def substitue(msg, message):
    reSubst = re.compile("^([^,][^,]*),(\d\d*),(.*)")
    lines = readFile("data/substitutions.dat")
    for l in lines:
        m = reSubst.match(l)
        if None != m:
            p = int(m.group(2))
            i = random.randint(0,1000)
            if i > p:
                continue
            options = m.group(3).split(";")
            if len(options) == 0:
                options[0]=""
            msg = msg.replace(m.group(1), options[random.randint(0,len(options))-1])
    return msg

def pick_random_delayed(filename, message):
    if os.path.exists(filename):
        print "Opening file " + filename
        delayRe = re.compile("(\d\d*),(\d\d*)  *(.*)")
        probabilityRe = re.compile("probability:(\d\d*)")
        lines = readFile(filename)
        if len(lines) < 1:
            return ("",0)
            
        m = probabilityRe.match(lines[0])
        probability = 50
        if None != m:
            probability = int(m.group(1))
            del lines[0]
                
        i = random.randint(0, 100)
        print "probability = " + str(probability) + ", i = " + str(i)
        if i > probability:
            print "probability = " + str(probability)
            return ("",0)
            
        choice = lines[random.randint(0,len(lines)-1)]
        choice = substitue(choice, message)
        choice = choice.replace("%U",message.nick)
            
        m = delayRe.match(choice)
        ti = 0
        if None != m:
            print "Match: " + choice
            ti = random.randint(int(m.group(1)),int(m.group(2)))
            te =  m.group(3)
        else:
            print "No Match: " +  choice
            ti = random.randint(3,6)
            te =  choice
        return (te,ti)
    else:
        print "Missing file " + filename
    return ("",0)

