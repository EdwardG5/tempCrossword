def fileToWords(fileRoute):
    words = open(fileRoute).read().split()
    return words