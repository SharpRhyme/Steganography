from PIL import Image
#an image manipulation module, used to alter the image to add text
import numpy as np
# a library for working with arrays,in this case array of pixels

def encrypt_image(Img_path, txt):
    img = np.asarray(Image.open(Img_path))
    #opens the path of the beginning image and makes it a numpy array
    width, height = img.shape[:-1]
    #gets the width and height of image 
    txt += "[END]"
    #adds [END] to the text arguemnt so we can find where our text is stored
    txt = txt.encode("ascii")
    #converts unicode string to ascii so python can read each character's ascii code
    txt_bits = "".join([format(i, "08b") for i in txt])
    #convets all ascii codes to binary
    
    img = img.flatten()
    #flattens the image so it is easier to work with
    
    for idx, bit in enumerate(txt_bits):
        val = img[idx]
        #the position of the image at idx index
        val = bin(val)
        #makes sure val is bianry
        val = val[:-1]+bit
        #removes the last bit (least significant) and replaces with the bit from the text
        img[idx] = int(val, 2)
        #adds the new binary value to the image at the original index
    img = img.reshape(width, height, -1)
    #unflattens image 
    img = Image.fromarray(img)
    img.save("modified.png")
    #saves the image  
        

def decrypt_image(Img_path):
    txt = ""
    #empty variable to add text into
    idx = 0
    #current index
    img = np.asarray(Image.open(Img_path))
    #converts image to numpy array
    width, height = img.shape[:-1]
    #gets the width and height of image 
    img = img.flatten()
    #flattens image to make it easier to work with
    while txt[-5:] != "[END]":
        bits = [bin(i)[-1] for i in img[idx:idx+8]]
        #converts to bits and gets data from the last bit (least significant) for 8 bytes
        bits = "".join(bits)
        #makes it a string
        txt += chr(int(bits,2))
        #adds the character to our txt variable
        idx += 8
        #as we iterate over 8 positions to get the full character we increment by 8 each time
        if idx > width-8:
        #if the index goes over the width of image
            print("No hidden message in this text!")
            break
    print(f"The hidden text is {txt}")
    
        
    
    
    
encrypt_image("image/ball-python.png", "The snake ever watches")
decrypt_image("modified.png")
#runs the function with the path to the image