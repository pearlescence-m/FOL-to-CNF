"""
The program converts statements from FOL to CNF.

List of assumptions:
• ”,” is AND
• ”.” is OR
• ”E” is Existential quantifier
• NOT statement is indicated as "~"
• ”V” is Universal quantifier
• ">" is implication
• "=" is bidirectional
• all prepositions consist of one capital letter (not words) except of V and E
"""

import re

# Step 1
def parseImplications(clause):

    for w in clause:
        if (w == '>') | (w == '='):
            i = clause.index(w)
            if clause[i - 1] == ']':
                clause[i] = "."
                k = i
                while (k > 0):
                    if clause[k] == "[":
                        clause[k+1] = "~"+clause[k+1]
                    k = k-1
            else:
                clause[i - 1] = "~" + clause[i - 1]
                clause[i] = "."
            print(clause)
    return clause

# Step 2
def parseNotsInwards(clause):

    for w in clause:
        ind = clause.index(w)
        if w.startswith("~V"):
            t = re.sub("~V", "E", clause[ind])
            clause[ind] = t
        if w.startswith("~E"):
            t = re.sub("~E", "V", clause[ind])
            clause[ind] = t
        if(w.startswith("~V")) | (w.startswith("~E")):
            i = ind+1
            while i < len(clause):
                if clause[i] == ".":
                    clause[i] = ","
                elif clause[i] == ",":
                    clause[i] = "."
                if clause[i] == "]":
                    break
                #issue with the subclause inside the clause
                if (clause[i] != ".") & (clause[i] != ",") & (clause[i] != "["):
                    clause[i] = "~"+clause[i]
                i = i + 1
        if w.startswith("~~"):
            t = re.sub("~~", "", clause[ind])
            clause[ind] = t
    return clause

# Step 3
def parseVariables(clause):

    vars = list()
    for w in clause:
        ind = clause.index(w)
        if (w.startswith("V")):
            e = re.split("V", w)
            if e[1] in vars:
                t = re.sub(e[1], "z", clause[ind])
                clause[ind] = t
                i = ind + 1
                while i < len(clause):
                    for let in clause[i]:
                        if let == e[1]:
                            g = re.sub(e[1], "z", clause[i])
                            clause[i] = g
                    if clause[i] == "]":
                        break
                    i = i + 1
                e[1] = "t"
            vars.append(e[1])
        # possible issue with the randomization of variable
        if (w.startswith("E")):
            e = re.split("E", w)
            if e[1] in vars:
                t = re.sub(e[1], "t", clause[ind])
                clause[ind] = t
                i = ind+1
                while i < len(clause):
                    for let in clause[i]:
                        if let == e[1]:
                            g = re.sub(e[1], "t", clause[i])
                            clause[i] = g

                    if clause[i] == "]":
                        break
                    i = i + 1
                e[1] = "t"
            vars.append(e[1])
        if (w.startswith("E")):
            del clause[ind]
    print(clause)
    return clause;

# Step 4
def skolemization(clause):

    if(clause[0].startswith("V")) | (clause[0].startswith("E")):
        var = clause[0][1]

    for w in clause:
        i = clause.index(w)
        if (w.find("(") != -1):
            a = w.index("(")
            if(w[a+1] != var):
                c = w[a+1].upper()
                c = c +"("+ var +")"
                g = re.sub(w[a+1], c, clause[i])
                clause[i] = g
        if (w.find(")") != -1):
            a = w.index(")")
            if (w[a - 1] != var):
                c = w[a - 1].upper()
                c = c + "(" + var + ")"
                g = re.sub(w[a - 1], c, clause[i])
                clause[i] = g
    print(clause)
    return clause

# Step 5
def dropUniversal(clause):
    del clause[0]
    print(clause)
    return clause

# Step 6
def distribution(clause):
    new = list()
    var = str()
    var1 = str()
    var2 = str()

    for w in clause:
        if(w == ","):
            d = clause.index(w)
            var1 = clause[d-1]
            var2 = clause[d+1]
        elif(w == "."):
            h  = clause.index(w)
            if(clause[h+1]) == "[":
                var = clause[h+2]
            else:
                var = clause[h+1]

    for w in clause:
        i = clause.index(w)
        new.append(w)
        if (w == var):
            new.append(".")
            new.append(var2)
        if(w == var1):
            del clause[i+2]
            new.insert(i+2, var)

    new.insert(2, ",")
    print(new)

    return new

clause = str()
choice = input("Please enter 1 to read from file or 2 to provide input from command line:")
if choice == '1':
    f = open('text', 'r')
    clause = f.readline()
elif choice == '2':
    clause = input("Your input: ")

stats = list(clause.split())
newclause = parseImplications(stats)
woNots = parseNotsInwards(newclause)
newstr = parseVariables(woNots)
newstr = skolemization(newstr)
newstr = dropUniversal(newstr)
result = distribution(newstr)
strg = str()

for item in result:
    strg += item
    strg += " "
print(strg)