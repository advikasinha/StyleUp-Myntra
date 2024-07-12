import torch
from PIL import Image
import torchvision.transforms as transforms

def load_image(image_file, size, device):
    image = Image.open(image_file)
    transform = transforms.Compose([
        transforms.Resize(size),
        transforms.ToTensor()
    ])
    image = transform(image).unsqueeze(0)
    return image.to(device, torch.float)

def load_images(content_file, style_file, device):
    imsize = 512 if torch.cuda.is_available() else 128
    content_img = load_image(content_file, imsize, device)
    style_img = load_image(style_file, [content_img.size(2), content_img.size(3)], device)
    return content_img, style_img