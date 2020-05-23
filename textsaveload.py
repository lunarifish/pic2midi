
# textsave
def text_save(content,filename,mode = 'a'):
    file = open(filename,mode)
    for i in range(len(content)):
        file.write(str(content[i])+'\n')
    file.close()
###

# textread
def text_read(filename):
    try:
        file = open(filename,'r')
    except IOError:
        error = []
        return error
    content = file.readlines()

    for i in range(len(content)):
        content[i] = content[i][:len(content[i])-1]

    file.close()
    return content
###