with open('/data/divt/data/Resources/Dictionary/vietnamese-dictionary.txt', 'w+') as w:
    with open('/data/divt/data/Resources/Dictionary/vietnamese-dictionary_.txt', 'r') as f:
        dict_ = f.read().replace('-','_').split('\n')
        dict_.sort()
        k = 0
        for i in dict_:
            k += 1
            print(k)
            w.write(i+'\n')
