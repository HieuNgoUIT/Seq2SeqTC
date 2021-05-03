# -*- coding: utf-8 -*-
import sys, argparse, random
from tqdm import tqdm
from Components.fat_finger import FatFinger
from Components.edit_distance import EditDistance
from Components.acronym import Acronym
from Components.teencode import Teencode
from Components.telex import Telex
from Components.region_new import Region

random.seed(123)

class Generator():
    def __init__(self):
        self.acronym = Acronym()
        self.teencode = Teencode()
        self.region = Region()
        self.telex = Telex()
        self.fat_finger = FatFinger()
        self.edit_distance = EditDistance()

    def generate_error(self, tokens, error_possible_indexes, error_names):
        # print(error_names)
        # print(type(error_names))
        # random.seed(56)
        if len(error_names) == 0:
            return None, None, None
        error_name = random.choice(error_names)
        #Acronym
        if error_name == 'ac':
            acronym_possible_index = [i for i in error_possible_indexes if self.acronym.generate(tokens[i]) != False]
            if len(acronym_possible_index) > 0:
                acronym_error_index = random.choice(acronym_possible_index)
                token = self.acronym.generate(tokens[acronym_error_index])
                return token, acronym_error_index, error_name
            else:
                error_names = list(filter((error_name).__ne__, error_names))
                return self.generate_error(tokens, error_possible_indexes, error_names)
        #Teencode
        elif error_name == 'tc':
            teencode_possible_index = [i for i in error_possible_indexes if self.teencode.generate(tokens[i]) != False]
            if len(teencode_possible_index) > 0:
                teencode_error_index = random.choice(teencode_possible_index)
                token = self.teencode.generate(tokens[teencode_error_index])
                return token, teencode_error_index, error_name
            else:
                error_names = list(filter((error_name).__ne__, error_names))
                return self.generate_error(tokens, error_possible_indexes, error_names)
        #Region
        elif error_name == 'rg':
            region_error_index = [i for i in error_possible_indexes if self.region.generate(tokens[i]) != False]
            if len(region_error_index) > 0:
                region_error_index = random.choice(region_error_index)
                token = self.region.generate(tokens[region_error_index])
                return token, region_error_index, error_name
            else:
                error_names = list(filter((error_name).__ne__, error_names))
                return self.generate_error(tokens, error_possible_indexes, error_names)
        #Telex
        elif error_name == 'tl':
            telex_possible_index = [i for i in error_possible_indexes if self.telex.generate(tokens[i]) != False]
            if len(telex_possible_index) > 0:
                telex_error_index = random.choice(telex_possible_index)
                token = self.telex.generate(tokens[telex_error_index])
                return token, telex_error_index, error_name
            else:
                error_names = list(filter((error_name).__ne__, error_names))
                return self.generate_error(tokens, error_possible_indexes, error_names)
        #Fat Finger
        elif error_name == 'ff':
            fat_finger_error_index = random.choice(error_possible_indexes)
            token = self.fat_finger.generate(tokens[fat_finger_error_index])
            return token, fat_finger_error_index, error_name
        #Edit Distance
        elif error_name == 'ed':
            edit_distance_error_index = random.choice(error_possible_indexes)
            token = self.edit_distance.generate(tokens[edit_distance_error_index])
            return token, edit_distance_error_index, error_name

    def error_per_sentence(self, ratio, ac, tc, rg, tl, ff, ed, contents):
        ratio /= 100
        #contents = contents.replace('\n', '. ')
        #sentences = [x for x in contents.split('.') if not x in ['', ' ', '  ', '\n', '\r', ' \r']]
        new_contents = []
        for sentence in tqdm(contents):
            tokens = sentence.split()
            num_error = int(len(tokens)*ratio) + 1
            error_possible_indexes = list(range(len(tokens)))
            for e in range(num_error):
                if error_possible_indexes == []:
                    break
                error_names = ['ac']*ac + ['tc']*tc + ['rg']*rg + ['tl']*tl + ['ff']*ff + ['ed']*ed
                tkn, ind, error_name = self.generate_error(tokens, error_possible_indexes, error_names)
                if ind == None:
                    continue
                tokens[ind] = tkn
                error_possible_indexes.remove(ind)
            new_sentences = ' '.join(token for token in tokens)
            new_contents.append(new_sentences) 
        return new_contents
        
