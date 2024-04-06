import os
import string
import random
from pprint import pprint

env_vars = [
    "ALLUSERSPROFILE",    # The path to the All Users profile directory.
    "CommonProgramFiles", # The path to common program files directory.
    "COLORTERM", # The path to common program files (x86) directory.
    "CommonProgramW6432", # The path to common program files (x64) directory.
    "HOMEDRIVE",          # The drive letter of the home directory.
    "ProgramFiles",       # The path to the Program Files directory.
    "SystemRoot",         # The path to the Windows directory.
    "SESSIONNAME",        # The name of the session under which the current process is running.
    "WINDIR",             # The path to the Windows directory.
]

# Build environment variable dictionary
current_username = os.getenv("USERNAME")
env_mapping = {}
for character in string.printable:
    env_mapping[character] = {}
    for var in env_vars:
        value = os.getenv(var)
        if value is None or current_username in value:
            continue
        if character in value:
            env_mapping[character][var] = [i for i, c in enumerate(value) if c == character]

def envhide_obfuscate(string):
    obf_code = []
    for c in string:
        if c not in env_mapping:
            obf_code.append(c)
        else:
            possible_vars = list(env_mapping[c].keys())
            if not possible_vars:
                obf_code.append(f'[char]{ord(c)}')
                continue
            else:
                chosen_var = random.choice(possible_vars)
                possible_indices = env_mapping[c][chosen_var]
                print(f"{chosen_var=}{possible_indices=}")
                chosen_index = random.choice(possible_indices)
                
                new_character = os.getenv(chosen_var)[chosen_index]
                ps_syntax = f'$env:{chosen_var}[{chosen_index}]'
                obf_code.append(ps_syntax)

    return obf_code

def ps_obfuscate(string):
    iex = envhide_obfuscate('iex')
    pieces = envhide_obfuscate(string)
    iex_stage = f'({",".join(iex)} -Join ${random.randint(1,99999)})'
    payload_stage = f'({",".join(pieces)} -Join ${random.randint(1,99999)})'
    
    return f"& {iex_stage} {payload_stage}"

ps_cmd = "dir"
print(ps_obfuscate(ps_cmd))
