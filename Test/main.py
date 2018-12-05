import Core.NN as NN
from Utils.Preprocessor import Preprocessor
import Utils.Meta as Meta

if __name__ == '__main__':
    p = Preprocessor()
    X, Y = p.load_data([
        '../DataSet/BarackObama.csv',
        '../DataSet/DonaldTrumpTweets'
    ], Meta.max_string_len)
    model = NN.train(X, Y)
    model.save('../Model/model')
