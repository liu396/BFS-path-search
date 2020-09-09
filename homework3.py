from _collections import deque
import heapq


def est_distance(a,b):
    year_distance=abs(a[0]-b[0])
    length=abs(a[1]-b[1])
    height=abs(a[2]-b[2])
    rest=abs(length-height)
    diag_step=min(length,height)
    return year_distance+diag_step*14+rest*10


def est_distance_2(initial,target,year_visited):
    if initial[0] not in year_visited:
        return -1
    year_distance=year_visited[initial[0]]
    length=abs(initial[1]-target[1])
    height=abs(initial[2]-target[2])
    rest=abs(length-height)
    diag_step=min(length,height)
    return year_distance+diag_step*14+rest*10


def bfs():
    # print("Run BFS")
    foo = open("input.txt","r")
    foo.readline()
    m, n = [int(w) for w in foo.readline().strip().split(' ')]
    initial = []
    target = []
    initial[0:2] = [int(n) for n in foo.readline().strip().split(' ')]
    target[0:2] = [int(n) for n in foo.readline().strip().split(' ')]
    initial=tuple(initial)
    target=tuple(target)
    # print("target: ",target)

    total_line = int (foo.readline())
    channels = {}
    for i in range(total_line):
        a,b,c,d=[int(n) for n in foo.readline().strip().split(' ')]
        if(d == a):
            continue;
        if (a,b,c) in channels:
            channels[(a,b,c)].add(d)
        else:
            channels[(a,b,c)]={d}
        if (d,b,c) in channels:
            channels[(d,b,c)].add(a)
        else:
            channels[(d, b, c)] = {a}

    cost = 0
    q = deque()
    parent = {}
    q.append(initial)
    parent[initial]=(-1,-1,-1)
    stop = 0
    visited=set()
    while q:
        rounds = len(q)
        # print("current q size: ",rounds)
        for i in range(rounds):
            tmp = q.popleft()
            # print("tmp: ",tmp)
            if tmp in visited:
                continue
            if tmp == target:
                stop = 1
                break
            visited.add(tmp)
            for i in range(-1, 2):
                if tmp[1] + i < 0 or tmp[1] + i > m - 1:
                    continue
                for j in range(-1, 2):
                    if tmp[2] + j < 0 or tmp[2] + j > n - 1:
                        continue
                    new_tmp = (tmp[0], tmp[1] + i, tmp[2] + j)
                    if new_tmp in visited or new_tmp in parent:
                        continue
                    q.append(new_tmp)
                    parent[new_tmp]=tmp
                    # print("son, parent: ",new_tmp,tmp)

            if tmp in channels:
                for j in channels[tmp]:
                    new_tmp=(j,tmp[1],tmp[2])
                    if new_tmp in visited or new_tmp in parent:
                        continue
                    q.append(new_tmp)
                    parent[new_tmp]=tmp

        if stop == 1:
            break
        cost = cost + 1


    foo.close()
    foo = open("output.txt", "w")
    # print("stop: ", stop)
    if stop == 0:
        foo.write("FAIL\n")
    else:
        foo.write("%d\n" % cost)
        foo.write("%d\n" % (cost + 1))
        buffer = []
        node = target
        while not node == (-1, -1, -1):
            # print("get in\n")
            buffer.append(node)
            node = parent[node]
        # print(buffer)
        # print("cost: ", cost)
        for i in range(len(buffer) - 1, -1, -1):
            # print("i:",i)
            foo.write("%d %d %d %d\n" % (buffer[i][0], buffer[i][1], buffer[i][2], int(i != len(buffer) - 1)))
    return


