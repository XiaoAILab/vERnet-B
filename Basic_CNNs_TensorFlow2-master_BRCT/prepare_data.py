import tensorflow as tf
import pathlib
import scipy.io as scio
from configuration import IMAGE_HEIGHT, IMAGE_WIDTH, CHANNELS, \
    BATCH_SIZE, train_dir, valid_dir, test_dir
from parse_tfrecord import get_parsed_dataset

def load_and_preprocess_image(img_path):
    # read pictures
    #print(img_path.numpy())
    img_raw = scio.loadmat(img_path.numpy())
    #print(img_raw['A'][:,:,:3])
    #time.sleep(10)
    # decode pictures
    A = img_raw['A']
    #B = A
    #A[:,:,3] = B[:,:,6]
    #A[:,:,4:] = B[:,:,3:6]
    img_tensor = tf.constant(A, dtype = tf.double)
    # resize
    # img_tensor = tf.image.resize(img_tensor, [image_height, image_width])
    img_tensor = tf.cast(img_tensor, tf.float32)
    # normalization
    img = img_tensor
    #img = img / 31.0
    #print(type(img_tensor))
    # print('**********')
    return img

def get_single_image(img_path):
    # read pictures
    #print(img_path.numpy())
    img_raw = scio.loadmat(img_path)
    #print(img_raw['A'][:,:,:3])
    #time.sleep(10)
    # decode pictures
    A = img_raw['A']
    #B = A
    #A[:,:,3] = B[:,:,6]
    #A[:,:,4:] = B[:,:,3:6]
    img_tensor = tf.constant(A, dtype = tf.double)
    # resize
    # img_tensor = tf.image.resize(img_tensor, [image_height, image_width])
    img_tensor = tf.cast(img_tensor, tf.float32)
    # normalization
    img = img_tensor
    #img = img / 31.0
    #print(type(img_tensor))
    # print('**********')
    return img


def get_images_and_labels(data_root_dir):
    # get all images' paths (format: string)
    data_root = pathlib.Path(data_root_dir)
    all_image_path = [str(path) for path in list(data_root.glob('*/*'))]
    # get labels' names
    label_names = sorted(item.name for item in data_root.glob('*/'))
    # dict: {label : index}
    label_to_index = dict((label, index) for index, label in enumerate(label_names))
    # get all images' labels
    all_image_label = [label_to_index[pathlib.Path(single_image_path).parent.name] for single_image_path in all_image_path]

    return all_image_path, all_image_label


def get_dataset(dataset_root_dir):
    all_image_path, all_image_label = get_images_and_labels(data_root_dir=dataset_root_dir)
    # print("image_path: {}".format(all_image_path[:]))
    # print("image_label: {}".format(all_image_label[:]))
    # load the dataset and preprocess images
    # image_dataset = tf.data.Dataset.from_tensor_slices(all_image_path).map(load_and_preprocess_image)
    image_dataset = tf.data.Dataset.from_tensor_slices(all_image_path).map(lambda x: tf.py_function(load_and_preprocess_image, [x], [tf.float32]))
    print(type(image_dataset))
    label_dataset = tf.data.Dataset.from_tensor_slices(all_image_label)
    dataset = tf.data.Dataset.zip((image_dataset, label_dataset))
    # tf.print(image_dataset)
    image_count = len(all_image_path)
    # print('********')
    return dataset, image_count

def generate_datasets():
    train_dataset, train_count = get_dataset(dataset_root_dir=train_dir)
    valid_dataset, valid_count = get_dataset(dataset_root_dir=valid_dir)
    test_dataset, test_count = get_dataset(dataset_root_dir=test_dir)

    # read the original_dataset in the form of batch
    train_dataset = train_dataset.shuffle(buffer_size=train_count).batch(batch_size=BATCH_SIZE)
    valid_dataset = valid_dataset.batch(batch_size=BATCH_SIZE)
    test_dataset = test_dataset.batch(batch_size=BATCH_SIZE)

    return train_dataset, valid_dataset, test_dataset, train_count, valid_count, test_count
