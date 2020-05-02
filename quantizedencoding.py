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

#Generate list of frequencies for selected TET
A4 = 440
C0 = A4*(2**(-57/12.0)) #calculate exact C0 from tuning reference
freq_max = 2093.0 #around C7
TET = 53 #choose equal temperament bins, consider rounding value later on
freqs = [C0]
idx = 0
while (freqs[idx] < freq_max):
    freqn = (freqs[idx])*(2**(1/float(TET)))
    freqs.append(freqn)
    idx += 1
freq_list_len = len(freqs)
print("freqs length :",freq_list_len)

#Traverse all paths
for i in range(len(all_paths)):
    
    print("i :", i)
    #For every file
    with open(all_paths[i]) as f:
        content = f.readlines() #read file into list of lines
        print(len(content))
        #QUANTIZATION
        
        #For every line
        j = 0
        new_content = []
        while (True):
            
            if (j<len(content)):
                
                freq = float(content[j].rstrip())
                
                #remove 0 and over freq_max (and negative, if they exist) values
                if (freq > 0 and freq<freq_max):
                    #find closest value to quantize to (should be implemented more efficiently in the future)
                    idx = 0
                    while (freq > freqs[idx]):
                        idx+=1
                    #freq is freqs[idx-1] and freqs[idx], find closer
                    min_dif = min(freq-freqs[idx-1], freqs[idx]-freq)
                    if (min_dif == freq-freqs[idx-1]):
                        new_content.append(str(round(freqs[idx-i], 1))+ "\n")
                        #new_content.append(str(freqs[idx-i])+ "\n")
                    else:
                        new_content.append(str(round(freqs[idx], 1))+ "\n")
                        #new_content.append(str(freqs[idx])+ "\n")
                j+=1

            else:
                #break if out of bounds
                break
            
                
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
        print(len(new_content))
        
        dif = max_consec - min_consec
        
        #For every line
        for j in range(len(new_content)):
            
            c_line = new_content[j].split(",")
            #print(j,c_line)
            c_line[1] = int(c_line[1].rstrip())
            if (c_line[1] <= (min_consec + (0.25*dif))):
                c_line[1] = 1
            elif ((c_line[1] > (min_consec + (0.25*dif))) and (c_line[1] < (max_consec - (0.25*dif)))):
                c_line[1] = 2
            elif (c_line[1] >= (max_consec - (0.25*dif))):
                c_line[1] = 3
            
            new_content[j] = c_line[0] + "," + str(c_line[1]) + "\n"
            
    #WRITE TO NEW FILE
            
    with open(os.path.join(write_dir, name[i]), 'w+') as f:
        f.writelines("%s" % line for line in new_content)
    break
