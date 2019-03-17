import argparse


def first(variable, input_dictionary):
    # Assuming the variable of interest in the parameters is called A
    first_dictionary = []
    for production in input_dictionary[variable]:
        # If A is a variable and A -> epsilon, then first(A) includes epsilon
        if production == 'epsilon':
            first_dictionary.append(production)
        # If A is a terminal, first(A) = {A}
        elif production[0].islower():
            first_dictionary.append(production[0])
        else:
            # If A is a variable and A -> y1..yn, then first(A) = first(y1..yn)
            for index, value in enumerate(production):
                first_y1 = first(value, input_dictionary)
                if 'epsilon' in first_y1 and not index == len(production)-1:
                    first_y1.remove("epsilon")
                    first_dictionary += first_y1
                    first_y2 = first(production[index+1],
                                     input_dictionary)
                    if 'epsilon' in first_y2:
                        first_y2.remove('epsilon')
                    first_dictionary += first_y2
                else:
                    first_dictionary += first_y1
                    break
    return set(first_dictionary)


def compute_first(input_dictionary):
    # Wrapper function that loops over the variables
    dictionary = {}
    for variable in input_dictionary:
        dictionary[variable] = first(variable, input_dictionary)
    return dictionary


def follow(variable, input_dictionary, first_dictionary):
    # Assuming the variable of interest in the parameters is called A
    follow_dictionary = []
    # If A is a start variable
    if list(input_dictionary.keys()).index(variable) == 0:
        follow_dictionary += '$'
    for key, productions in input_dictionary.items():
        for production in productions:
            if variable == production[-1]:
                follow_dictionary += follow(key,
                                            input_dictionary, first_dictionary)
            for index, symbol in enumerate(production):
                if symbol == variable and index+1 <= len(production)-1:
                    if production[index+1].islower():
                        follow_dictionary += production[index+1]
                    else:
                        next_symbol_first = first_dictionary[production[index+1]].copy(
                        )
                        if 'epsilon' in next_symbol_first:
                            next_symbol_first.remove('epsilon')
                            follow_dictionary += follow(production[index+1],
                                                        input_dictionary, first_dictionary)
                        follow_dictionary += next_symbol_first
    return set(follow_dictionary)


def compute_follow(input_dictionary, first_dictionary):
    # Wrapper function that loops over the variables
    dictionary = {}
    for variable in input_dictionary:
        dictionary[variable] = follow(
            variable, input_dictionary, first_dictionary)
    return dictionary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        add_help=True, description='Sample Commandline')
    parser.add_argument('--file', action="store",
                        help="path of file to take as input", nargs="?", metavar="file")
    args = parser.parse_args()
    if args.file is not None:
        input_dictionary = {}
        with open(args.file, "r") as file:
            # Preprocess
            lines = file.readlines()
            lines = list(map(lambda element: element.replace("\n", ""), lines))
            for line in lines:
                rule = line.split(":")
                input_dictionary[rule[0].strip()] = list(
                    map(lambda element: element.replace(" ", '').strip(), rule[1].split("|")))
            # Compute first and follow
            first_dictionary = compute_first(input_dictionary)
            follow_dictionary = compute_follow(
                input_dictionary, first_dictionary)
            # Write to file
            o = open("task_5_1_result.txt", "w+")
            for variable in input_dictionary:
                o.write(variable + " : " + " ".join(first_dictionary[variable]) + " : " + " ".join(
                    follow_dictionary[variable]) + "\n")
