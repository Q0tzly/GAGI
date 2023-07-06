import random
import os
import numpy as np
from PIL import Image
from src.ciede2000 import np_rgb_ciede2000, load_array


class GAGI:
    def __init__(self):
        self.gen = 0        #画像の世代
        self.img_n = 2**4   #10     世代ごとのimgの数
        self.img_count = 0  #一時的にimgの数をカウントする
        self.img_x = 16     #imgの幅
        self.img_y = 16     #imgの高さ
        self.score_ciede2000 = np.array([])     #ciede2000に通した後のimgのリスト
        self.score_number_ciede2000 = []    #ciede2000に通した後のimgの番号のリスト
        self.score_list = []    #fn competeに通した後のimgのリスト(4つ)
        self.score_number = []  #fn competeに通した後のimgの番号のリスト(４つ)
        self.gen_score_list = []

    def main(self):
        self.rm_all()   #まず、originalないにある画像を全て消す
        self.score_number_ciede2000 = list(range(0, self.img_n, 1))     #self.score_number_ciede2000のリストの中を 0 to self.img_n とする

        #load.teach(), random_array より取得したものを ciede2000 に通すのを、 img_n 回実行して、その全てを self.score_ciede2000 に代入する -> self.score_ciede2000
        for _ in range(self.img_n):
            teach_array = self.load_teach()
            random_array = self.load_random()
            score_tmp = 0
            score_tmp_add = 0
            for i in range(16):
                for j in range(16):
                    rgb1 = load_array(teach_array, i, j)
                    rgb2 = load_array(random_array, i, j)
                    score_tmp = np_rgb_ciede2000(rgb1, rgb2)
                    score_tmp_add += score_tmp
            self.score_ciede2000 = np.append(self.score_ciede2000, [score_tmp_add])

        #compete_score() により、self.score_ciede2000 から２つずつとって、それを競争させて、self.gen_score_list に入れる
        self.compete()

    #original内の画像をrmする
    def rm_all(self):
        dir = './date/original'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))


    #教示画像を読み込む
    def load_teach(self):
        teach_array = np.array(Image.open('source/mario.jpg'))
        return teach_array


    #self.genによって、画像をランダム生成するか、画像を読み込むか決める　一回につき、一つの画像を読み込む -> return
    def load_random(self):
        if self.gen == 0:
            file_name = 'date/original/' + str(self.gen) + '_' + str(self.img_count) + 'ori_img.jpg'
            random_array = np.random.randint(0, 256, (self.img_x, self.img_y, 3)).astype(np.uint8)
            random_img = Image.fromarray(random_array)
            random_img.save(file_name)
        else:
            file_name = 'date/gen/' + str(self.gen) +'_' + str(self.img_count) + '_gen.jpg'
            random_array = np.array(Image.open(file_name))

        self.img_count += 1
        return random_array


    #self.score_ciede2000 のリストより。２つずつ値を取得して、self.score_number_ciede2000に代入する
    def compete(self):
        while len(self.score_ciede2000) >= 4:
            score_tmp = []
            score_number_tmp = []
            for _ in range(2):
                score_1 = self.score_ciede2000[0]
                score_2 = self.score_ciede2000[1]
                self.score_ciede2000 = np.delete(self.score_ciede2000, [0, 1])
                result_min = min(score_1, score_2)
                score_tmp.append(result_min)

                print(score_1)
                print()
                print(score_2)
                print()
                print(result_min)

                if score_1 == result_min:
                    score_number_tmp = self.score_number_ciede2000.pop(0)
                    del self.score_number_ciede2000[1]
                else:
                    score_number_tmp = self.score_number_ciede2000.pop(1)
                    del self.score_number_ciede2000[0]

            self.score_ciede2000 = np.append(self.score_ciede2000, score_tmp)

            self.score_number_ciede2000.append(score_number_tmp)

            print(score_number_tmp)
            print(self.score_number_ciede2000)

        self.score_list = self.score_ciede2000[:4]
        self.score_number = self.score_number_ciede2000[:4]

        if len(self.score_list) < 4 and len(self.score_ciede2000) >= 2:
            self.score_list = np.append(self.score_list, self.score_ciede2000[:2])
            self.score_ciede2000 = self.score_ciede2000[2:]

        if len(self.score_list) < 4:
            print("Not enough scores to compete.")

        self.score_ciede2000 = np.array(self.score_ciede2000)
        self.score_list = np.array(self.score_list)

    '''
    def gen_next():
        choce_num = random.randrange(0, 3)
        load_array(self.score_list, )
    '''


GA = GAGI()
if __name__ == "__main__":
    GA.main()
