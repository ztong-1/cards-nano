class Solution:
    def judgePoint24(self, cards:[int]) -> bool:
        def process_ops(ops):
            res = "(" + ops[-1][1] + ")"
            for i in range(len(ops)-2, -1, -1):
                if "+" in ops[i][1] or "-" in ops[i][1]:
                    curr_exp = "(" + ops[i][1] + ")"
                else:
                    curr_exp = ops[i][1]
                    
                if ops[i][0] == "+":
                    res = res + "-" + curr_exp
                elif ops[i][0] == ".-":
                    res = curr_exp + "-" + res
                elif ops[i][0] == "-.":
                    res = curr_exp + "+" + res
                elif ops[i][0] == "*":
                    res = res + "/" + curr_exp
                elif ops[i][0] == "./":
                    res = curr_exp + "/" + res
                else:
                    res = curr_exp + "*" + res
                if i != 0:
                    res = "(" + res + ")"
            return res + " = 24."

        # x is numerator, y is denominator
        def dfs(x, y, remain, ops):
            # print("x", x, "y", y, "remain:", remain, ops)
            if len(remain) == 2:
                x_y = x / y
                temp = remain[0] + remain[1]
                if temp == x_y:
                    # print("a")
                    #print(ops + [("", str(remain[0])+"+"+str(remain[1]))])
                    print(process_ops(ops + [("", str(remain[0])+"+"+str(remain[1]))]))
                    return True
                temp = remain[0] - remain[1]
                if temp == x_y:
                    # print("b")
                    #print(ops + [("", str(remain[0])+"-"+str(remain[1]))])
                    print(process_ops(ops + [("", str(remain[0])+"-"+str(remain[1]))]))
                    return True
                temp = remain[1] - remain[0]
                if temp == x_y:
                    # print("c")
                    #print(ops + [("", str(remain[1])+"-"+str(remain[0]))])
                    print(process_ops(ops + [("", str(remain[1])+"-"+str(remain[0]))]))
                    return True
                temp = remain[1] * remain[0]
                if temp == x_y:
                    # print("d")
                    #print(ops + [("", str(remain[0])+"*"+str(remain[1]))])
                    print(process_ops(ops + [("", str(remain[0])+"*"+str(remain[1]))]))
                    return True
                temp = remain[0]/remain[1]
                if temp == x_y:
                    # print("e")
                    #print(ops + [("", str(remain[0])+"/"+str(remain[1]))])
                    print(process_ops(ops + [("", str(remain[0])+"/"+str(remain[1]))]))
                    return True
                temp = remain[1]/remain[0]
                if temp == x_y:
                    # print("f")
                    #print(ops + [("", str(remain[1])+"/"+str(remain[0]))])
                    print(process_ops(ops + [("", str(remain[1])+"/"+str(remain[0]))]))
                    return True
                return False
                
            for i in range(len(remain)):
                r = remain[i]
                # x/y - r
                # print("1", r,x,y)
                new_x, new_y = x - r*y, y
                temp = dfs(new_x, new_y, remain[:i] + remain[(i+1):], ops+[("-.",str(r))])
                if temp:
                    return True
                # x/y + r
                # print("2", r,x,y)
                new_x, new_y = x + r*y, y
                temp = dfs(new_x, new_y, remain[:i] + remain[(i+1):], ops+[("+",str(r))])
                if temp:
                    return True
                # r - x/y
                # print("3", r,x,y)
                new_x, new_y = r*y - x, y
                temp = dfs(new_x, new_y, remain[:i] + remain[(i+1):], ops+[(".-",str(r))])
                if temp:
                    return True
                # (x/y) / r
                # print("4", r,x,y)
                new_x, new_y = x, y*r 
                temp = dfs(new_x, new_y, remain[:i] + remain[(i+1):], ops+[("/.",str(r))])
                if temp:
                    return True
                # r / (x/y)
                # print("5", r,x,y)
                new_x, new_y = r*y, x
                temp = dfs(new_x, new_y, remain[:i] + remain[(i+1):], ops+[("./",str(r))])
                if temp:
                    return True
                # r * (x/y)
                # print("6", r,x,y)
                new_x, new_y = r*x, y
                temp = dfs(new_x, new_y, remain[:i] + remain[(i+1):], ops+[("*",str(r))])
                if temp:
                    return True
            

            if len(remain) == 4:    
                for i in range(3):
                    for j in range(i+1,4):
                        c1, c2 = cards[i], cards[j]
                        comp = list(set(range(4)) - set([i,j])) # complement
                        c3, c4 = cards[comp[0]], cards[comp[1]]
                        temp_xy = []
                        temp_xy.append((c1+c2,1))
                        temp_xy.append((c1-c2,1))
                        temp_xy.append((c2-c1,1))
                        temp_xy.append((c1*c2,1))
                        temp_xy.append((c1,c2))
                        temp_xy.append((c2,c1))
                        temp_ops = []
                        temp_ops.append(str(c1)+"+"+str(c2))
                        temp_ops.append(str(c1)+"-"+str(c2))
                        temp_ops.append(str(c2)+"-"+str(c1))
                        temp_ops.append(str(c1)+"*"+str(c2))
                        temp_ops.append(str(c1)+"/"+str(c2))
                        temp_ops.append(str(c2)+"/"+str(c1))
                        for k in range(6):
                            new_x, new_y = temp_xy[k][0]+24*temp_xy[k][1], temp_xy[k][1]
                            temp = dfs(new_x, new_y, [c3, c4], ops+[("+", temp_ops[k])])
                            if temp:
                                return True
                            new_x, new_y = temp_xy[k][0]-24*temp_xy[k][1], temp_xy[k][1]
                            temp = dfs(new_x, new_y, [c3, c4], ops+[(".-", temp_ops[k])])
                            if temp:
                                return True
                            new_x, new_y = 24*temp_xy[k][1]-temp_xy[k][0], temp_xy[k][1]
                            temp = dfs(new_x, new_y, [c3, c4], ops+[("-.", temp_ops[k])])
                            if temp:
                                return True
                            
                            if temp_xy[k][0] != 0:
                                new_x, new_y = 24*temp_xy[k][0], temp_xy[k][1]
                                temp = dfs(new_x, new_y, [c3, c4], ops+[("*", temp_ops[k])])
                                if temp:
                                    return True
                            if temp_xy[k][0] != 0:
                                new_x, new_y = temp_xy[k][0], 24*temp_xy[k][1]
                                temp = dfs(new_x, new_y, [c3, c4], ops+[("./", temp_ops[k])])
                                if temp:
                                    return True
                            if temp_xy[k][0] != 0:
                                new_x, new_y = 24*temp_xy[k][1], temp_xy[k][0]
                                temp = dfs(new_x, new_y, [c3, c4], ops+[("/.", temp_ops[k])])
                                if temp:
                                    return True
                return False
        
        res = dfs(24, 1, cards, [])
        return res
            


#s = Solution()
#res = s.judgePoint24([5,1,1,5])
#if res == False:
#    print("No solution exists.")


