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
    with open("../train.txt", 'r') as f:
        for line in f:
            contents.append(line.replace("\n",""))
            count += 1
            if count == 10:
                break
    
    error_contents = generator_r.error_per_sentence(ratio, ac, tc, rg, tl, ff, ed, contents)
    with open("../valid.json", "w") as f2:
        for src, trg in zip(contents, error_contents):
            result = {
                "src": src.strip(),
                "trg": trg.strip()
            }
            temp = str(result) + "\n"
            f2.write(temp.replace("'","\""))
    # assert len(contents) == len(error_contents)
    # import pandas as pd 
    # df = pd.DataFrame({'src': contents, 'trg': error_contents})
    # df.to_csv('10train.csv')

    
    
    