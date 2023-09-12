from  PIL import Image, ImageTk


def make_image(file, size = (33, 22)):
    image = Image.open(file)
    image = image.resize(size)
    photo = ImageTk.PhotoImage(image)
    return photo