def ucs():
    # print("Run UCS")
    foo = open("input.txt", "r")
    foo.readline()
    m, n = [int(w) for w in foo.readline().strip().split(' ')]
    initial = []
    target = []
    initial[0:2] = [int(n) for n in foo.readline().strip().split(' ')]
    target[0:2] = [int(n) for n in foo.readline().strip().split(' ')]
    initial = tuple(initial)
    target = tuple(target)
    # print("target: ",target)

    total_line = int(foo.readline())
    channels = {}
    for i in range(total_line):
        a, b, c, d = [int(n) for n in foo.readline().strip().split(' ')]
        if (d == a):
            continue;
        if (a, b, c) in channels:
            channels[(a, b, c)].add(d)
        else:
            channels[(a, b, c)] = {d}
        if (d, b, c) in channels:
            channels[(d, b, c)].add(a)
        else:
            channels[(d, b, c)] = {a}

    visited=set() # save cost
    parent={(-1,-1,-1):[(-1,-1,-1),0]} # save parents
    q=[]
    heapq.heappush(q,(0,initial,(-1,-1,-1)))
    stop=0
    nb = [-1,0,1]
    count=0
    while q:
        cost,tmp,tmp_parent = heapq.heappop(q)
        # print("tmp: ",tmp)
        if tmp in visited:
            continue
        if tmp == target:
            visited.add(tmp)
            parent[tmp]=[tmp_parent,cost]
            stop = 1
            break
        visited.add(tmp)
        parent[tmp] = [tmp_parent,cost]
        for i in nb:
            if tmp[1] + i < 0 or tmp[1] + i > m - 1:
                continue
            for j in nb:
                if i==j==0 or tmp[2] + j < 0 or tmp[2] + j > n - 1:
                    continue
                new_tmp = (tmp[0], tmp[1] + i, tmp[2] + j)
                if new_tmp not in visited:
                    if i!=0 and j!=0:
                        attempt = 14
                    else:
                        attempt = 10
                    heapq.heappush(q,(cost+attempt,new_tmp,tmp))

        if tmp in channels:
            for j in channels[tmp]:
                new_tmp = (j, tmp[1], tmp[2])
                if new_tmp not in visited:
                    attempt = abs(j - tmp[0])
                    heapq.heappush(q, (cost + attempt, new_tmp, tmp))

    foo=open("output.txt","w")
    # print("stop: ",stop)
    if stop == 0:
        foo.write("FAIL\n")
    else:
        buffer = []
        node = list(target)
        node.append(parent[target][1])
        while node[0:3]!= [-1,-1,-1]:
            buffer.append(node)
            node = list(parent[tuple(node[0:3])][0])
            # print("node: ",node)
            node.append(parent[tuple(node)][1])
            # print(node)
        # print("buffer: ",buffer)

        foo.write("%d\n" % (buffer[0][3]))
        foo.write("%d\n" % (len(buffer)))
        foo.write("%d %d %d %d\n" % (buffer[-1][0], buffer[-1][1], buffer[-1][2],buffer[-1][3]))
        for i in range(len(buffer)-2,-1,-1):
            # print("i:",i)
            foo.write("%d %d %d %d\n" % (buffer[i][0],buffer[i][1],buffer[i][2],buffer[i][3]-buffer[i+1][3]))

    return



