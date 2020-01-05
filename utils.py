import io

def readtext(filename):
    with open(filename,'r') as f:
        return f.read()

def text_warp(text, words_per_line):

    text_wrapped=""
    paragraphs=text.split('\n\n')

    for i in range(0,len(paragraphs)):
        paragraphs[i]=paragraphs[i].split('\n') 
    for p in paragraphs:
        for line in p:
            for i in range(0,len(line)//words_per_line+1):
                text_wrapped+= (line[words_per_line*i:words_per_line*(i+1)]+'\n')
        text_wrapped+='\n'

    line_lists=io.StringIO(text_wrapped).readlines()

    return line_lists
