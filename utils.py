def load_image(image_file, size, device):
    image = Image.open(image_file).convert('RGB')
    loader = transforms.Compose([
        transforms.Resize(size),
        transforms.ToTensor()
    ])
    image = loader(image).unsqueeze(0)
    return image.to(device, torch.float)

def tensor_to_pil(tensor):
    image = tensor.cpu().clone()
    image = image.squeeze(0)
    image = transforms.ToPILImage()(image)
    return image