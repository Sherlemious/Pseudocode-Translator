import os
import config

index = 0
equality = config.equality
operators = config.operators
statements = config.statements


def condition(statement):
    """
    :param statement: The statement to be evaluated
    :return: The evaluated statement
    """
    statement.replace('MOD', '%').replace('DIV', '//').replace('<>', '!=').replace('><', '!=')
    statement.replace('OR', 'or').replace('AND', 'and').replace('NOT', 'not')

    x = len(statement)
    for ch in range(x):
        char = statement[ch]
        if char == "=":
            if statement[ch - 1] not in equality and statement[ch + 1] not in equality:
                statement = statement[:ch] + "=" + statement[ch:]

    return statement


def convertUpperLower(statement):
    """

    """
    temp = statement.lower()

    while 'ucase(' in temp:
        pos = temp.find('ucase(')
        closeBracket = temp[pos:].find(')') + pos

        statement = statement[:pos] + statement[pos + 6:closeBracket] + '.upper()' + statement[closeBracket + 1:]
        temp = statement.lower()

    while 'lcase(' in temp:
        pos = temp.find('lcase(')
        closeBracket = temp[pos:].find(')') + pos

        statement = statement[:pos] + statement[pos + 6:closeBracket] + '.lower()' + statement[closeBracket + 1:]
        temp = statement.lower()

    return statement


def subString(statement):
    """
    :param statement: String
    :return: The string with the substring function
    substring format: substring(string, start, end)
    """
    temp = statement.lower()

    while 'substring(' in temp:
        pos = temp.find('substring(')
        firstComma = temp[pos:].find(',') + pos
        secondComma = temp[firstComma + 1:].find(',') + firstComma + 1
        closeBracket = temp[pos:].find(')') + pos

        start = temp[firstComma + 1:secondComma].strip()
        end = temp[secondComma + 1:closeBracket].strip()

        statement = statement[:pos] + statement[pos + 10:firstComma] + '[' + str(int(start) - 1) + ':' + str(
            int(start) - 1 + int(end)) + ']' + statement[closeBracket + 1:]
        temp = statement.lower()

    return statement


def evaluation(statement):
    statement = statement.replace('MOD', '%').replace('DIV', '//').replace('OR', 'or').replace('AND', 'and').replace(
        'NOT', 'not')
    statement = statement.replace('random', 'random.random')
    statement = statement.replace('INT', 'int')
    statement = statement.replace('LENGTH', 'len')
    statement = statement.replace('length', 'len')
    statement = convertUpperLower(statement)
    statement = subString(statement)
    return statement


def evaluate(line, indentation=0):
    """
    :param line: The line to be evaluated
    :param indentation: The indentation of the line
    :return: The evaluated line
    """
    while '] [' in line:
        line = line.replace('] [', '][')
    if line.upper().find("USERINPUT") == -1:
        return " " * indentation + evaluation(line)
    else:
        var = line.split('=')[0].strip()
        return " " * indentation + var + " = " + "eval(input())"


def PRINT(line, indentation=0):
    line = line[5:].strip()
    output = " " * indentation + "print(" + line + ")"

    return output


def OUTPUT(line, indentation):
    line = line[6:].strip()
    output = " " * indentation + "print(" + line + ")"

    return output


def INPUT(line, indentation=0):
    lst = line.upper().strip().split()
    if "," not in lst:
        output = " " * indentation + line[line.find("INPUT") + 6:].strip() + " = " + "eval(input())"

    return output


def WHILE(line, indentation=0):
    global index
    index += 4
    line = line[5:]
    line_temp = line.upper()
    if line_temp.find("DO") != -1:
        line = line[:line_temp.find("DO")]
    output = " " * indentation + "while" + condition(line) + ":"
    return output


def ENDWHILE():
    global index
    index -= 4


def REPEAT(indentation):
    global index
    index += 4
    return " " * indentation + "while True:"


