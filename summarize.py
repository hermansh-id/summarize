import re
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np


def word_freq(sentence, stop_words, all_words):
    words = word_tokenize(sentence)
    freq = {}
    for word in words:
        if word.lower() not in stop_words:
            if word in freq:
                freq[word] += 1
            else:
                freq[word] = 1
    max_freq = max(freq.values())
    for word in freq.keys():
        freq[word] /= max_freq
    return [freq.get(word, 0) for word in all_words]


def pagerank(similarity_matrix, eps=1.0e-8, d=0.85):
    N = similarity_matrix.shape[0]
    v = np.ones(N) / N
    while True:
        v_old = np.copy(v)
        for i in range(N):
            v[i] = (1 - d) + d * np.sum(similarity_matrix[i, :]
                                        * v_old) / np.sum(similarity_matrix[i, :])
        if np.abs(v - v_old).max() < eps:
            break
    return v


def summarize(text, n=3):
    stop_words = set(stopwords.words('indonesian'))
    sentences = sent_tokenize(text)
    clean_sentences = [re.sub(r'\W', ' ', s) for s in sentences]
    clean_sentences = [re.sub(r'\s+', ' ', s) for s in clean_sentences]
    all_words = set(
        [word.lower() for sentence in clean_sentences for word in word_tokenize(sentence)])
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                similarity_matrix[i][j] = cosine_distance(word_freq(
                    clean_sentences[i], stop_words, all_words), word_freq(clean_sentences[j], stop_words, all_words))
    sentence_scores = pagerank(similarity_matrix)
    ranked_sentences = [(score, i) for i, score in enumerate(sentence_scores)]
    ranked_sentences = sorted(ranked_sentences, reverse=True)
    summary_sentences = []
    for i in range(n):
        index = ranked_sentences[i][1]
        summary_sentences.append(sentences[index])
    summary = ' '.join(summary_sentences)
    return summary
