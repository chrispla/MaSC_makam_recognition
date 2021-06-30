# Turkish Makam Recognition

Code for the deep learning approaches to makam recognition on the CompMusic Dunya Turkish makam corpus

### File reading

Files are read from the soundfiles folder, and their makam is retrieved by constructing the name of the pitch file from the name of the soundfile and finding in which folder in otmm_makm_recognition_dataset/data they exist. An array Y also holds all labels (makams).

### CNN Preprocessing

Files are read as time series using the `librosa.core.load` method with default parameters, so the audio is automatically resampled to a rate of 22050. The constant-Q transform of the audio signal is then computed using `librosa.core.cqt`, and all the computed cqts are appended into an array holding all cqts keeping the same order as the label array `Y`. Default parameter values for the `librosa.core.cqt` method are used, keeping the 22050 sampling rate and using a hop length of 512, except for the number of bins which is set to 371 and the bins per octave which is set to 53. The reasoning behind this is that in Turkish music theory the octave is divided into 53 equal intervals known as commas, so to capture this frequency granularity we need to set the parameters of the transform accordingly. The number of bins is set to 371 to account for 7 octaves with 53 bins each. 
While one dimension of the cqt array for each audio file is going to reflect those 371 bins, the other varies according to the duration of the soundfile. While audio truncation could have been used, depending on the variance of duration of pieces, a lot of useful information may have been used. Linear interpolation over a 2D grid is instead used to resample all the cqt arrays to a size of (371, 3710). The selection of 3710 is based on a reasonable balance between not downsampling the input cqt arrays too much while also avoiding having to upsample too many short pieces. The resampled cqts are placed in array X.

### LSTM Preprocessing

My algorithm for converting the pitch series files in the CompMusic Dunya makam corpus is given below. Its purpose is to reduce the dimensionality of the pitch series information by compressing the note durations into a 3-level significance scale to separate decorative notes and notes significant to recognizing the tonic from other notes.

```javascript
for (all lines):
  delete value if 0
  quantize value to scale (e.g. 53ET) 
  // pad start of pitch value with zeros appropriately so that the length of the pitch value is 5 e.g. 130 -> 00130
for (all lines):
  merge all neighboring values to one, and keep track of the number of consecutive occurrences k 
  // e.g. 1300\n 1200\n 1200\n 1200\n 760\n 760\n will become 1300,1\n 1200,3\n 760,2\n
find kmin and kmax		
for (all lines):
  if k < (kmin + 0.25*(kmax-kmin)): replace with 1
	if (kmin + 0.25*(kmax-kmin)) < k < (kmin + 0.75*(kmax-kmin)): replace with 2
	If k > (kmin + 0.75*(kmax-kmin)): replace with 3
```

### Train-Test Split

A test size of 33% is selected by shuffling the data and splitting them in a stratified fashion. At this stage, further methods can be used to get a better picture of results due to the size of the dataset.

### CNN Model

The sequential model, the conventional method of a linear stack of layers, is used. The architecture of the network consists of 6 parts: convolution, pooling, batch normalization, flattening, the fully connected layer, and dropout.

3 convolutional layers are used, with 64 filters, the relu activation function, and a (3,3) kernel size for the first two with a (2,2) kernel size for the third. At each layer, 2 dimensional max pooling with a pool size of (2,2) and batch normalization is performed. The output is then flattened and fed to a dense layer of 64 neurons with the relu activation function. After dropout, the final output comes from a dense layer with 20 neurons, as we have 20 makams, using the activation function softmax.




