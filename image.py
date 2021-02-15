from PIL import Image

image = Image.open("./assets/newdice.png")
newImage = image.resize((40,40))
newImage.save("./assets/dice2.png")