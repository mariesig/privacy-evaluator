import os

import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D,
    MaxPooling2D,
    Flatten,
    Dense,
    BatchNormalization,
    ReLU,
    SpatialDropout2D,
    GlobalAveragePooling2D,
    Dropout,
)


__all__ = ["DCTI", "dcti"]


class Block(tf.keras.Model):
    def __init__(self, filters: int):
        super().__init__()

        self.model = Sequential(
            [
                Conv2D(filters, kernel_size=3, padding="same"),
                BatchNormalization(),
                ReLU(),
            ]
        )

    def call(self, x, training=False):
        return self.model(x, training=training)


class DCTI(tf.keras.Model):
    def __init__(self):
        super().__init__()

        self.model = Sequential(
            [
                Block(64),
                Block(64),
                SpatialDropout2D(0.3),
                MaxPooling2D((2, 2)),
                Block(128),
                Block(128),
                SpatialDropout2D(0.3),
                MaxPooling2D((2, 2)),
                Block(256),
                Block(256),
                Block(256),
                SpatialDropout2D(0.4),
                MaxPooling2D((2, 2)),
                Block(512),
                Block(512),
                SpatialDropout2D(0.4),
                MaxPooling2D((2, 2)),
                Block(512),
                GlobalAveragePooling2D(),
                Flatten(),
                Dropout(0.5),
                Dense(10, activation="softmax"),
            ]
        )

    def call(self, x, training=False):
        return self.model(x, training=training)


def dcti(pretrained: bool = True) -> DCTI:
    """
    DCTI model from
    `"Lightweight Deep Convolutional Network for Tiny Object Recognition"
    <https://www.scitepress.org/Papers/2018/67520/67520.pdf>`_.

    Note:
        The pre-trained model expects inputs to be first scaled to [0, 1] and
        then normalized with tensorflow.image.per_image_standardization

    Args:
        pretrained (bool): If True, returns a model pre-trained on CIFAR-10
    """
    if pretrained:
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, "dcti", "model")
        model = tf.keras.models.load_model(path)
    else:
        model = DCTI()

    return model
