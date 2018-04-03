import copy

def checkDependency(schema,FDs,Decomp):
    temp_fd_ls = copy.deepcopy(FDs[schema])

    fd_ls = getFDs(temp_fd_ls)

    for item in Decomp:
        for fd in fd_ls:
            if set(fd).issubset(set(item[1])):
               fd_ls.remove(fd)

    if len(fd_ls) == 0:
        print('Dependecy Preserving.')
    else:
        print('Not Dependecy Preserving.')
    return

def getFDs(temp_fds):
    newfd = []
    i = -1
    lhs = []
    rhs = []
    while len(temp_fds[0]) > 0:
        if temp_fds[0][0] not in lhs:
            lhs.append(temp_fds[0][0])
            temp_fds[0].remove(temp_fds[0][0])
            rhs.append([temp_fds[1][0]])
            temp_fds[1].remove(temp_fds[1][0])
            i += 1
        else:
            temp_fds[0].remove(temp_fds[0][0])
            rhs[i].append(temp_fds[1][0])
            temp_fds[1].remove(temp_fds[1][0])
    for left in lhs:
        newfd.append(left)
        i = lhs.index(left)
        for right in rhs[i]:
            if right not in newfd[i]:
                newfd[i].append(right)
    return newfd