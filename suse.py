##### sinny usage examples #####
import sinny

def runScramble(verbosity=2):
    # get a new scramble
    scr_a = sinny.getScramble()

    # solve with verbosity level 2
    res = sinny.solver(scr_a, verbosity=verbosity) # i.e. stages = default_stages

    return [scr_a, res]

def main():
    # perform runScramble
    verbosity = 2
    rs_res = runScramble(verbosity) # default verbosity is 2.

    # batch solves
    sinny.batch(n_scrambles=3, verbosity=verbosity) # i.e. stages = default_stages

    # print(f"ret val: {rs_res}")

if '__name__' == '__main__':
    main()