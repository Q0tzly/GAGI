import random
import os
import numpy as np
from PIL import Image
from src.ciede2000 import np_rgb_ciede2000, load_array


class GAGI:
    def __init__(self):
        self.gen = 0
        self.img_n = 2**10
        self.img_count = 0
        self.img_x = 16
        self.img_y = 16
        self.score_ciede2000 = np.array([])
        self.score_list = []

    def main(self):
        self.rm_all()

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
        print(self.score_ciede2000)

        self.compete_score()
        print(self.score_list)

    def rm_all(self):
        dir = './date/original'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))


    def load_teach(self):
        teach_array = np.array(Image.open('source/mario.jpg'))
        return teach_array


    '''
    def load_random(self):
        img_count = 0
        for img_count in range(self.img_n):
            if self.gen == 0:
                file_name = 'date/original/' + str(self.gen) + '_' + str(img_count) + 'ori_img.jpg'
                random_array = np.random.randint(0, 256, (self.img_x, self.img_y, 3)).astype(np.uint8)
                random_img = Image.fromarray(random_array)
                random_img.save(file_name)
            else:
                file_name = 'date/gen/' + str(self.gen) +'_' + str(self.img_count) + '_gen.jpg'
                random_array = np.array(Image.open(file_name))
            img_count += 1

        return random_array

    '''


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




    def compete_score(self):
        while len(self.score_ciede2000) >= 4:
            score_tmp = []
            for _ in range(2):
                score_1 = self.score_ciede2000[0]
                score_2 = self.score_ciede2000[1]
                self.score_ciede2000 = np.delete(self.score_ciede2000, [0, 1])
                score_tmp.append(min(score_1, score_2))

            self.score_ciede2000 = np.append(self.score_ciede2000, score_tmp)

        self.score_list = self.score_ciede2000[:4]
        if len(self.score_list) < 4 and len(self.score_ciede2000) >= 2:
            self.score_list = np.append(self.score_list, self.score_ciede2000[:2])
            self.score_ciede2000 = self.score_ciede2000[2:]

        if len(self.score_list) < 4:
            print("Not enough scores to compete.")

        self.score_ciede2000 = np.array(self.score_ciede2000)
        self.score_list = np.array(self.score_list)


GA = GAGI()
if __name__ == "__main__":
    GA.main()
