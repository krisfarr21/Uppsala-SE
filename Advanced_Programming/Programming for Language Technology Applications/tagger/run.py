import argparse
import pickle

import yaml

from tagger import pre_process, model
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import pandas as pd

def run(args):
    pass
    mode = args.mode
    gold = args.gold
    with open(args.config, "r") as yaml_in:
        config = yaml.load(yaml_in)

    if mode == "train":
        print(f"Training a model on {config['train_file']}.")
        X, Y = pre_process.load_dataset(config["train_file"])
        X, Y = pre_process.prepare_data_for_training(X, Y)
        tagger = model.POSTagger()
        tagger.fit_and_report(X, Y, config["crossval"], config["n_folds"])
        tagger.save_model(config["model_file"])

    elif mode == "tag":
        print(f"Tagging text using pretrained model: {config['model_file']}.")
        with open(config["model_file"], "rb") as model_in:
            tagger = pickle.load(model_in)
        if args.text.endswith(".txt"): #if we pass a txt file to argparse
            with open (args.text,'r') as file:
                content = file.read()
            sentence = " ".join([space.rstrip() for space in content.splitlines() if space.strip()]) #remove empy lines
            tagged_sent = tagger.tag_sentence(sentence)
        else: #if we pass a simple sentence to argparse
            tagged_sent = tagger.tag_sentence(args.text)
        tokens_tags = "" 
        for token in tagged_sent:
            tokens_tags += (f"{token[0]}\t{token[1]}".expandtabs(15)) +"\n"
        with open(args.text+".tag", "w") as output: #save the tagged file in a new file
            output.write(tokens_tags)

    elif mode == "eval":
        print(f"Evaluating model on {args.gold}.") # gold file
        X, Y = pre_process.load_dataset(args.gold)
        y_true = [j for i in Y for j in i] # correct data (pos tags) for classification report
        print(f"Loading model from {config['model_file']}.")
        with open(config["model_file"], "rb") as model_in:
            tagger = pickle.load(model_in)
        all_words = [] # keep the word-tokens from X
        for sentence in X:
            for word in sentence: 
                all_words.append(word)
        tagged_sent = tagger.tag_sentence(all_words)
        y_pred = [] # test data (pos tags) for classification report
        for token in tagged_sent:
            y_pred.append(token[1]) # take second element of tuple
        matrix = confusion_matrix(y_true,y_pred)
        pos = [pos_tag for pos_tag in y_true]
        pos.append(pos_tag for pos_tag in y_pred)
        pos = pos.pop() # the last element of this list is an unknown object
        target_names = list(set(pos))
        report = classification_report(y_true, y_pred, target_names=target_names.sort())
        print(report)
          
    else:
        print(f"{args.mode} is an incompatible mode. Must be either 'train' or 'tag'.")



if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description="")

    PARSER.add_argument('--mode', metavar='M', type=str,
                        help="")
    ARGS = PARSER.parse_args()

    run(ARGS)
