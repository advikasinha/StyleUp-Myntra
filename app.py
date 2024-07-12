import streamlit as st
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from PIL import Image
import matplotlib.pyplot as plt
import torchvision.transforms as transforms
import torchvision.models as models
import copy
import numpy as np
import os

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Image size
imsize = 512 if torch.cuda.is_available() else 128

# Load an image and preprocess
def load_image(image_path, size):
    image = Image.open(image_path)
    transform = transforms.Compose([
        transforms.Resize(size),
        transforms.ToTensor()
    ])
    image = transform(image).unsqueeze(0)
    return image.to(device, torch.float)

# Dynamic load images
def dynamic_load_images(content_path, style_path, size):
    content_img = load_image(content_path, size)
    style_img = load_image(style_path, [content_img.size(2), content_img.size(3)])
    assert style_img.size() == content_img.size(), "Style and content images must be of the same size"
    return content_img, style_img

# Show image
def show_image(tensor):
    image = tensor.cpu().clone().squeeze(0)
    image = transforms.ToPILImage()(image)
    plt.imshow(image)
    plt.axis('off')
    plt.show()

# Content Loss
class ContentLoss(nn.Module):
    def __init__(self, target, weight=1.0):
        super(ContentLoss, self).__init__()
        self.target = target.detach()
        self.weight = weight

    def forward(self, input):
        self.loss = self.weight * F.mse_loss(input, self.target)
        return input

# Gram Matrix for Style Loss
def gram_matrix(input):
    batch_size, num_channels, height, width = input.size()
    features = input.view(batch_size * num_channels, height * width)
    G = torch.mm(features, features.t())
    return G.div(batch_size * num_channels * height * width)

# Style Loss
class StyleLoss(nn.Module):
    def __init__(self, target_feature):
        super(StyleLoss, self).__init__()
        self.target = gram_matrix(target_feature).detach()

    def forward(self, input):
        G = gram_matrix(input)
        self.loss = F.mse_loss(G, self.target)
        return input

# Normalization Layer
class Normalization(nn.Module):
    def __init__(self, mean, std):
        super(Normalization, self).__init__()
        self.mean = torch.tensor(mean).view(-1, 1, 1).to(device)
        self.std = torch.tensor(std).view(-1, 1, 1).to(device)

    def forward(self, img):
        return (img - self.mean) / self.std

# Get model and losses
def get_model_and_losses(cnn, normalization_mean, normalization_std, style_img, content_img):
    cnn = copy.deepcopy(cnn)
    normalization = Normalization(normalization_mean, normalization_std).to(device)
    content_losses = []
    style_losses = []
    model = nn.Sequential(normalization)

    i = 0
    for layer in cnn.children():
        if isinstance(layer, nn.Conv2d):
            i += 1
            name = 'conv_{}'.format(i)
        elif isinstance(layer, nn.ReLU):
            name = 'relu_{}'.format(i)
            layer = nn.ReLU(inplace=False)
        elif isinstance(layer, nn.MaxPool2d):
            name = 'pool_{}'.format(i)
        elif isinstance(layer, nn.BatchNorm2d):
            name = 'bn_{}'.format(i)
        else:
            raise RuntimeError(f'Unrecognized layer: {layer.__class__.__name__}')

        model.add_module(name, layer)

        if name in ['conv_4']:  # Content layer
            target = model(content_img).detach()
            content_loss = ContentLoss(target)
            model.add_module(f"content_loss_{i}", content_loss)
            content_losses.append(content_loss)

        if name in ['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']:  # Style layers
            target_feature = model(style_img).detach()
            style_loss = StyleLoss(target_feature)
            model.add_module(f"style_loss_{i}", style_loss)
            style_losses.append(style_loss)

    for i in range(len(model) - 1, -1, -1):
        if isinstance(model[i], ContentLoss) or isinstance(model[i], StyleLoss):
            break

    model = model[:(i + 1)]
    return model, style_losses, content_losses

# Get input optimizer
def get_input_optimizer(input_img):
    optimizer = optim.LBFGS([input_img.requires_grad_()])
    return optimizer

# Run style transfer
def run_style_transfer(cnn, normalization_mean, normalization_std, content_img, style_img, input_img, num_steps=300, style_weight=1000000, content_weight=1):
    model, style_losses, content_losses = get_model_and_losses(cnn, normalization_mean, normalization_std, style_img, content_img)
    optimizer = get_input_optimizer(input_img)

    run = [0]
    while run[0] <= num_steps:
        def closure():
            input_img.data.clamp_(0, 1)
            optimizer.zero_grad()
            model(input_img)
            style_score = sum(sl.loss for sl in style_losses)
            content_score = sum(cl.loss for cl in content_losses)

            style_score *= style_weight
            content_score *= content_weight

            loss = style_score + content_score
            loss.backward()

            run[0] += 1
            return style_score + content_score

        optimizer.step(closure)

    input_img.data.clamp_(0, 1)
    return input_img

# Streamlit UI
st.title("DesignerHub - Style Transfer")
content_image = st.file_uploader("Upload Content Image", type=["jpg", "png"])
style_image = st.file_uploader("Upload Style Image", type=["jpg", "png"])

if content_image and style_image:
    content_img, style_img = dynamic_load_images(content_image, style_image, imsize)

    # Initialize CNN
    cnn = models.vgg19(pretrained=True).features.to(device).eval()
    cnn_normalization_mean = [0.485, 0.456, 0.406]
    cnn_normalization_std = [0.229, 0.224, 0.225]

    input_img = content_img.clone()
    output_img = run_style_transfer(cnn, cnn_normalization_mean, cnn_normalization_std, content_img, style_img, input_img)

# Convert tensor to PIL image
    output_image = output_img.cpu().detach().squeeze(0)
    output_image = transforms.ToPILImage()(output_image)

# Display output
    st.image(output_image, caption='Output Image', use_column_width=True)
