#Script to convert pitch series files from otmm_makam dataset to a quantized encoding
#PROVIDE LINK FOR ALGORITHM DESCRIPTION

#Library Importing
import glob
import os
import numpy as np
import math

#Reading paths of .pitch files
read_dir = "./otmm_makam_recognition_dataset/data/" #pitch file directory
all_paths = [] #list holding all file paths
all_names = [] # list holding all names
for root, dirs, files in os.walk(read_dir):
    for name in files:
        if '.pitch' in name:
                all_paths.append(os.path.join(root, name))
                all_names.append(name);
print("Number of files:", str(len(all_paths)))

#Writing parameters
write_dir = "./qdata/" #write directory
octave_folding = False

#TET parameters
A4 = 440.0 #A4 tuning reference, float
freq_max = 2093.0 #around C7
TET = 53 #choose equal temperament bins
rounding_precision = 1 #must adjust based on TET

#Traverse all paths
for i in range(len(all_paths)):
    
    print("File:", all_names[i])
    #For every file
    with open(all_paths[i]) as f:
        content = f.readlines() #read file into list of lines
        
        #QUANTIZATION
        
        #For every line
        j = 0
        new_content = []
            
        for j in range(len(content)):
            
            freq = float(content[j].rstrip())

            #remove 0 and over freq_max (and negative, if they exist) values
            if (freq > 0 and freq<freq_max):
                
                #calculate offset from tuning, aka amount of notes away (in specified TET)
                #round it to nearest note, and then use the rounded value to calculate quantized note
                offset = round(TET * math.log(freq/A4, 2)) #calculate offset from tuning reference
                new_freq = round(A4 * (2**(offset/float(TET))),rounding_precision) 
                
                print(str(freq) + "/" + str(new_freq))
                new_content.append(str(new_freq) + "\n")
                
                
        #ENTRY MERGE 
            
        #count consecutive entries
        consec = 1
        
        #keep min and max for significance value
        min_consec = 100000
        max_consec = 0   
            
        #For every line
        idx = 0
        while (True):
            if (idx+1 < len(new_content)):  
                if (new_content[idx] == new_content[idx+1]):
                    #if next entry same as current, remove and keep track of streak
                    del new_content[idx+1]
                    consec+=1
                else:
                    #if next line different, alter current entry, increment idx, end streak
                    new_content[idx] = (new_content[idx].rstrip()) + "," + str(consec) + "\n"
                    idx+=1
                    if (consec > max_consec):
                        max_consec = consec
                    if (consec < min_consec):
                        min_consec = consec
                    consec = 1
            else:
                if (len(new_content[idx].split(","))==1):
                    #handle last value if not already handled
                    new_content[idx] = (new_content[idx].rstrip()) + "," + str(consec) + "\n"
    
                    if (consec > max_consec):
                        max_consec = consec
                    if (consec < min_consec):
                        min_consec = consec
                break
        
        #SIGNIFICANCE VALUE
        
        dif = max_consec - min_consec
        
        #For every line
        for j in range(len(new_content)):
            
            c_line = new_content[j].split(",")
            c_line[1] = int(c_line[1].rstrip())
            if (c_line[1] <= (min_consec + (0.05*dif))):
                c_line[1] = 1
            elif ((c_line[1] > (min_consec + (0.05*dif))) and (c_line[1] < (max_consec - (0.3*dif)))):
                c_line[1] = 2
            elif (c_line[1] >= (max_consec - (0.3*dif))):
                c_line[1] = 3
            
            new_content[j] = c_line[0] + "," + str(c_line[1]) + "\n"
            
    #WRITE TO NEW FILE
    with open(os.path.join(write_dir, all_names[i]), 'w+') as f:
        f.writelines("%s" % line for line in new_content)