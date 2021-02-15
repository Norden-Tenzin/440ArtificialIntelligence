from PIL import Image

image = Image.open("./assets/newdice.png")
newImage = image.resize((45,45))
newImage.save("./assets/dice2.png")