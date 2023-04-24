from django.apps import AppConfig
import pickle
from pathlib import Path
import os
import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras.layers import Layer
from linda.settings import BASE_DIR
from serModel.model.model_arch import TIMNET_Model, WeightLayer
import argparse

class SermodelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'serModel'

    model_path = os.path.join(BASE_DIR,'serModel/model/cpmodel_weights.h5')

    # ser_model = pickle.load(open(model_path, 'rb'))

    args = argparse.Namespace(activation='relu', batch_size=64, beta1=0.93, beta2=0.98, data='RAVDE', dilation_size=8, dropout=0.1, epoch=300, filter_size=39, kernel_size=2, lr=0.001, model_path='./Models/', random_seed=46, result_path='./Results/', split_fold=5, stack_size=1)

    CLASS_LABELS = ('angry', 'calm', 'disgust', 'fear', 'happy', 'neutral','sad', 'surprise')

    ser_model = TIMNET_Model(args=args, input_shape=(196, 39), class_label=CLASS_LABELS)

    # ser_model = tf.keras.models.load_model(model_path,custom_objects={"WeightLayer": WeightLayer})

    ser_model.create_model()
    ser_model.model.load_weights(model_path)
