import connectDB

global attrType,foreignKey
foreignKey = {}
attrType = {}
def createTables(schema,Decomp):
    connectDB.c.execute('PRAGMA table_info({});'.format(schema))
    types = connectDB.c.fetchall()
    for item in types:
        attrType[item[1]] = item[2]

    for item in Decomp:
        addTable(schema,item)
    return


def addTable(schema,attr):
    print(attr)
    foreignKey[attr[0]] = []
    sqlCommand = 'CREATE TABLE '
    schName = attr[0] + ' ( '
    sqlCommand = sqlCommand + schName
    for item in attr[1]:
       sqlCommand = sqlCommand + item + ' ' + attrType[item] + ', '
    for item in attr[2][0]:
        sqlCommand += 'PRIMARY KEY('
        if len(item) > 1:
            for i in item:
                foreignKey[attr[0]].append(i)
                if (item.index(i)) == (len(item) - 1):
                    sqlCommand += i +')'
                else:
                    sqlCommand += i +', '
        else:
            foreignKey[attr[0]].append(item[0])
            sqlCommand += item[0]
            sqlCommand += ')'
    Fkey = []
    Fref = []
    for item in attr[2][0]:
        for i in item:
            for key in foreignKey:
                if attr[0] != key and i in foreignKey[key]:
                    if i not in Fkey:
                        Fkey.append(i)
                        Fref.append(key)
    if len(Fkey) < 1:
        sqlCommand += ')'
    else:
        while len(Fkey) > 0:
            sqlCommand += ', FOREIGN KEY (' + Fkey[0] +') REFERENCES ' + Fref[0]
            Fkey.remove(Fkey[0])
            Fref.remove(Fref[0])
            if len(Fkey) < 1:
                sqlCommand += ')'
    
    connectDB.c.execute('{}'.format(sqlCommand))

    return