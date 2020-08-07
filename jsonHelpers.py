# pylint: disable=W0614
import sys
import json
import random
from helper import *
from itertools import combinations
import copy


def jsonRandomTyped(jsonInput: dict, key_set: list):
    ''' Mutates values of each combination in the input to random values according to input value types '''
    output = []

    for i in range(6):
        for subset in key_set:
            mutatedJson = copy.deepcopy(jsonInput)
            for key in subset:
                # find value type and generate random value according to that
                val = jsonInput[key]
                val = valGenerateTyped(val, i + 2)

                mutatedJson[key] = val

            output.append(mutatedJson)
    return output


def fuzzJSON(sampleInputFile, binary, lock):

    print("Fuzzing the JSON formatted sample input...\n", end="")

    key_set = []

    sampleInputFile.seek(0)
    jsonInput = sampleInputFile.read()
    jsonInput = json.loads(jsonInput)

    choices = list(jsonInput.keys())

    for i in range(1, len(choices) + 1):
        for combs in combinations(choices, i):
            key_set.append(combs)

    # attempt to fuzz 3 times
    for _ in range(3):
        mutations = jsonRandomTyped(jsonInput, key_set)
        for i in mutations:
            if sendInputAndCheck(binary, json.dumps(i), lock):
                return True, "Found vulnerability in JSON!"
    return False


if __name__ == "__main__":
    # for testing
    fuzzJSON(open("./binaries/json1.txt", "r"), "./binaries/json1")
