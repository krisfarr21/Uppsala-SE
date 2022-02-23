import spacy
import os, json
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import pandas as pd
import datetime
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import argparse




nlp = spacy.load("en_core_web_sm")	# load the language model and store it in the nlp variable

def vectorization(terms, path = None, title = None, output = None):

	if path == None:
		path = "./us_presidential_speeches/" 

	#listing all files in a directory with os.listdir and then finding only those that end in '.json'
	try:
		json_files = [pos_json for pos_json in os.listdir(path) if pos_json.endswith('.json')]
	except:
		print("Error! Directory does not exist.")
		sys.exit(1) # exit program

	#fit_transform method works with str, unicode or file objects, thus we store the data we need from json files to lists as str
	text = []
	time = []
	for file in json_files:
		with open(path+file, "r") as infile:
			speech = json.load(infile)
			text.append(speech["Speech"])
			time.append(speech["Date"])

	#create new format for the dates that will be included in the dataframe
	new_dates = [] 
	for date in time:
		date = datetime.datetime.strptime(date, '%B %d, %Y').strftime('%Y-%m-%d') 
		new_dates.append(date)



	############### VECTORIZER ############### 

	#account for unigrams,bigrams,trigrams and filter out stop words
	vectorizer = TfidfVectorizer(stop_words = 'english', ngram_range=(1,3)) 

	#Learn vocabulary and idf| return a Tf-idf-weighted document-term matrix. columns=features and rows=scores
	X = vectorizer.fit_transform(text, y=None) 
	
	Year = []
	Score = []
	Term = [] 

	for word in terms: # find the weight of the words we want
		for speeches in range(len(text)): # in every speech
			try:
				column_position = vectorizer.vocabulary_[word] # if you have the name of the term and you look for the column position of it at the tf-idf matrix 
			except:
				print("Error! Word(s) out of vocabulary.")
				sys.exit(1) 

			# feature name is converted to index: from column (term) choose all rows (the weight of this particular word in all speeches)
			choose_row = X[:,column_position].todense() 
			denselist = np.array(choose_row).flatten().tolist() # flatten the matrix to an 1d array (a simple list)
			Year.append(new_dates[speeches])
			Score.append(denselist[speeches])
			Term.append(word)
	data_frame = list(zip(Year,Score,Term))
	df = pd.DataFrame(data_frame,columns = ['Date','Score','Term'])

	return df


############### LINE PLOT ############### 


def visualization(terms, path = None, title = None, output = None):
	df = vectorization(terms, path = None, title = None, output = None)
	print(df)
	df['Date'] =pd.to_datetime(df['Date'], format = '%Y-%m-%d') # convert data from string format to object format
	df['Date'] = df['Date'].dt.year # keep year for x axes
	sns.set(style="whitegrid")
	g = sns.relplot(data=df, x="Date",y="Score",kind = "line",hue="Term", ci=None)

	if title == None:
		pass
	else:
		g.fig.suptitle(title) #create plot title
	if output == None:
		output_name = "_".join(terms).replace(" ", "_") # underscore concatenation
		plt.savefig(output_name + '.png') # save the file
	else:
		plt.savefig(output + '.png')


	


def Main():
	parser = argparse.ArgumentParser(description = "Visualization")
	parser.add_argument('--terms', type=str, nargs='+', metavar = " ", help="Given terms") 
	parser.add_argument('--path', type= str, metavar = " " , help="Speech directory") 
	parser.add_argument('--title', type=str, metavar = " " , help="Chart title")
	parser.add_argument('--output', type=str, metavar = " " , help="Plot png")
	args = parser.parse_args()
	if len(args.terms) > 5 or <1:
		parser.error("Maximum number of terms is 5 and at least 1.")
	vectorization(args.terms,args.path,args.title,args.output)
	visualization(args.terms,args.path,args.title,args.output)


if __name__ == '__main__':
	Main()