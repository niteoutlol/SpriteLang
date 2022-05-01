import sys
import os

op_counter = 0
def opcount(reset = False):
    global op_counter
    if reset:
        op_counter = 0
    result = op_counter
    op_counter += 1
    return result

TEST_OP = opcount()
OPERATIONS = opcount()

INDENTS = 0

def indent():
    result = ""
    for i in range(INDENTS):
        result += "    "
    return result

def loadprogram(filepath):
    program = open(filepath, 'r').read()
    #program += "<EOF>"
    return program

keywords = ["print"]

def lexline(line: str):
    line = line.split("(")
    line = [i.replace(")", "") for i in line]
    for i in range(len(line)):
        print(line[i])
        if line[i].startswith("//"):
            del line[i]
            pass
        elif line[i] in keywords:
            pass
        elif line[i].isnumeric():
            line[i] = "INT:" + line[i]
        elif isinstance(line[i], str):
            line[i] = "STRING:" + line[i]
        else:
            print("Syntax error has occured.")
            return line
    return line

def parseline(line: list):
    #for i in range(len(line)):
    #    ln = line[i]
    #    if ln == "print":
    return line

def indexexists(list, index):
    return (index < len(list))

def compileprogram(program, programpath):
    program = program.split("\n")
    for i in range(len(program)):
        line = lexline(program[i])
        line = parseline(line)
        print(line)
        basename = os.path.basename(programpath)
        if basename.endswith(".sprite"):
            basename = basename[:-len(".sprite")]
            basename += ".py"
        with open(basename, "w") as out:
            if line[0] == "print":
                value = ""
                if indexexists(line, 1):
                    if "STRING:" in line[1]:
                        value = line[1].replace("STRING:", "")
                    elif "INT:" in line[1]:
                        value = line[1].replace("INT:", "")
                    else:
                        print("Parser error")
                print(value)
                if line[i].isnumeric():
                    out.write("print(%d)\n" % value)
                else:
                    out.write("print(%s)\n" % value)

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
        print("[INFO] Generating %s" % (basename + ".py"))
        compileprogram(program, program_path)
    else:
        exit(1)