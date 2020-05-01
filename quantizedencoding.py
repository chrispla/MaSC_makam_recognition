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
print(freq_list_len)
print(freqs)

#Traverse all paths
for i in range(len(all_paths)):
    
    #For every file
    with open(all_paths[i]) as f:
        content = f.readlines() #read file into list of lines
        
        #QUANTIZATION
        
        #For every line
        for j in range(len(content)):
            
            freq = float(content[j].rstrip())
            
            #remove 0 and over freq_max (and negative, if they exist) values
            if ((freq <= 0) or (freq > freq_max)):
                content.remove(j)
            else:
                #find closest value to quantize to (should be implemented more efficiently in the future)
                idx = 0
                while (freq < freqs[idx]):
                    idx+=1
                #freq is freqs[idx-1] and freqs[idx], find closer
                min_dif = min(freq-freq[idx-1], freq[idx]-freq)
                if (min_dif == freq-freq[idx-1]):
                    content[j] = str(round(freq[idx-i], 1))+ "\n"
                else:
                    content[j] = str(round(freq[idx], 1))+ "\n"
                
        #ENTRY MERGE 
                    
        #count consecutive entries
        consec = 1
        
        #keep min and max for significance value
        min_consec = 100000
        max_consec = 0   
            
        #For every line
        idx = 0
        while (True):
            if (idx+1 <= len(content)):  
                if (content[idx] == content[idx+1]):
                    #if next entry same as current, remove and keep track of streak
                    content.remove(idx+1)
                    consec+=1
                else:
                    #if next line different, alter current entry, increment idx, end streak
                    n_line = (content[j].rstrip()) + "," + str(consec) + "\n"
                    idx+=1
                    if (consec > max_consec):
                        max_consec = consec
                    if (consec < min_consec):
                        min_consec = consec
                    consec = 1
        
        #SIGNIFICANCE VALUE
        
        dif = max_consec - min_consec
        
        #For every line
        for j in range(len(content)):
            
            c_line = content[j].split(",")
            c_line[1] = int(c_line[1].rstrip())
            if (c_line[1] <= (min_consec + (0.25*dif))):
                c_line[1] = 1
            elif ((c_line[i] > (min_consec + (0.25*dif))) and (c_line[i] < (max_consec - (0.25*dif)))):
                c_line[1] = 2
            elif (c_line[1] >= (max_consec - (0.25*dif))):
                c_line[1] = 3
            
            content[j] = c_line[0] + "," + str(c_line[1]) + "\n"
            
    #WRITE TO NEW FILE
            
    with open(os.path.join(write_dir, name[i]), 'w+') as f:
        f.writelines("%s" % line for line in content)
