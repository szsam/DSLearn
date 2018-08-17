import Utils.Helper as Helper
import warnings
warnings.filterwarnings(action='ignore',category=UserWarning,module='gensim')
import gensim


def get_word2vec_model(filename):
    model = gensim.models.KeyedVectors.load_word2vec_format(filename, binary=True)
    Helper.debug("[SUCCESS] Load Word2Vec Model From File: " + filename)
    return model


def str2vec(data_set):
    return NotImplemented
