import random
import shutil
import os
import numpy as np
from PIL import Image
from src.ciede2000 import np_rgb_ciede2000, load_array, get_bd, get_sd


class GAGI:
    def __init__(self):
        #設定可能なパラメータ
        self.gen_num = 600      #世代の上限(2以上) (1000)
        self.img_n = 2**4       #世代ごとのimgの数(4以上) (2**8)
        self.e_img = 4          #世代ごとの選ばれるimgの数 (4)
        self.probability = 20   #変異確率(1 to 100) (5)
        self.cw = 1             #ciede2000の重み(0以上) (1)
        self.bw = 1             #明度の重み(0以上) (1)
        self.sw = 1             #彩度の重み(0以上) (1)
        self.img_x = 16         #imgの幅 (16)
        self.img_y = 16         #imgの高さ (16)
        self.teach_img = 'img/mario.jpg' #教師画像のpath ('img/mario.jpg)

        self.parameta_set = "d"
        self.gen = 0
        self.img_count = 0
        self.teach_score = 0
        self.score_ciede2000 = np.array([])
        self.score_b = np.array([])
        self.score_s = np.array([])
        self.score_number_ciede2000 = []
        self.score_list = []
        self.gen_score_list = np.array([])


    def main(self):
        print("こんにちは")
        self.put_text()


        self.rm_all()
        self.teach_score = self.load_teach()
        for self.gen in range(self.gen_num):
            print(str(self.gen) + 'gen')
            self.score_number_ciede2000.clear()
            self.score_ciede2000 = np.array([])
            self.score_b = np.array([])
            self.score_s = np.array([])
            self.score_number_ciede2000 = list(range(0, self.img_n, 1))
            self.img_count = 0

            for _ in range(self.img_n):
                random_array = self.load_random()
                score_ciede2000_tmp = 0
                score_ciede2000_tmp_add = 0
                score_b_tmp = 0
                score_b_tmp_add = 0
                score_s_tmp = 0
                score_s_tmp_add = 0
                for i in range(self.img_x):
                    for j in range(self.img_y):
                        rgb1 = load_array(self.teach_score, i, j)
                        rgb2 = load_array(random_array, i, j)
                        score_ciede2000_tmp = np_rgb_ciede2000(rgb1, rgb2)
                        score_b_tmp = get_bd(rgb1, rgb2)
                        score_s_tmp = get_sd(rgb1, rgb2)
                        score_ciede2000_tmp_add += score_ciede2000_tmp
                        score_b_tmp_add += score_b_tmp
                        score_s_tmp_add += score_s_tmp

                self.score_ciede2000 = np.append(self.score_ciede2000, [score_ciede2000_tmp_add])
                self.score_b = np.append(self.score_b, score_b_tmp_add)
                self.score_s = np.append(self.score_s, score_b_tmp_add)

            self.score_ciede2000 = self.score_ciede2000[:self.img_n]
            self.score_b = self.score_b[:self.img_n]
            self.score_s = self.score_s[:self.img_n]

            self.compete()
            self.delete_files('./data/tmp/', str(self.gen - 1))
            self.gen_next()

        self.finish()


    def put_text(self):
            print("あなたはパラメータのセットをすることができます")
            print("細部までパラメータをセットする場合は y")
            print("簡単にセットする場合は e")
            print("デフォルト設定を使いたい場合は d を打ってください")
            print("終了する場合は exit か C-c で終了できます")
            self.parameta_set = input(": ")
            print(" ")
            if self.parameta_set == "y":
                print("パラメータのセットアップを行います")
                print("画像のパス以外は半角数字で入力してください")
                print(" ")
                print("世代の上限(2以上)")
                self.gen_num = int(input(": "))
                print("世代ごとの画像の数(2以上)")
                self.img_n = int(input(": "))
                print("世代ごとに生き残る画像の数(1以上)")
                self.e_img = int(input(": "))
                print("変異確率(0 から 100) ")
                self.probability = int(input(": "))
                print("ciede2000の評価関数の重み(0以上)")
                self.cw = int(input(": "))
                print("明度の評価関数の重み(0以上)")
                self.bw = int(input(": "))
                print("彩度の評価関数の重み(0以上)")
                self.sw = int(input(": "))
                print(" ")
                print("画像の高さと幅は教師データと同じにすることを推奨します")
                print("画像の横の長さ")
                self.img_x = int(input(": "))
                print("画像の縦の長さ")
                self.img_y = int(input(": "))
                print("教師画像のパス")
                self.teach_img = str(input(": "))
                print("パラメータのセットを終了したので画像を生成します")
                print(" ")

            elif self.parameta_set == "e":
                print("簡単なパラメータのセットアップを行います")
                print("画像のパス以外は半角数字で入力してください")
                print(" ")
                print("世代の上限(2以上)")
                self.gen_num = int(input(": "))
                print("世代ごとの画像の数(2以上)")
                self.img_n = int(input(": "))
                print("世代ごとに生き残る画像の数(1以上)")
                self.e_img = int(input(": "))
                print("変異確率(0 から 100) ")
                self.probability = int(input(": "))
                print("パラメータのセットを終了したので画像を生成します")
                print(" ")

            elif self.parameta_set == "d":
                print("デフォルト設定で画像の生成を開始します")

            elif self.parameta_set == "exit":
                print("終了します")
                exit()

            else:
                self.put_text()


    def delete_files(self, directory, keyword):
    # ディレクトリ内のファイルを走査します
        for filename in os.listdir(directory):
            if keyword in filename:
                file_path = os.path.join(directory, filename)
                os.remove(file_path)


    def rm_all(self):
        dir1 = './data/original'
        for i in os.listdir(dir1):
            os.remove(os.path.join(dir1, i))

        dir2 = './data/gen'
        for j in os.listdir(dir2):
            os.remove(os.path.join(dir2, j))

        dir3 = './data/tmp/'
        for k in os.listdir(dir3):
            os.remove(os.path.join(dir3, k))

        dir3 = './data/final/'
        for l in os.listdir(dir3):
            os.remove(os.path.join(dir3, l))


    #教示画像を読み込む
    def load_teach(self):
        teach_array = np.array(Image.open(self.teach_img))
        return teach_array


    def load_random(self):
        if self.gen == 0:
            file_name = 'data/original/' + str(self.gen) + '_' + str(self.img_count) + '_ori.jpg'
            random_array = np.random.randint(0, 256, (self.img_x, self.img_y, 3)).astype(np.uint8)
            random_img = Image.fromarray(random_array)
            random_img.save(file_name)
        else:
            file_name = 'data/tmp/' + str(self.gen) +'_' + str(self.img_count) + '_gen.jpg'
            random_array = np.array(Image.open(file_name))

        self.img_count += 1
        return random_array


    def compete(self):
        score = []
        score_tmp = []
        score_i = []

        score_ciede2000 = self.score_ciede2000
        score_b = self.score_b / 2
        score_s = self.score_s

        score_tmp = (score_ciede2000 * self.cw + score_b * self.bw + score_s * self.sw)/2
        score_sorted_indices = np.argsort(score_tmp)  # score_tmp の要素を小さい順にソートし、インデックスを取得する
        score_sorted = score_tmp[score_sorted_indices]  # ソートされた score_tmp の要素を取得する
        score = score_sorted[:self.e_img]  # 上位4つの要素を取得する

        for s in score:
            index = np.where(score_tmp == s)[0][0]  # score_tmp における要素 s のインデックスを取得する
            score_i.append(index)

        self.score_ciede2000 = score
        self.score_number_ciede2000 = score_i

        for _ in range(len(self.score_ciede2000)):
            if self.gen == 0:
                for i in range(len(self.score_number_ciede2000)):
                    num = self.score_number_ciede2000[i]
                    file_name = str(self.gen) + '_' + str(num) + '_ori.jpg'
                    shutil.copyfile("./data/original/" + file_name, "./data/gen/" + file_name)

            else:
                for i in range(len(self.score_number_ciede2000)):
                    num = self.score_number_ciede2000[i]
                    file_name = str(self.gen) + '_' + str(num) + '_gen.jpg'
                    shutil.copyfile("./data/tmp/" + file_name, "./data/gen/" + file_name)

        print(self.score_ciede2000)
        print(self.score_number_ciede2000)
        print()


    def gen_next(self):
        if self.gen == 0:
            for n in range(self.img_n):
                image_array = np.zeros((self.img_x, self.img_y, 3), dtype=np.uint8)
                file_name = 'data/tmp/' + str(self.gen + 1) +'_' + str(n) + '_gen.jpg'
                for i in range(self.img_x):
                    for j in range(self.img_y):
                        m_probability = self.probability

                        if m_probability == 0:
                            choce_rgb = [random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256)]
                            image_array[i, j] = choce_rgb

                        else:
                            load_img_n = random.randint(0, len(self.score_number_ciede2000) - 1)
                            load_file_name = 'data/gen/' + str(self.gen) +'_' + str(self.score_number_ciede2000[load_img_n]) + '_ori.jpg'
                            random_array = np.array(Image.open(load_file_name))
                            rgb = load_array(random_array, i, j)
                            image_array[i, j] = rgb

                img = Image.fromarray(image_array)
                img.save(file_name)

        else:
            for n in range(self.img_n):
                image_array = np.zeros((self.img_x, self.img_y, 3), dtype=np.uint8)
                file_name = 'data/tmp/' + str(self.gen + 1) +'_' + str(n) + '_gen.jpg'
                for i in range(self.img_x):
                    for j in range(self.img_y):
                        m_probability = random.randint(0, 100)
                        if m_probability == 0:
                            choce_rgb = [random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256)]
                            image_array[i, j] = choce_rgb
                        else:
                            load_img_n = random.randint(0, len(self.score_number_ciede2000) - 1)
                            load_file_name = 'data/gen/' + str(self.gen) +'_' + str(self.score_number_ciede2000[load_img_n]) + '_gen.jpg'
                            random_array = np.array(Image.open(load_file_name))
                            rgb = load_array(random_array, i, j)
                            image_array[i, j] = rgb
                img = Image.fromarray(image_array)
                img.save(file_name)


    def finish(self):
        for i in range(len(self.score_number_ciede2000)):
            num = self.score_number_ciede2000[i]
            file_name = str(self.gen + 1) + '_' + str(num) + '_gen.jpg'
            shutil.copyfile("./data/tmp/" + file_name, "./data/final/" + file_name)
        print('finish')
        print(self.score_ciede2000)
        print(self.score_number_ciede2000)



GA = GAGI()
if __name__ == "__main__":
    GA.main()
