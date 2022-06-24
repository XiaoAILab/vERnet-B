from . import resnet

model_list = [
    resnet.resnet_18(), resnet.resnet_34(), resnet.resnet_50(), resnet.resnet_101(), resnet.resnet_152()
]


def get_model2idx_dict():
    return dict((v, k) for k, v in enumerate(model_list))


def get_model(idx):
    return model_list[idx]
