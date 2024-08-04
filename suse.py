##### sinny usage examples #####
import sinny

# get a new scramble
scr_a = sinny.getScramble()

# solve with verbosity level 2
res = sinny.solver(scr_a, verbosity=2) # i.e. stages = default_stages

# batch solves
sinny.batch(n_scrambles=3, verbosity=2) # i.e. stages = default_stages

# print(f"ret val: {res}")
