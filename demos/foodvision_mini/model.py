import torch
import torchvision
from torchvision import transforms
from torch import nn
def create_model(num_class:int=3,seed:int=42):
    weights=torchvision.models.EfficientNet_B2_Weights.DEFAULT
    transform=weights.transforms()
    model=torchvision.models.efficientnet_b2(weights=weights)
    for params in model.parameters():
        params.requires_grad=False
    torch.manual_seed(seed)
    model.classifier=nn.Sequential(nn.Dropout(p=0.3, inplace=True),nn.Linear(in_features=1408, out_features=num_class, bias=True))
    return model,transform
