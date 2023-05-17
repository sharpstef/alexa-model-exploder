"""
 Language Model Exploder
 Author: Stefania Sharp
 Last Updated: 4/14/2022

 To Run: python model_exploder.py myModel.json
 Output: csv file with two columns (utterance and intent)
 
 Takes in a language model in any language and outputs a file with 
 filled utterances for intents that are not AMAZON built-in. Reformats 
 utterances to lowercase, remove some unnecessary punctuation 
 (keeps apostophes and periods). Skips AMAZON built-in slots. 

 It is recommended that you review output to remove any grammatically 
 incorrect utterances post processing. 
"""
#!/usr/bin/python

import itertools
import json
import os
import re
import sys


def importJSON(input):
    try:                                                                           
        data = json.load(input)

        if "interactionModel" in data and "languageModel" in data["interactionModel"]:
            return data["interactionModel"]
        else:                                               
            print("Input file is not a supported Alexa language model. Must contain attributes interactionModel and languageModel.")     
            return None    

    except ValueError:                        
        print("Invalid format. Input file must be JSON.")                                                        
        return None 

def formatLine(line):
    line = re.sub(r"[^\w\d'.\-\s]+",'', line) 
    line = line.lower()
    line = line.rstrip()
    return line

def compressSlots(data):
    # Compress the slots down into arrays
    if "types" in data and len(data["types"]) > 0:
        slots = {}

        for type in data["types"]:
            slotName = type["name"]
            slots[slotName] = []
            for value in type["values"]:
                # Add the synonyms and the value
                if "value" in value["name"]:
                    slots[slotName].append(value["name"]["value"])

                if "synonyms" in value["name"]:
                    slots[slotName] = slots[slotName] + value["name"]["synonyms"]

        return slots

def main():
    # Get name of json file from args
    if len(sys.argv) < 2:
        print("No file provided. Please supply a JSON file when invoking the script.")
        exit()

    fileName = sys.argv[1]
    print("File to be expanded: "+fileName)

    # Read file in
    inputFile = open(sys.argv[1])
    data = importJSON(inputFile)
    if data == None:
        exit()
    inputFile.close()

    # Open the output file for writing
    outFileName = fileName.replace('.json', '') + "_expanded.csv"
    if os.path.exists(outFileName):
        os.remove(outFileName)
    outputFile = open(outFileName,"a")

    data = data["languageModel"]
    # Object to hold all of the utterances for each intent
    slots = compressSlots(data)

    # Go through each intent and expand the utterances. Skip intents with Amazon built-in slots.
    for intent in data["intents"]:
        if len(intent["samples"]) > 0 and "AMAZON." not in intent["name"]:

            # Prep data holders
            name = intent["name"]

            # Find all Amazon slots for intent to skip utterances that contain them
            amazonSlots = []
            customSlots = []
            for slot in intent["slots"]:
                if "AMAZON." in slot["type"]:
                    amazonSlots.append("{"+slot["name"]+"}")
                else:
                    customSlots.append(slot["name"])

            # Loop through utterances and fill the slots
            for utterance in intent["samples"]:
                regex = r"\{(.*?)\}"

                # Skip any utterance that has an Amazon built-in
                if not any(x in utterance for x in amazonSlots):

                    # Prep slots for itertools for this utterance
                    localSlots = []
                    matches = re.findall(regex,utterance)

                    # Check if utterance has no slots
                    if len(matches) < 1:
                        utterance = formatLine(utterance)
                        outputFile.write(utterance+","+name+"\n")
                    else:
                        for slot in re.findall(regex, utterance):
                            # Slot names do not always match slot types, get the type to compare with stored
                            slotName = next((x for x in intent["slots"] if x["name"] == slot), None)
                            if slotName != None:
                                localSlots.append(slots[slotName["type"]])

                        # Create combinations of slots within utterance
                        for localValues in list(itertools.product(*localSlots)):
                            temp = utterance
                            for n in range(len(localValues)):
                                temp = re.sub(regex, localValues[n], temp, 1)
                    
                            # Print the utterance to file
                            temp = formatLine(temp)
                            outputFile.write(temp+","+name+"\n")

    outputFile.close()

if __name__ == "__main__":
    main()
