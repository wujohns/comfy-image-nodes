from PIL import ImageSequence, Image, ImageOps
import numpy as np
import torch

class AddBgColor:
  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "images": ("IMAGE", ),
        "color_code": ("STRING", {"default": "#ffffff"})
      }
    }
  
  RETURN_TYPES = ("IMAGE", )
  FUNCTION = "add_bgcolor"
  CATEGORY = "comfy_image_nodes"

  def add_bgcolor(self, images, color_code):
    image = images[0]
    i = 255. * image.cpu().numpy()
    img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

    rgb_color = tuple(int(color_code[i:i+2], 16) for i in (1, 3, 5))
    background = Image.new('RGB', (10, 10), rgb_color)
    background = background.resize(img.size)
    background.paste(img, (0, 0), img)

    output_images = []
    for i in ImageSequence.Iterator(background):
        i = ImageOps.exif_transpose(i)
        if i.mode == 'I':
            i = i.point(lambda i: i * (1 / 255))
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
        output_images.append(image)

    if len(output_images) > 1:
        output_image = torch.cat(output_images, dim=0)
    else:
        output_image = output_images[0]

    return (output_image, )
