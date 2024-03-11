import csv
import sys 
from collections import defaultdict

def ask_question(question):
    while True:
        answer = input(question + " (yes/no): ").lower()
        if answer == 'yes' or answer == 'no':
            return True if answer == "yes" else False
        else:
            print("Please answer with 'yes' or 'no'.")

# Pokemon class that stores all information about one pokemon as an object 
class Pokemon:
    def __init__(self,
                 name,
                 generation,
                 national_pokedex_number,
                 type_one,
                 type_two,
                 height,
                 weight,
                 hp,
                 attack,
                 defense,
                 special_attack,
                 special_defense,
                 speed,
                 number_abilities,
                 is_legendary,
                 is_mythical, 
                 has_mega,
                 has_gigantamax,
                 has_evolved,
                 can_evolve,
                 resistance_map):
        self.name = name
        self.generation = generation
        self.national_pokedex_number = national_pokedex_number
        self.type_one = type_one
        self.type_two = type_two
        self.height = height
        self.weight = weight
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed
        self.base_stat_total = hp + attack + defense + special_attack + special_defense + speed
        self.number_abilities = number_abilities
        self.is_legendary = is_legendary
        self.is_mythical = is_mythical
        self.has_mega = has_mega
        self.has_gigantamax = has_gigantamax
        self.has_evolved = has_evolved
        self.can_evolve = can_evolve
        self.resistance_map = resistance_map

    def print_list(self):
        attributes = [
            self.name,
            self.generation,
            self.national_pokedex_number,
            self.type_one,
            self.type_two,
            self.height,
            self.weight,
            self.hp,
            self.attack,
            self.defense,
            self.special_attack,
            self.special_defense,
            self.speed,
            self.base_stat_total,
            self.number_abilities,
            self.is_legendary,
            self.is_mythical,
            self.has_mega,
            self.has_gigantamax,
            self.has_evolved,
            self.can_evolve,
            self.resistance_map
        ]

        print(attributes) 

    def print_json(self):
        attributes = {
            "name": self.name,
            "generation": self.generation,
            "national_pokedex_number": self.national_pokedex_number,
            "type_one": self.type_one,
            "type_two": self.type_two,
            "height": self.height,
            "weight": self.weight,
            "hp": self.hp,
            "attack": self.attack,
            "defense": self.defense,
            "special_attack": self.special_attack,
            "special_defense": self.special_defense,
            "speed": self.speed,
            "base_stat_total": self.base_stat_total,
            "number_abilities": self.number_abilities,
            "is_legendary": self.is_legendary,
            "is_mythical": self.is_mythical,
            "has_mega": self.has_mega,
            "has_gigantamax": self.has_gigantamax,
            "has_evolved": self.has_evolved,
            "can_evolve": self.can_evolve,
            "resistance_map": self.resistance_map,  # Add resistance_map attribute
        }

        print("{")
        for key, value in attributes.items():
            if isinstance(value, dict):
                value_str = ', '.join([f'"{k}": {v}' for k, v in value.items()])
                print(f'  "{key}": {{ {value_str} }},')
            else:
                print(f'  "{key}": "{value}",')
        print("}")


# Methods to create and modify KB

