'''
tool to visualize the initial KB (list of pokemon) in either list or json format 
usage:
    python3 displayKB // not specified so assumed list 
    python3 displayKB 0 // for list
    python3 displayKB 1 // for json 
'''
from PokemonAkinator import generate_KB, print_KB 
import sys 

print_version = 0
if len(sys.argv) > 1: 
    print_version = int(sys.argv[1])

KB = generate_KB()
print_KB(KB, print_version)