
f = open("dlgs.txt", "w")

for i in range(1,21):

    
    f.write( "dlg.count" + str(i) + ".setText(str(len(os.listdir('gui_images/Class"+str(i)+"/'))))\n")
