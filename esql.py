#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""
Author => Aryan Sidhwani
Project Started => 6/6/2020
First Stable => 12/6/2020
Last Updated => 5/4/2021 (update9)

Update highlights:
 --> deletes the intermediate files (temporary)
 --> merged all functions into one file 'esql.py'
 --> minor ui improvements
 --> completed commentary
"""
from __future__ import print_function
win = False
cur_table = ''
ValidFieldTypes = ["int", "decimal", "str", "date", "bool"]
thm = "pretty"
from os import system,chdir,path,listdir,mkdir,getcwd
import pickle
import ast
import copy




#parent_dir = "/home/makemake/Documents"   # --- Change this folder to whichever (rw) folder you want to make a fresh folder inside it if not already created
parent_dir = getcwd()
directory = "esql_folder"



chdir(parent_dir)
ldr = listdir()

if directory not in ldr:
    mkdir(directory)

pathres = path.join(parent_dir, directory)






from sys import platform,version_info
if "win" in str(platform) or "Win" in str(platform):
    win = True
if version_info < (3,0):
    input = raw_input


welcstr = """
__        __   _                            _____     
\ \      / /__| | ___ ___  _ __ ___   ___  |_   _|__  
 \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \   | |/ _ \ 
  \ V  V /  __/ | (_| (_) | | | | | |  __/   | | (_) |
   \_/\_/ \___|_|\___\___/|_| |_| |_|\___|   |_|\___/ 
                                                      
 _____ ____   ___  _     
| ____/ ___| / _ \| |    
|  _| \___ \| | | | |    
| |___ ___) | |_| | |___ 
|_____|____/ \__\_\_____|


NEW USER GUIDE :

==> Start by creating a database by \'set database\' command
==> Use \'set table\' command to create an empty table, and selecting it as current table
==> You can then load data into that table by \'store data\' command

