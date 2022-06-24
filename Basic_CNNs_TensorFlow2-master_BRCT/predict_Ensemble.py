import sys

import tensorflow as tf
from configuration import save_model_dir
from prepare_data import get_single_image
from models import get_model
import numpy as np
import scipy.io as scio

try:
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            print(e)

    idx = int(sys.argv[1])
    mat_path = sys.argv[2]
    result_path = sys.argv[3]
    protein_HGVS = sys.argv[4]

    # get the original_dataset
    image_tensor = get_single_image(mat_path)
    image = tf.expand_dims(image_tensor, axis=0)

    #model_list = ["model", "model11", "model12", "model21", "model22", "model31", "model32"]
    model_list = ["model/model", "model7/model", "model6/model"]
    #model_list = ['ndmodel1/modelepoch-150', 'ndmodel2/modelepoch-150', 'ndmodel3/modelepoch-150']
    model_count = len(model_list)
    
    predictions_all = np.zeros((2,model_count))
    #labels_all = np.zeros(test_count)

    for i in range(model_count):

        # load the models
        model = get_model(idx)
        model.load_weights(filepath=save_model_dir+model_list[i])
        # model = tf.saved_model.load(save_model_dir)

        # Get the accuracy on the test set
        #loss_object = tf.keras.metrics.SparseCategoricalCrossentropy()
        #test_loss = tf.keras.metrics.Mean()
        #test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy()

        # @tf.function
        prediction = model(image, training=False)
        predictions_numpy = prediction.numpy()
            #labels_all = labels
            # predictions_all[:,:,0] = predictions_numpy
            # # t_loss = loss_object(labels, predictions)
            # print(labels)
            # # print(predictions)
            # test_loss(t_loss)
            # test_accuracy(labels, predictions)

        predictions_all[:,i] = predictions_numpy
            # print("loss: {:.5f}, test accuracy: {:.5f}".format(test_loss.result(),
            #                                                 test_accuracy.result()))
        #predictions_ensemble = predictions_all[:,:,0]
        #print(predictions_all)
        #predictions = tf.constant(predictions_all, dtype = tf.double)
    predictions_ensemble = np.copy(predictions_all[:,0])
    print(predictions_all)
    for i in range(1,model_count):
        t1 = abs(predictions_ensemble[1] - 0.5)
        t2 = abs(predictions_all[1,i] - 0.5)
        #print(t1,t2)
        if(t1 < t2):
            predictions_ensemble[:] = predictions_all[:,i]
    #print(predictions_all[21,1,:])
    if((predictions_ensemble[1] < 0.9) & (predictions_ensemble[1]> 0.1)):
    #if(1==0):
        vote = 0
        for i in range(model_count):
            if(predictions_all[1,i] > 0.5):
                vote = vote + 1
        #print("%d:%d" % (j,vote))
        if(vote > 1):
            for i in range(model_count):
                if(predictions_all[1,i] > predictions_ensemble[1]):
                        predictions_ensemble[:] = predictions_all[:,i]
        else:
            for i in range(model_count):
                if(predictions_all[1,i] < predictions_ensemble[1]):
                    predictions_ensemble[:] = predictions_all[:,i]
    print(predictions_ensemble)

    with open(result_path, 'w') as f:
        f.write(str(predictions_ensemble[1]))
except:
    sys.exit(0)
sys.exit(idx)
