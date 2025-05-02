# MRI-Ovary-Cyst-AI
This repository describes an AI model to run on MR images to segment ovary and ovarian cysts. 

###Under Constructions

## This repository is created to release the model weights for the following abstract: "AI-based Approach for Ovary and Ovarian Cyst Segmentation at  MRI in Pre-pubertal and Pubertal Females".
## Please cite if you are using the model: 
### 

### We have used 3D full resolution [nnUNet framework](https://www.nature.com/articles/s41592-020-01008-z). Follow the instrustion below to run inference on new dataset using our model.

### Insturctions: 
1. First, create a conda environment. You can name it to your liking; for example, ***'ct-env'***.
2. Install nnUNet. Installation process can be found in the following link: [documentation/installation_instructions.md](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/installation_instructions.md)
3. Download the model weights from the following link: [MRI-Ovary-Cyst-AI](https://zenodo.org/records/15329885?token=eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjU5YzI0MjJkLWNkMDktNDE1ZS05Mjc0LTc3YjM2Y2EyMWM4OCIsImRhdGEiOnt9LCJyYW5kb20iOiIyM2M4MTU0NjRlZjg2NTkxZDQxOTQyNjIwMmZjZTM0NCJ9.ivvEtitWku8DaeJXeBRrlW4Vtmq1EINRcCcXXhKXBKDImgRiEDnQFCAro344ANAZB1zH09yW9neM44oF9-MhAg)
4. The model weights should be inside the,***'nnUNet_results'*** folder. This is important for nnUNet to identify which dataset to process. Please make another folder ***'nnUNet_raw'***, ***'nnUNet_preprocessed'*** in the same file path where the unziped ***'nnUNet_results'*** folder is kept. 
5. nnU-Net expects datasets in a structured format. This format is inspired by the data structure of the Medical Segmentation Decthlon. Please read the following link for dataset conversion: [how-to-use-nnUNet](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/how_to_use_nnunet.md)
6. Image file should be in nifti format. USe the following package: [TCIA_processing](https://github.com/lab-midas/TCIA_processing) and use the following command to conver the images from DICOM to NIFTI:
  ````
    python3 -W ignore tcia_dicom_to_nifti.py /PATH/TO/DICOM/ /PATH/TO/NIFTI/
  ````
7.  FS T2W MRIs should be renamed as channel 1 input with ***'_0000.nii.gz'*** extension and T2W MRIs ***'_0001.nii.gz'***. Example PET image: ***id-023_2014-09_0000.nii.gz***, CT Image: ***id-023_2014-09_0001.nii.gz***
8. The images needs to be put inside the ***'/nnUNet_raw/Datasetxxx_MRI-Ovary-Cys/imagesTe'*** path. where xxx is the dataset number. see the readme_dataset.txt file to see, which dataset corresponds to what type of modalities used to train. 
9. ***"dataset_fingerprint.json"***, ***"nnUNetPlans.json"***,***"dataset.json"*** files should place inside ***"/nnUNet_preprocessed/Datasetxxx1_MRI-Ovary-Cys"*** path.    
10. Once everything is set, run the bash file ***"inference.sh"*** to run inference using the model weights. Please modify the folder paths ***'nnUNet_raw'***, ***'nnUNet_preprocessed'***,***'nnUNet_results'*** according to your set up directories inside the *.sh* file.

