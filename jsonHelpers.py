# pylint: disable=W0614
import sys
import json
import random
from helper import *
from itertools import combinations


def jsonRandomTyped(jsonInput: dict, key_set: list):
    ''' Mutates values of each combination in the input to random values according to input value types '''
    output = []

    for i in range(14):
        for subset in key_set:
            mutatedJson = jsonInput
            for key in subset:
                # find value type and generate random value according to that
                val = jsonInput[key]
                val = valTypeCheck(val, i)

                mutatedJson[key] = val

            output.append(mutatedJson)
    return output

def fuzzJSON(sampleInputFile, binary):

    print("Fuzzing the JSON formatted sample input...\n", end="")

    key_set = []

    sampleInputFile.seek(0)
    jsonInput = sampleInputFile.read()
    jsonInput = json.loads(jsonInput)

    choices = list(jsonInput.keys())

    for i in range(1, len(choices) + 1):
        for combs in combinations(choices, i):
            key_set.append(combs)

    mutations = jsonRandomTyped(jsonInput, key_set)
    for i in mutations:
        sendInputAndCheck(binary,json.dumps(i),"Found vulnerability in JSON!")

if __name__ == "__main__":
    # for testing
    fuzzJSON(open("./binaries/json1.txt", "r"), "./binaries/json1")