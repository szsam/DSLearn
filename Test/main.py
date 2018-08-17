import Utils.Preprocessor as Preprocessor
import Utils.Meta as Meta
import Core.NN as NN


if __name__ == "__main__":
    # words_path = "../DataSet/Friends-Corpus/friends-final-modified.txt"
    # model_path = "../DataSet/GoogleNews-vectors-negative300-SLIM.bin"

    p = Preprocessor.Preprocessor()
    X, Y = p.load_data(max_len=Meta.max_string_len)
    model = NN.train(X, Y)
    model.save('../Model/model')