def astar():
    # print("Run A*")
    foo = open("input.txt", "r")
    foo.readline()
    m, n = [int(w) for w in foo.readline().strip().split(' ')]
    initial = []
    target = []
    initial[0:2] = [int(n) for n in foo.readline().strip().split(' ')]
    target[0:2] = [int(n) for n in foo.readline().strip().split(' ')]
    initial = tuple(initial)
    target = tuple(target)
    # print("target: ",target)

    foo.readline()
    line = foo.readline()
    channels = {}
    if line:
        a, b, c, d = [int(n) for n in line.strip().split(' ')]
        if (d != a):
            channels[(a, b, c)] = [d]
            channels[(d, b, c)] = [a]
    # print(channels)

    line = foo.readline()
    while line:
        # print("line: ",line)
        a, b, c, d = [int(n) for n in line.strip().split(' ')]
        # print(a, b, c, d)
        if (a, b, c) in channels:
            if d not in channels[(a, b, c)]:
                channels[(a, b, c)].append(d)
        else:
            channels[(a, b, c)] = [d]
        if (d, b, c) in channels:
            if a not in channels[(d, b, c)]:
                channels[(d, b, c)].append(a)
        else:
            channels[(d, b, c)] = [a]
        line = foo.readline()

    # print(channels)

    visited={} # save cost
    visited[(-1,-1,-1)]=0
    parent={} # save parents
    estimate={} # save estimate cost
    q=[]
    heapq.heappush(q,(est_distance(initial,target),0,initial,(-1,-1,-1)))
    stop=0
    count=0
    while q:
        # count=count+1
        dummy,cost,tmp,tmp_parent=heapq.heappop(q)
        # if (count%10000==0):
        if tmp == target:
            visited[tmp] = cost
            parent[tmp] = tmp_parent
            stop=1
            break
        if tmp in visited:
            continue
        visited[tmp] = cost
        parent[tmp] = tmp_parent
        for i in range(-1, 2):
            if tmp[1] + i < 0 or tmp[1] + i > m - 1:
                continue
            for j in range(-1, 2):
                if tmp[2] + j < 0 or tmp[2] + j > n - 1:
                    continue
                new_tmp = (tmp[0], tmp[1] + i, tmp[2] + j)
                if new_tmp in visited:
                    continue
                if abs(i)+abs(j) == 2:
                    attempt = 14
                else:
                    attempt = 10
                if new_tmp not in estimate:
                    estimate[new_tmp]=est_distance(new_tmp,target)
                heapq.heappush(q,(cost+attempt+estimate[new_tmp],cost+attempt,new_tmp,tmp))

        if tmp in channels:
            for j in channels[tmp]:
                new_tmp = (j, tmp[1], tmp[2])
                attempt = abs(j-tmp[0])
                if new_tmp in visited:
                    continue
                if new_tmp not in estimate:
                    estimate[new_tmp] = est_distance(new_tmp, target)
                heapq.heappush(q,(cost+attempt+estimate[new_tmp],cost+attempt,new_tmp,tmp))

    foo = open("output.txt", "w")
    # print("stop: ", stop)
    if stop == 0:
        foo.write("FAIL\n")
    else:
        buffer = []
        node = list(target)
        node.append(visited[target])
        while node[0:3] != [-1, -1, -1]:
            buffer.append(node)
            node = list(parent[tuple(node[0:3])])
            # print("node: ", node)
            node.append(visited[tuple(node)])
            # print(node)
        # print("buffer: ", buffer)

        foo.write("%d\n" % (buffer[0][3]))
        foo.write("%d\n" % (len(buffer)))
        foo.write("%d %d %d %d\n" % (buffer[-1][0], buffer[-1][1], buffer[-1][2], buffer[-1][3]))
        for i in range(len(buffer) - 2, -1, -1):
            # print("i:", i)
            foo.write("%d %d %d %d\n" % (buffer[i][0], buffer[i][1], buffer[i][2], buffer[i][3] - buffer[i + 1][3]))

    return


