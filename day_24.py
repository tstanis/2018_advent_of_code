import re
import math
import copy

original_armies = []
armies = []
immune_boost = 0

def reset():
    global armies
    armies = copy.deepcopy(original_armies)
    #print(armies)

with open('day_24.txt', 'r') as fp:
    team = None
    id = 0
    for line in fp:
        if line.startswith("Immune"):
            team = "immune"
        elif line.startswith("Infection"):
            team = "infection"
        else:
            army = {'id': id}
            
            numbers = re.findall(r'-?\d+', line)
            #print(numbers)
            if len(numbers) < 4:
                continue
            id += 1
            army['team'] = team
            army['units'] = int(numbers[0])
            army['hp'] = int(numbers[1])
            army['attack'] = int(numbers[2])
            army['initiative'] = int(numbers[3])
            vulnerable = re.findall(r'\(.*\)', line)
            alltypes = list(map(lambda x: x.lstrip(), vulnerable[0].split(';'))) if vulnerable else []
            #print(alltypes)
            for eachtype in alltypes:
                eachtype.lstrip()
                words = eachtype.split(' ')
                vultype = words[0].replace('(', '').replace(')', '')
                #print(vultype)
                vuls = map(lambda x: x.replace(',', ''), words[2:])
                for vul in vuls:
                    army[vul.replace(')', '')] = vultype
            original_armies.append(army)
            words = line.split()
            for i in range(0, len(words)):
                if words[i] == 'damage':
                    army['attack_type'] = words[i - 1]
                    break

def effective_power(army):
    global immune_boost
    return army['units'] * (army['attack'] + (immune_boost if army['team'] == 'immune' else 0))

def get_dmg(attack, defend):
    if attack['attack_type'] not in defend:
        return effective_power(attack)
    else:
        vul = defend[attack['attack_type']]
        if vul == 'weak':
            return int(2 * effective_power(attack))
        elif vul == 'immune':
            return 0
    return 0

def target():
    targets = {}
    targeting_order = sorted(armies, key=lambda a: (effective_power(a), a['initiative']), reverse=True)
    choosen = set()
    for army in targeting_order:
        def score(x):
            return (get_dmg(army, x), effective_power(x), x['initiative'])
        if army['units'] <= 0:
            continue
        choices = sorted([x for x in armies if x['units'] > 0 and x['id'] != army['id'] and x['team'] != army['team'] and x['id'] not in choosen], 
            key=score, reverse=True)
        if len(choices) > 0 and get_dmg(army, choices[0]) > 0:
            #print(str(army['id']) + " power: " + str(effective_power(army)) + " Choices: " + str(choices))
            #print("Choices: " + str(list(map(score, choices))))
            targets[army['id']] = choices[0]['id']
            choosen.add(choices[0]['id'])
        # else:
        #     print("No targets for " + str(army['id']))
    return targets

def find_army_by_id(id):
    for army in armies:
        if army['id'] == id:
            return army
    return None

def take_damage(army, dmg):
    units_dead = min(army['units'], int(int(dmg) / int(army['hp'])))
    #print("Army " + str(army['id']) + " loses " + str(units_dead))
    army['units'] -= units_dead

def attack(targets):
    attacking_order = sorted(armies, key=lambda army: army['initiative'], reverse=True)
    #print(attacking_order)
    for attacker in attacking_order:
        if attacker['units'] <= 0:
            continue
        if attacker['id'] not in targets:
            continue
        target = find_army_by_id(targets[attacker['id']])
        dmg = get_dmg(attacker, target)
        #print("Army " + str(attacker['id']) + " attacks " + str(target['id']) + " for " + str(dmg))
        take_damage(target, dmg)

def army_summary(army):
    print("Army " + str(army['id']) + " team " + army['team'] + " has " + str(army['units']) + " units")

def battle_over():
    num_immune = 0
    num_infect = 0
    for army in armies:
        if army['team'] == 'immune' and army['units'] > 0:
            num_immune += 1
        elif army['units'] > 0:
            num_infect += 1
    #print((num_immune, num_infect))
    if num_immune == 0:
        return 'infect'
    elif num_infect == 0:
        return 'immune'
    else:
        return None



winner = "infect"
immune_boost = 37
while winner == "infect":
    reset()
    print(armies)
    # for army in armies:
    #     if army['units'] > 0:
    #         army_summary(army)
    immune_boost += 1
    while not battle_over():
        targets = target()
        #print(targets)
        attack(targets)
        # for army in armies:
        #     if army['units'] > 0:
        #         army_summary(army)
    winner = battle_over()
    for army in armies:
        if army['units'] > 0:
            army_summary(army)
    print(winner + " wins with immune_boost " + str(immune_boost))

print("SUM: " + str(sum(map(lambda a: a['units'], filter(lambda a: a['units'] > 0, armies)))))
            
                    