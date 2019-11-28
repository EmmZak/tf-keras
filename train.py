import tensorflow as tf

base_model = InceptionV3(weights='imagenet', include_top=False)