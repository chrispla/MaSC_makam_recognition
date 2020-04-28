#Script to convert pitch series files from otmm_makam dataset to a quantized encoding
#PROVIDE LINK FOR ALGORITHM DESCRIPTION

#Library Importing
import glob
import os
import numpy as np

#Reading paths of .pitch files
read_dir = "./otmm_makam_recognition_dataset/data/" #pitch file directory
all_paths = [] #list holding all file paths
all_names = [] # list holding all names
for root, dirs, files in os.walk(read_dir):
    for name in files:
        if '.pitch' in name:
                all_paths.append(os.path.join(root, name))
                all_names.append(name);

#Writing parameters
write_dir = "./qdata/" #write directory
octave_folding = False

#Generate list of frequencies for 53ET
C0 = 16.352
freq_max = 2093.0 #around C7
freq53TET = [C0]
idx = 0
while (freq53TET[idx] < freq_max):
    freq53TET.append(freq53TET[idx] + ((freq53TET[idx])**(1/53.0)))
    idx += 1
freq_list_len = len(freq53TET)

#Traverse all paths
for i in range(len(all_paths)):
    with open(all_paths[i]) as f:
        content = f.readlines() #read file into list of lines
        
        #remove 0 (and negative, if they exist) values
        for j in range(len(content)):
            if ((float(content.rstrip()) <= 0) or (float(content.rstrip()) > freq_max)):
                content.remove(j)
        
        #find closest value to quantize to
        
                
    
    
    
    open(os.path.join(write_dir, name[i]), 'w+')
    
    
         
    