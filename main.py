import sys
import os

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

keywords = ["print", "math"]

def lexline(line: str):
    line = line.split("(")
    line = [i.replace(")", "") for i in line]
    for i in range(len(line)):
        if line[i] in keywords:
            pass
        elif "//" in line[i]:
            line[i] = line[i].replace("//", "")
            line[i] = "#" + line[i]
        elif line[i].isnumeric():
            line[i] = "int(" + line[i] + ")"
        elif isinstance(line[i], str):
            line[i] = "str(" + line[i] + ")"
        else:
            print("Syntax error has occured.")
    return line

def parseline(line: list):
    # if indexexists(line, 1):
    #     #if "STRING:" in line[1]:
    #     #    line = line[1].replace("STRING:", "")
    #     #elif "INT:" in line[1]:
    #     #    line = line[1].replace("INT:", "")
    #     #else:
    #     #    print("Parser error")
    #     pass
    # else:
    #     print("Indexing error")
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
        #print(line)
        with open(basename, "a") as out:
            if "#" in line[0]:
                out.write(line[0] + "\n")
            elif line[0] == "print":
                if line[1].isnumeric():
                    out.write("print(%d)\n" % line[1])
                else:
                    out.write("print(%s)\n" % line[1])
            elif line[0] == "math":
                out.write("# Math is not implemented")
            elif "" in line[0]:
                out.write("\n")
            
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
