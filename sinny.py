import subprocess

#### define path to nissy ####
nissy_name = '.\\nissy-2.0.7.exe'

#### get a test scramble ####
comproc = subprocess.run(nissy_name + '  scramble', capture_output=True)
scramble = comproc.stdout.decode()[:-2] + ' ' # remove ctrl chars and add a trailing space

#### define solving stages ####
stages = [' solve eo ', ' solve dr-eo ', ' solve htr ', ' solve '] # stages with whitespaces
# note: may move out of htr at the last stage

doTestSolve = True

#### solve cube in stages ####
def solver(scramble, verbosity=0):

    ## decide how much info to show
    show_scramble = False
    show_solution = False
    if verbosity == 0:
        pass
    if verbosity >= 1:
        show_scramble = True
    if verbosity >= 2:
        show_solution = True

    if show_scramble:
        print('scramble: ' + scramble)
    
    ## initialise partial solutions and keep track of solution length
    additional_moves = ''
    solution_length = 0

    ## solve the scramble step by step using eo>dr>htr>solved
    for stage in stages:

        # solved -> (scramble+partialsolution) -> getcontinuation
        comproc = subprocess.run(nissy_name + stage + scramble + additional_moves, capture_output=True)
        raw_output = comproc.stdout.decode() # raw_output has the solution for the next stage

        if show_solution:
            print(raw_output, end='')

        processed_output = raw_output[:raw_output.index('(')] # strip movecount
        additional_moves += processed_output
        solution_length += int(raw_output[raw_output.index('(')+1:raw_output.index(')')]) # get movecount and add to cumsum

    ## print soln to terminal
    if verbosity > 1:
        print(f'solution: {additional_moves}({solution_length})')# + additional_moves +) # does not reflect cancellations into moves between stages
        #print('length: ' + str(solution_length))
        #print()
    elif verbosity == 1:
        print('solution: ' + additional_moves)
    
    return [additional_moves, solution_length]

## test solve
if doTestSolve:
    solver(scramble, 2)

def many_solves(n_scrambles = 10, verbosity=2):
    cumsum_moves = 0
    for n in range(n_scrambles):
        print(f'scramble number {n}...')
        comproc = subprocess.run(nissy_name + '  scramble', capture_output=True)
        scramble = comproc.stdout.decode()[:-2] + ' '
        cumsum_moves += solver(scramble, verbosity)[1]
        if verbosity > 0:
            print()
    
    #print(f'avg: {cumsum_moves} / {n_scrambles} = {cumsum_moves // n_scrambles} R {cumsum_moves % n_scrambles}')
    return cumsum_moves


def batch(n_scrambles=10, verbosity=2):
    #n_scrambles = 10
    print()
    print(f'performing test with {n_scrambles} scrambles...')
    cumsum_moves = many_solves(n_scrambles, verbosity)
    print('test complete')
    #print(f'avg: {cumsum_moves} / {n_scrambles} = {cumsum_moves // n_scrambles} R {cumsum_moves % n_scrambles}')
    print(f'avg: {cumsum_moves} / {n_scrambles} = {cumsum_moves / n_scrambles:.2f}')
    return cumsum_moves

def experiment():
    pass

def main():
    pass

batch(10, 2)
