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

def main():
    rows = []
    with open('Pokemon.csv', 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)

    print("Welcome to the Pokinator: Pokemon identification program!")
    has_multiple_types = ask_question("Does the species have more than one type?")
    rows = removeTypes(has_multiple_types, rows)
    for i in rows:
        print(i)
    is_water_type = ask_question("Is the type Water?")


    # is_capable_of_evolving = ask_question("Is the species capable of evolving?")
    has_particular_type = ask_question("Does the species have a particular type?")
    is_particular_color = ask_question("Is the species a particular color?")
    has_particular_body_shape = ask_question("Is the species a particular body shape?")

    print("\nSpecies characteristics summary:")
    print("Has more than one type:", has_multiple_types)
    # print("Capable of evolving:", is_capable_of_evolving)
    print("Has a particular type:", has_particular_type)
    print("Is a particular color:", is_particular_color)
    print("Has a particular body shape:", has_particular_body_shape)

if __name__ == "__main__":
    main()