def UNTIL(line, indentation):
    global index
    index -= 4
    line = line[5:]
    output = " " * indentation + "if" + condition(line) + ":"
    br = " " * (indentation + 4) + "break"
    return [output, br]


def IF(line, indentation):
    global index
    ln = line.upper()
    if ln.find("THEN") != -1:
        line = line[:ln.find("THEN")]
    index += 4
    line = line[2:]
    output = " " * indentation + "if" + condition(line) + ":"
    return output


def FOR(line, indentation):
    global index
    index += 4
    line = line[3:].strip()
    variable = line[:line.find('=')].strip()
    line = line.upper()
    start = line[line.find('=') + 1:line.find('TO')].strip()
    end = line[line.find('TO') + 2:].strip()
    output = " " * indentation + "for " + variable + " in range(" + str(int(start) - 1) + "," + end + "):"

    return output


def DECLARE():
    pass


def NEXT():
    global index
    index -= 4


def ENDIF():
    global index
    index -= 4


def ELSE(indentation):
    global index
    return " " * (indentation - 4) + "else:"


def initialize_lists_dict(lines):
    global index
    out = []
    lists = []
    for line in lines:
        l = line.strip()
        if l.find('[') != -1:
            bef_br = l[:l.find('[')].upper()

            flag = False
            for op in (statements + operators):
                if bef_br.find(op) != -1:
                    flag = True
            if flag:
                continue
            name = l[:l.find('[')]
            if name not in lists:
                lists.append(name)
                out.append(name + '={}')

    return out


def initialize_lists_list(lines):
    """
    :param lines, list of lines from the input.txt file
    :return: list, lines initializing
    """
    global index
    out = []
    undeclaredArrayNames = {}  # Array Names with their corresponding number of rows
    declaredArrayNames = []
    for line in lines:
        l = line.strip().replace(' ', '')
        if l.find('[') == -1:
            continue

        bef_br = l[:l.find('[')].upper()

        flag = False
        for op in (statements + operators):
            if bef_br.find(op) != -1:
                flag = True
        if flag:
            continue

        name = l[:l.find('[')]

        if l.find(',') != -1:  # This means that an array is assigned to the variable somewhere in the program
            # Example x = [1, 2, 3]
            declaredArrayNames.append(name)
            continue

        if name not in undeclaredArrayNames:
            undeclaredArrayNames[name] = 1

        if line.find("][") != -1:
            undeclaredArrayNames[name] = 2

    for name in undeclaredArrayNames.keys():
        if name in declaredArrayNames:
            continue

        if undeclaredArrayNames[name] == 1:
            out.append(name + '=[0 for i in range(1000)]')
        else:
            out.append(name + '=[[0 for i in range(1000)] for f in range(1000)]')

    return out


def OPEN(line, indentation):
    # Format of OPEN statement: OPEN filename FOR Read/Write FOR filename
    global index
    index += 4
    temp = line.upper()
    readMode = 'w+' if temp.find('WRITE') != -1 else 'r'
    filename = line.strip().split()[1]

    output = " " * indentation + "with open(" + filename + ",'" + readMode + f"') as {filename}:"

    return output


def WRITEFILE(line, indentation):
    # Format: WRITEFILE filename, <variable>
    filename = line.strip().split()[1].replace(',', '')
    output = " " * indentation + filename + ".write(" + line[line.find(',') + 1:].strip() + ")"

    return output


def READFILE(line, indentation):
    # Format: READFILE filename, <variable>
    filename = line.strip().split()[1].replace(',', '')
    output = " " * indentation + line[line.find(',') + 1:].strip() + f" = {filename}.readline()"

    return output


def CLOSEFILE():
    # Format: CLOSEFILE filename
    global index
    index -= 4


