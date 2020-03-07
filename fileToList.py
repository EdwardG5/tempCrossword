def fileToWords(fileRoute):
    fp = open(fileRoute)
    words = fp.read().split()
    fp.close()
    return words