def astar_2():
    # print("Run A*")
    foo = open("input.txt", "r")
    foo.readline()
    m, n = [int(w) for w in foo.readline().strip().split(' ')]
    initial = []
    target = []
    initial[0:2] = [int(n) for n in foo.readline().strip().split(' ')]
    target[0:2] = [int(n) for n in foo.readline().strip().split(' ')]
    initial = tuple(initial)
    target = tuple(target)
    # print("target: ",target)
    year_to_year={} # year to year list for calculating the year distance

    total_line=int(foo.readline())
    channels = {}
    for i in range(total_line):
        a, b, c, d = [int(n) for n in foo.readline().strip().split(' ')]
        if a == d:
            continue;
        if (a,b,c) in channels:
            channels[(a,b,c)].add(d)
        else:
            channels[(a,b,c)]={d}
        if (d, b, c) in channels:
            channels[(d, b, c)].add(a)
        else:
            channels[(d, b, c)] = {a}

        if a in year_to_year:
            year_to_year[a].add(d)
        else:
            year_to_year[a]={d}

        if d in year_to_year:
            year_to_year[d].add(a)
        else:
            year_to_year[d] = {a}

    # print("channels: ",channels)
    # print("year to year:",year_to_year)

    year_visited = {} #save year to target distance
    #run Dijkstra to get year to target year distance
    year_q=[]
    heapq.heappush(year_q,(0,target[0]))
    while year_q:
        tmp_cost,tmp_year=heapq.heappop(year_q)
        if tmp_year in year_visited:
            continue
        year_visited[tmp_year] = tmp_cost
        if tmp_year not in year_to_year:
            continue
        for son_year in year_to_year[tmp_year]:
            heapq.heappush(year_q,(tmp_cost+abs(tmp_year-son_year),son_year))

    # print("year_to_target: ",year_visited)
    del year_to_year

    visited = set() # save cost
    parent={(-1,-1,-1):[(-1,-1,-1),0]} # save parents and cost
    estimate = {} # save estimate cost
    q=[]
    h_distance=est_distance_2(initial,target,year_visited)
    # print("h_distance: ",h_distance)
    if h_distance != -1:
        heapq.heappush(q,(h_distance,0,initial,(-1,-1,-1)))
    stop=0
    nb=[-1,0,1]
    while q:
        # count=count+1
        dummy,cost,tmp,tmp_parent=heapq.heappop(q)
        # if (count%10000==0):
        #     print("est_cost: ",cost)
        # print("tmp: ",tmp)
        if tmp in visited:
            continue
        if tmp == target:
            visited.add(tmp)
            parent[tmp] = (tmp_parent,cost)
            stop=1
            break
        visited.add(tmp)
        parent[tmp] = (tmp_parent,cost)
        for i in nb:
            if tmp[1] + i < 0 or tmp[1] + i > m - 1:
                continue
            for j in nb:
                if i == j == 0 or tmp[2] + j < 0 or tmp[2] + j > n - 1:
                    continue
                new_tmp = (tmp[0], tmp[1] + i, tmp[2] + j)
                if new_tmp in visited:
                    continue
                if i!=0 and j!=0:
                    attempt = 14
                else:
                    attempt = 10
                if new_tmp not in estimate:
                    estimate[new_tmp]=est_distance_2(new_tmp,target,year_visited)
                if estimate[new_tmp] != -1:
                    heapq.heappush(q,(cost+attempt+estimate[new_tmp],cost+attempt,new_tmp,tmp))

        if tmp in channels:
            for j in channels[tmp]:
                new_tmp = (j, tmp[1], tmp[2])
                if new_tmp in visited:
                    continue
                attempt = abs(j-tmp[0])
                if new_tmp not in estimate:
                    estimate[new_tmp]=est_distance_2(new_tmp,target,year_visited)
                if estimate[new_tmp] != -1:
                    heapq.heappush(q, (cost + attempt + estimate[new_tmp], cost + attempt, new_tmp, tmp))

    foo=open("output.txt","w")
    # print("stop: ",stop)
    if stop == 0:
        foo.write("FAIL\n")
    else:
        buffer = []
        node = list(target)
        node.append(parent[target][1])
        while node[0:3]!= [-1,-1,-1]:
            buffer.append(node)
            node = list(parent[tuple(node[0:3])][0])
            # print("node: ",node)
            node.append(parent[tuple(node)][1])
            # print(node)
        print("buffer: ",buffer)

        foo.write("%d\n" % (buffer[0][3]))
        foo.write("%d\n" % (len(buffer)))
        foo.write("%d %d %d %d\n" % (buffer[-1][0], buffer[-1][1], buffer[-1][2],buffer[-1][3]))
        for i in range(len(buffer)-2,-1,-1):
            # print("i:",i)
            foo.write("%d %d %d %d\n" % (buffer[i][0],buffer[i][1],buffer[i][2],buffer[i][3]-buffer[i+1][3]))

    return


fo = open("input.txt","r")
method = fo.readline().strip()
fo.close()
del fo
if method == "BFS":
    bfs()
    # print("End")
elif method == 'UCS':
    ucs()
    # print("End")
elif method =="A*":
    astar_2()
    # print("End")
else:
    print("No valid method")