def FUNCTION(line, indentation):
    global index
    index += 4
    line = line[9:]
    c = line.count(':')
    for _ in range(c - 1):
        line = line[:line.find(':')] + line[line.find(','):]
    line = line[:line.find(':')] + line[line.find(')'):line.find(')') + 1]
    output = " " * indentation + "def " + line[:line.find(')') + 1] + ":"
    return output


def ENDFUNCTION():
    global index
    index -= 4


def RETURN(line, indentation):
    output = " " * indentation + "return " + line[6:].strip()
    return output


def CALL(line, indentation):
    output = " " * indentation + line[4:].strip()
    return output


def PROCEDURE(line, indentation):  # Same as FUNCTION
    global index
    index += 4
    line = line[9:]
    c = line.count(':')
    for _ in range(c - 1):
        line = line[:line.find(':')] + line[line.find(','):]
    line = line[:line.find(':')] + line[line.find(')'):line.find(')') + 1]
    output = " " * indentation + "def " + line[:line.find(')') + 1] + ":"
    return output


def ENDPROCEDURE():
    global index
    index -= 4


def convertToPython(lines, output_list):
    global index
    output_list += initialize_lists_list(lines)
    for line in lines:
        if line[:5].upper() == "WHILE":
            output_list.append(WHILE(line, index))
        elif line[:6].upper() == "REPEAT":
            output_list.append(REPEAT(index))
        elif line[:2].upper() == "IF":
            output_list.append(IF(line, index))
        elif line[:5].upper() == "PRINT":
            output_list.append(PRINT(line, index))
        elif line[:5].upper() == "OUTPUT":
            output_list.append(OUTPUT(line, index))
        elif line[:5].upper() == "UNTIL":
            output_list.extend(UNTIL(line, index))
        elif line[:8].upper() == "ENDWHILE":
            ENDWHILE()
        elif line[:3].upper() == "FOR":
            output_list.append(FOR(line, index))
        elif line[:4].upper() == "NEXT":
            NEXT()
        elif line[:5].upper() == "ENDIF":
            ENDIF()
        elif line[:5].upper() == "ELSE":
            output_list.append(ELSE(index))
        elif line[:5].upper() == "INPUT":
            output_list.append(INPUT(line, index))
        elif line[:7].upper() == "DECLARE":
            DECLARE()
        elif line[:2].upper() == "//":
            continue
        elif line[:4].upper() == "OPEN":
            output_list.append(OPEN(line, index))
        elif line[:9].upper() == "WRITEFILE":
            output_list.append(WRITEFILE(line, index))
        elif line[:8].upper() == "READFILE":
            output_list.append(READFILE(line, index))
        elif line[:9].upper() == "CLOSEFILE":
            continue
        elif line[:8].upper() == "FUNCTION":
            output_list.append(FUNCTION(line, index))
        elif line[:11].upper() == "ENDFUNCTION":
            ENDFUNCTION()
        elif line[:6].upper() == "RETURN":
            output_list.append(RETURN(line, index))
        elif line[:4].upper() == "CALL":
            output_list.append(CALL(line, index))
        elif line[:9].upper() == "PROCEDURE":
            output_list.append(PROCEDURE(line, index))
        elif line[:12].upper() == "ENDPROCEDURE":
            ENDPROCEDURE()
        else:
            if "=" in line:
                output_list.append(evaluate(line, index))


def main():
    input_list = []
    path = os.path.dirname(__file__)
    path.replace("\\", "/")
    pseudocode = path + "/input.txt"
    pythonCode = path + "/output.py"

    with open(pseudocode, "r") as file:
        line_List = list(file)

    for i in range(len(line_List)):
        line_List[i] = line_List[i].strip()

    output_list = ["import random", "import math"]

    convertToPython(line_List, output_list)
    output_list.append("input(\"Press enter to exit \")")

    with open(pythonCode, "w") as file:
        for item in output_list:
            file.write("%s\n" % item)

    code_to_execute = compile("\n".join(output_list), "<string>", "exec")
    exec(code_to_execute)


main()
