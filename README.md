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