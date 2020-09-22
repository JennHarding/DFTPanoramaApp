from music21 import corpus
import os

# print(os.getcwd())
music21_mozart_corpus = ['mozart/k155/movement1.mxl', 'mozart/k156/movement1.mxl', 
                  'mozart/k458/movement1.mxl']

music21_bach_corpus = ['bach/bwv244.10.mxl', 'bach/bwv244.15.mxl', 'bach/bwv244.17.mxl', 'bach/bwv244.25.mxl', 'bach/bwv244.3.mxl']

music21_beethoven_corpus = ['beethoven/opus18no1/movement1.mxl', 'beethoven/opus18no1/movement2.mxl', 'beethoven/opus18no1/movement3.mxl', 'beethoven/opus18no1/movement4.mxl']

# music21_corpus = music21_mozart_corpus + music21_bach_corpus + music21_beethoven_corpus

corpus = 'C:\\Users\\jennd\\Documents\\Dissertation\\FilesForAnalysis\\'

CRIM_corpus = 'C:\\Users\\jennd\\Desktop\\CRIM\\'

# print(os.listdir(corpus))

moz = 'Moz_SQs\\'
mess = 'Messiaen\\'
harb = 'Harbison\\'
mei = 'MEI\\'
elvis = 'ELVIS\\'
test = 'TestScores\\'
micro = 'Microtonal\\'

mozSQs = [x for x in os.listdir(corpus+moz)]
mess_misc = [x for x in os.listdir(corpus+mess)]
harbs = [x for x in os.listdir(corpus+harb)]
# meis = [x for x in os.listdir(corpus+mei)]
# tests = [x for x in os.listdir(corpus+test)]
# elvis_corpus = [x for x in os.listdir(corpus+elvis)]
CRIM = [x for x in os.listdir(CRIM_corpus)]
micros = [x for x in os.listdir(corpus+micro)]

# full_corpus = mozSQs + music21_corpus + mess_misc + harbs + meis + tests

# full_corpus = mozSQs + mess_misc + elvis_corpus + tests + meis

# full_corpus = CRIM 

full_corpus = mozSQs + mess_misc + micros + harbs