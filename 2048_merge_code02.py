"""
    2048游戏平面单向单列基础算法
"""
def zero_to_end(list01):
    result_list=[]
    for i in range(4):
        if list01[i]!=0:
            result_list.append(list01[i])
    result_list=result_list+[0]*list01.count(0)
    list01[:]=result_list[:]

# def zero_to_end(list01):
#     for item in list01:
#         if item==0:
#             list01.remove(item)
#             list01.append(0)

def merge(list01):
    zero_to_end(list01)
    for i in range(len(list01)-1):
        if list01[i]!=0 and list01[i]==list01[i+1]:
            list01[i],list01[i+1]=list01[i]*2,0
    zero_to_end(list01)
    return list01

def print_map(list_result):
    for i in range(len(list_result)):
        for j in range(len(list_result[i])):
            print(list_result[i][j], end="  ")
        print()

def move_up(result_list):
    for i in range(len(result_list)):
        list_merge= [result_list[j][i] for j in range(len(result_list[i]))]
        merge(list_merge)
        for j in range(len(list_merge)):
            result_list[j][i]=list_merge[j]

def move_left(result_list):
    for i in range(len(result_list)):
        list_merge=[]
        for j in range(len(result_list[i])):
            list_merge.append(result_list[i][j])
        merge(list_merge)
        for j in range(len(list_merge)):
            result_list[i][j]=list_merge[j]

def move_right(result_list):
    for i in range(len(result_list)):
        list_merge = []
        for j in range(len(result_list)-1,-1,-1):
            list_merge.append(result_list[i][j])
        merge(list_merge)
        for j in range(len(list_merge)):
            result_list[i][len(result_list)-1-j]=list_merge[j]

def move_down(result_list):
    for i in range(len(result_list)):
        list_merge=[]
        for j in range(len(result_list)-1,-1,-1):
            list_merge.append(result_list[j][i])
        merge(list_merge)
        for j in range(len(result_list[i])):
            result_list[len(result_list)-1-j][i] = list_merge[j]
    return result_list


