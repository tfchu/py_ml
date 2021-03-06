'''
Question: Binary classification
Given Pokemons: x1, x2, x3..., each represented by a vector of features
Feature vector: [attack, sp_atk], i.e. [[x1_1, x1_2], [x2_1, x2_2], ...]. 
Type: WATER (Class 1 or C1), NORMAL (Class 2 or C2)
Calculate P(C1|x), i.e. given a new Pokemon x, what is the probability of being type WATER? 

Assumption
P(x|C): given a Class (e.g. WATER type), the locations of the Pokemons follow Gaussian distribution

Steps
1. Web scraping pulls Pokemon data from a website. Then declare the training and validation data from acquired data. 
    get_features() -> web_scraping()
2. Calculate posterior probability of P(C1|x), 
   * With both different covariance, and common covariance
    get_posterior() -> get_mean_covariance()
3. Plot contour of P(C1|x) and training set/validation set. Then test accuracy. 
    plot_training_set()
    test_plot_validation_set(): if P(C1|x) > 0.5 then correct

Result (Accuracy)
with [Attack, Sp_Atk]
different covariance    70%
common covariance       59%

Reference
http://cs231n.github.io/python-numpy-tutorial/#numpy
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

# [attack, sp_atk]
# Training set: (Class 1) water 89 samples, (Class 2) normal 65 samples
water_t = np.array([[48, 50], [63, 65], [83, 85], [103, 135], [52, 65], [82, 95], [50, 40], [65, 50], [95, 70], [40, 50], [70, 80], [65, 40], [75, 100], [75, 130], [45, 45], [70, 70], [65, 45], [95, 85], [105, 25], [130, 50], [40, 70], [65, 95], [67, 35], [92, 65], [45, 70], [75, 100], [10, 15], [125, 60], [155, 70], [85, 85], [65, 110], [40, 90], [60, 115], [80, 55], [115, 65], [65, 44], [80, 59], [105, 79], [38, 56], [58, 76], [20, 20], [50, 60], [75, 90], [45, 25], [85, 65], [75, 100], [95, 55], [55, 65],[65, 65], [105, 105], [40, 80], [95, 95], [75, 90], [70, 50], [85, 60], [110, 85], [150, 95], [30, 40], [50, 60], [70, 90], [30, 55], [50, 95], [30, 50], [90, 65], [120, 95], [140, 110], [70, 70], [90, 90], [48, 46], [78, 76], [80, 50], [120, 90], [15, 10], [60, 100], [70, 70], [40, 55], [60, 75], [80, 95], [64, 74], [104, 94], [84, 114], [90, 45], [30, 40], [100, 150], [150, 180], [51, 61], [66, 81], [86, 111], [85, 55]])
normal_t = np.array([[45, 35], [60, 50], [80, 70], [80, 135], [56, 25], [56, 25], [81, 50], [71, 40], [60, 31], [90, 61], [45, 45], [70, 85], [45, 40], [70, 65], [90, 58], [85, 35], [110, 60], [55, 60], [5, 35], [95, 40], [125, 60], [100, 40], [48, 48], [55, 45], [75, 65], [60, 85], [110, 65], [46, 35], [76, 45], [30, 36], [50, 86], [30, 40], [70, 40], [80, 90], [70, 65], [80, 50], [130, 75], [80, 105], [95, 85], [20, 20], [80, 40], [10, 75], [30, 30], [70, 50], [55, 30], [85, 75], [60, 35], [80, 55], [160, 95], [51, 51], [71, 71], [91, 91], [20, 20], [45, 35], [65, 55], [60, 60], [40, 40], [115, 60], [70, 70], [90, 60], [55, 30], [75, 40], [120, 50], [45, 35], [85, 55]])

# Validation set: (Class 1) water 54 samples, (Class 2) normal 52 samples
water_v = np.array([[65, 60], [105, 85], [48, 57], [83, 92], [49, 49], [69, 69], [20, 60], [65, 105], [120, 150], [80, 80], [100, 100], [55, 63], [75, 83], [100, 108], [53, 53], [98, 98], [50, 50], [65, 65], [95, 85], [92, 80], [92, 80], [78, 53], [108, 83], [44, 44], [87, 87], [40, 65], [60, 85], [75, 40], [72, 129], [72, 129], [56, 62], [63, 83], [95, 103], [145, 153], [52, 39], [105, 54], [60, 60], [53, 58], [73, 120], [110, 130], [54, 66], [69, 91], [74, 126], [20, 25], [140, 140], [53, 43], [63, 53], [40, 40], [70, 50], [35, 20], [125, 60], [60, 30], [105, 70], [75, 95]])
normal_v = np.array([[100, 60], [66, 44], [76, 54], [136, 54], [55, 42], [82, 64], [5, 15], [65, 92], [85, 40], [85, 80], [80, 135], [160, 80], [120, 120], [55, 35], [85, 60], [60, 25], [80, 35], [110, 45], [55, 36], [77, 50], [115, 65], [60, 60], [60, 80], [50, 40], [95, 65], [60, 40], [100, 60], [110, 40], [83, 37], [123, 57], [77, 128], [128, 77], [36, 32], [56, 50], [50, 40], [50, 73], [68, 109], [80, 65], [38, 61], [55, 109], [75, 30], [85, 40], [120, 75], [70, 30], [110, 55], [75, 45], [125, 55], [60, 90], [95, 95], [95, 95], [115, 75], [60, 135]])

# [defense, sp_def]
# Training set: water 89 samples, normal 65 samples
#water_t = np.array([[65, 64], [80, 80], [100, 105], [120, 115], [48, 50], [78, 80], [40, 40], [65, 50], [95, 90], [35, 100], [65, 120], [65, 40], [110, 80], [180, 80], [55, 70], [80, 95], [100, 25], [180, 45], [90, 25], [115, 50], [70, 25], [95, 45], [60, 50], [65, 80], [55, 55], [85, 85], [55, 20], [79, 100], [109, 130], [80, 95], [60, 95], [100, 55], [125, 70], [90, 45], [105, 70], [64, 48], [80, 63], [100, 83], [38, 56], [58, 76], [50, 50], [80, 80], [75, 100], [45, 25], [85, 65], [80, 110], [85, 55], [95, 95], [35, 35], [75, 75], [70, 140], [95, 95], [115, 115], [50, 50], [70, 70], [90, 90], [110, 110], [30, 50], [50, 70], [70, 100], [30, 30], [100, 70], [32, 52], [20, 20], [40, 40], [70, 65], [35, 35], [45, 45], [43, 41], [73, 71], [65, 35], [85, 55], [20, 55], [79, 125], [70, 70], [50, 50], [70, 70], [90, 90], [85, 55], [105, 75], [105, 75], [130, 65], [55, 65], [90, 140], [90, 160], [53, 56], [68, 76], [88, 101], [60, 60]])
#normal_t = np.array([[40, 35], [55, 50], [75, 70], [80, 80], [35, 35], [35, 35], [60, 70], [70, 80], [30, 31], [65, 61], [20, 25], [45, 50], [35, 40], [60, 65], [55, 62], [45, 35], [70, 60], [75, 75], [5, 105], [80, 80], [100, 100], [95, 70], [48, 48], [50, 65], [70, 85], [70, 75], [65, 110], [34, 45], [64, 55], [30, 56], [50, 96], [15, 20], [55, 55], [65, 65], [70, 65], [50, 50], [75, 75], [90, 95], [62, 65], [35, 45], [105, 70], [10, 135], [41, 41], [61, 61], [30, 30], [60, 50], [60, 35], [80, 55], [100, 65], [23, 23], [43, 43], [63, 73], [40, 40], [45, 35], [65, 55], [60, 60], [60, 75], [60, 60], [70, 70], [70, 120], [30, 30], [50, 40], [70, 60], [40, 40], [60, 60]])
# Validation set: water 54, normal 52
#water_v = np.array([[35, 30], [55, 50], [48, 62], [68, 82], [56, 61], [76, 86], [50, 120], [107, 107], [100, 120], [80, 80], [100, 100], [45, 45], [60, 60], [85, 70], [48, 48], [63, 63], [40, 40], [55, 55], [75, 75], [65, 55], [65, 55], [103, 45], [133, 65], [50, 50], [63, 63], [50, 85], [70, 105], [80, 45], [90, 90], [90, 90], [40, 44], [52, 56], [67, 71], [67, 71], [67, 56], [115, 86], [60, 60], [62, 63], [88, 89], [120, 90], [54, 56], [69, 81], [74, 116], [20, 25], [130, 135], [62, 52], [152, 142], [52, 72], [92, 132], [40, 30], [140, 90], [130, 130], [70, 70], [115, 130]])
#normal_v = np.array([[66, 66], [44, 56], [84, 96], [94, 96], [42, 37], [64, 59], [5, 65], [45, 42], [40, 85], [95, 95], [70, 75], [110, 110], [120, 120], [39, 39], [69, 69], [45, 45], [65, 65], [90, 90], [50, 30], [62, 42], [80, 55], [86, 86], [126, 126], [40, 40], [60, 60], [50, 50], [70, 70], [95, 95], [50, 50], [75, 75], [77, 128], [90, 77], [38, 36], [77, 77], [43, 38], [58, 54], [72, 66], [60, 90], [33, 43], [52, 94], [30, 30], [50, 50], [75, 75], [30, 30], [60, 60], [50, 50], [80, 60], [80, 110], [95, 95], [95, 95], [65, 95], [85, 91]])

'''
# [attack, sp_atk, defense, sp_def, speed]
water_t = np.array([[48, 50, 65, 64, 43], [63, 65, 80, 80, 58], [83, 85, 100, 105, 78], [103, 135, 120, 115, 78], [52, 65, 48, 50, 55], [82, 95, 78, 80, 85], [50, 40, 40, 40, 90], [65, 50, 65, 50, 90], [95, 70, 95, 90, 70], [40, 50, 35, 100, 70], [70, 80, 65, 120, 100], [65, 40, 65, 40, 15], [75, 100, 110, 80, 30], [75, 130, 180, 80, 30], [45, 45, 55, 70, 45], [70, 70, 80, 95, 70], [65, 45, 100, 25, 40], [95, 85, 180, 45, 70], [105, 25, 90, 25, 50], [130, 50, 115, 50, 75], [40, 70, 70, 25, 60], [65, 95, 95, 45, 85], [67, 35, 60, 50, 63], [92, 65, 65, 80, 68], [45, 70, 55, 55, 85], 
[75, 100, 85, 85, 115], [10, 15, 55, 20, 80], [125, 60, 79, 100, 81], [155, 70, 109, 130, 81], [85, 85, 80, 95, 60], [65, 110, 60, 95, 65], [40, 90, 100, 55, 35], [60, 115, 125, 70, 55], [80, 55, 90, 45, 55], [115, 65, 105, 70, 80], [65, 44, 64, 48, 43], [80, 59, 80, 63, 58], [105, 79, 100, 83, 78], [38, 56, 38, 56, 67], [58, 76, 58, 76, 67], [20, 20, 50, 50, 40], [50, 60, 80, 80, 50], [75, 90, 75, 100, 70], [45, 25, 45, 25, 15], [85, 65, 85, 65, 35], [75, 100, 80, 110, 30], [95, 55, 85, 55, 85], [55, 65, 95, 95, 35], [65, 65, 35, 35, 65], [105, 105, 75, 75, 45], [40, 80, 70, 140, 70], 
[95, 95, 95, 95, 85], [75, 90, 115, 115, 85], [70, 50, 50, 50, 40], [85, 60, 70, 70, 50], [110, 85, 90, 90, 60], [150, 95, 110, 110, 70], [30, 40, 30, 50, 30], [50, 60, 50, 70, 50], [70, 90, 70, 100, 70], [30, 55, 30, 30, 85], [50, 95, 100, 70, 65], [30, 50, 32, 52, 65], [90, 65, 20, 20, 65], [120, 95, 40, 40, 95], [140, 110, 70, 65, 105], [70, 70, 35, 35, 60], [90, 90, 45, 45, 60], [48, 46, 43, 41, 60], [78, 76, 73, 71, 60], [80, 50, 65, 35, 35], [120, 90, 85, 55, 55], [15, 10, 20, 55, 80], [60, 100, 79, 125, 81], [70, 70, 70, 70, 70], [40, 55, 50, 50, 25], [60, 75, 70, 70, 45], 
[80, 95, 90, 90, 65], [64, 74, 85, 55, 32], [104, 94, 105, 75, 52], [84, 114, 105, 75, 52], [90, 45, 130, 65, 55], [30, 40, 55, 65, 97], [100, 150, 90, 140, 90], [150, 180, 90, 160, 90], [51, 61, 53, 56, 40], [66, 81, 68, 76, 50], [86, 111, 88, 101, 60], [85, 55, 60, 60, 71]])

