import sys
import numpy 

rows = []
line = sys.stdin.readline().split()
i = len(line)

while(i>0):
  

    rows.append(numpy.array(line))
    line = sys.stdin.readline().split()  
    i-=1

array_2D = numpy.stack(rows)

print(array_2D)
