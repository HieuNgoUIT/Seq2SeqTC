# -*- coding: utf-8 -*-
import sys, argparse, random
from tqdm import tqdm
from Components.fat_finger import FatFinger
from Components.edit_distance import EditDistance
from Components.acronym import Acronym
from Components.teencode import Teencode
from Components.telex import Telex
from Components.region_new import Region

class Generator():
    def __init__(self):
        self.acronym = Acronym()
        self.teencode = Teencode()
        self.region = Acronym()
        self.telex = Telex()
        self.fat_finger = FatFinger()
        self.edit_distance = EditDistance()

    def error_per_sentence(self, ratio, ac, tc, rg, tl, ff, ed, contents):
        ratio /= 100
        num_edit_distance = ed
        num_teencode = tc
        num_acronym = ac
        num_fat_finger = ff
        num_telex = tl
        num_region = rg
    
        contents = contents.replace('\n', '. ')
        sentences = [x for x in contents.split('.') if not x in ['', ' ', '  ', '\n', '\r', ' \r']]
        new_contents = ''
        statistics_error = {'ac' : 0, 'tc' : 0, 'rg' : 0, 'tl' : 0, 'ff' : 0, 'ed' : 0, 'num_sentence' : 0, 'num_token' : 0}
        for sentence in tqdm(sentences):
            tokens = sentence.split()
            statistics_error['num_sentence'] += 1
            statistics_error['num_token'] += len(tokens)
            num_error = int(len(tokens)*ratio) + 1
            error_possible_indexes = random.sample(list(range(len(tokens))), num_error)
            acronym_error_indexes = []
            teencode_error_indexes = []
            region_error_indexes = []
            telex_error_indexes = []
            fat_finger_error_indexes = []
            edit_distance_error_indexes = []
            
            for i in range(num_acronym):
                if len(error_possible_indexes) == 0:
                    break
                acronym_possible_index = [i for i in error_possible_indexes if self.acronym.generate(tokens[i]) != False]
                if len(acronym_possible_index) > 0:
                    acronym_error_index = random.choice(acronym_possible_index)
                    tokens[acronym_error_index] = self.acronym.generate(tokens[acronym_error_index])
                    acronym_error_indexes.append(acronym_error_index)
                    error_possible_indexes.remove(acronym_error_index)
            
            #generate teencode error
            for i in range(num_teencode):
                if len(error_possible_indexes) == 0:
                    break
                teencode_possible_index = [i for i in error_possible_indexes if self.teencode.generate(tokens[i]) != False]
                if len(teencode_possible_index) > 0:
                    teencode_error_index = random.choice(teencode_possible_index)
                    tokens[teencode_error_index] = self.teencode.generate(tokens[teencode_error_index])
                    teencode_error_indexes.append(teencode_error_index)
                    error_possible_indexes.remove(teencode_error_index)

            #generate region error
            for i in range(num_region):
                if len(error_possible_indexes) == 0:
                    break
                region_possible_index = [i for i in error_possible_indexes if self.region.generate(tokens[i]) != False]
                if len(region_possible_index) > 0:
                    region_error_index = random.choice(region_possible_index)
                    tokens[region_error_index] = self.region.generate(tokens[region_error_index])
                    region_error_indexes.append(region_error_index)
                    error_possible_indexes.remove(region_error_index)

            #generate telex error
            for i in range(num_telex):
                if len(error_possible_indexes) == 0:
                    break
                telex_possible_index = [i for i in error_possible_indexes if self.telex.generate(tokens[i]) != False]
                if len(telex_possible_index) > 0:
                    telex_error_index = random.choice(telex_possible_index)
                    tokens[telex_error_index] = self.telex.generate(tokens[telex_error_index])
                    telex_error_indexes.append(telex_error_index)
                    error_possible_indexes.remove(telex_error_index)

            #generate fat finger error
            for i in range(num_fat_finger):
                if len(error_possible_indexes) == 0:
                    break
                fat_finger_error_index = random.choice(error_possible_indexes)
                tokens[fat_finger_error_index] = self.fat_finger.generate(tokens[fat_finger_error_index])
                fat_finger_error_indexes.append(fat_finger_error_index)
                error_possible_indexes.remove(fat_finger_error_index)

            #generate edit distance error
            for i in range(num_edit_distance):
                if len(error_possible_indexes) == 0:
                    break
                edit_distance_error_index = random.choice(error_possible_indexes)
                tokens[edit_distance_error_index] = self.edit_distance.generate(tokens[edit_distance_error_index])
                edit_distance_error_indexes.append(edit_distance_error_index)
                error_possible_indexes.remove(edit_distance_error_index)
            
            new_sentences = ' '.join(token for token in tokens)
            statistics_error['ac'] += len(acronym_error_indexes)
            statistics_error['tc'] += len(teencode_error_indexes)
            statistics_error['rg'] += len(region_error_indexes)
            statistics_error['tl'] += len(telex_error_indexes)
            statistics_error['ff'] += len(fat_finger_error_indexes)
            statistics_error['ed'] += len(edit_distance_error_indexes)
            
            input_contents = '\n'.join(x for x in sentences)
            new_contents += (new_sentences+'\n')
            
        return statistics_error, input_contents, new_contents
        
