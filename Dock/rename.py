import os
os.getcwd()
collection = "data unkown"
i=120
for i, filename in enumerate(os.listdir(collection)):
    os.rename("data unkown/" + filename, "data unkown/"+"sample3_"+str(i) + ".jpg")
              
