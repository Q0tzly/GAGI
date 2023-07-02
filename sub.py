import os

def rm_all():
        dir = './date/original'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

rm_all()
