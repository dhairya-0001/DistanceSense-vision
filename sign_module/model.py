import torch
import torch.nn as nn
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights

class SignClassifier(nn.Module):
    def __init__(self, num_classes=15):
        super(SignClassifier, self).__init__()
        # Load pretrained MobileNetV2
        self.model = mobilenet_v2(weights=MobileNet_V2_Weights.IMAGENET1K_V1)
        
        # Freeze early layers for transfer learning
        for param in self.model.features.parameters():
            param.requires_grad = False
            
        # Replace the final classifier layer
        self.model.classifier[1] = nn.Linear(self.model.classifier[1].in_features, num_classes)
        
    def forward(self, x):
        return self.model(x)
