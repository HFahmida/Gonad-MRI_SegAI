import SimpleITK as sitk
import numpy as np
import pandas as pd
import os

def extract_volume_GT(mask_dir, out_dir, outdir, mod):

    patient_list = [f for f in sorted(os.listdir(mask_dir)) if f.endswith("_modified.nii.gz")]

    list_stat2= []

    print(f"Number of files in the folder ", len(patient_list))
    for i, id in enumerate(patient_list):   
        print("reading id: ",id)
        id_info= id.replace(".nii.gz", "")
        patient_path= os.path.join(mask_dir, id)
        image_mask = sitk.ReadImage(patient_path)
        img_spacing = image_mask.GetSpacing()
        mask_cc_pred= sitk.ConnectedComponent(image_mask)
        gt_rois = sitk.GetArrayFromImage(mask_cc_pred)
        N_pred = np.max(gt_rois)

 
        overall_testicular_volume = np.count_nonzero(gt_rois > 0) * img_spacing[0] * img_spacing[1] * img_spacing[2] * 0.001
        if N_pred>2 or N_pred<2:
            new_mask= sitk.GetImageFromArray(gt_rois)
            new_mask.CopyInformation(image_mask)
            for meta_elem in image_mask.GetMetaDataKeys():
                new_mask.SetMetaData(meta_elem, image_mask.GetMetaData(meta_elem))
            sitk.WriteImage(new_mask,os.path.join(outdir,id)) 
        elif N_pred<2:
            print(id,  N_pred) 
        else:
            
            no_testis =  gt_rois.max()
            groi = np.zeros(shape=gt_rois.shape, dtype=int)
            x_min1 = np.min(np.nonzero(gt_rois==1)[2])            
            x_min2 = np.min(np.nonzero(gt_rois==2)[2])

            if x_min2<x_min1:
                groi[gt_rois==2]=1
                groi[gt_rois==1]=2
            else: 
                groi[gt_rois==1]=1
                groi[gt_rois==2]=2    
            right =  np.count_nonzero(groi == 1) * img_spacing[0] * img_spacing[1] * img_spacing[2] * 0.001
            left =  np.count_nonzero(groi == 2) * img_spacing[0] * img_spacing[1] * img_spacing[2] * 0.001
            xminr = np.min(np.nonzero(groi==1)[2])            
            xminl = np.min(np.nonzero(groi==2)[2])

            list_stat2.append({"Patients ID": id_info, "Number of Testicales" : no_testis, "Total testicular volume [cm^3]" : overall_testicular_volume,
                                    f"Right_testicular_volume": right, "Left_testicular_volume": left, "right_X_min": xminr, "Left_X_min" : xminl})
        filename1 = f'Total_volume_{mod}_Unannotated_Images.xlsx'
        pd.DataFrame(list_stat2).to_excel(os.path.join(out_dir, filename1))



if __name__ == "__main__":

    gtDir =f'/nnUNet_raw/Dataset102_MRI-testie/labelsTe'
    ai_pred_path =  f'/nnUNet_results/Dataset102_MRI-testie/nnUNetTrainer__nnUNetPlans__3d_fullres/test_set/'
    stats_path= f'/nnUNet_results/Dataset102_MRI-testie/nnUNetTrainer__nnUNetPlans__3d_fullres/Results/test_set/'
    os.makedirs(stats_path, exist_ok=True)
    
    ab = "test_set_stats"
    extract_volume(ai_pred_path, stats_path, mod="AI",ab=ab)
    extract_volume(gtDir, stats_path, mod="GT", ab=ab)

