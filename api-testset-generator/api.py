from Components.generator_number import Generator as GeneratorNumber
from Components.generator_ratio import Generator as GeneratorRatio

generator_n = GeneratorNumber()
generator_r = GeneratorRatio()

if __name__ == "__main__":
    ratio = 20
    ac = 0
    tc = 0
    rg = 33
    tl = 33
    ff = 33
    ed = 1

    contents = []
    count = 0
    with open("../valid.txt", 'r') as f:
        for line in f:
            contents.append(line.replace("\n",""))
    
    error_contents = generator_r.error_per_sentence(ratio, ac, tc, rg, tl, ff, ed, contents)
    with open("../valid_trg.txt", "w") as f2:
        for ec in error_contents:
            f2.write(ec + "\n")

    
    
    