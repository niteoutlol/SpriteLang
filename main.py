import sys
import os
from tkinter import E

INDENTS = 0
VARS = []

def indent():
    result = ""
    for _ in range(INDENTS):
        result += "    "
    return result

def isfloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def loadprogram(filepath):
    program = open(filepath, 'r').read()
    return program

keywords = ["make"]
functions = ["print"]

def typecheck(string):
    if string.startswith(" "):
        string = string.replace(" ", "", 1)
    if "+" in string or "-" in string or "/" in string or "//" in string or "*" in string:
        return string
    elif string.isnumeric():
        return "int(" + string + ")"
    elif isfloat(string):
        return "float(" + string + ")"
    elif isinstance(string, str):
        if "\"" and "\"" in string:
            return "str(" + string + ")"
        else:
            if string in VARS:
                return string
            else:
                print("Invalid type has been found.")
                exit()
    else:
        print("Something very weird has just occured and i have no idea how you did that.")

def mathreplace(string):
    string = string.split()
    string = f"str({string[0]} {string[1]} {string[2]})"
    return string

def lexline(line: str):
    line = line.split("(")
    line = [i.replace(")", "") for i in line]
    line = [i.replace(";", "") for i in line]
    for i in range(len(line)):
        if "//" in line[i]:
            return line
        if "+" in line[0] or "-" in line[0] or "/" in line[0] or "//" in line[0] or "*" in line[0]:
            line = line[i].split("=")
            line[1] = mathreplace(line[1])
            line[0] = f"{line[0]}= {line[1]}"
            del line[1]
            return line
        if "make " in line[i]:
            return line
        elif line[i] in functions or line[i] in keywords:
            return line
        elif line[i] == "":
            return line
        else:
            line[i] = typecheck(line[i])
    return line

def parseline(line: list):
    if "//" in line[0]:
        line = line[0].replace("//", "#")
        line += "\n"
        line = str(line)
        return line
    if "+" in line[0] or "-" in line[0] or "/" in line[0] or "//" in line[0] or "*" in line[0]:
        pass
    if "make " in line[0]:
        line = line[0].replace("make ", "")
        line = line.split("=")
        line[len(line) - 1] = typecheck(line[len(line) - 1])
        line[0] = line[0].replace(" ", "")
        if not line[0] in VARS:
            VARS.append(line[0])
        line[0] += " ="
        line += "\n"
        line = " ".join(line)
    elif line[0] == "print":
        line = "print(%s)\n" % line[1]
    elif "" in line[0]:
        line = ("\n")
    else:
        print("Something very weird has just occured and i have no idea how you did that.")
        exit()
    line = str(line)
    return line

def indexexists(list, index):
    return (index < len(list))

def compileprogram(program, programpath):
    program = program.split("\n")
    basename = os.path.basename(programpath)
    if basename.endswith(".sprite"):
        basename = basename[:-len(".sprite")]
        basename += ".py"
    with open(basename, "w") as out:
        out.write("")
    for i in range(len(program)):
        line = lexline(program[i])
        line = parseline(line)
        with open(basename, "a") as out:
            out.write(line)
            
if __name__ == "__main__":
    argv = sys.argv
    assert len(argv)  >= 1
    compiler_name, *argv = argv
    if len(argv) < 2:
        print("ERROR: No subcommand provided.")
        exit(1)
    subcommand, *argv = argv

    if subcommand == "com":
        # TODO: -r flag for the com that runs the application upon successfull compilation
        if len(argv) < 1:
            print("ERROR: No input file is provided for the compilation")
            exit(1)
        program_path, *argv = argv
        program = loadprogram(program_path)
        ext = ".sprite"
        basename = os.path.basename(program_path)
        if basename.endswith(ext):
            basename = basename[:-len(ext)]
        print("[COM] Compiling %s" % (basename + ".py"))
        compileprogram(program, program_path)
        print("[COM] Compiled %s" % (basename + ".py"))
        print("[RUN] Executing %s\n" % (basename + ".py"))
        exec(open(basename + ".py").read())
    else:
        exit(1)
