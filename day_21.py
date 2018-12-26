import re

program = []
inst_reg = -1

with open('day_21.txt', 'r') as fp:
    for line in fp:
        opcode = line.split()[0]
        args = list(map(int, re.findall(r'\d+', line)))
        if opcode == '#ip':
            inst_reg = args[0]
        else:
            program.append((opcode, args))

def execute_reg_ins(reg, operands, ins):
    reg[operands[2]] = ins(reg[operands[0]], reg[operands[1]])

def execute_value_ins(reg, operands, ins):
    reg[operands[2]] = ins(reg[operands[0]], operands[1])

def execute_compare_ir_ins(reg, operands, ins):
    reg[operands[2]] = ins(operands[0], reg[operands[1]])

def execute_compare_ri_ins(reg, operands, ins):
    execute_value_ins(reg, operands, ins)

def execute_compare_rr_ins(reg, operands, ins):
    execute_reg_ins(reg, operands, ins)

def seti(reg, operands):
    reg[operands[2]] = operands[0]

def setr(reg, operands):
    reg[operands[2]] = reg[operands[0]]

def add(a, b):
    return a + b

def mul(a, b):
    return a * b

def ban(a, b):
    return a & b

def bor(a, b):
    return a | b

def gt(a, b):
    return 1 if a > b else 0

def eq(a, b):
    return 1 if a == b else 0

inst_map = {
    "seti" : seti,
    "setr" : setr,
    "addi" : lambda a, b: execute_value_ins(a, b, add),
    "muli" : lambda a, b: execute_value_ins(a, b, mul),
    "bani" : lambda a, b: execute_value_ins(a, b, ban),
    "bori" : lambda a, b: execute_value_ins(a, b, bor),
    "addr" : lambda a, b: execute_reg_ins(a, b, add),
    "mulr" : lambda a, b: execute_reg_ins(a, b, mul),
    "banr" : lambda a, b: execute_reg_ins(a, b, ban),
    "borr" : lambda a, b: execute_reg_ins(a, b, bor),
    "gtir" : lambda a, b: execute_compare_ir_ins(a, b, gt),
    "gtri" : lambda a, b: execute_compare_ri_ins(a, b, gt),
    "gtrr" : lambda a, b: execute_compare_rr_ins(a, b, gt),
    "eqir" : lambda a, b: execute_compare_ir_ins(a, b, eq),
    "eqri" : lambda a, b: execute_compare_ri_ins(a, b, eq),
    "eqrr" : lambda a, b: execute_compare_rr_ins(a, b, eq)
}
num_ins = 0
unique_ends = set()
def run_program(program, control_start):
    global num_ins
    regs = [control_start, 0, 0, 0, 0, 0]
    inst_ptr = 0
    opcode = []
    args = []
    num_ins = 0
    while inst_ptr < len(program):
        if inst_reg >= 0:
            regs[inst_reg] = inst_ptr
        
        inst = program[inst_ptr]
        opcode = inst[0]
        args = inst[1]
        #before = regs.copy()
  
        inst_map[opcode](regs, args)

        if inst_ptr == 30:
            if regs[4] in unique_ends:
                print("Duplicate! ")
            else:
                unique_ends.add(regs[4])
            print(str(num_ins + 1) + " pc: " + str(inst_ptr) +  " " + str(opcode) + " " + str(args) + " " + str(list(map(str, regs))))
        if inst_reg >= 0:
            inst_ptr = regs[inst_reg]
        inst_ptr += 1
        num_ins += 1
    return regs 

print(program)

starts = [0]
for start in starts:
    num_ins = 0
    regs = run_program(program, start)
    print(regs)
    print("Finished: " + str(start) + " in " + str(num_ins))