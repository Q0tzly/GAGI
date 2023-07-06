import numpy as np

score_ciede2000 = np.array([0, 1, 2, 3])
score_tmp = [4, 5]
score_number_ciede2000 = [0, 1, 2, 3]
score_number_tmp = 4

score_ciede2000 = np.append(score_ciede2000, score_tmp)
score_number_ciede2000.append(score_number_tmp)

print(score_ciede2000)
print(score_number_ciede2000)
