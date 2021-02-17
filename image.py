from PIL import Image

image = Image.open("./assets/fire.png")
newImage = image.resize((40,40))
newImage.save("./assets/smallfire.png")