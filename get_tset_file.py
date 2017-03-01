from random import randint
from numpy import random as rand 
from random import randint
f = open('test_file1.txt', 'w')
for i in range(0,1000):
    girlType = randint(1,3)
    if girlType==1:
        face = float(randint(1,40)+rand.rand())
        figure = float(randint(1,70)+rand.rand())
        height = float(randint(150,190)+rand.rand())
    elif girlType==2:
        face = float(randint(20,80)+rand.rand())
        figure = float(randint(20,100)+rand.rand())
        height = float(randint(150,170)+rand.rand())
    elif girlType==3:
        face = float(randint(60,100)+rand.rand())
        figure = float(randint(30,100)+rand.rand())
        height = float(randint(150,170)+rand.rand())
    f.write("%f\t%f\t%f\t%d\n"%(face,figure,height,girlType))
f.close()