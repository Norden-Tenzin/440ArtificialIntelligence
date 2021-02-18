from PIL import Image

image = Image.open("./assets/firedice.png")
newImage = image.resize((40,40))
newImage.save("./assets/smallfiredice.png")