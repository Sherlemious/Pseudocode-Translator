import os

index = 0

equality = [">", "<", "="]

def condition(statement):
    statement.replace('MOD', '%').replace('DIV', '//').replace('<>', '!=')
    statement.replace('OR', 'or').replace('AND', 'and').replace('NOT', 'not')
    eq = statement.find('=')

    x = len(statement)
    for ch in range(x):
        char = statement[ch]
        if char == "=":
            if statement[ch-1] not in equality and statement[ch+1] not in equality:
                statement = statement[:ch] + "=" + statement[ch:]

    return statement


def evaluation(statement):
    statement.replace('MOD', '%').replace('DIV', '//').replace('OR', 'or').replace('AND', 'and').replace('NOT', 'not')
    return statement


def evaluate(line, indentation=0):
    if line.upper().find("USERINPUT") == -1:
        return " " * indentation + evaluation(line)
    else:
        line.split()
        return " " * indentation + line[0] + " = " + "input()"


def PRINT(line, indentation=0):
    line = line[5:]
    output = " " * indentation + "print(" + line + ")"

    return output


def INPUT(line, indentation=0):
    lst = line.upper().strip().split()
    if "," not in lst:
        output = " " * indentation + line[line.find("INPUT")+6:].strip() + " = " + "input()"

    return output


def WHILE(line, indentation=0):
    global index
    index += 4
    line = line[5:]
    if line.find("DO") != -1:
        line = line[:line.find("DO")]
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
    if line.find("THEN") != -1:
        line = line[:line.find("THEN")]
    index += 4
    line = line[2:]
    output = " " * indentation + "if" + condition(line) + ":"
    return output


def FOR(line, indentation):
    global index
    index += 4
    line = line[3:]
    line.strip()
    variable = line[:line.find('=')]
    start = line[line.find('=') + 1:line.find('TO')].strip()
    end = line[line.find('TO') + 2:].strip()
    output = " " * indentation + "for " + variable + " in range(" + start + end + "):"

    return output


def NEXT():
    global index
    index -= 4


def ENDIF():
    global index
    index -= 4


def ELSE(indentation):
    global index
    return " " * (indentation - 4) + "else:"


input_list = []
output_list = []


def Main(lines):
    global index, output_list
    for line in lines:
        if line[:5] == "WHILE":
            output_list.append(WHILE(line, index))
        else:
            if line[:6] == "REPEAT":
                output_list.append(REPEAT(index))
            else:
                if line[:2] == "IF":
                    output_list.append(IF(line, index))
                else:
                    if line[:5] == "PRINT":
                        output_list.append(PRINT(line, index))
                    else:
                        if line[:5] == "UNTIL":
                            output_list.extend(UNTIL(line, index))
                        else:
                            if line[:8] == "ENDWHILE":
                                ENDWHILE()
                            else:
                                if line[:3] == "FOR":
                                    output_list.append(FOR(line, index))
                                else:
                                    if line[:4] == "NEXT":
                                        NEXT()
                                    else:
                                        if line[:5] == "ENDIF":
                                            ENDIF()
                                        else:
                                            if line[:5] == "ELSE":
                                                output_list.append(ELSE(index))
                                            else:
                                                if line[:5] == "INPUT":
                                                    output_list.append(INPUT(line, index))
                                                else:
                                                    if "=" in line:
                                                        output_list.append(evaluate(line, index))


path = os.path.dirname(__file__)
path.replace("\\", "/")
pseudocode = path + "/input.txt"
python = path + "/output.txt"

Main(input_list)

with open(pseudocode, "r") as file:
    line_List = list(file)

for i in range(len(line_List)):
    line_List[i] = line_List[i].strip()

Main(line_List)

with open(python, "w") as file:
    for item in output_list:
        file.write("%s\n" % item)
