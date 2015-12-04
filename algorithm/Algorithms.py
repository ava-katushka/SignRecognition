__author__ = 'ava-katushka'

# requires picture in "L" mode (grey)
def centerOfMass(pixels, width, height):
    mass = 0
    imoment = 0
    jmoment = 0
    for i in range(0, width):
        for j in range(0, height):
            inverted = 255 - pixels[i, j]
            imoment += i * inverted
            jmoment += j * inverted
            mass += inverted
    centerOfMass = [imoment / mass, jmoment / mass]
    # print centerOfMass
    return centerOfMass
