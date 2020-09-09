import random


foo=open("input_42.txt",'w')
foo.write("BFS\n")
m=100
n=100
num_channel = 100000
min_year = 0
max_year = 8888
year_list=[]
for i in range(8000):
    year_list.append(random.randint(min_year,max_year))

foo.write("%d %d\n" % (m,n))
initial=[year_list[random.randint(0,len(year_list)-1)],random.randint(0,m-1),random.randint(0,n-1)]
target=[year_list[random.randint(0,len(year_list)-1)],random.randint(0,m-1),random.randint(0,n-1)]

foo.write("%d %d %d\n" % (initial[0],initial[1],initial[2]))
foo.write("%d %d %d\n" % (target[0],target[1],target[2]))

foo.write("%d\n" % (num_channel))

for i in range(num_channel):
    foo.write("%d %d %d %d\n" % (year_list[random.randint(0,len(year_list)-1)],random.randint(0,m-1),random.randint(0,n-1),year_list[random.randint(0,len(year_list)-1)]))

# for i in range(m):
#     for j in range(n):
#         foo.write("%d %d %d %d\n" % (initial[0],i,j,year_list[random.randint(0,len(year_list)-1)]))




