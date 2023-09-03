import time
import os
from tqdm import tqdm
import pandas as pd
import seaborn as sns
import random

def count(img_dir):
    print("Counting number of classes in training ....")
    # img_dir = "test_images" # image and txt directory.
    classes_txt = f"{img_dir}/classes.txt" # path of the classes.txt

    class_index = {}
    count = {}
    cls = open(classes_txt)
    cls = cls.read().split("\n")
    for i, c in enumerate(cls):
        if len(c) == 0:
            continue
        class_index[i] = c
        count[c] = 0

    img_list = [f"/static/annot/{i}" for i in os.listdir(img_dir) if i.endswith(".jpg")]
    txt_list = [i for i in os.listdir(img_dir) if i.endswith(".txt")]
    img_list = sorted(img_list)
    txt_list = sorted(txt_list)
    print(f"Total number of images in training Dataset -> {len(txt_list)}\n\n")
    random_images = random.sample(img_list, 5)
    for c, txt in tqdm(enumerate(txt_list)):
        txt_path = f"{img_dir}/{txt}"
        data = pd.read_csv(txt_path, sep=" ", header=None, names=["class", "xm", "ym", "x", "y"])
        for k, v in class_index.items():
            count[v] += len(data[data["class"] == k])

    count = {k:v for k, v in count.items() if v!=0}

    return random_images, count