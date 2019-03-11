import string

def reformat():
    rf = open('stories2reformatted.txt', 'w')
    with open('stories2.txt', 'r') as unformatted:
        for line in unformatted.readlines():
            if line != "\n":
                rf.write("'" + line.strip() + "' +\n")
            else:
                rf.write(line)
    rf.close()

reformatted = False;
if not reformatted:
    with open("stories2reformatted.txt", 'w+') as f:
        f.write("")
    reformat()