# generates the pokemon KB and returns a list of pokemon facts       
def generate_KB():
    # returns integer of the number represented by the roman numeral 
    def get_number_from_roman(roman_numeral):
        if roman_numeral == "I":
            return 1
        elif roman_numeral == "II":
            return 2
        elif roman_numeral == "III":
            return 3
        elif roman_numeral == "IV":
            return 4
        elif roman_numeral == "V":
            return 5
        elif roman_numeral == "VI":
            return 6
        elif roman_numeral == "VII":
            return 7
        elif roman_numeral == "VIII":
            return 8
        else:
            return None  # Return None for unsupported Roman numerals

    def get_num_abilities(entry): 
        total_num = 0
        for i in range(19, 23):
            if len(entry[i]) > 0: 
                total_num += 1
        return total_num

    def get_evolution_info(pokemon_name, entry):
        has_evolved = False
        can_evolve = False
        evolution_chain = entry[44:51]
        if evolution_chain[0] == "Egg":
            evolution_chain.pop(0)
            evolution_chain.pop(0)
        if pokemon_name not in evolution_chain or evolution_chain.index(pokemon_name) != 0: 
            has_evolved = True
        if pokemon_name in evolution_chain: 
            evolution_index = evolution_chain.index(pokemon_name)
            if evolution_index != len(evolution_chain) -1 and  pokemon_name in evolution_chain and len(evolution_chain[evolution_index + 1]) > 0:
                can_evolve = True
        return has_evolved, can_evolve
    
    def create_resistance_map(entry): 
        type_resistance_map = {}
        type_resistance_map['normal'] = float(entry[23])
        type_resistance_map['fire'] = float(entry[24])
        type_resistance_map['water'] = float(entry[25])
        type_resistance_map['electric'] = float(entry[26])
        type_resistance_map['grass'] = float(entry[27])
        type_resistance_map['ice'] = float(entry[28])
        type_resistance_map['fighting'] = float(entry[29])
        type_resistance_map['poison'] = float(entry[30])
        type_resistance_map['ground'] = float(entry[31])
        type_resistance_map['flying'] = float(entry[32])
        type_resistance_map['psychic'] = float(entry[33])
        type_resistance_map['bug'] = float(entry[34])
        type_resistance_map['rock'] = float(entry[35])
        type_resistance_map['ghost'] = float(entry[36])
        type_resistance_map['dragon'] = float(entry[37])
        type_resistance_map['dark'] = float(entry[38])
        type_resistance_map['steel'] = float(entry[39])
        type_resistance_map['fairy'] = float(entry[40])
        return type_resistance_map

    KB = [] # list of Pokemon Objects 
    with open('pokemon_data.csv', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t') # tab seperated, not comma seperated
        next(csv_reader, None) # skiping header 
        for entry in csv_reader: 
            # parse each pokemon entry into a Pokemon Object 
            name = entry[2]
            generation = get_number_from_roman(entry[1])
            national_pokedex_number = int(entry[0])
            type_one = entry[4] if len(entry[4]) > 0 else None 
            type_two = entry[5] if len(entry[5]) > 0 else None 
            height = float(entry[9])
            weight = float(entry[10])
            hp = int(entry[13])
            attack = int(entry[14])
            defense = int(entry[15])
            special_attack = int(entry[16])
            special_defense = int(entry[17])
            speed = int(entry[18])
            number_abilities = get_num_abilities(entry)
            is_legendary = True if int(entry[42]) == 1 else False
            is_mythical = True if int(entry[43]) == 1 else False
            has_mega = True if len(entry[52]) > 0 else False
            has_gigantamax = True if len(entry[51]) > 0 else False
            has_evolved, can_evolve = get_evolution_info(name, entry)
            resistance_map = create_resistance_map(entry)

            newPokemonFact = Pokemon(
                name, 
                generation,
                national_pokedex_number, 
                type_one,
                type_two, 
                height,
                weight, 
                hp, 
                attack,
                defense,
                special_attack,
                special_defense, 
                speed, 
                number_abilities,
                is_legendary,
                is_mythical, 
                has_mega, 
                has_gigantamax, 
                has_evolved,
                can_evolve,
                resistance_map
            )
            KB.append(newPokemonFact)

    return KB

# will filter the KB based on the provided query("attribute_name:operator:value")
# an example would be "type_one:=:grass"
def filter_KB(query, KB): 
    query_parts = query.split(":")
    if len(query_parts) != 3:
        print("Incorrect Query format")
        exit 

    # prepare value of the query 
    if query_parts[2] == "True":
        query_parts[2] = True
    elif query_parts[2] == "False":
        query_parts[2] = False
    elif query_parts[2].isnumeric():
        query_parts[2] = int(query_parts[2])
    elif query_parts[2].replace(".", "").isdigit():
        query_parts[2] = float(query_parts[2])

    if query_parts[0] == "type": # exception, this checks for both type_one and type_two
        if query_parts[1] == "=":
            return list(filter(lambda pokemon: getattr(pokemon, 'type_one') == query_parts[2] or getattr(pokemon, 'type_two') == query_parts[2], KB))
        else:
            return list(filter(lambda pokemon: getattr(pokemon, 'type_one') != query_parts[2] and getattr(pokemon, 'type_two') != query_parts[2], KB))
    elif query_parts[0] == "resist_type":
        if query_parts[1] == "=":
            return list(filter(lambda pokemon: (getattr(pokemon, 'resistance_map'))[query_parts[2]] < 1.0, KB))
        else: 
            return list(filter(lambda pokemon: (getattr(pokemon, 'resistance_map'))[query_parts[2]] >= 1.0, KB))
    elif query_parts[0] == "weak_type":
        if query_parts[1] == "=":
            return list(filter(lambda pokemon: (getattr(pokemon, 'resistance_map'))[query_parts[2]] > 1.0, KB))
        else: 
            return list(filter(lambda pokemon: (getattr(pokemon, 'resistance_map'))[query_parts[2]] <= 1.0, KB))
    elif query_parts[0] == "has_dual_type":
        if query_parts[2] == True: 
            return list(filter(lambda pokemon: getattr(pokemon, 'type_one') != None and getattr(pokemon, 'type_two') != None, KB))
        else:
            return list(filter(lambda pokemon: getattr(pokemon, 'type_one') != None and getattr(pokemon, 'type_two') == None, KB))
    elif query_parts[1] == "=":
        return list(filter(lambda pokemon: getattr(pokemon, query_parts[0]) == query_parts[2], KB))
    elif query_parts[1] == "!=":
        return list(filter(lambda pokemon: getattr(pokemon, query_parts[0]) != query_parts[2], KB))
    elif query_parts[1] == ">":
        return list(filter(lambda pokemon: getattr(pokemon, query_parts[0]) > query_parts[2], KB))
    elif query_parts[1] == "<":
        return list(filter(lambda pokemon: getattr(pokemon, query_parts[0]) < query_parts[2], KB))
    elif query_parts[1] == ">=":
        return list(filter(lambda pokemon: getattr(pokemon, query_parts[0]) >= query_parts[2], KB))
    elif query_parts[1] == "<=":
        return list(filter(lambda pokemon: getattr(pokemon, query_parts[0]) <= query_parts[2], KB))

# only works for attributes with numeric type: int or float 
def get_average(atttribute, KB):
    total = 0
    for entry in KB: 
        total += getattr(entry, atttribute)
    return total/len(KB)

def get_KB_type_matchup(KB):
    number_pokemon_weak = defaultdict(int)
    number_pokemon_resist = defaultdict(int)
    number_type = defaultdict(int)
    for entry in KB: 
        number_type[entry.type_one] += 1
        if entry.type_two is not None: 
            number_type[entry.type_two] += 1
        
        for key, value in entry.resistance_map.items():
            if value < 1.0:
                number_pokemon_resist[key] += 1
            elif value > 1.0: 
                number_pokemon_weak[key] += 1
    return number_pokemon_weak, number_pokemon_resist, number_type

def print_KB(KB, mode):
    for entry in KB:
        if mode == 0:
            entry.print_list()
        else:
            entry.print_json()

def check_solution(KB):
    if len(KB) == 1: 
        print("The Pokemon you guessed was " + KB[0].name)
        sys.exit()

# main method, runs the game 
def main():
    KB = generate_KB()
    print("Welcome to the Pokinator: Pokemon identification program!")
    print("Currently", len(KB), "in the knowledge base")

    # dual type or not 
    has_multiple_types = ask_question("Does the pokemon have more than one type?")
    KB = filter_KB("has_dual_type:=:" + str(has_multiple_types), KB)

    # generations 
    possible_generations = [1,2,3,4,5,6,7,8]
    while len(possible_generations) != 1: 
        in_generation = None
        if len(possible_generations) == 2: 
            in_generation = ask_question("Is the pokemon from generation " + str(possible_generations[0]) + "?")
        else:
            in_generation = ask_question("Is the pokemon from generation " + str(possible_generations[0]) + 
                                     " to " + str(possible_generations[(len(possible_generations)//2) - 1]) + "?")
        if in_generation == True:
            possible_generations = possible_generations[0: len(possible_generations)//2]
        else: 
            possible_generations = possible_generations[(len(possible_generations)//2):]

    # base stat total 
    KB = filter_KB("generation:=:" + str(possible_generations[0]), KB)
    average_base_stat_total = get_average('base_stat_total', KB)
    greater_than_avergae = ask_question('Does your pokemon have a base stat total greater than ' + str(average_base_stat_total) + "?")
    opernad = "<="
    if greater_than_avergae:
        opernad = ">"
    KB = filter_KB("base_stat_total:" +opernad + ":" + str(average_base_stat_total), KB)

    def search_for_type(KB, type_check_stack, resist_check_stack, weak_check_stack):
        
        def remove_elements_from_map(map, stack):
            if stack is not None:
                for element in stack:
                    if element in map:
                        del map[element]

        found_type = False
        checked_resist = False
        checked_weak = False
        while not found_type: 
            if len(KB) == 1: 
                return KB, KB[0].type_one, type_check_stack, resist_check_stack, weak_check_stack
            number_weak, number_resist, num_type = get_KB_type_matchup(KB) # get type info
            remove_elements_from_map(num_type, type_check_stack)
            remove_elements_from_map(number_resist, resist_check_stack)
            remove_elements_from_map(number_weak, weak_check_stack)

            values_to_chose = []
            most_common_type = max(num_type, key=num_type.get) 
            most_common_type_value = num_type[most_common_type]
            values_to_chose.append(most_common_type_value)

            most_common_weakness = max(number_weak, key=number_weak.get) if len(number_weak) != 0 else None 
            most_common_weakness_value = number_weak[most_common_weakness] if most_common_weakness != None else None 
            if most_common_weakness is not None: values_to_chose.append(most_common_weakness_value)


            most_common_resist = max(number_resist, key=number_resist.get) if len(number_resist) != 0 else None 
            most_common_resist_value = number_resist[most_common_resist] if most_common_resist != None else None 
            if most_common_resist is not None: values_to_chose.append(most_common_resist_value)

            maxValue = max(values_to_chose)
            if maxValue == most_common_type_value or (checked_resist and checked_weak):
                checked_weak = False
                checked_resist = False
                type_check_stack.append(most_common_type)
                answer = ask_question("Does you pokemon have this type: " + most_common_type + "?")
                if answer:
                    found_type = True
                    KB = filter_KB("type:=:" + most_common_type, KB)
                    return KB, most_common_type, type_check_stack, resist_check_stack, weak_check_stack
                else:
                    KB = filter_KB("type:!=:" + most_common_type, KB)
            elif maxValue == most_common_resist_value and not checked_resist and most_common_resist is not None:
                checked_resist = True
                resist_check_stack.append(most_common_resist)
                answer = ask_question("Does you pokemon resist this type: " + most_common_resist + "?") 
                if answer:
                    KB = filter_KB("resist_type:=:" + most_common_resist, KB)
                else:
                    KB = filter_KB("resist_type:!=:" + most_common_resist, KB)                  
            elif not checked_weak and most_common_weakness is not None:
                checked_weak = True
                weak_check_stack.append(most_common_weakness)
                answer = ask_question("Is your pokemon weak to this type: " + most_common_weakness + "?")
                if answer:
                    KB = filter_KB("weak_type:=:" + most_common_weakness, KB)
                else:
                    KB = filter_KB("weak_type:!=:" + most_common_weakness, KB)
               
    KB, first_type, type_stack, resist_stack, weak_stack = search_for_type(KB, [], [], [])
    check_solution(KB)

    if has_multiple_types:
        KB ,second_type, _, _, _ = search_for_type(KB, type_stack, resist_stack, weak_stack)
        check_solution(KB)

    # ask remaining pokemon: 
    while len(KB) != 1:
        pokemon_name = KB[0].name
        answer = ask_question("Is this your pokemon: " + pokemon_name + "?")
        if answer:
            KB = filter_KB("name:=:" + pokemon_name, KB)
        else:
            KB = filter_KB("name:!=:" + pokemon_name, KB)
    check_solution(KB)

if __name__ == "__main__":
    main()

