This file was built upon the concept of modular programming, each file containing a component of the part of speech
tagger which are then consolidated in the run.py file.

-----
Files
-----

(i) pre_process.py -> It contains the necessary functions to load data from text and .conllu files and to
to prepare data for training purposes. Make sure that your files are in the correct or else the functions
will not work. Furthermore, it includes a feature engineering function to improve the classification
matrix accuracy. 

(ii) model.py -> Through this file, the ML model can be modified by changing the attribute in the POSTagger
constructur. The other methods allow the possibility to fit the data and output execute a cross validation
report, to save model and to tag both non-vectorized and vectorized sentences, depending on your desired format.

(iii) run.py --> Finally, run.py consolidates together the methods found in the above files. Through this file,
data can be trained, tagged and evaluated by using CMDs as the following:

--------
Commands
--------

TRAIN: pythonX run.py --mode train [train_file] --config config.yaml

pythonX --> use your installed version (e.g. python3) [if this does not work, use 'python' only]
train_file --> this file can be configured through config.yaml (.txt or .conllu file); [train_file] can be left out
if file is configured

- A 5-fold cross-validation result should be outputted. The number of folds can be changed through model.py.

TAG: pythonX run.py --mode tag --text [your_file.txt] -- config.yaml

pythonX --> use your installed version (e.g. python3) [if this does not work, use 'python' only]
your_file --> any file in .txt format

Tagged data can be saved by adding '> name.txt' at the end of the command.

EVAL: pythonX run.py --mode eval --gold your_gold_file --config config.yaml

pythonX --> use your installed version (e.g. python3) [if this does not work, use 'python' only]
your_gold_file --> .txt or .conllu file (check format)

- A classification matrix should be outputted. Different models can be used to test different results. The Logistic
Regression and Multinomial Naive Bayes models were used in our tests, both providing worse results than the Linear
Support Vector Classification model.






