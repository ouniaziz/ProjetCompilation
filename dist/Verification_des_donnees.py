import csv
import ply.lex as lex
import ply.yacc as yacc
import re
import charset_normalizer

# List of all Tunisian governorates (states)
TUNISIAN_STATES = [
    "Ariana", "Beja", "Ben Arous", "Bizerte", "Gabes", "Gafsa", "Jendouba",
    "Kairouan", "Kasserine", "Kebili", "Le Kef", "Mahdia", "La Manouba",
    "Medenine", "Monastir", "Nabeul", "Sfax", "Sidi Bouzid", "Siliana",
    "Sousse", "Tataouine", "Tozeur", "Tunis", "Zaghouan"
]

# Regular expression for valid names (letters and spaces only)
NAME_REGEX = r"^[a-zA-Zéàâôîç\s]+$"

# --------- LEXER ---------
tokens = ['STATE']

def t_STATE(t):
    r'[a-zA-Zéàâôîç\s]+'
    if t.value.strip() in TUNISIAN_STATES:
        t.type = 'STATE'
        return t
    else:
        t.type = 'ERROR'
        return t

t_ignore = ' \t'

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex()

# --------- PARSER ---------
def p_valid_state(p):
    'state : STATE'
    p[0] = p[1]

def p_error(p):
    pass

parser = yacc.yacc()

# --------- ENCODING DETECTION ---------
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = charset_normalizer.detect(file.read())
        return result['encoding']

# --------- VALIDATION FUNCTIONS ---------
def validate_tunisian_states(csv_file, state_column):
    valid_states = []
    invalid_states = []

    encoding = detect_encoding(csv_file)
    with open(csv_file, 'r', encoding=encoding) as file:
        reader = csv.DictReader(file)
        for row_number, row in enumerate(reader, start=1):
            state = row[state_column].strip()
            lexer.input(state)
            try:
                parser.parse(state)
                valid_states.append((state, row_number))
            except Exception:
                invalid_states.append((state, row_number))

    return valid_states, invalid_states

def validate_names(csv_file, nom_column, prenom_column):
    valid_names = []
    invalid_names = []

    encoding = detect_encoding(csv_file)
    with open(csv_file, 'r', encoding=encoding) as file:
        reader = csv.DictReader(file)
        for row_number, row in enumerate(reader, start=1):
            nom = row[nom_column].strip()
            prenom = row[prenom_column].strip()

            if re.match(NAME_REGEX, nom) and re.match(NAME_REGEX, prenom):
                valid_names.append((f"{nom} {prenom}", row_number))
            else:
                invalid_names.append((f"{nom} {prenom}", row_number))

    return valid_names, invalid_names

# --------- MAIN PROGRAM ---------
#if __name__ == '__main__':
def check_errors(csv_file):
    res = set()
    #csv_file = 'etudiants_tunisiens_final(Sheet1).csv'
    nom_column = 'Nom'
    prenom_column = 'Prenom'
    state_column = 'State'

    # Validate names
    valid_names, invalid_names = validate_names(csv_file, nom_column, prenom_column)
    print("Valid names:")
    for name, row_number in valid_names:
        print(f"Row {row_number}: {name}")

    print("\nInvalid names:")
    for name, row_number in invalid_names:
        print(f"Row {row_number}: {name}")
        res.add(row_number-1)

    # Validate Tunisian states
    valid_states, invalid_states = validate_tunisian_states(csv_file, state_column)
    print("\nValid states:")
    for state, row_number in valid_states:
        print(f"Row {row_number}: {state}")

    print("\nInvalid states:")
    for state, row_number in invalid_states:
        print(f"Row {row_number}: {state}")
        res.add(row_number-1)
    
    return res
