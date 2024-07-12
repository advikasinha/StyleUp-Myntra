import streamlit as st
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
import torchvision.transforms as transforms
import torchvision.models as models #for VGG or ResNet, transfer learning

import copy #creates shallows and deep copies of objects in Python

# Load custom CSS
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# Set device for PyTorch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
imsize = 512 if torch.cuda.is_available() else 128

# Load the pre-trained VGG19 model
cnn = models.vgg19(pretrained=True).features.to(device).eval()

# Normalization constants
cnn_normalization_mean = torch.tensor([0.485, 0.456, 0.406]).to(device)
cnn_normalization_std = torch.tensor([0.229, 0.224, 0.225]).to(device)

# Function to load images
def load_image(image_file):
    image = Image.open(image_file)
    return image

# Function to transform images for the model
def transform_image(image, size=512):
    transform = transforms.Compose([
        transforms.Resize(size),
        transforms.ToTensor()
    ])
    image = transform(image).unsqueeze(0)
    return image.to(device, torch.float)

# Define content and style loss classes
class ContentLoss(nn.Module):
    def __init__(self, target, weight=1.0):
        super(ContentLoss, self).__init__()
        self.target = target.detach()
        self.weight = weight

    def forward(self, input):
        self.loss = self.weight * F.mse_loss(input, self.target)
        return input

def gram_matrix(input):
    batch_size, num_channels, height, width = input.size()
    features = input.view(batch_size * num_channels, height * width)
    G = torch.mm(features, features.t())
    return G.div(batch_size * num_channels * height * width)

class StyleLoss(nn.Module):
    def __init__(self, target_feature):
        super(StyleLoss, self).__init__()
        self.target = gram_matrix(target_feature).detach()

    def forward(self, input):
        G = gram_matrix(input)
        self.loss = F.mse_loss(G, self.target)
        return input

# Normalization class
class Normalization(nn.Module):
    def __init__(self, mean, std):
        super(Normalization, self).__init__()
        self.mean = torch.tensor(mean).view(-1, 1, 1).to(device)
        self.std = torch.tensor(std).view(-1, 1, 1).to(device)

    def forward(self, img):
        print("Input image shape:", img.shape)
        print("Mean shape:", self.mean.shape)
        print("Std shape:", self.std.shape)
        return (img - self.mean) / self.std


# Function to get model and losses
def get_model_and_losses(cnn, normalization_mean, normalization_std,
                         style_img, content_img,
                         content_layers=['conv_4'],
                         style_layers=['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']):
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

        if name in content_layers:
            target = model(content_img).detach()
            content_loss = ContentLoss(target)
            model.add_module(f"content_loss_{i}", content_loss)
            content_losses.append(content_loss)

        if name in style_layers:
            target_feature = model(style_img).detach()
            style_loss = StyleLoss(target_feature)
            model.add_module(f"style_loss_{i}", style_loss)
            style_losses.append(style_loss)

    for i in range(len(model) - 1, -1, -1):
        if isinstance(model[i], ContentLoss) or isinstance(model[i], StyleLoss):
            break

    model = model[:(i + 1)]
    return model, style_losses, content_losses

# Function to get optimizer
def get_input_optimizer(input_img):
    optimizer = optim.LBFGS([input_img.requires_grad_()])
    return optimizer

# Function to run style transfer
def run_style_transfer(cnn, normalization_mean, normalization_std,
                       content_img, style_img, input_img, num_steps=300,
                       style_weight=1000000, content_weight=1):
    model, style_losses, content_losses = get_model_and_losses(cnn, normalization_mean, normalization_std, style_img, content_img)
    optimizer = get_input_optimizer(input_img)

    run = [-200]
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
            if run[0] % 50 == 0:
                st.write(f"run {run[0]}: Style Loss : {style_score.item()} Content Loss: {content_score.item()}")

            return style_score + content_score

        optimizer.step(closure)

    input_img.data.clamp_(0, 1)
    return input_img

# Streamlit layout
st.title("DesignerHub")
st.markdown("Welcome to DesignerHub! Upload your content and style images for a unique style transfer experience.")

content_image = st.file_uploader("Upload Content Image", type=["jpg", "jpeg", "png"])
style_image = st.file_uploader("Upload Style Image", type=["jpg", "jpeg", "png"])

if content_image and style_image:
    content_img = load_image(content_image)
    style_img = load_image(style_image)

    st.image(content_img, caption="Content Image", use_column_width=True)
    st.image(style_img, caption="Style Image", use_column_width=True)

    if st.button("Run Style Transfer"):
        input_img = transform_image(content_img)
        output_img = run_style_transfer(cnn, cnn_normalization_mean, cnn_normalization_std,
                                 content_img, style_img, input_img, 
                                 num_steps=300, style_weight=1000000, content_weight=1)


        output_image = transforms.ToPILImage()(output_img.squeeze(0).cpu())
        st.image(output_image, caption="Output Image", use_column_width=True)
