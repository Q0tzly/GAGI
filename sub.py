import os

def rm_all():
    dir1 = './date/original'
    for i in os.listdir(dir1):
        os.remove(os.path.join(dir1, i))

    dir2 = './date/draw'
    for j in os.listdir(dir2):
        os.remove(os.path.join(dir2, j))
rm_all()
