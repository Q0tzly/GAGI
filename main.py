import random
import shutil
import os
import numpy as np
from PIL import Image
from src.ciede2000 import np_rgb_ciede2000, load_array


class GAGI:
    def __init__(self):
        #設定可能なパラメータ
        self.gen_num = 1000     #世代の上限(2以上)
        self.img_n = 2**8       #世代ごとのimgの数(4以上)
        self.probability = 1    #変異確率(1 to 100)
        self.img_x = 50         #imgの幅
        self.img_y = 50         #imgの高さ
        self.teach_img = 'img/kinopio.jpg' #教師画像のpath

        self.gen = 0
        self.img_count = 0
        self.score_ciede2000 = np.array([])
        self.score_number_ciede2000 = []
        self.score_list = []
        self.gen_score_list = np.array([])


    def main(self):
        self.rm_all()
        for self.gen in range(self.gen_num):
            print(str(self.gen) + 'gen')
            self.score_number_ciede2000.clear()
            self.score_ciede2000 = np.array([])
            self.score_number_ciede2000 = list(range(0, self.img_n, 1))
            self.img_count = 0

            for _ in range(self.img_n):
                teach_array = self.load_teach()
                random_array = self.load_random()
                score_tmp = 0
                score_tmp_add = 0
                for i in range(self.img_x):
                    for j in range(self.img_y):
                        rgb1 = load_array(teach_array, i, j)
                        rgb2 = load_array(random_array, i, j)
                        score_tmp = np_rgb_ciede2000(rgb1, rgb2)
                        score_tmp_add += score_tmp
                self.score_ciede2000 = np.append(self.score_ciede2000, [score_tmp_add])

            self.compete()
            self.gen_next()

        self.finish()


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
        teach_array = np.array(Image.open(self.teach_img))
        return teach_array


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


    def compete(self):
        while len(self.score_ciede2000) > 4:
            score_tmp = []
            score_number_tmp = []

            score_1 = self.score_ciede2000[0]
            score_2 = self.score_ciede2000[1]
            self.score_ciede2000 = np.delete(self.score_ciede2000, [0, 1])
            result_min = min(score_1, score_2)
            score_tmp.append(result_min)

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
                    file_name = str(self.gen) + '_' + str(num) + '_ori.jpg'
                    shutil.copyfile("./date/original/" + file_name, "./date/gen/" + file_name)

            else:
                for i in range(len(self.score_number_ciede2000)):
                    num = self.score_number_ciede2000[i]
                    file_name = str(self.gen) + '_' + str(num) + '_gen.jpg'
                    shutil.copyfile("./date/tmp/" + file_name, "./date/gen/" + file_name)
        print(self.score_ciede2000)
        print(self.score_number_ciede2000)
        print()


    def gen_next(self):
        if self.gen == 0:
            for n in range(self.img_n):
                image_array = np.zeros((self.img_x, self.img_y, 3), dtype=np.uint8)
                file_name = 'date/tmp/' + str(self.gen + 1) +'_' + str(n) + '_gen.jpg'
                for i in range(self.img_x):
                    for j in range(self.img_y):
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
                image_array = np.zeros((self.img_x, self.img_y, 3), dtype=np.uint8)
                file_name = 'date/tmp/' + str(self.gen + 1) +'_' + str(n) + '_gen.jpg'
                for i in range(self.img_x):
                    for j in range(self.img_y):
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
            file_name = str(self.gen) + '_' + str(num) + '_gen.jpg'
            shutil.copyfile("./date/tmp/" + file_name, "./date/final/" + file_name)
        print('finish')
        print(self.score_ciede2000)
        print(self.score_number_ciede2000)



GA = GAGI()
if __name__ == "__main__":
    GA.main()