normal_t = np.array([[45, 35, 40, 35, 56], [60, 50, 55, 50, 71], [80, 70, 75, 70, 101], [80, 135, 80, 80, 121], [56, 25, 35, 35, 72], [56, 25, 35, 35, 72], [81, 50, 60, 70, 97], [71, 40, 70, 80, 77], [60, 31, 30, 31, 70], [90, 61, 65, 61, 100], [45, 45, 20, 25, 20], [70, 85, 45, 50, 45], [45, 40, 35, 40, 90], [70, 65, 60, 65, 115], [90, 58, 55, 62, 60], [85, 35, 45, 35, 75], [110, 60, 70, 60, 110], [55, 60, 75, 75, 30], [5, 35, 5, 105, 50], [95, 40, 80, 80, 90], [125, 60, 100, 100, 100], [100, 40, 95, 70, 110], [48, 48, 48, 48, 48], [55, 45, 50, 65, 55], [75, 65, 70, 85, 75], 
[60, 85, 70, 75, 40], [110, 65, 65, 110, 30], [46, 35, 34, 45, 20], [76, 45, 64, 55, 90], [30, 36, 30, 56, 50], [50, 86, 50, 96, 70], [30, 40, 15, 20, 15], [70, 40, 55, 55, 85], [80, 90, 65, 65, 85], [70, 65, 70, 65, 45], [80, 50, 50, 50, 40], [130, 75, 75, 75, 55], [80, 105, 90, 95, 60], [95, 85, 62, 65, 85], [20, 20, 35, 45, 75], [80, 40, 105, 70, 100], [10, 75, 10, 135, 55], [30, 30, 41, 41, 60], [70, 50, 61, 61, 100], [55, 30, 30, 30, 85], [85, 75, 60, 50, 125], [60, 35, 60, 35, 30], [80, 55, 80, 55, 90], [160, 95, 100, 65, 100], [51, 51, 23, 23, 28], [71, 71, 43, 43, 48], 
[91, 91, 63, 73, 68], [20, 20, 40, 40, 20], [45, 35, 45, 35, 50], [65, 55, 65, 55, 90], [60, 60, 60, 60, 60], [40, 40, 60, 75, 50], [115, 60, 60, 60, 90], [70, 70, 70, 70, 70], [90, 60, 70, 120, 40], [55, 30, 30, 30, 60], [75, 40, 50, 40, 80], [120, 50, 70, 60, 100], [45, 35, 40, 40, 31], [85, 55, 60, 60, 71]])

