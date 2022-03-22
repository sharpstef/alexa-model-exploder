# Alexa Language Model Exploder
Takes in a language model in any language and outputs a file with filled utterances for intents that are not AMAZON built-in. Reformats utterances to lowercase, remove some unnecessary punctuation (keeps apostophes and periods). Skips AMAZON built-in slots. 

It is recommended that you review output to remove any grammatically incorrect utterances post processing. 

## To Run
```
python model_exploder.py myModel.json
```

## Output
csv file with two columns (utterance and intent)


## Notes
- Skips AMAZON built-in intents
- Skips utterances with AMAZON built-in slots
- Reformats utterances to remove most punctuation (excluding . and ')
- Reformats utterances to lowercase
- Assumes that JSON is formatted in standard custom skill format

## Bugs, issues and enhancements  

This project is presented as-is. 


## License  
  
The QR Code APL Skill is under the [Apache License 2.0](https://github.com/sharpstef/alexa-model-exploder/blob/main/LICENSE.txt).  