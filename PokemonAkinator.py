import csv

def ask_question(question):
    while True:
        answer = input(question + " (yes/no): ").lower()
        if answer == 'yes' or answer == 'no':
            return answer
        else:
            print("Please answer with 'yes' or 'no'.")

def removeTypes(answer, rows):
    new_rows = []
    if answer == 'yes':
        for pokemon in rows:
            if pokemon[3] != '':
                new_rows.append(pokemon)
        print('removed pokemon with only 1 type')
        return new_rows
    if answer == 'no':
        for pokemon in rows:
            if pokemon[3] == '':
                new_rows.append(pokemon)
        print('removed pokemon with multiple types')
        return new_rows

def removeSpecificType(type, answer, rows):
    new_rows = []
    if answer == 'yes':
        for pokemon in rows:
            if pokemon[2] == type or pokemon[3] == type:
                new_rows.append(pokemon)
        print('only pokemon with', type, 'remain')
        return new_rows
    if answer == 'no':
        for pokemon in rows:
            if pokemon[2] != type and pokemon[3] != type:
                new_rows.append(pokemon)
        print('removed pokemon with type', type)
        return new_rows

def remainingTypes(rows):
    types = []
    for pokemon in rows:
        if pokemon[2] not in types:
            types.append(pokemon[2])
        if pokemon[3] not in types:
            types.append(pokemon[3])
    return types



def main():
    rows = []
    with open('Pokemon.csv', 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)

    print("Welcome to the Pokinator: Pokemon identification program!")
    print("Currently", len(rows), "in the knowledge base")

    has_multiple_types = ask_question("Does the species have more than one type?")
    rows = removeTypes(has_multiple_types, rows)
    print("Currently", len(rows), "in the knowledge base")

    # Type asker
    asked_types = []
    types = remainingTypes(rows)
    confirmed_types = []
    for ptype in types:
        remaining_types = remainingTypes(rows)
        if asked_types == remainingTypes(rows):
            break
        if ptype == '':
            asked_types.append('')
        if ptype not in asked_types and len(rows) != 0 and ptype != '' and ptype in remaining_types:
            is_type = ask_question("Is the type " + ptype + "?")
            rows = removeSpecificType(ptype, is_type, rows)
            asked_types.append(ptype)
            if is_type == 'yes':
                confirmed_types.append(ptype)
            print("Currently", len(rows), "in the knowledge base")
            if len(rows) == 0:
                print("That Pokemon does not exist in our system :(")
                return -1

    # is_capable_of_evolving = ask_question("Is the species capable of evolving?")
    # has_particular_type = ask_question("Does the species have a particular type?")
    # is_particular_color = ask_question("Is the species a particular color?")
    # has_particular_body_shape = ask_question("Is the species a particular body shape?")

    for pokemon in rows:
        print(pokemon)

    print("\nSpecies characteristics summary:")
    print("Has more than one type:", has_multiple_types)
    print("Types:", confirmed_types[0], confirmed_types[1])
    # print("Capable of evolving:", is_capable_of_evolving)
    # print("Has it evolved from something?, has_evolved)
    # print("Has a particular type:", has_particular_type)
    # print("Is a particular color:", is_particular_color)
    # print("Has a particular body shape:", has_particular_body_shape)

if __name__ == "__main__":
    main()