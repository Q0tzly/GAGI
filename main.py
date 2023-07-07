import random
import shutil
import os
import numpy as np
from PIL import Image
from src.ciede2000 import np_rgb_ciede2000, load_array


class GAGI:
    def __init__(self):
        self.gen = 0        #画像の世代
        self.gen_num = 10   #世代の上限
        self.img_n = 2**8   #8     世代ごとのimgの数
        self.img_count = 0  #一時的にimgの数をカウントする
        self.img_x = 16     #imgの幅
        self.img_y = 16     #imgの高さ
        self.score_ciede2000 = np.array([])     #ciede2000に通した後のimgのリスト
        self.score_number_ciede2000 = []    #ciede2000に通した後のimgの番号のリスト
        self.score_list = []    #fn competeに通した後のimgのリスト(4つ)
        self.gen_score_list = np.array([])


    def main(self):
        self.rm_all()   #まず、originalないにある画像を全て消す

        for self.gen in range(self.gen_num):
            self.score_number_ciede2000.clear()
            self.score_ciede2000 = np.array([])
            print(self.score_number_ciede2000)
            self.score_number_ciede2000 = list(range(0, self.img_n, 1))     #self.score_number_ciede2000のリストの中を 0 to self.img_n とする
            print(self.score_number_ciede2000)
            self.img_count = 0

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
            self.gen_next()
            print(self.gen)

        self.finish()


    #original内の画像をrmする
    def rm_all(self):
        dir1 = './date/original'
        for i in os.listdir(dir1):
            os.remove(os.path.join(dir1, i))

        dir2 = './date/gen'
        for j in os.listdir(dir2):
            os.remove(os.path.join(dir2, j))

        dir3 = './date/tmp/'
        for k in os.listdir(dir3):
            os.remove(os.path.join(dir3, k))

        dir3 = './date/final/'
        for l in os.listdir(dir3):
            os.remove(os.path.join(dir3, l))


    #教示画像を読み込む
    def load_teach(self):
        teach_array = np.array(Image.open('source/mario.jpg'))
        return teach_array


    #self.genによって、画像をランダム生成するか、画像を読み込むか決める　一回につき、一つの画像を読み込む -> return
    def load_random(self):
        if self.gen == 0:
            file_name = 'date/original/' + str(self.gen) + '_' + str(self.img_count) + '_ori.jpg'
            random_array = np.random.randint(0, 256, (self.img_x, self.img_y, 3)).astype(np.uint8)
            random_img = Image.fromarray(random_array)
            random_img.save(file_name)
        else:
            file_name = 'date/tmp/' + str(self.gen) +'_' + str(self.img_count) + '_gen.jpg'
            random_array = np.array(Image.open(file_name))

        self.img_count += 1
        return random_array


    #self.score_ciede2000 のリストより。２つずつ値を取得して、self.score_number_ciede2000に代入する
    def compete(self):
        while len(self.score_ciede2000) > 4:
            score_tmp = []
            score_number_tmp = []

            score_1 = self.score_ciede2000[0]
            score_2 = self.score_ciede2000[1]
            self.score_ciede2000 = np.delete(self.score_ciede2000, [0, 1])
            result_min = min(score_1, score_2)
            score_tmp.append(result_min)

            print(self.score_number_ciede2000)
            print(self.score_ciede2000)

            if score_1 == result_min:
                score_number_tmp = self.score_number_ciede2000.pop(0)
                del self.score_number_ciede2000[1]
            else:
                score_number_tmp = self.score_number_ciede2000.pop(1)
                del self.score_number_ciede2000[0]

            self.score_ciede2000 = np.append(self.score_ciede2000, score_tmp)
            self.score_number_ciede2000.append(score_number_tmp)

            if self.gen == 0:
                for i in range(len(self.score_number_ciede2000)):
                    num = self.score_number_ciede2000[i]
                    print(num)
                    file_name = str(self.gen) + '_' + str(num) + '_ori.jpg'
                    shutil.copyfile("./date/original/" + file_name, "./date/gen/" + file_name)

            else:
                for i in range(len(self.score_number_ciede2000)):
                    num = self.score_number_ciede2000[i]
                    print(num)
                    file_name = str(self.gen) + '_' + str(num) + '_gen.jpg'
                    shutil.copyfile("./date/tmp/" + file_name, "./date/gen/" + file_name)


    def gen_next(self):
        if self.gen == 0:
            for n in range(self.img_n):
                image_array = np.zeros((16, 16, 3), dtype=np.uint8)
                file_name = 'date/tmp/' + str(self.gen + 1) +'_' + str(n) + '_gen.jpg'
                for i in range(16):
                    for j in range(16):
                        m_probability = random.randint(0, 100)
                        if m_probability == 0:
                            choce_rgb = [random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256)]
                            image_array[i, j] = choce_rgb
                        else:
                            load_img_n = random.randint(0, 3)
                            load_file_name = 'date/gen/' + str(self.gen) +'_' + str(self.score_number_ciede2000[load_img_n]) + '_ori.jpg'
                            random_array = np.array(Image.open(load_file_name))
                            rgb = load_array(random_array, i, j)
                            image_array[i, j] = rgb
                img = Image.fromarray(image_array)
                img.save(file_name)

        else:
            for n in range(self.img_n):
                image_array = np.zeros((16, 16, 3), dtype=np.uint8)
                file_name = 'date/tmp/' + str(self.gen + 1) +'_' + str(n) + '_gen.jpg'
                for i in range(16):
                    for j in range(16):
                        m_probability = random.randint(0, 100)
                        if m_probability == 0:
                            choce_rgb = [random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256)]
                            image_array[i, j] = choce_rgb
                        else:
                            load_img_n = random.randint(0, 3)
                            load_file_name = 'date/gen/' + str(self.gen) +'_' + str(self.score_number_ciede2000[load_img_n]) + '_gen.jpg'
                            random_array = np.array(Image.open(load_file_name))
                            rgb = load_array(random_array, i, j)
                            image_array[i, j] = rgb
                img = Image.fromarray(image_array)
                img.save(file_name)

    def finish(self):
        for i in range(len(self.score_number_ciede2000)):
            num = self.score_number_ciede2000[i]
            print(num)
            file_name = str(self.gen) + '_' + str(num) + '_gen.jpg'
            shutil.copyfile("./date/tmp/" + file_name, "./date/final/" + file_name)
        print('finish')



GA = GAGI()
if __name__ == "__main__":
    GA.main()
