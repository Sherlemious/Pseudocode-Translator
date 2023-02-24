from config import *
def add_error(error_name, errors, line_no="NA"):
    error_no = len(errors)
    meta = f"Error #{str(error_no)} on line #{str(line_no)}:"
    errors[meta] = error_name
    return errors

def detect_errors(lines):
    errors = {}

    for l in range(len(lines)):
        line = lines[l]
        line = line.upper()
        if line[-1] in operators:
            add_error("Missing Variable/Number", l)

        for ch in range(len(line)):
            if line[ch] == ',':
                try:
                    if line[ch - 1] != " ":
                        line = line[:ch] + " " + line[ch:]
                    if line[ch + 1] != " ":
                        line = line[:ch + 1] + " " + line[ch + 1:]
                except IndexError:
                    if ch == 0:
                        add_error("Comma in the beginning of line", ch)
                    else:
                        add_error("Comma in the end of line", ch)

    op_counts = {
        "WHILE": sum('WHILE' in s for s in lines),
        "FOR": sum('FOR' in s for s in lines),
        "REPEAT": sum('REPEAT' in s for s in lines),
        "IF": sum('IF' in s for s in lines),
    }
    Closers_counts = {
        "ENDWHILE": sum('ENDWHILE' in s for s in lines),
        "NEXT": sum('NEXT' in s for s in lines),
        "UNTIL": sum('UNTIL' in s for s in lines),
        "ENDIF": sum('ENDIF' in s for s in lines),
    }

    if op_counts['WHILE'] > Closers_counts["ENDWHILE"]:
        errors = add_error("Unclosed WHILE Loop", errors)
    if op_counts['REPEAT'] > Closers_counts["UNTIL"]:
        errors = add_error("Unclosed REPEAT Loop", errors)
    if op_counts['IF'] > Closers_counts["ENDIF"]:
        errors = add_error("Unclosed IF statement", errors)
    if op_counts['FOR'] > Closers_counts["NEXT"]:
        errors = add_error("Unclosed FOR Loop", errors)

    return errors

def getErrors(lines):
    return detect_errors(lines)