Type \'exit\' to exit Anytime
"""

#FUNCTIONS

def cdate(datelist):
    """
    A function converting a list of [dd,mm,yyyy] format to a date integer yyyymmdd for comparison purposes in select query
    """
    s = ''
    ncdn = False
    if len(str(datelist[0])) == 1:
        dd = "0" + str(datelist[0])
    elif len(str(datelist[0])) == 2:
        dd = str(datelist[0])
    else:
        return None
    if len(str(datelist[1])) == 1:
        mm = "0" + str(datelist[1])
    elif len(str(datelist[1])) == 2:
        mm = str(datelist[1])
    else:
        return None
    ystr = str(datelist[2])
    if ystr[0] == "-":   # --- notices and flags if year is negative, backwards compatibility 101
        ncdn = True
        ystr = ystr[1:]
    if len(ystr) > 4:
        return None
    yyyy = ystr
    if ncdn == False:
        s = yyyy + mm + dd
    else:
        s = "-" + yyyy + mm + dd
    s = int(s)
    return s


def root():
    """
    Going to the root / base directory
    """

    chdir(pathres)



def set_db(what = False):
    """
    Function used to set the database name or create an empty table of that name
    """
    if what:
        helpstr = 'Sets the default database to work in or creates a new one'
        return helpstr

    root()
    name = input("Select Database --> ")
    
    res = ()
    # taking the ls
    dirres = listdir()

    for element in dirres:
        if not path.isfile(path.join(pathres, element)):
            res += (element,)

    if name not in res:
        mkdir(path.join(pathres, name))

    chdir(path.join(pathres, name))
        

def set_tb(what = False):
    """
    Function used to set the table name or create an empty table of that name
    """
    if what:
        helpstr = 'Function used to set the table name or create an empty table of that name'
        return helpstr
    name = input("Select Table --> ")
    global cur_table
    cur_table = name
    
    # if the file is empty, load() errors out and {} is put in the table file
    dtdb = {}
    try:
        dtdb = load(cur_table)
    except:
        print('Empty file, please store data in the selected table')
        dump({}, cur_table)


def show_db(what = False):
    """
    Shows all the databases present in the relative root directory
    """
    if what:
        helpstr = 'Shows all the databases present in the relative root directory'
        return helpstr
    root()
    
    dirres = listdir()

    for element in dirres:
        if not path.isfile(path.join(pathres, element)):
            print(element)


def show_tb(what = False):
    """
    Shows all the tables present in the selected database, or in the relative root if you haven't selected a database
    """
    if what:
        helpstr = 'Shows all the tables present in the selected database'
        return helpstr
    
    dirres = listdir()
    for element in dirres:
        if path.isfile(path.join( getcwd(), element)) and "bison" in element:
            print(element[:-6])


def stringsort(strs, desc = False):
    """
    called internally by when some words are to be sorted
    The name is quite self explanatory
    takes LIST OF WORDS and TRUE or FALSE for descending or ascending order respectively
    returns sorted list
    """
    l = strs
    for e1 in range(len(l)):
        
        # the # is innserted before every word so that first swap is done acc to first letter, refer to the if condition after while
        l[e1] = ("#" + l[e1])
    
    # finding the greatest word to make every word of equal length later
    gr8 = len(l[0])
    for e2 in l:
        if len(e2) > gr8:
            gr8 = len(e2)
    d = {}
    for e3 in range(len(l)):

        #this is done to make every word length equal to of longest word, filling the blanks
        e9 = l[e3]
        l[e3] = l[e3] + ("\x00"*(gr8-len(l[e3])))
        
        #dictionary to know which word has how many \x00s
        d[l[e3]] = gr8-len(e9)
    
    for c in range(1,gr8):
        #the c value indicates the index of the string which is being compared
        
        for a in range(len(l)-1):
            # a is an insertion sort variable so that swaps occur till the correct place is reached
            
            b = a
            if desc == True or desc == "desc":
                while ord(l[b][c]) < ord(l[b+1][c]) and b >= 0 and b+1<len(l):
                    if l[b][:c] == l[b+1][:c]:
                        k = l[b] #the swaps
                        l[b] = l[b+1]
                        l[b+1] = k
                    b -= 1
            else:
                while ord(l[b][c]) > ord(l[b+1][c]) and b >= 0 and b+1<len(l):
                    if l[b][:c] == l[b+1][:c]:
                        k = l[b]
                        l[b] = l[b+1]
                        l[b+1] = k
                    b -= 1
    for e4 in range(len(l)):
        if d[l[e4]] == 0:
            pass
        else:
            l[e4] = l[e4][:-d[l[e4]]]
            # removing the \x00s using data from dictionary
    
    for e5 in range(len(l)):
        # removing the #s
        l[e5] = l[e5][1:]
    return l


def store_data(what = False):
    """
    Takes a DICTIONARY of fields mapped to valid data types
    defaults to current selected table
    type pk after a column name to make it primary key
    """
    if what:
        helpstr = 'Interactive Menu to create a table, asks for fields only once'
        return helpstr
    print('\nTYPE exit TO EXIT\n')
    dtdb = {}
    try:
        dtdb = load(cur_table)
    except:
        dump({}, cur_table)
    
    # the case when table is empty, creates a new fields dictionary
    if dtdb == {}:
        fields = {}
        cn = 1
        print("""
        --> Type pk after column name to make it primary key
        --> The primary key is later used to do stuff like deleting rows
        --> DO NOT use invalid characters like ?,/@# in column name
        --> Valid Data Types:
        """)
        
        # printing the valid data types
        xi = 0
        while xi in range(0,len(ValidFieldTypes)):
            print('        ==> ', xi+1, ".", ValidFieldTypes[xi])
            xi += 1
        
        # asking for column names to create a new fields dictionary
        while True:
            x = input("Enter %dth Column Name --> " % cn)
            if x != "exit" or x != "Exit":
                y = input("Enter %dth Column Type --> " % cn)
            if x == "exit" or x == "Exit" or y == "exit" or y == "Exit":
                break
            elif y in ValidFieldTypes:
                fields[x] = y
            else:
                print("Not a valid data type, skipping this column this time")
                cn -= 1
            cn += 1
    
    # if fields is not made in the above section, i.e, table wasn't empty,
    # creates a fields dictionary again and enters values acc to it
    if 'fields' not in locals() :
        fields = {}
        fieldks = list(list(dtdb.values())[0].keys())
        for key in dtdb:
            lfields = []
            row = dtdb[key]
            rfields = {}
            
            # puts the data type for each value in table in the rfields dictionary
            for field in row:
                val = row[field]
                if 'int' in str(type(val)):
                    rfields[field] = 'int'
                elif 'str' in str(type(val)):
                    rfields[field] = 'str'
                elif 'bool' in str(type(val)):
                    rfields[field] = 'bool'
                elif 'list' in str(type(val)):
                    rfields[field] = 'date'
                elif 'float' in str(type(val)):
                    rfields[field] = 'decimal'
                elif val == None or val == '':
                    rfields[field] = 'str'
                else:
                    print('INVALID DATA TYPE FOUND!')
                    return None
            
            # lfields is the list of rfields for each rows
            # each element of lfields should be same if there is no null value
            lfields.append(rfields)
        
        # even if null value is detected, the rest of the values in the field dominate using this function called
        # and thus the values are entered according to that
        fields = mostoccuringfields(lfields)
    
    # uses the fields dictionary if fields were created earlier but rows were not inserted
    else:
        fieldks = list(fields.keys())
    
    while True:
        x = {}
        b = 0
        while b < len(fieldks):
            fstr = fieldks[b]
            print('', fields[fstr])
            
            # for integer fields, asks for input till acceptable and uses int function
            if fields[fstr] == 'int':
                run1 = True
                while run1 == True:
                    try:
                        finp = input("Enter value for {0} {1} --> ".format(fstr, fields[fstr]))
                        if finp == "exit" or finp == "e" or finp == "no" or finp == "Exit":
                                return None
                        else:
                            finp = int(finp)
                            run1 = False
                    except:
                        print("\n\n", "PLEASE ENTER AN INTEGER", "\n")
            
            # for decimal fields, asks for input till acceptable and uses float function
            elif fields[fstr] == 'decimal':
                run1 = True
                while run1 == True:
                    try:
                        finp = input("Enter value for {0} {1} --> ".format(fstr, fields[fstr]))
                        if finp == "exit" or finp == "e" or finp == "no" or finp == "Exit":
                                return None
                        else:
                            finp = float(finp)
                            run1 = False
                    except:
                        print("\n\n", "PLEASE ENTER AN INTEGER OR DECIMAL", "\n")
            
            # For boolean fields, asks for input once and modifies finp variable accordingly which is to be sent to table file in the end
            elif fields[fstr] == 'bool':
                finp1 = input("Enter value for {0} {1} --> ".format(fstr, fields[fstr]))
                if finp1 == "exit":
                    return None
                if finp1 == "no" or finp1 == "No" or finp1 == "False" or finp1 == "false" or finp1 == "none" or finp1 == "n" or finp1 == "N" or finp1 == "None" or finp1 == "f" or finp1 == "0":
                    finp = False
                else:
                    finp = True
            
            # for date fields, asks for input till acceptable and uses split method and saves to table as [dd,mm,yyyy] list
            elif fields[fstr] == 'date':
                print('enter in dd/mm/yyyy format')
                ret = True
                while ret == True:
                    date = input("Enter value for {0} {1} --> ".format(fstr, fields[fstr]))
                    if date == "exit":
                        return None
                    elif "/" in date:
                        date = date.split("/")
                        ret = False
                    elif "-" in date:
                        date = date.split("-")
                        ret = False
                    elif "." in date:
                        date = date.split(".")
                        ret = False
                    elif " " in date:
                        date = date.split()
                        ret = False
                    elif "," in date:
                        date = date.split(",")
                        ret = False
                    else:
                        print("Invalid Date format, enter in dd/mm/yyyy")
                        ret = True
                dd = int(date[0])
                mm = int(date[1])
                yyyy = int(date[2])
                finp = [dd,mm,yyyy]
            else:
                finp = input("Enter %s --> " % (fstr))
                if finp == "exit":
                    return None
            
            # adds the processed input to the x dictionary to be stored in file
            x[fstr] = finp
            b += 1
        dtdb[len(dtdb)+1] = x
        dump(dtdb, cur_table)


def mostoccuringfields(list_of_field_dicts):
    """
    Used in situations when few of the entries have None values in them
    takes list of field dicts for each row and gives the most occured one
    """
    # converting each field_dict to string because dictionary : value pair isnt possible (unhashable data type)
    i = 0
    while i < len(list_of_field_dicts):
        list_of_field_dicts[i] = str(list_of_field_dicts[i])
        i += 1
    
    # making a dict of field_dict : occurence pairs
    fieldoccur = {}
    for i in list_of_field_dicts:
        if i in list(fieldoccur.keys()):
            fieldoccur[i] += 1
        else:
            fieldoccur[i] = 1
    
    # returns the one if there is no discrepancies in field types acc to read values
    if len(list(fieldoccur.keys())) == 1:
        return eval(list(fieldoccur.keys())[0])
    
    # searching for the most occured field_dict
    gr8 = list(fieldoccur.keys())[0]
    for field_dict in fieldoccur:
        if fieldoccur[field_dict] > fieldoccur[gr8]:
            gr8 = field_dict
            
    return gr8

def load_data(what = False):
    """
    loads data and prints them in json.dumps fashion
    can take a TABLE NAME argument or defaults it to current table name
    can be useful when rawdisp misbehaves or viewing a short table
    """
    if what:
        helpstr = 'loads data and prints them in json.dumps fashion'
        return helpstr
    
    # loads data from table file, exits if empty
    dtdb = {}
    try:
        dtdb = load(cur_table)
    except:
        print('Table empty, please use \'store data\' to store someting')
        return None
    
    # displays data for each row json.dumps style
    for s in dtdb.keys():
        print("\n",s,"th entry: ")
        print(dumps(dtdb[s], indent = 6))


def rawdisp(dtdb = False, lotups = False, what = False, neatness = 3):
    """
    Displays the table, takes in two positional parameters:
    ==> dtdb, which is the esql specific format of a table
    ==> lotups, which is the general list of rows e.g. --> [('sn', 'name', 'job'), (1, 'john', 'assassin')] form
    """
    if what:
        helpstr = 'Displays the contents of the currently selected table or input as parameters'
        return helpstr

    # the case when the list of tuples is not given, converting the dtdb to list of tuples form
    if not lotups:
        if not dtdb:
            try:
                dtdb = load(cur_table)
            except:
                print(cur_table, 'table is empty or corrupt')
                return None

        # changing the dtdb from table dictionary form to list of tuples form
        # appending the fieldnames as the first tuple in the list
        
        if dtdb == {}:
            print('Empty table')
            return None
        
        dtdb1 = []
        htup = ()
        for k in dtdb[1].keys():
            htup += (k,)
        dtdb1.append(htup)
        
        # appending the rows one by one
        ldata = []
        for s1 in dtdb.keys():
            tup = ()
            for s2 in dtdb[s1].values():
                tup += (s2,)
            ldata.append(tup)
        
        # adding the collected tuples from table to the list
        dtdb1 += ldata
        lotups = dtdb1
        
    # making a list of longest words in a column for later use
    grlist = []
    for icol in range(len(lotups[0])):

        # searching for longest word in each column
        gr8 = lotups[0][icol]
        for irow in range(len(lotups)):
            if len(str(lotups[irow][icol])) > len(str(gr8)):
                gr8 = lotups[irow][icol]

        # extra 3 whitespaces for neat-ness
        grlist.append(len(str(gr8)) + neatness)

    print()
    # actual printing process row by row
    for row in range(len(lotups)):
        for icol in range(len(lotups[row])):
            if row == 0 and icol == len(lotups[row])-1:
                print(lotups[row][icol],  '\n', '-' * (sum(grlist) + neatness * (len(grlist) - 1)), end = '', sep = '')
            else:
                print(lotups[row][icol], end = ' ' * ( grlist[icol] - len(str(lotups[row][icol])) ) )
        print()


def checc(dtup,conditionstring):
    """
    checc function
    checks for a condition given the DICT_OF_TUPLES (containing each column => row pair) and CONDITION
    called by select function internally
    """
    command = ""
    for keys in dtup:
        # if the value is string, use apostrophe around it
        if 'str' in str(type(dtup[keys])) or 'unicode' in str(type(dtup[keys])):
            # writing the values with inverted commas so that python treats it as string as well
            command += "{} = '{}';".format(keys,dtup[keys])
        else:
            # keeps the string without inverted commas to not make it a string
            command += "{} = {};".format(keys,dtup[keys])
    command += "({});".format(conditionstring)
    
    def convertExpr2Expression(Expr):
            Expr.lineno = 0
            Expr.col_offset = 0
            result = ast.Expression(Expr.value, lineno=0, col_offset = 0)

            return result
        
    def exec_with_return(code):
        code_ast = ast.parse(code)

        init_ast = copy.deepcopy(code_ast)
        init_ast.body = code_ast.body[:-1]

        last_ast = copy.deepcopy(code_ast)
        last_ast.body = code_ast.body[-1:]

        exec(compile(init_ast, "<ast>", "exec"), globals())
        if type(last_ast.body[0]) == ast.Expr:
            return eval(compile(convertExpr2Expression(last_ast.body[0]), "<ast>", "eval"),globals())
        else:
            exec(compile(last_ast, "<ast>", "exec"),globals())
    
    return exec_with_return(command)
    
    

    """
    command = "".join(["{} = '{}';".format(keys, dtup[keys) for keys in dtup
        if ('str' in dtup[keys] or 'unicode' in dtup[keys]) )

        + "".join(["{} = {};".format(keys, dtup[keys) for keys in dtup
        + "print({})".format(conditionstring)
    """


def select(listofheads = None, condition = None, odbf = None, desc = None, distinct = None, what = False):
    """
    select query
    takes LIST_OF_FIELDS to be shown (or just "*" for all) AND a CONDITION as arguments
    Optional:
    A 3rd 'order by' field argument, can be integer, float, or string type field
    A 4th argument True or False for ordering in descending and ascending order respectively
    If No arguments given, asks the user the above parameters using input()
    Condition String, Order by, and Desc Fields can be left empty, optional inputs
    """
    if what:
        helpstr = 'Selects the relevant records and displays them'
        return helpstr
    print("Pro tip -> type * or leave empty in select what field to select all the headers")
    
    # asks for each parameter if not passed into the function
    allhds = False
    if not listofheads:
        listofheads = input("Select What Columns? [separate by commas] --> ")
        if listofheads == "" or listofheads == "*":
            allhds = True
        elif ',' not in listofheads:
            allhds = 2
        else:
            listofheads = listofheads.split(',')

    if not condition:
        condition = input("Condition for row selection --> ")
    if not odbf:
        odbf = input("Orderby --> ")
    if not desc:
        desc = input("desc --> ")
    if not distinct:
        distinct = input("Distinct --> ")
    
    # setting the default value of decreasing order
    if desc == '' or desc == "no" or desc == "False" or desc == "false":
        desc = False
    elif desc == "True" or desc == "true" or desc == "yes":
        desc = True
    dtdb = ''
    
    # loading the data
    
    dtdb = load(cur_table)
    
    # taking all fields if entered asterisk or left listofheads empty
    if allhds == True:
        listofheads = list(list(dtdb.values())[0].keys())

    if 'list' not in str(type(listofheads)):
        listofheads = [listofheads]
    heads = listofheads

    # selects all rows if condition is True or left empty
    entries = []
    if condition == True or condition == '':
        for z in range(len(dtdb)):
            tup = ()
            for keys in list(dtdb.values())[z]:
                if keys in heads:
                    tup += (list(dtdb.values())[z][keys],)
            entries.append(tup)
    
    # selects the rows for which condition is satisfied if otherwise
    else:
        for z in range(len(dtdb.keys())):
            
            # these lines make rcpairs dictionary containing field : value pair for each zth row
            # pass the dictionary to checc() which checks if condition satisfies
            tup = tuple(y for y in list(dtdb.values())[z].values())
            rcpairs = dict(zip(list(list(dtdb.values())[0].keys()), tup))
            tupc = checc(rcpairs,condition)
            
            # if row satisfies the condition, it is added to the entries list
            if tupc == True:
                tup = ()
                for keys in list(dtdb.values())[z]:
                    if keys in heads:
                        tup += (list(dtdb.values())[z][keys],)
                entries.append(tup)
    
    # the case in which order by is specified
    if odbf != '':
        
        # extracting rows from entries
        
        # date type uses a different dts because it puts yyyymmdd number in the lts and then sorts it
        # rest of the sortable types already have their sort function
        if 'list' in str(type(list(dtdb.values())[0][odbf])):
            n = heads.index(odbf)
            dts = {}
            for i in entries:
                datevar = cdate(i[n])
                if datevar == None:
                    print("The entered orderby value is invalid")
                    return None
                else:
                    dts[datevar] = i
            lts = list(dts.keys())
        else:
            # for the rest of the data types
            n = heads.index(odbf)
            dts = {}
            for i in entries:
                dts[i[n]] = i
            lts = list(dts.keys())
        
        if 'int' in str(type(list(dtdb.values())[0][odbf])) or 'float' in str(type(list(dtdb.values())[0][odbf])):

            # the sorting
            if desc == False or desc == "asc":
                lts.sort()
            elif desc == True or desc == "desc":
                lts.sort(reverse = True)
            else:
                print('desc value invalid')
                return None
        
        elif 'str' in str(type(list(dtdb.values())[0][odbf])):
            
            # the sorting
            if desc == False or desc == "asc":
                lts = stringsort(lts)
            elif desc == True or desc == "desc":
                lts = stringsort(lts, True)
        
        # the case in which order by field's first value is found to be date type
        elif 'list' in str(type(list(dtdb.values())[0][odbf])):
            
            # the sorting
            if desc == False or desc == "asc":
                lts.sort()
            elif desc == True or desc == "desc":
                lts.sort(reverse = True)
            else:
                print('desc value invalid')
                return None
        else:
            print('Field type not sortable')
        entries = []
        for j in lts:
            entries.append(dts[j])

    # finding the primary key for distinct
    for sp in list(dtdb.values())[0].keys():
        if sp[-2:] == "pk":
            pk = sp
    
    # the case when distinct is not mentioned
    if distinct == None or distinct == '':
        pass
    else:
        
        # distinct test
        lsi = []
        lvals = []
        for si in list(dtdb.values()):
            if si[distinct] in lsi:
                lvals.append(si[pk])
            lsi.append(si[distinct])
        sod = {}
        for so in entries:
            for h1 in dtdb:
                ide = True
                for joe in so:
                    if joe not in list(dtdb[h1].values()):
                        ide = False
                if ide == True:
                    sod[dtdb[h1][pk]] = so
        for s5 in sod:
            if s5 in lvals:
                del entries[entries.index(sod[s5])]
    
    # displaying the final entries with heads
    heads = tuple(heads)
    entries.insert(0, heads)
    rawdisp(lotups = entries)


def delt(what = False):
    """
    Deletes a row given the PRIMARY KEY VALUE, PRIMARY KEY VALUES IN LIST or CONDITION STRING
    """
    if what:
        helpstr = 'Deletes a row given the primary key value, primary key values in list form or some condition'
        return helpstr
    
    # user input here
    tbd = eval(input("Which Row(s)?\n>>"))
    print("If you forgot to put pk after a column name to make primary key, delete function would still work for condition strings")
    print("Ex - give 'sn == 4' in 'which rows' parameter")
    
    # loading and checking if empty table
    dtdb = ''
    try:
        dtdb = load(cur_table)
    except:
        dump({}, cur_table)
        print('Empty bison file, use store data to add data')
        return None
    
    # checking if user input matches primary key and deleting if found
    # flags the deletion so that further checking doesn't occur
    run = True
    for t1 in dtdb:
        for t2 in dtdb[t1]:
            if dtdb[t1][t2] == tbd and t2[-2:] == "pk":
                run = False
                del dtdb[t1]
                break
        if run == False:
            break
    
    # checking for list for primary key values if user entered a list
    # and appending to a deletion list if found , and then, deleting one by one
    if 'list' in str(type(tbd)) and run == True:
        l1 = []
        for t1 in dtdb:
            for t2 in dtdb[t1]:
                if (dtdb[t1][t2] in tbd) and t2[-2:] == "pk":
                    l1.append(t1)
        for t3 in l1:
            del dtdb[t3]
        if len(l1) != 0:
            print("\n", len(l1), "rows affected")
    
    # checking for the condition if user entered a string deleting if match found
    elif 'str' in str(type(tbd)) and run == True:
        l2 = []
        for z in range(len(dtdb.keys())):
            tup = tuple(y for y in list(dtdb.values())[z].values())
            rcpairs = dict(zip(list(list(dtdb.values())[0].keys()), tup))
            tupc = checc(rcpairs,tbd)
            if tupc == True:
                l2.append(list(dtdb.keys())[z])
        for z1 in l2:
            del dtdb[z1]
        if len(l2) != 0:
            print("\n", len(l2), "rows affected")
    
    # if no match occurs (direct primary key row number, list of row numbers
    # and condition string matching fails altogether), displays 'No Rows Affected'
    else:
        if run == True:
            print("No Rows Affected")
    dtdb = dict(zip([i for i in range(1,len(list(dtdb.keys()))+1)], list(dtdb.values())))
    dump(dtdb, cur_table)
    if run == False:
        print("\n1 row affected")


def update(what = False):
    """
    Updates the table given the FIELD to be updated, the NEW VALUE, and the row(s) to be updated
    Rows which are to be updated can be selected by giving a PRIMARY KEY, a LIST of primary keys or a CONDITION STRING
    """
    if what:
        helpstr = 'Updates the table by taking Column, new value and primary key list or condition string from user'
        return helpstr
    
    # user input here
    tbu = input("Which Row(s)? [primary key list or condition string]\n--> ")
    if tbu == "*" or tbu == '':
        pass
    else:
        tbu = eval(tbu)
    
    # getting a new value to update required field from user
    field = input("Which Column?\n--> ")
    newval = eval(input("New Value: \n--> "))
    
    # loading and checking for empty table
    dtdb = ''
    try:
        dtdb = load(cur_table)
    except:
        dump({}, cur_table)
        print('EMPTY TABLE, USE store data TO ADD SOME')
        return None
    
    # adds primary key of every row to to-be-updated if to-be-updated was left empty
    if tbu == "*" or tbu == '':
        li = []
        for s1 in dtdb.values():
            for s2 in s1.keys():
                if s2[-2:] == "pk":
                    li.append(s1[s2])
        tbu = li
    
    # giving new value to every row if tbu is made above
    run = True
    for t1 in dtdb:
        for t2 in dtdb[t1]:
            if dtdb[t1][t2] == tbu and t2[-2:] == "pk":
                run = False
                dtdb[t1][field] = newval
                break
        if run == False:
            break
    
    # prints message according to updated-already flag
    # and proceeds further only if flag says not-updated-yet
    if run == False:
        print("\n1 row affected")
    
    # searches for list of rows' primary keys if user entered a list and adds them to l1 list
    if 'list' in str(type(tbu)) and run == True:
        l1 = []
        for t1 in dtdb:
            for t2 in dtdb[t1]:
                if (dtdb[t1][t2] in tbu) and t2[-2:] == "pk":
                    l1.append(t1)
        if len(l1) != 0:
            print("\n", len(l1), "rows affected")
            
    # solves for a condition string and adds them to l1 list if user entered a string
    elif 'str' in str(type(tbu)) and run == True:
        l1 = []
        for z in range(len(dtdb.keys())):
            tup = tuple(y for y in list(dtdb.values())[z].values())
            rcpairs = dict(zip(list(list(dtdb.values())[0].keys()), tup))
            tupc = checc(rcpairs,tbu)
            if tupc == True:
                l1.append(list(dtdb.keys())[z])
        if len(l1) != 0:
            print("\n", len(l1), "rows affected")
    
    # updates the data if l1 list was made by above two conditions
    if run == True and 'l1' in locals():
        for z1 in l1:
            dtdb[z1][field] = newval
    
    # displays nothing affected if no conditions/lists/key match
    if run == True and 'l1' not in locals():
        print("No Rows affected, unmatching arguments")
        return None
    dtdb = dict(zip([i for i in range(1,len(list(dtdb.keys()))+1)], list(dtdb.values())))
    dump(dtdb,cur_table)


def maxval(what = False):
    """
    Finds the row with maximum value of the given FIELDNAME
    optional inputs if multiple rows --> Order by and descending order, can be left empty
    """
    if what:
        helpstr = 'Finds the row with maximum value of the given field name'
        return helpstr
    
    # user input here
    fieldname = input("Which Column?\n --> ")
    orderbyfield = input("Orderby --> ")
    desc = input("desc --> ")
    distinct = input("Distinct --> ")
    
    # setting the default values and conditional values from user input
    if desc == '' or desc == "no" or desc == "False" or desc == "false":
        desc = False
    elif desc == "True" or desc == "true" or desc == "yes":
        desc = True
    if distinct == '' or distinct == "None" or distinct == "none":
        distinct = ''
    
    # loads the table and checks if empty
    try:
        dtdb = load(cur_table)
    except:
        dump({}, cur_table)
        print('EMPTY TABLE, USE store data TO ADD SOME')
        return None
    
    # errors out if field's 1st entry is boolean type, because, incomparable
    if 'bool' in str(type(list(dtdb.values())[0][fieldname])):
        print("Boolean Values are incomparable")
        return None
    
    # checks if field's first entry is integer or float
    # and displays the maximum-value-entry by max()
    elif 'int' in str(type(list(dtdb.values())[0][fieldname])) or 'float' in str(type(list(dtdb.values())[0][fieldname])):
        l = []
        for z1 in range(len(dtdb)):
            l.append(list(dtdb.values())[z1][fieldname])
        select("*", '%s == %s' % (fieldname ,max(l)), orderbyfield, desc, distinct)
    
    # checks if field's first entry is list, i.e., date type and then,
    # calls cdate function for each date and uses max() to display the latest-date-row
    elif 'list' in str(type(list(dtdb.values())[0][fieldname])):
        l = []
        for z1 in range(len(dtdb)):
            datevar = cdate(list(dtdb.values())[z1][fieldname])
            if datevar == None:
                print("Invalid fieldname")
                return None
            else:
                l.append(datevar)
        dms = str(max(l))
        if len(dms) == 8:
            dlist = [int(dms[-2:]), int(dms[4:6]), int(dms[:4])]
            select("*", '%s == %s' % (fieldname, dlist), orderbyfield, desc, distinct)
        else:
            print("Maximum %s is: " % fieldname, max(l))


def minval(what = False):
    """
    Finds the row with minimum value of the given FIELDNAME
    optional inputs if multiple rows --> Order by and descending order, can be left empty
    """
    if what:
        helpstr = 'Finds the row with minimum value of the given field name'
        return helpstr
    
    # user input here
    fieldname = input("Which Column?\n--> ")
    orderbyfield = input("Orderby --> ")
    desc = input("desc --> ")
    distinct = input("Distinct --> ")
    
    # setting the default values and conditional values from user input
    if desc == '' or desc == "no" or desc == "False" or desc == "false":
        desc = False
    elif desc == "True" or desc == "true" or desc == "yes":
        desc = True
    if distinct == '' or distinct == "None" or distinct == "None":
        distinct = ''
    
    # loads the table and checks if empty
    try:
        dtdb = load(cur_table)
    except:
        dump({}, cur_table)
        print('EMPTY TABLE, USE store data TO ADD SOME')
        return None
    
    # errors out if field's 1st entry is boolean type, because, incomparable
    if 'bool' in str(type(list(dtdb.values())[0][fieldname])):
        print("Boolean Values are incomparable")
        return None
    
    # checks if field's first entry is integer or float
    # and displays the maximum-value-entry by max()
    elif 'int' in str(type(list(dtdb.values())[0][fieldname])) or 'float' in str(type(list(dtdb.values())[0][fieldname])):
        l = []
        for z1 in range(len(dtdb)):
            l.append(list(dtdb.values())[z1][fieldname])
        select("*", '%s == %s' % (fieldname, min(l)), orderbyfield, desc, distinct)

    # checks if field's first entry is list, i.e., date type and then,
    # calls cdate function for each date and uses max() to display the latest-date-row
    elif 'list' in str(type(list(dtdb.values())[0][fieldname])):
        l = []
        for z1 in range(len(dtdb)):
            datevar = cdate(list(dtdb.values())[z1][fieldname])
            if datevar == None:
                print("Invalid fieldname")
                return None
            else:
                l.append(datevar)
        dms = str(min(l))
        if len(dms) == 8:
            dlist = [int(dms[-2:]), int(dms[4:6]), int(dms[:4])]
            select("*", '%s == %s' % (fieldname, dlist), orderbyfield, desc, distinct)
        else:
            print("Minimum %s is: " % fieldname, min(l))


def selcount(what = False):
    """
    Finds the number of rows with matching conditions
    Input --> Condition String
    """
    if what:
        helpstr = 'Finds the number of rows with matching conditions'
        return helpstr
    
    # user input here
    condition = input("Condition for row selection --> ")
    if condition == '' or condition == "*" or condition == "True":
        condition = True
    
    # loads and checks for empty table
    try:
        dtdb = load(cur_table)
    except:
        dump({}, cur_table)
        print('EMPTY TABLE, USE store data TO ADD SOME')
        return None
    
    # solves for the condition if some condition string is given
    if condition != True:
        l1 = []
        for z in range(len(dtdb.keys())):
            tup = tuple(y for y in list(dtdb.values())[z].values())
            rcpairs = dict(zip(list(list(dtdb.values())[0].keys()), tup))
            tupc = checc(rcpairs,condition)
            if tupc == True:
                l1.append(list(dtdb.keys())[z])
        print("==> ", len(l1))
    
    # displays the cardinality if condition is just True, i.e., count all
    else:
        print("==> ", len(dtdb))


def selsum(what = False):
    """
    Finds the sum of summable Columns, given the COLUMN NAME
    optional input --> condition, can be left empty
    """
    if what:
        helpstr = 'Finds the sum of summable Columns, given the field name'
        return helpstr
    
    # user input here
    fieldname = input("Which Column?\n--> ")
    condition = input("Condition for row selection --> ")
    
    # giving default value True , i.e., all rows if condition is left empty
    if condition == '' or condition == "True" or condition == "*":
        condition = True
    
    # loads the table and checks if empty
    try:
        dtdb = load(cur_table)
    except:
        dump({}, cur_table)
        print('EMPTY TABLE, USE store data TO ADD SOME')
        return None
    
    # solves for the condition if some condtion string is given
    if condition != True:
        l1 = []
        for z in range(len(dtdb.keys())):
            tup = tuple(y for y in list(dtdb.values())[z].values())
            rcpairs = dict(zip(list(list(dtdb.values())[0].keys()), tup))
            tupc = checc(rcpairs,condition)
            if tupc == True:
                l1.append(list(dtdb.keys())[z])
        
        # sums up the row numbers' field value which got matched
        # and displays message while ignoring the elements which aren't numerical
        sum1 = 0
        for s1 in dtdb:
            if s1 in l1:
                try:
                    sum1 += dtdb[s1][fieldname]
                except:
                    print("Things are not adding up!")
        print("==> ", sum1)
    
    # the sum-them-all case
    else:
        sum1 = 0
        for s1 in dtdb:
            try:
                sum1 += dtdb[s1][fieldname]
            except:
                print("Things are not adding up!")
        print("==> ", sum1)


def selavg(what = False):
    """
    Finds the Arithmetic Mean of summable Columns, given the COLUMN NAME
    optional input --> condition, can be left empty
    """
    if what:
        helpstr = 'Finds the Arithmetic Mean of summable Columns, given the COLUMN NAME'
        return helpstr
    
    # user input here
    fieldname = input("Which Column?\n--> ")
    condition = input("Condition for row selection --> ")
    
    # setting condition to True if it is left empty, i.e., finding average of all values
    if condition == '' or condition == "True" or condition == "*":
        condition = True
    
    # loads the table and checks if empty
    try:
        dtdb = load(cur_table)
    except:
        dump({}, cur_table)
        print('EMPTY TABLE, USE store data TO ADD SOME')
        return None
    
    # solving for the condition if condition string is given 
    # and appending row numbers to l1 list if matched
    if condition != True:
        l1 = []
        for z in range(len(dtdb.keys())):
            tup = tuple(y for y in list(dtdb.values())[z].values())
            rcpairs = dict(zip(list(list(dtdb.values())[0].keys()), tup))
            tupc = checc(rcpairs,condition)
            if tupc == True:
                l1.append(list(dtdb.keys())[z])
        
        # finding average of the field values of rows in l1 list
        sum1 = 0
        for s1 in dtdb:
            if s1 in l1:
                try:
                    sum1 += dtdb[s1][fieldname]
                except:
                    print("Things are not adding up!")
        print("==> ", sum1/len(l1))
    
    # the average them all case
    else:
        sum1 = 0
        for s1 in dtdb:
            try:
                sum1 += dtdb[s1][fieldname]
            except:
                print("Things are not adding up!")
        print("==> ", sum1/len(dtdb))


def merge(what = False):
    """
    Merges rows of many tables with same columns
    """
    if what:
        helpstr = 'Merges rows of many tables with same columns'
        return helpstr
    
    # user input loop to add to list of tables to be merged
    lots = []
    print("--Enter exit in the following field to stop joining tables--")
    while True:
        t = input("Enter the name of a table in the selected database to join -->")
        lots.append(t)
        if lots[-1] == "exit":
            lots = lots[:-1]
            break
    
    # adds tables one by one to an empty table dtdb if fields match exactly
    dtdb = {}
    antilots = []
    for tname in lots:
    
        # the first run when first table in list is to be added to empty list
        # and then second to first is done in else block
        if dtdb == {}:
            ctdb = {}
            ctdb = load(tname)
            dtdb = ctdb
        
        # merges n+1th to nth table if fields match
        # and adds table name to antilots list if they don't
        else:
            dtdb1 = {}
            dtdb1 = load(tname)
            
            # the condition to match fields
            if list(list(dtdb1.values())[0].keys()) == list(list(dtdb.values())[-1].keys()):
                for s1 in dtdb1:
                    
                    # appending rows to table in loop
                    if s1 not in list(dtdb.keys()):
                        dtdb[s1] = dtdb1[s1]
                    
                    # if s1 row number is already in to-be-added-to table,
                    # takes the successor of the last row number as new row number
                    # to avoid data loss
                    else:
                        s1a = str(int(list(dtdb.keys())[-1]) + 1)
                        dtdb[s1a] = dtdb1[s1]
            
            # the case where fields don't match, adding not-merged tables to antilots list
            else:
                print("ERROR:\nColumns are not same, rejecting %dth table" % lots.index(tname))
                antilots.append(tname)
    
    # converting the new table to standard form and naming and saving it
    dtdb = dict(zip([i for i in range(1,len(list(dtdb.keys()))+1)], list(dtdb.values())))
    newname = input("Give a name to the new table --> ")
    dump(dtdb, newname)
    
    # filtering the not-merged tables (antilots) out of the list of input to-be-merged
    for s3 in antilots:
        del lots[lots.index(s3)]
    
    # deleting the already merged tables, to avoid redundacy
    for s2 in lots:
        drop(s2)


def drop(tablename = None, what = False):
    """
    Deletes the given tables, can take a table as argument also
    """
    if what:
        helpstr = 'Deletes the given table'
        return helpstr
    
    # taking user input as list of tables or a single table to be deleted
    if tablename == None:
        tablename = input("Enter the name of the table you want to delete (or separate by space if want to delete many) --> ")
    if ' ' in tablename:
        tablelist = tablename.split()
    else:
        tablelist = [tablename]
    
    # deleting each table's corresponding file
    for tablename in tablelist:
        if win == False:
            system("rm %s.bison" % tablename)
        else:
            system("del %s.bison" % tablename)


def dropdb(what = False):
    """
    Deletes the given databases given a list of databases or a single database
    """
    if what:
        helpstr = 'Deletes the given database'
        return helpstr
    
    # going to the file's relative root where all databases are there
    root()
    
    # taking user input as list of databases or a single database to be deleted
    dbn = input("Enter the name of database you want to delete (or separate by space if want to delete many) --> ")
    if ' ' in dbn:
        dblist = dbn.split()
    else:
        dblist = [dbn]
    
    # deleting each database's corresponding folder
    for dbn in dblist:
        if win == False:
            system("rm -rf %s" % dbn)
        else:
            system("rmdir  /q /s %s" % dbn)


def arcol(what = False):
    """
    Adds, removes, or renames a column to/from/in the current table
    """
    if what:
        helpstr = 'Adds, removes, or renames a column to/from/in the current table'
        return helpstr
    
    # loads and checks if table is empty
    try:
        dtdb = {}
        dtdb = load(cur_table)
    except:
        print("select a table with some data, or store data in the selected table")
    
    # user input loop to choose between adding, removing or renaming column
    run1 =  True
    while run1:
        choice = input("Do you want to\n1. Add an empty Column? or \n2. Remove a Column\n3. Rename a Column Enter 1,2 or 3 -->")
        try:
            choice = int(choice)
            run1 = False
        except:
            print("Not an integer!")
    
    # adding condition
    if choice == 1:
        c1 = input("Enter the name of new column --> ")
        for c2 in dtdb:
            dtdb[c2].update({c1:None})
    
    # removing a column of user's choice
    elif choice == 2:
        c3 = input("Enter the name of column you wish to remove --> ")
        if c3 in list(list(dtdb.values())[0].keys()):
            c5 = list(dtdb.keys()) 
            for c4 in c5:
                del dtdb[c4][c3]
        else:
            print("Column not found!")
    
    # renaming a column
    else:
        c6 = input("Enter the old name of column you wish to rename --> ")
        c7 = input("Enter the new name --> ")
        fks = list(list(dtdb.values())[0].keys())
        if c6 in fks:
            for c8 in list(dtdb.keys()):
                l3 = list(dtdb[c8].keys())
                l4 = list(dtdb[c8].values())
                l3[l3.index(c6)] = c7
                dtdb[c8] = dict(zip(l3,l4))
            print(dtdb)
        else:
            print("Column not found!")
    
    # saving the changes
    dump(dtdb, cur_table)


def helpme(what = False):
    """
    Lists all the commands with a command number and its description in the form of a table
    """
    if what:
        helpstr = 'Lists out all the commands available'
        return helpstr
    print("Following commands are available: \n")
    ct1 = 1
    dc1 = {}
    for a in commands:
        dc1[ct1] = {'S.No.' : ct1, 'Command' : a, 'description' : commands[a](what = True) }
        ct1 += 1
    rawdisp(dc1)

def helpme1(what = False):
    """
    Implements help function to see all the docstrings in each function
    """
    if what:
        helpstr = 'Gives the docstrings of each function for detailed information'
        return helpstr
    help(esql)

def credit(what = False):
    """
    Rolls the credits
    """
    if what:
        helpstr = 'Displays the credits'
        return helpstr
    print(" _________________________________________ ")
    print("/ I imported os.system, os.chdir,         \ ")
    print("| os.path, sys.platform,                  |")
    print("| sys.version_info,                       |")
    print("| __future__.print_function, functions    |")
    print("|and pickle module, wrote the rest myself |")
    print("\ Author is Aryan Sidhwani btw            /")
    print(" ----------------------------------------- ")
    print("   \    ,-^-.")
    print("    \   !oYo!")
    print("     \ /./=\.\______  ")
    print("          ##        )\/\ ")
    print("           ||-----w|| ")
    print("           ||      || ")


def run():
    """
    The function may be imported and run or, run directly 
    by uncommenting the run() in __main__
    """
    print(welcstr)
    helpme()
    while True:
        
        # the command prompt
        c = input("\nesql>> ")
        
        # the case when command itself is entered
        if c in list(commands.keys()):
            commands.get(c)()
        
        # the case when command number is entered
        elif c in [str(x) for x in range(1,len(commands)+1)]:
            commands.get(list(commands.keys())[int(c)-1])()
        
        elif c == "exit" or c == "Exit":
            break
        else:
            print("Unknown command, type help to see all known commands")
    c = input("Press Enter to exit  ")


def dump(database, filename):
    """
    Saves the given table inside a file of given name in parameter
    """
    file1 = open(filename + '.bison', 'wb')
    pickle.dump(database, file1)
    file1.close()

def load(filename):
    '''
    Reads and loads the table from table file and returns it
    '''
    file1 = open(filename + '.bison', 'rb')
    database = pickle.load(file1)
    file1.close()
    return database

def dumps(dictionary, indent = 4):
    '''
    Returns a string in json.dumps style given a table (dictionary)
    as a positional argument and a number (indent) as a keyword argument
    '''
    st = ''
    greatest = len(str(list(dictionary.keys())[0]))
    for key in dictionary:
        if len(str(key)) > greatest:
            greatest = len(str(key))
    st += '{\n'
    for key in dictionary:
        st += ' ' * indent + str(key) + ' '*(greatest-len(str(key))) + '   ' + '==>' + '   ' + str(dictionary[key]) + ','
        st += '\n'
    st = st[:-2]
    st += '\n}'
    return st


# command list for run() function

commands = {"show databases" : show_db,
            "set database" : set_db,
            "show tables" : show_tb,
            "set table" : set_tb,
            "store data" : store_data,            
            "display" : rawdisp,
            "select" : select,
            "delete" : delt, 
            "update" : update,
            "change column" : arcol,
            "maxval" : maxval,
            "minval" : minval,
            "count" : selcount,
            "sum" : selsum,
            "avg" : selavg,
            "drop table" : drop,
            "merge tables" : merge,
            "drop database" : dropdb,
            "dump data" : load_data,
            "help" : helpme,
            "more help" : helpme1,
            "credits" : credit
            }

run()

'''
tbd / next update:
composite key
foreign key
group by .. having ..
cross join
natural join
conditional join
count, select, average etc. attached inside select function
converting the table to [(heads), (row1), ...] form by giving
an optional parameter in load to return in the same form as read
else, by default converts to json form and then returns it
making a nicer table displayer with custom styles
do smth like select price*qty from .... or other such algebraic expressions
separate the create table and store data thing entirely (can have an empty table
with a desc file attached to it)
'''
