import os

def rm_all():
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
rm_all()
