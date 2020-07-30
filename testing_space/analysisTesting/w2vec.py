import gensim, logging
import os




class SentenceParser():

	def __init__(self, dirname):
		self.sourcedir = dirname
	
	
	def __iter__(self):
		for fname in os.listdir(self.sourcedir):
			for line in open(os.path.join(self.sourcedir, fname)):
				yield line.split()
				





sentences = SentenceParser('./files/')

#min count is a cut off for word counts. For this small example we use 1 because it is a single abstract.
model = gensim.models.Word2Vec(sentences, min_count=1)

print(model.similarity('adversarial', 'victim'))


model.save('./tmp/word2vec.model')