water_v = np.array([[65, 60, 35, 30, 85], [105, 85, 55, 50, 115], [48, 57, 48, 62, 34], [83, 92, 68, 82, 39], [49, 49, 56, 61, 66], [69, 69, 76, 86, 91], [20, 60, 50, 120, 50], [65, 105, 107, 107, 86], [120, 150, 100, 120, 100], [80, 80, 80, 80, 80], [100, 100, 100, 100, 100], [55, 63, 45, 45, 45], [75, 83, 60, 60, 60], [100, 108, 85, 70, 70], [53, 53, 48, 48, 64], [98, 98, 63, 63, 101], [50, 50, 40, 40, 64], [65, 65, 55, 55, 69], [95, 85, 75, 75, 74], [92, 80, 65, 55, 98], [92, 80, 65, 55, 98], [78, 53, 103, 45, 22], [108, 83, 133, 65, 32], [44, 44, 50, 50, 55], [87, 87, 63, 63, 98], [40, 65, 50, 85, 40], [60, 85, 70, 105, 60], [75, 40, 80, 45, 65], [72, 129, 90, 90, 108], [72, 129, 90, 90, 108], [56, 62, 40, 44, 71], [63, 83, 52, 56, 97], [95, 103, 67, 71, 122], [145, 153, 67, 71, 132], [52, 39, 67, 56, 50], [105, 54, 115, 86, 68], [60, 60, 60, 60, 30], [53, 58, 62, 63, 44], [73, 120, 88, 89, 59], [110, 130, 120, 90, 70], [54, 66, 54, 56, 40], [69, 91, 69, 81, 50], [74, 126, 74, 116, 60], [20, 25, 20, 25, 40], [140, 140, 130, 135, 30], [53, 43, 62, 52, 45], [63, 53, 152, 142, 35], [40, 40, 52, 72, 27], [70, 50, 92, 132, 42], [35, 20, 40, 30, 80], [125, 60, 140, 90, 40], [60, 30, 130, 130, 5], [105, 70, 70, 70, 92], [75, 95, 115, 130, 85]])
normal_v = np.array([[100, 60, 66, 66, 115], [66, 44, 44, 56, 85], [76, 54, 84, 96, 105], [136, 54, 94, 96, 135], [55, 42, 42, 37, 85], [82, 64, 64, 59, 112], [5, 15, 5, 65, 30], [65, 92, 45, 42, 91], [85, 40, 40, 85, 5], [85, 80, 95, 95, 50], [80, 135, 70, 75, 90], [160, 80, 110, 110, 100], [120, 120, 120, 120, 120], [55, 35, 39, 39, 42], [85, 60, 69, 69, 77], [60, 25, 45, 45, 55], [80, 35, 65, 65, 60], [110, 45, 90, 90, 80], [55, 36, 50, 30, 43], [77, 50, 62, 42, 65], [115, 65, 80, 55, 93], [60, 60, 86, 86, 50], [60, 80, 126, 126, 50], [50, 40, 40, 40, 75], [95, 65, 60, 60, 115], [60, 40, 50, 50, 75], [100, 60, 70, 70, 95], [110, 40, 95, 95, 55], [83, 37, 50, 50, 60], [123, 57, 75, 75, 80], [77, 128, 77, 128, 90], [128, 77, 90, 77, 128], [36, 32, 38, 36, 57], [56, 50, 77, 77, 78], [50, 40, 43, 38, 62], [50, 73, 58, 54, 72], [68, 109, 72, 66, 106], [80, 65, 60, 90, 102], [38, 61, 33, 43, 70], [55, 109, 52, 94, 109], [75, 30, 30, 30, 65], [85, 40, 50, 50, 75], [120, 75, 75, 75, 60], [70, 30, 30, 30, 45], [110, 55, 60, 60, 45], [75, 45, 50, 50, 50], [125, 55, 80, 60, 60], [60, 90, 80, 110, 60], [95, 95, 95, 95, 59], [95, 95, 95, 95, 95], [115, 75, 65, 95, 65], [60, 135, 85, 91, 36]])
'''
'''
# fake features
water_t = np.array([[161.0, 152.0], [180.0, 158.0], [157.0, 150.0], [120.0, 137.0], [140.0, 175.0], [143.0, 149.0], [140.0, 156.0], [120.0, 171.0], [126.0, 162.0], [158.0, 143.0], [161.0, 144.0], [175.0, 177.0], [169.0, 151.0], [120.0, 173.0], [172.0, 121.0], [150.0, 147.0], [125.0, 127.0], [156.0, 176.0], [148.0, 164.0], [149.0, 180.0], [120.0, 157.0], [174.0, 150.0], [163.0, 153.0], [176.0, 170.0], [178.0, 124.0], [179.0, 157.0], [138.0, 162.0], [179.0, 126.0], [127.0, 142.0], [161.0, 160.0], [145.0, 168.0], [163.0, 125.0], [155.0, 169.0], [161.0, 157.0], [169.0, 163.0], [136.0, 130.0], [173.0, 146.0], [133.0, 181.0], [135.0, 170.0], [138.0, 130.0], [148.0, 163.0], [162.0, 131.0], [142.0, 167.0], [134.0, 169.0], [140.0, 181.0], [130.0, 178.0], [135.0, 157.0], [181.0, 171.0], [132.0, 136.0], [168.0, 171.0]])
normal_t = np.array([[61.0, 34.0], [35.0, 72.0], [20.0, 68.0], [28.0, 43.0], [42.0, 51.0], [63.0, 57.0], [44.0, 33.0], [54.0, 67.0], [46.0, 47.0], [60.0, 45.0], [47.0, 70.0], [51.0, 73.0], [46.0, 66.0], [45.0, 51.0], [30.0, 56.0], [27.0, 70.0], [72.0, 29.0], [79.0, 42.0], [26.0, 75.0], [25.0, 50.0], [31.0, 70.0], [31.0, 59.0], [56.0, 48.0], [22.0, 77.0], [45.0, 65.0], [21.0, 36.0], [80.0, 47.0], [23.0, 65.0], [24.0, 57.0], [31.0, 29.0], [76.0, 38.0], [69.0, 81.0], [58.0, 76.0], [47.0, 39.0], [26.0, 55.0], [38.0, 56.0], [66.0, 20.0], [56.0, 65.0], [40.0, 72.0], [59.0, 48.0], [65.0, 20.0], [55.0, 37.0], [34.0, 49.0], [26.0, 21.0], [75.0, 80.0], [23.0, 53.0], [25.0, 38.0], [25.0, 29.0], [42.0, 35.0], [54.0, 64.0]])
water_v = np.array([[150, 150]])
normal_v = np.array([])
'''
# mean, covar of Gaussian
mean_c1 = 0
mean_c2 = 0
covar_c1 = 0
covar_c2 = 0

def plot_raw_training_set():
    fig, axs = plt.subplots(1, 2, sharex=True, sharey=True)
    axs[0].plot(water_t.T[0], water_t.T[1], 'o', color='blue')
    axs[1].plot(normal_t.T[0], normal_t.T[1], 'o', color='red')
    axs[0].set(xlabel='Attack', ylabel='Sp_Atk', title='WATER', xlim=(0, 200), ylim=(0, 200))
    axs[1].set(xlabel='Attack', ylabel='Sp_Atk', title='NORMAL')
    axs[0].grid(True)
    axs[1].grid(True)
    plt.show()        

# return mean, covariance of a given type
# we're using 2 features, so mean is a vector of 2 elements, covariance is 2x2 matrix
# e.g. 
# mean = np.array([69 54])
# covar = np.array([[816 284] [284 485]]
def get_mean_covariance(type):
    if type == 'Water':
        training_set = water_t
    else:
        training_set = normal_t
    D = len(water_t[0])
    mean = np.sum(training_set, axis=0)/len(training_set)
    covar = np.zeros((D, D))
    for i in range(len(training_set)):
        covar = covar + np.dot(np.reshape((training_set[i] - mean), (D, 1)), np.reshape((training_set[i] - mean), (1, D))) 
    covar = covar / len(training_set)
    print('{}: '.format(type))
    print('mean')
    print(mean)
    print('covariance')
    print(covar)

    global mean_c1, mean_c2, covar_c1, covar_c2
    if type == 'Water':
        mean_c1, covar_c1 = mean, covar
    if type == 'Normal':
        mean_c2, covar_c2 = mean, covar

# return posterior probability, a scalar between 0 ~ 1
# x: a Pokemon represented by array [feature feature]
# common_var: whether ot use common variance or not, default to False
def get_posterior(x, common_covar):
    D = len(water_t[0])
    # mean_c1, covar_c1 = get_mean_covariance('Water')
    # mean_c2, covar_c2 = get_mean_covariance('Normal')

    p_c1 = len(water_t)/(len(water_t) + len(normal_t))
    p_c2 = len(normal_t)/(len(water_t) + len(normal_t))

    if common_covar:
        covar = p_c1 * covar_c1 + p_c2 * covar_c2
        p_x_c1 = 1 / np.sqrt((2*np.pi)**D * np.linalg.det(covar)) * np.exp(-0.5 * np.reshape(x - mean_c1, (1, D)).dot(np.linalg.inv(covar)).dot(np.reshape(x - mean_c1, (D, 1))))
        p_x_c2 = 1 / np.sqrt((2*np.pi)**D * np.linalg.det(covar)) * np.exp(-0.5 * np.reshape(x - mean_c2, (1, D)).dot(np.linalg.inv(covar)).dot(np.reshape(x - mean_c2, (D, 1))))
    else:
        p_x_c1 = 1 / np.sqrt((2*np.pi)**D * np.linalg.det(covar_c1)) * np.exp(-0.5 * np.reshape(x - mean_c1, (1, D)).dot(np.linalg.inv(covar_c1)).dot(np.reshape(x - mean_c1, (D, 1))))
        p_x_c2 = 1 / np.sqrt((2*np.pi)**D * np.linalg.det(covar_c2)) * np.exp(-0.5 * np.reshape(x - mean_c2, (1, D)).dot(np.linalg.inv(covar_c2)).dot(np.reshape(x - mean_c2, (D, 1))))
    
    p_c1_x = p_c1 * p_x_c1 / (p_c1 * p_x_c1 + p_c2 * p_x_c2)
    return np.asscalar(p_c1_x)      # [[p]] convert to scalar

    #p_c2_x = p_c2 * p_x_c2 / (p_c1 * p_x_c1 + p_c2 * p_x_c2)
    #return np.asscalar(p_c2_x)      # [[p]] convert to scalar
    #return np.asscalar(p_x_c1)     # gaussian distribution

# plot the contour of posterior probability (red has larger probability) and data set points in dots
# data_set_type: 'training' or 'validation'
# common_var: whether ot use common variance or not, default to False
def plot_data_set(data_set_type, common_covar):
    if data_set_type == 'training':
        water_d = water_t
        normal_d = normal_t
    elif data_set_type == 'validation':
        water_d = water_v
        normal_d = normal_v

    x = np.linspace(0, 200, 50)        # attack
    y = np.linspace(0, 200, 50)        # sp_atk
    Z = np.zeros((len(y), len(x)))
    X, Y = np.meshgrid(x, y)
    for i in range(len(y)):
        for j in range(len(x)):
            #print('x: {}, y: {}'.format(j, i))
            Z[i][j] = get_posterior(np.array([x[j], y[i]]), common_covar)
    print(Z)

    fig, ax = plt.subplots()
    ax.contourf(X, Y, Z, 50, alpha=0.5, cmap=plt.get_cmap('jet'))
    CS = ax.contour(X, Y, Z, [0.5], colors='r')
    ax.clabel(CS, inline=1, fontsize=12, manual=[(175, 75)])

    # # training set
    ax.plot([water_d.T[0]], [water_d.T[1]], 'o', color='blue')
    ax.plot([normal_d.T[0]], [normal_d.T[1]], 'o', color='red')
    ax.set(xlabel = 'Attack', ylabel = 'Sp_Atk', title = '{} set: water (blue), normal (red)'.format(data_set_type))
    #plt.title('{} set: water (blue), normal (red)'.format(data_set_type))
    #plt.legend(('Water', 'Normal'))
    #plt.xlabel('Attack')
    #plt.ylabel('Sp_Atk')
    plt.show()

# plot training data set
# common_var: whether ot use common variance or not, default to False
def plot_training_set(common_covar = False):
    # get and set mean, covariance
    get_mean_covariance('Water')
    get_mean_covariance('Normal')
    plot_data_set('training', common_covar)

# test and plot validation data set
# common_var: whether ot use common variance or not, default to False
def test_plot_validation_set(common_covar = False):
    # get and set mean, covariance
    get_mean_covariance('Water')
    get_mean_covariance('Normal')

    validation_set = water_v
    #validation_set = normal_v

    count = 0
    for i in range(len(validation_set)):
        p = get_posterior(validation_set[i], common_covar)
        if p >= 0.5:
            count = count + 1
    print('Accuracy: {0:.0%}'.format(count / len(validation_set)))
    plot_data_set('validation', common_covar)

def test_multivariate_gaussian_contour():
    N = 100
    X = np.linspace(0, 200, N)
    Y = np.linspace(0, 200, N)
    X, Y = np.meshgrid(X, Y)

    get_mean_covariance('Water')
    mu = mean_c1
    Sigma = covar_c1

    pos = np.empty(X.shape + (2,))
    pos[:, :, 0] = X
    pos[:, :, 1] = Y

    F = multivariate_normal(mu, Sigma)
    Z = F.pdf(pos)
    #print(Z[75])
    #print(Z)
    plt.contourf(X, Y, Z, 50, alpha=0.5, cmap=plt.get_cmap('jet'))
    plt.show()

# 1. use get_features() to get data set
# 2. use plot_training_set() to plot posterior contour and training data set
# 3. use test_plot_validation_set() to test our model and plot posterior contour and validation data set
def main():
    #plot_raw_training_set()
    #plot_training_set(common_covar=False)
    test_plot_validation_set(common_covar=True)
    #test_multivariate_gaussian_contour()

if __name__ == '__main__':
    main()