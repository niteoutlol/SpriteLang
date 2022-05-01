import sys
import subprocess
import shlex
import os

op_counter = 0
def opcount(reset = False):
    global op_counter
    if reset:
        op_counter = 0
    result = op_counter
    op_counter += 1
    return result

PUSH_OP = opcount(True)
TEST_OP = opcount()
PRINT_OP = opcount()
OPERATIONS = opcount()

INDENTS = 0

def indent():
    result = ""
    for i in range(INDENTS):
        result += "    "
    return result

def push(x):
    return (PUSH_OP, x)

def compile(program, outpath):
    basename = os.path.basename(program_path)
    if basename.endswith(".sprite"):
        basename = basename[:-len(".sprite")]
        basename += ".py"
    with open(basename, "w") as outfile:
        outfile.write("stack = []\n\n")
        for ip in range(len(program)):
            op = program[ip]
            assert OPERATIONS == 3, "Exhaustive handling of ops in compilation."
            if op[0] == PUSH_OP:
                outfile.write(indent() + "stack.append(%s)\n" % op[1])
                ip += 1
            elif op[0] == TEST_OP:
                outfile.write(indent() + "print(\"This is a test operation\")\n")
                ip += 1
            elif op[0] == PRINT_OP:
                outfile.write(indent() + "a = stack.pop()\n")
                outfile.write(indent() + "print(a)\n")
                ip += 1
            else:
                assert False, "Unreachable"

def parse(token):
    (filepath, row, col, word) = token
    assert OPERATIONS == 3, "Exhaustive operation handling in the parser."
    if word == "test":
        return (TEST_OP, )
    elif word == "print":
        return (PRINT_OP, )
    else:
        try:
            if "\"" in word:
                word.replace("\"", "")
                if "\"" in word:
                    word.replace("\"", "")
                    return push(word)
            else:
                return push(int(word))
        except ValueError as err:
            print("%s:%d:%d: %s" % (filepath, row, col, err))
            exit(1)

def crossreference_blocks(program):
    return program

def find_col(line, start, predicate):
    while start < len(line) and not predicate(line[start]):
        start += 1
    return start

def lexfile(file_path):
    with open(file_path, "r") as f:
        for (row, line) in enumerate(f.readlines()):
            for (col, token) in lexline(line):
                yield (file_path, row, col, token)

def lexline(line):
    col = find_col(line, 0, lambda x: not x.isspace())
    while col < len(line):
        col_end = find_col(line, col, lambda x: x.isspace())
        if line[col] == '"':
            col_end = find_col(line, col+1, lambda x: x == '"')
            # TODO: report unclosed string literals as proper compiler errors instead of python asserts
            assert line[col_end] == '"'
            text_of_token = line[col+1:col_end]
            # TODO: converted text_of_token to bytes and back just to unescape things is kinda sus ngl
            # Let's try to do something about that, for instance, open the file with "rb" in lex_file()
            yield (col, 1, bytes(text_of_token, "utf-8").decode("unicode_escape"))
            col = find_col(line, col_end+1, lambda x: not x.isspace())
        else:
            col_end = find_col(line, col, lambda x: x.isspace())
            text_of_token = line[col:col_end]
            try:
                yield (col, 1, int(text_of_token))
            except ValueError:
                yield (col, 0, text_of_token)
            col = find_col(line, col_end, lambda x: not x.isspace())

def loadprogram(filepath):
    return crossreference_blocks([parse(token) for token in lexfile(filepath)])

if __name__ == "__main__":
    argv = sys.argv
    assert len(argv) >= 1
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
        compile(program, program_path)
    else:
        exit(1)