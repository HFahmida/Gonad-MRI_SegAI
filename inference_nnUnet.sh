#!/bin/bash
#SBATCH --partition=gpu
#SBATCH --cpus-per-task=20 
#SBATCH --gres=gpu:a100:1
#SBATCH --mem=40g
#SBATCH --time=10-0:00:00
#SBATCH --output="Path-to-bashfile/inference_nnUNet.out"
#SBATCH --error="Path-to-bashfile/inference_nnUNet.err"

cd Path-to-bashfile
"Activate conda environment"

export nnUNet_raw="Path-to-nnUNet_downloaded_folder/nnUNet_raw"
export nnUNet_preprocessed="Path-to-nnUNet_downloaded_folder/nnUNet_preprocessed"
export nnUNet_results="Path-to-nnUNet_downloaded_folder/nnUNet_results"

 #chage the "XXX to a number, see the readme_dataset.txt file. 

OMP_NUM_THREADS=1 nnUNetv2_predict -d DatasetXXX_MRI-Ovary-Cyst -i $nnUNet_raw/DatasetXXX_MRI-Ovary-Cyst/imagesTe -o $nnUNet_results/DatasetXXX_MRI-Ovary-Cyst/nnUNetTrainer__nnUNetPlans__3d_fullres/test_set/ -f all -tr nnUNetTrainer -c 3d_fullres -p nnUNetPlans

