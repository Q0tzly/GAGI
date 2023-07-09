import os

def rm_all():
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
rm_all()
