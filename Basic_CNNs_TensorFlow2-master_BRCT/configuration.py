
DEVICE = "gpu"   # cpu or gpu

# some training parameters
EPOCHS = 200
BATCH_SIZE = 26
NUM_CLASSES = 2
IMAGE_HEIGHT = 214
IMAGE_WIDTH = 214
CHANNELS = 7
LEARNING_RATE = 1e-3

#save_model_dir = "saved_model/model"
save_model_dir = "/data1/lc/vEPnet_web/Source/Basic_CNNs_TensorFlow2-master_BRCT/model_weight/"
save_every_n_epoch = 10
test_image_dir = "dataset/test.tmp484/0/BRCA1_BRCT_V1000_h_nrint.mat"

dataset_dir = "dataset/"
#dataset_dir = "dataset/dataset3/"
train_dir = dataset_dir + "train"
valid_dir = dataset_dir + "valid"
test_dir = dataset_dir + "single_test"
train_tfrecord = dataset_dir + "train.tfrecord"
valid_tfrecord = dataset_dir + "valid.tfrecord"
test_tfrecord = dataset_dir + "test.tfrecord"
# VALID_SET_RATIO = 1 - TRAIN_SET_RATIO - TEST_SET_RATIO
TRAIN_SET_RATIO = 0.9
TEST_SET_RATIO = 0


