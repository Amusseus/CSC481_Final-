import subprocess as sb 
import select 
from PokemonAkinator import Pokemon, generate_KB
from collections import defaultdict

game_path = 'PokemonAkinator.py'

'''
Game statistics to monitor: 
    - avergae num questions for all pokemon 
    - average num question for that type 
    - average num question for that generation 
    - average num question of mono/dual type 
'''
total_number_question_all = 0
total_number_pokemon = 0

total_number_questions_generation = defaultdict(int)
total_number_pokemon_generation = defaultdict(int)

total_number_questions_type = defaultdict(int)
total_number_pokemon_type = defaultdict(int)

total_number_questions_mono = 0
total_number_pokemon_mono = 0

total_number_questions_dual = 0
total_number_pokemon_dual = 0

def update_statistic(pokemon, number_questions):
    global total_number_question_all, total_number_pokemon
    global total_number_questions_dual, total_number_pokemon_dual
    global total_number_questions_mono, total_number_pokemon_mono

    total_number_question_all += number_questions
    total_number_pokemon += 1

    if pokemon.type_one is not None:
        total_number_questions_type[pokemon.type_one] += number_questions
        total_number_pokemon_type[pokemon.type_one] += 1

    if pokemon.type_two is not None:
        total_number_questions_type[pokemon.type_two] += number_questions
        total_number_pokemon_type[pokemon.type_two] += 1

    total_number_questions_generation[pokemon.generation] += number_questions
    total_number_pokemon_generation[pokemon.generation] += 1

    if pokemon.type_one is not None and pokemon.type_two is not None: 
        total_number_questions_dual += number_questions
        total_number_pokemon_dual += 1
    else:
        total_number_questions_mono += number_questions
        total_number_pokemon_mono += 1

def find_solution(pokemon, question):
    question_list = question.split()
    if question_list[0] == 'MUL_TYPE':
        return True if pokemon.type_one != None and pokemon.type_two != None else False 
    elif question_list[0] == 'GEN_FROM':
        min_range = int(question_list[1])
        max_range = int(question_list[3])
        return True if pokemon.generation >= min_range and pokemon.generation <= max_range else False 
    elif question_list[0] == 'GEN':
        check_generation = int(question_list[1])
        return True if pokemon.generation == check_generation else False 
    elif question_list[0] == 'BASE_STAT':
        check_stat = float(question_list[1])
        return True if pokemon.base_stat_total > check_stat else False
    elif question_list[0] == 'RESIST_TYPE':
        return True if pokemon.resistance_map[question_list[1]] < 1 else False
    elif question_list[0] == 'WEAK_TYPE':
        return True if pokemon.resistance_map[question_list[1]] > 1 else False
    elif question_list[0] == 'HAVE_TYPE':
        return True if pokemon.type_one == question_list[1] or pokemon.type_two == question_list[1] else False
    elif question_list[0] == 'POKEMON':
        return True if pokemon.name == question_list[1] else False 
    else:
        return True

KB = generate_KB()
for entry in KB:
    print("GUESSING POKEMON: " + entry.name)
    # play the pokemon akinator game for each entry     
    process = sb.Popen(['python3', game_path, "1"], stdin=sb.PIPE, stdout=sb.PIPE)
    while True: 
        return_code = process.poll()
        if return_code is not None:
            # game over, stop playing 
            break
        else:
            # game is still running, keep playing 
            game_fds = process.stdout

            # get game question 
            ready_to_read, _, _ = select.select([game_fds], [], [])
            game_output = ""
            finish_phrase = "(yes/no):"
            end_phrase = "***"
            while True: 
                if game_fds in ready_to_read:
                    current_read = game_fds.read(1).decode('utf-8')
                    game_output += current_read
                    if entry.name == "Type:Null":
                        print(game_output)
                    if game_output[-(len(finish_phrase)):] == finish_phrase or game_output[-len(end_phrase):] == end_phrase:
                        # found end
                        break 
            # check if game is over 
            if game_output[-len(end_phrase):] == end_phrase:
                game_output_list = game_output.split()
                update_statistic(entry, int(game_output_list[3]))
                print(game_output)
                break 
            
            solution = find_solution(entry, game_output)
            # answer game question 
            answer = "yes\n" if solution else "no\n"
            process.stdin.write(answer.encode())
            process.stdin.flush()
        
print("The average number of questions for all pokemon: " + str(total_number_question_all/total_number_pokemon))
for key in total_number_questions_generation.keys():
    print("The average number of questions for this generation " + str(key) + " : " + str(total_number_questions_generation[key]/total_number_pokemon_generation[key]))
for key in total_number_questions_type.keys():
    print("The average number of questions for the type " + key + " : " + str(total_number_questions_type[key]/total_number_pokemon_type[key]))
print("The average number of questions for mono-type pokemon: " + str(total_number_questions_mono/total_number_pokemon_mono))
print("The average number of questions for dual pokemon: " + str(total_number_questions_dual/total_number_pokemon_dual))
