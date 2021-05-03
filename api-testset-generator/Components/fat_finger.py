import sys, random

DELETE = -1 # removes a character in the string
CAPS_LOCK = 1 # change the remaning characters to ALL CAPS

quertyKeyNeighbors = {
    # row 1
    '`':  ['1', '\t'], '1':  ['`', '2', '\t', 'q'], '2':  ['1', '3', 'q', 'w'], '3':  ['2', '4', 'w', 'e'], '4':  ['3', '5', 'e', 'r'],
    '5':  ['4', '6', 'r', 't'], '6':  ['5', '7', 't', 'y'], '7':  ['6', '8', 'y', 'u'], '8':  ['7', '9', 'u', 'i'], '9':  ['7', '0', 'i', 'o'],
    '0':  ['9', '-', 'o', 'p'], '-':  ['0', '=', 'p', '['], '+':  ['-', '[', ']', DELETE],
    # row 2
    '\t': ['`', '1', 'q', 'a'], 'q':  ['1', '2', 'w', 'a', CAPS_LOCK], 'w':  ['2', '3', 'q', 'e', 'a', 's'], 'e':  ['3', '4', 'w', 'r', 's', 'd'],
    'r':  ['4', '5', 'e', 't', 'd', 'f'], 't':  ['5', '6', 'r', 'y', 'f', 'g'], 'y':  ['6', '7', 't', 'u', 'g', 'h'], 'u':  ['7', '8', 'y', 'i', 'h', 'j'],
    'i':  ['8', '9', 'u', 'o', 'j', 'k'], 'o':  ['9', '0', 'i', 'p', 'k', 'l'], 'p':  ['0', '-', 'o', '[', 'l', ';'], '[':  ['-', '=', 'p', ']', ';', '\'', '\n'],
    ']':  ['=', '[', '\\', '\'', '\n', DELETE], '\\': [']', '\n', DELETE],
    # row 3
    'a':  ['q', 'w', 's', '', 'z', CAPS_LOCK], 's':  ['w', 'e', 'a', 'd', 'z', 'x'], 'd':  ['e', 'r', 's', 'f', 'x', 'c'], 'f':  ['r', 't', 'd', 'g', 'c', 'v'],
    'g':  ['t', 'y', 'f', 'h', 'v', 'b'], 'h':  ['y', 'u', 'g', 'j', 'b', 'n'], 'j':  ['u', 'i', 'h', 'k', 'n', 'm'], 'k':  ['i', 'o', 'j', 'l', 'm', ','],
    'l':  ['o', 'p', 'k', ';', ',', '.'], ';':  ['p', '[', 'l', '\\', '.', '/'], '\'': ['[', ']', ';', '\n', '/', DELETE],
    # row 4
    'z':  ['a', 's', '', 'x'], 'x':  ['s', 'd', 'z', 'c', ' '], 'c':  ['d', 'f', 'x', 'v', ' '], 'v':  ['f', 'g', 'c', 'b', ' '],
    'b':  ['g', 'h', 'v', 'n', ' '], 'n':  ['h', 'j', 'b', 'm', ' '], 'm':  ['j', 'k', 'n', ',', ' '], ',':  ['k', 'l', 'm', '.', ' '],
    '.':  ['l', ';', ',', '/'], '/':  [';', '\'', ',', '/'],
    # row 5
    ' ':  ['x', 'c', 'v', 'b', 'n', 'm'],
}

quertyKeyShiftPairs = {
    # row 1
    '`':  '~', '1':  '!', '2':  '@', '3':  '#', '4':  '$', '5':  '%', '6':  '^', '7':  '&', '8':  '*', '9':  '(', '0':  ')', '-':  '_', '+':  '=',
    # row 2
    '\t': '', 'q':  'Q', 'w':  'W', 'e':  'E', 'r':  'R', 't':  'T', 'y':  'Y', 'u':  'U', 'i':  'I', 'o':  'O', 'p':  'P', '[':  '{', ']':  '}', '\\': '|',
    # row 3
    'a':  'A', 's':  'S', 'd':  'D', 'f':  'F', 'g':  'G', 'h':  'H', 'j':  'J', 'k':  'K', 'l':  'L', ';':  ':', '\'': '"',
    # row 4
    'z':  'Z', 'c':  'C', 'x':  'X', 'v':  'V', 'b':  'B', 'n':  'N', 'm':  'M', ',':  '<', '.':  '>', '/':  '?',
    # row 5
    ' ':  ' '
}

english_letters=list("abcdefghijklmnopqrstuvwxyz")

class FatFinger():
    def reverseAndMergeShiftPairs(self, shiftPairs=quertyKeyShiftPairs):
        pairKeys = shiftPairs.keys()
        mergedMap = shiftPairs.copy()
        for key in pairKeys:
            value = shiftPairs[key]
            mergedMap[value] = key
        return mergedMap

    def shiftSwapGenerator( self, string='', shiftMap=quertyKeyShiftPairs):
        mergedMap = self.reverseAndMergeShiftPairs( quertyKeyShiftPairs)
        index = 0;
        while index < len(string):
            next = index + 1
            char = string[index]
            if not char in english_letters:
                yield char
                index = next
                continue
            shifted = mergedMap[char]
            swapped = string[:index] + shifted + string[next:]
            index = next
            yield swapped

    def shiftAndMergeNeighorKeys(self, neighborMap=quertyKeyNeighbors, shiftMap=quertyKeyShiftPairs):
        mergedShiftMap = self.reverseAndMergeShiftPairs(shiftMap)
        neighborKeys = neighborMap.keys()
        mergedMap = neighborMap.copy()
        for key in neighborKeys:
            shifted = mergedShiftMap[key]
            mergedMap[shifted] = neighborMap[key]
        return mergedMap

    def neighborSwapGenerator( self, string='', neighborMap=quertyKeyNeighbors, shiftNeighbors=True, slurNeighbors=False):
        if (shiftNeighbors):
            shiftMap = self.reverseAndMergeShiftPairs(quertyKeyShiftPairs)
        mergedMap = self.shiftAndMergeNeighorKeys(neighborMap)
        index = 0
        while index < len(string):
            next = index + 1
            prefix = string[:index]
            suffix = string[next:]
            char = string[index]
            if not char in english_letters:
                yield char
                index = next
                continue
            for near in mergedMap[string[index]]:
                if near == DELETE:
                    yield prefix[:-1] + suffix
                elif near == CAPS_LOCK:
                    yield prefix + suffix.upper()
                else:
                    yield prefix + near + suffix
                    if shiftNeighbors:
                        yield prefix + shiftMap[near] + suffix
                    if slurNeighbors:
                        yield prefix + near + char + suffix
                        yield prefix + char + near + suffix
                        if shiftNeighbors:
                            yield prefix + shiftMap[near] + char + suffix
                            yield prefix + char + shiftMap[near] + suffix
            index = next

    def generate(self, token):
        generators = []
        # print(self.shiftSwapGenerator(token))
        # print(self.neighborSwapGenerator(token, shiftNeighbors=True, slurNeighbors=True))
        generators.append( self.shiftSwapGenerator(token))
        generators.append( self.neighborSwapGenerator(token, shiftNeighbors=True, slurNeighbors=True))
        generated_error = []
        for generator in generators:
            while True:
                try:
                    generated_error.append(generator.__next__())
                except StopIteration:
                    break
        return random.choice(generated_error)