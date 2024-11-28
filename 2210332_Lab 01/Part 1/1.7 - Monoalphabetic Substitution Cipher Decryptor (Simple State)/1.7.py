import json

from nostril import nonsense
from ortools.sat.python import cp_model

with open("wxrd.json", "r") as f:
    words_dictionary = json.load(f)


def filter_words(length):
    return {
        word: words_dictionary[word] for word in words_dictionary if len(word) == length
    }


# Creates the model.
model = cp_model.CpModel()

cipher = input("Enter the cipher text: ")
code = cipher.lower()

# Assign numeric values to letters
val = {chr(i + 96): i for i in range(1, 27)}

dict = {}
known = {}
varlist = []
freq = {}
to_var = {}

# Count frequency of each letter
for l in set(code):
    if l.isalpha():
        freq[l] = code.count(l)
        var = model.NewIntVar(1, 26, l)
        varlist.append(var)
        to_var[l] = var
    elif not l.isspace():
        code = code.replace(l, " ")

freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

model.AddAllDifferent(varlist)

# Creates the constraints.
for word in code.split():
    dict.update({word: len(word)})

sort = sorted(dict.items(), key=lambda x: x[1])

for word in sort:
    solution = []
    for pos_word in filter_words(word[1]):
        is_word = model.NewBoolVar(f"{word[0]}_is_{pos_word}")
        solution.append(is_word)
        for i in range(word[1]):
            model.Add(to_var[word[0][i]] == val[pos_word[i]]).OnlyEnforceIf(is_word)
    model.AddExactlyOne(solution)


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):

    def __init__(self, variables, reverse_val, code, cipher):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.variables = variables
        self.reverse_val = reverse_val
        self.code = code
        self.cipher = cipher
        self.solution_count = 0

    def on_solution_callback(self):
        self.solution_count += 1
        solution = []
        plaintext = list(self.cipher)
        for char in self.code:
            if char.isalpha():
                solution.append(self.reverse_val[self.Value(self.variables[char])])
            else:
                solution.append(char)
        if len([c for c in solution if c.isalpha()]) >= 6 and nonsense(
            "".join(solution)
        ):
            return
        print("\033[95m" + f"Plaintext #{self.solution_count}:" + "\033[97m", end=" ")
        for c in range(len(solution)):
            if solution[c].isalpha():
                plaintext[c] = solution[c].upper()
        print("".join(plaintext))


# Reverse mapping from values to letters
reverse_val = {v: k for k, v in val.items()}

# Create a solver and solve.
solver = cp_model.CpSolver()

# Ensure the file is empty before writing
solution_printer = VarArraySolutionPrinter(to_var, reverse_val, code, cipher)
solver.parameters.enumerate_all_solutions = True
status = solver.Solve(model, solution_printer)

if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
    print("\033[91m" + "No solution found.")
