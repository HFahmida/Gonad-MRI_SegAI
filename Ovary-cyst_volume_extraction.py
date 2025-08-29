import SimpleITK as sitk
import numpy as np
import pandas as pd
import os
import cc3d
import glob


def volumetrics(mask1,ovary_mask, img_spacing, no):

    halfx= int(mask1.shape[2]/2)
    a= np.where(mask1[:, : , :halfx]==no)
    ovary_mask[:, : , :halfx][a] = 1
    b= np.where(mask1[:, : , halfx:]==no)
    ovary_mask[:, : , halfx:][b] = 2

    overall_Ovary_volume = np.count_nonzero(ovary_mask > 0) * img_spacing[0] * img_spacing[1] * img_spacing[2] * 0.001
    right_volume = np.count_nonzero(ovary_mask == 1) * img_spacing[0] * img_spacing[1] * img_spacing[2] * 0.001
    left_volume = np.count_nonzero(ovary_mask == 2) * img_spacing[0] * img_spacing[1] * img_spacing[2] * 0.001

    return overall_Ovary_volume,right_volume,left_volume

def extract_volume(mask_dir, out_dir, mod):

    patient_list = [f for f in sorted(os.listdir(mask_dir)) if f.endswith(".nii.gz")]
    list_stat2= []
    a=[]
    print(f"Number of files in the folder ", len(patient_list))
    for i, id in enumerate(patient_list):   
        print("reading id: ",id)
        id_info= id.replace(".nii.gz", "")
        patient_path= os.path.join(mask_dir, id)
        image_mask = sitk.ReadImage(patient_path)
        img_spacing = image_mask.GetSpacing()
        mask1 = sitk.GetArrayFromImage(image_mask)

        if np.count_nonzero(mask1 > 0) == 0:
            print(f"this patient has no contour")
            T_OV=0
            R_OV=0
            L_OV=0
            T_CV=0
            R_CV=0
            L_CV=0

        
        ovary_mask = np.zeros_like(sitk.GetArrayFromImage(image_mask))
        T_OV,R_OV,L_OV = volumetrics(mask1,ovary_mask, img_spacing, no=1)
        if np.max(mask1)==2:
            cyst_mask = np.zeros_like(sitk.GetArrayFromImage(image_mask))
            T_CV,R_CV,L_CV = volumetrics(mask1,cyst_mask, img_spacing, no=2)
            a= "Yes"
        else: 
            a= "No"
            T_CV=0
            R_CV=0
            L_CV=0

        list_stat2.append({"Patients ID": id_info, "Total Ovary volume [cm^3]" : T_OV,
                            "Right Ovary Volume": R_OV,"Left Ovary Volume": L_OV,"Cyst": a, "Total Cyst volume [cm^3]" : T_CV,
                            "Right Cyst  Volume": R_CV,"Left Cyst  Volume": L_CV })
    filename1 = f'Total_volume_{mod}.xlsx'
    pd.DataFrame(list_stat2).to_excel(os.path.join(out_dir, filename1))
      


if __name__ == "__main__":
    for rn in ["Run-5"]:
        for jk, nametreat in enumerate(["Dataset101_MRI-Ovary-Cyst", "Dataset102_MRI-Ovary-Cyst"]):

            ai_pred_path = f'{rn}/nnUNet_results/{nametreat}/nnUNetTrainer__nnUNetPlans__3d_fullres/test/'
            stats_path= f'/nnUNet_results/{nametreat}/nnUNetTrainer__nnUNetPlans__3d_fullres/Results/test/'
            if not os.path.exists(ai_pred_path):
                continue
            if not os.path.exists(stats_path):
                os.makedirs(stats_path)
            gtDir = f'/nnUNet_raw/{nametreat}/labelsTe'
            extract_volume(ai_pred_path, stats_path, mod="AI")
            extract_volume(gtDir, stats_path, mod="GT")