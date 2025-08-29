# Gonad-MRI_SegAI
## Overview 
This repository describes an AI model to run on MR images to segment GONADS and ovarian cysts. 
## Introducing Gonad-MRI_SegAI :rocket:
This repository is created to release the model weights for the following abstract: "AI-based Approach for Automated Gonad Volume Quantification Using MRI in Healthy Adolescents across Puberty".
Please cite if you are using the model: ***coming soon***
## Installation and prerequisites
First clone the repo and cd into the directory:
```
git clone https://github.com/HFahmida/Gonad-MRI_SegAI.git
cd Gonad-MRI_SegAI
```
Then create a conda env and install the dependencies:
```
conda create -n mri_gonad python=3.10 -y
conda activate mri_gonad
```
Install nnUNet. Installation process can be found in the following link: [documentation/installation_instructions.md](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/installation_instructions.md)

## How to use
### Data Preparation

Image file should be in nifti format. Use the **dicom_to_nifti_conversion.py** file to convert dicom images
```
python dicom_to_nifti_conversion.py [--dicom_path dicom_folder] [--nifti_path nifti-outpath]
```
nnU-Net expects datasets in a structured format. This format is inspired by the data structure of the Medical Segmentation Decthlon. Please read the following link for dataset conversion: [how-to-use-nnUNet](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/how_to_use_nnunet.md)

For duel modality (FS-T2W and T2W AI model), FS T2W MRIs should be renamed as channel 1 input with ***'_0000.nii.gz'*** extension and T2W MRIs ***'_0001.nii.gz'***. Example FS-T2W image: ***id-023_2014-09_0000.nii.gz***, T2W Image: ***id-023_2014-09_0001.nii.gz***

For single modality (FS-T2W AI or T2W AI model), both MRIs should be renamed as channel 1 input individually with ***'_0000.nii.gz'*** extension. Example FS-T2W image: ***id-023_2014-09_0000.nii.gz*** for FS T2W only AI, T2W Image: ***id-023_2014-09_0000.nii.gz*** for T2W only AI

## Inference
#### Model weights
Download the Pretrained model checkpoints and Images from the following link: [MRI-Gonad_SegAI](https://zenodo.org/records/15329885?token=eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjU5YzI0MjJkLWNkMDktNDE1ZS05Mjc0LTc3YjM2Y2EyMWM4OCIsImRhdGEiOnt9LCJyYW5kb20iOiIyM2M4MTU0NjRlZjg2NTkxZDQxOTQyNjIwMmZjZTM0NCJ9.ivvEtitWku8DaeJXeBRrlW4Vtmq1EINRcCcXXhKXBKDImgRiEDnQFCAro344ANAZB1zH09yW9neM44oF9-MhAg)
We have provided scripts for running inference. 

#### For Ovary and Cyst Segmentation model: 
**Dataset101_MRI-Ovary-Cyst: FS-T2W and T2W MRI [T2W image is resampled to FS T2W image size and spacing] used to train the model** 
**Dataset102_MRI-Ovary-Cyst: FS-T2W MRI used to train the model** 
**Dataset103_MRI-Ovary-Cyst: T2W MRI used to train the model**  
```
sbatch inference_Ovary-Cyst_AI_model.sh 

```

#### For testicle Segmentation model: 
**Dataset101_MRI-testie: Testicular Whole model trained using T2W MRI** 
**Dataset101_MRI-testie: Testicular side-separated model trained using T2W MRI** 

```
sbatch inference_Testicular_AI_model.sh 

```


