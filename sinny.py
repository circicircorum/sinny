import subprocess

#### define path to nissy ####
nissy_name = '.\\nissy-2.0.7.exe'

#### get a test scramble ####
comproc = subprocess.run(nissy_name + '  scramble', capture_output=True)
scramble = comproc.stdout.decode()[:-2] + ' ' # remove ctrl chars and add a trailing space

#### define solving stages ####
default_stages = [' solve eo ', ' solve dr-eo ', ' solve htr ', ' solve '] # stages with whitespaces
# note: may move out of htr at the last stage

## (alternative stages)
#stages = [' solve eoud ', ' solve drud ', ' solve htr-drud ', ' solve htrfin ']
## stages with whitespaces using U/D EO and without going out of HTR at the end
#stages = [' solve eofb ', ' solve drud-eofb ', ' solve htr-drud ', ' solve htrfin ']
# ^ the thing that i actly intended to do oops (but with like, even more restrictions) (now chngd in main())

#### solve cube in stages ####
def solver(scramble, verbosity=0, stages=default_stages):

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
        raw_output = raw_output[:-2] # strip \r\n

        processed_output = raw_output[:raw_output.index('(')] # strip movecount
        additional_moves += processed_output
        movecount = int(raw_output[raw_output.index('(')+1:raw_output.index(')')])
        solution_length += movecount

        if show_solution:
            #print(raw_output)#, end='') # \r\n has been stripped so add a newline back in
            print(f'{processed_output}//{stage[7:]}({movecount}/{solution_length})') # note: strip ' solve ' from stage (potential source of bugs (:fingerscrossed:))

    ## print soln to terminal
    if verbosity > 1:
        print(f'solution: {additional_moves}({solution_length})') # does not reflect cancellations into moves between stages
    elif verbosity == 1:
        print(f'solution: {additional_moves}({solution_length})') # same output as of now
    
    return [additional_moves, solution_length]

def many_solves(n_scrambles = 10, verbosity=2, stages=default_stages):
    cumsum_moves = 0
    for n in range(n_scrambles):
        print(f'scramble number {n}...')
        comproc = subprocess.run(nissy_name + '  scramble', capture_output=True)
        scramble = comproc.stdout.decode()[:-2] + ' '
        cumsum_moves += solver(scramble, verbosity, stages=stages)[1]
        if verbosity > 0:
            print()
    
    #print(f'avg: {cumsum_moves} / {n_scrambles} = {cumsum_moves // n_scrambles} R {cumsum_moves % n_scrambles}')
    return cumsum_moves

def batch(n_scrambles=10, verbosity=2, stages=default_stages):
    #n_scrambles = 10
    print()
    print(f'performing test with {n_scrambles} scrambles...')
    cumsum_moves = many_solves(n_scrambles, verbosity, stages)
    print('test complete')
    #print(f'avg: {cumsum_moves} / {n_scrambles} = {cumsum_moves // n_scrambles} R {cumsum_moves % n_scrambles}')
    print(f'avg: {cumsum_moves} / {n_scrambles} = {cumsum_moves / n_scrambles:.2f}')
    return cumsum_moves

def experiment():
    pass

def main():
    import sys
    import argparse
    parser = argparse.ArgumentParser(
        prog='sinny',
        description='nissy-based script - performs a test solve by default',
        epilog='contact deadmanlsh if u needs helps'
    )
    parser.add_argument('-b', '--batchsize', type=int, help='perform test with batch of given size')
    parser.add_argument('-s', '--stages', type=int, help='the method to use as defined by stages (see code)', default=1) # note: not default_stages :)
    #parser.add_argument('-o', '--output', help='file to save output to (wip)')
    parser.add_argument('-v', '--verbosity', type=int, help='level of verbosity to use', default=2)
    parser.add_argument('-d', '--debug', action='store_true', help='display debug information')
    parser.add_argument('-t', '--notest', action='store_true', help='suppress test solve at the beginning')
    args = parser.parse_args()

    doTestSolve = True
    doBatchSolves = False
    nBatchSize = 3
    if args.notest:
        doTestSolve = False
    if args.batchsize is not None:
        doBatchSolves = True #doBatchSolves = True
        nBatchSize = args.batchsize #nBatchSize = 10
    batch_verbosity = args.verbosity #batch_verbosity = 2
    test_verbosity = args.verbosity # same for now

    stages = default_stages
    if args.stages == 1:
        stages = [' solve eofb ', ' solve drud-eofb ', ' solve htr-drud ', ' solve htrfin ']
    
    ## test solves
    if doTestSolve:
        solver(scramble, test_verbosity, stages=stages)
    if doBatchSolves:
        batch(nBatchSize, batch_verbosity, stages=stages)

if __name__ == '__main__':
    main()