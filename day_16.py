import re

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

def could_be_reg_ins(before_reg, after_reg, operands, ins):
    return after_reg[operands[2]] == ins(before_reg[operands[0]], before_reg[operands[1]])

def could_be_value_ins(before_reg, after_reg, operands, ins):
    return after_reg[operands[2]] == ins(before_reg[operands[0]], operands[1])

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

def could_be_compare_ir(before_reg, after_reg, operands, ins):
    return after_reg[operands[2]] == ins(operands[0], before_reg[operands[1]])

def could_be_compare_ri(before_reg, after_reg, operands, ins):
    return could_be_value_ins(before_reg, after_reg, operands, ins)

def could_be_compare_rr(before_reg, after_reg, operands, ins):
    return could_be_reg_ins(before_reg, after_reg, operands, ins)

simple_operations = [(add, "add"), (mul, "mul"), (ban, "ban"), (bor, "bor")]
compare_operations = [(gt, "gt"), (eq, "eq")]

observations = []
test_program = []

in_before = False
with open('day_16.txt', 'r') as fp:
    before = None
    instruction = None
    after = None
    for line in fp:
        if line.startswith("Before:"):
            before = list(map(int, re.findall(r'\d+', line)))
            in_before = True
        elif line.startswith("After:"):
            after = list(map(int, re.findall(r'\d+', line)))
            observations.append((before, after, instruction))
            in_before = False
        else:
            parts = list(map(int, re.findall(r'\d+', line)))
            if len(parts) == 4:
                instruction = parts
                if not in_before:
                    test_program.append(instruction)

print(len(observations))
print(len(test_program))
observation_choices = []
opcode_meaning = {}

for observation in observations:
    num_could_be = 0
    before_reg = observation[0]
    after_reg = observation[1]
    opcode = observation[2][0]
    operands = observation[2][1:]
    could_be = set()
    if after_reg[operands[2]] == operands[0]:
        could_be.add("seti")
    if after_reg[operands[2]] == before_reg[operands[0]]:
        could_be.add("setr")
    for ops in simple_operations:
        if could_be_reg_ins(before_reg, after_reg, operands, ops[0]):
            could_be.add(ops[1] + "r")
        if could_be_value_ins(before_reg, after_reg, operands, ops[0]):
            could_be.add(ops[1] + "i")
    for ops in compare_operations:
        if could_be_compare_ir(before_reg, after_reg, operands, ops[0]):
            could_be.add(ops[1] + "ir")
        if could_be_compare_ri(before_reg, after_reg, operands, ops[0]):
            could_be.add(ops[1] + "ri")
        if could_be_compare_rr(before_reg, after_reg, operands, ops[0]):
            could_be.add(ops[1] + "rr")
    observation_choices.append(len(could_be))

    if opcode in opcode_meaning:
        opcode_meaning[opcode] = opcode_meaning[opcode] & could_be
    else:
        opcode_meaning[opcode] = could_be

print("More Than 3: " + str(len(list(filter(lambda x: x >= 3, observation_choices)))))
print(opcode_meaning)

while len(list(filter(lambda x: len(x) > 1, opcode_meaning.values()))) > 0:
    for opcode, meaning in opcode_meaning.items():
        if len(meaning) == 1:
            the_meaning = list(meaning)[0]
            print("Truth: " + str(opcode) + " means " + the_meaning)
            # for sure we know this one
            for other_opcode, other_meaning in opcode_meaning.items():
                if opcode != other_opcode:
                    if the_meaning in other_meaning:
                        other_meaning.remove(the_meaning)
    print(opcode_meaning)
            
reg = [0, 0, 0, 0]
for ins in test_program:
    ins_name = list(opcode_meaning[ins[0]])[0]
    operands = ins[1:]
    run = False
    print("Run: " + str(ins_name) + " " + str(operands))
    for op in simple_operations:
        if ins_name.startswith(op[1]):
            if ins_name.endswith('r'):
                execute_reg_ins(reg, operands, op[0])
            else:
                execute_value_ins(reg, operands, op[0])
            run = True
    if not run:
        for op in compare_operations:
            if ins_name.startswith(op[1]):
                if ins_name.endswith('ir'):
                    execute_compare_ir_ins(reg, operands, op[0])
                elif ins_name.endswith('ri'):
                    execute_compare_ri_ins(reg, operands, op[0])
                else:
                    execute_compare_rr_ins(reg, operands, op[0])
                run = True
    if not run:
        if ins_name == "seti":
            reg[operands[2]] = operands[0]
        elif ins_name == "setr":
            reg[operands[2]] = reg[operands[0]]
        else:
            print("FAIL!")
    print("Result: " + str(reg))



