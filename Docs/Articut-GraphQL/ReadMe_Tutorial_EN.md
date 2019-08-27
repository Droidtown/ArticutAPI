### Complete Guide to Articut-Graphql

**Articut-GraphQL** is an alternative of [spaCy](https://spacy.io/) spaCy for Chinse text in the Python Natural Language Processing environment and aims to become the de facto library for Chinese NLP tasks. There are some really good reasons for its popularity:

#### Easy to use
Written in Pure Python (**version 3.6.1+**), one can easily get a copy of it from the project page[ project page](https://github.com/Droidtown/ArticutAPI)  on Github.

#### ACCURATE
Chinese language lacks of affixes indicating the lexical POS, the syntax of the sentence plays an important role in determining the POS of each word. Since Articut Chinese Word Segmentation (CWS) system is driven by syntactica structure, it's POS accuracy is one of the leading solutions in Chinese NLP tools.

#### Batteries included
Index preserving tokenization (details about this later)
Part Of Speech tagging (POS), 
Named Entity Recognition (NER),
Focus on Chinese language,
Easy and understandable visualizations

#### Extensible with Machine Learning (or DeepLearning) tools
If you like, Articut-GraphQL can be easily fused with mainstream machine learning tools such Scikit-Learn, TensorFlow, gensim among others.

***

### Quickstart

#### Installation
Na, Articut-GrahQL does not require installation. Just `git clone` a copy of your own:

`git clone https://github.com/Droidtown/ArticutAPI.git`

 Then you are ready to rock & roll.

#### Prepare text and save it locally.
	from ArticutAPI import Articut
	import json
		
	articut = Articut()
	inputSTR = "會被大家盯上，才證明你有實力。" #Put your Chinese text here.
	result = articut.parse(inputSTR)
	with open ("articutResult.json", "w", encoding="utf-8") as aFILE:
	    json.dump(result, aFILE, ensure_ascii=False)

#### Load the processed text to Articut-GraphQL
	from ArticutAPI import Articut
	from pprint import pprint
	import json
	graphQLResult = articut.graphQL.query(
	    filePath="articutResult.json",
	    query="""
		{
		  meta {
		    lang
		    description
		  }
		  doc {
		    text
		    tokens {
		      text
		      pos_
		      tag_
		      isStop
		      isEntity
		      isVerb
		      isTime
		      isClause
		      isKnowledge
		    }
		  }
		}""")
	pprint(graphQLResult)

 ***
### Conclusions

Articut-GraphQL is a modern, reliable NLP tool for doing NLP with Python. WIth the GraphQL and commandline duel interface, It can act as the central part of your production NLP pipeline.