import SimpleITK as sitk
import numpy as np
import pandas as pd
import os
import cc3d
'''
This function calculates statistics on the connected components calculated segmentation masks.
This code will calculate statistics in two ways. one will be with pure AI outputs where we consider all 
segmentation masks including TP and FP. In the second method, we manually identify the FP and remove the FP 
from the semgmentation mask to calculate the statistics. 

*** important note: for the removal of the FP from sengmentation mask, it is required to create a text file
called " NIH_cases.txt" where all the patients id separeted by "=" sign and FP segment numbers in "," separated format.
the file name can be anything but but needed to be changed in the code as check. check the main function to change the 
file name. give the file path ***

The statistics this code calculates: 

1. Number of lesions : highest number of connected component in segmenstation mask
2. Overall SUVmax : each lesion SUVmax and taking max value of all. 
3. Overall SUVmean: mean of SUV value of all lesions
4. Overall lesion volume : sum of volume of all lesions calculated in cm^3
5. overall total lesion glycolysis : SUVmean*volume for each lesion and sum them all. 
6. We also calculate each lesions SUVmax, SUVmean and lesion volume and lesion glucolysis. 

results will be written into excel files and saved in to the mask_dir. change the directory if you need somewhere 
else to be stored. 
'''

def lesion_level_stats(mask_dir, suv_dir,out_dir, mod, aname):

    mask_data = [f for f in sorted(os.listdir(mask_dir)) if f.endswith('.nii.gz')]

    list_of_glycolysis=[]
    list_total_Lesion_glycolysis = []
    list_stat= []
    subject_id =[]
    a=[]
    b=[]
    c=[]
    d=[]
    print(f"Number of files in the folder ", len(mask_data))

    for i, file_i in enumerate(mask_data):
        # if 'PHEO_D_01' in file_i:
        #     continue

        list_lesion_glycolysis = []
        # mask_dir2 = '/data/MIP/fahmida_PETCT/Fahmida_PETCT/biowulf_nnUNet/NIH_Cases_converted/OS_NK_New/OS-NK_28Day_Mask_MERGED'
        # if not os.path.exists(os.path.join(mask_dir2,file_i)):
        #     continue
        print("reading file: ",file_i)
        image_mask = sitk.ReadImage(os.path.join(mask_dir,file_i))
        img_spacing = image_mask.GetSpacing()
        mask_direction = image_mask.GetDirection()
        mask1 = sitk.GetArrayFromImage(image_mask)
        print(img_spacing, mask_direction)
        mask, N_gt = cc3d.connected_components(mask1,return_N=True)


        # if file_i == 'NK-008-2_pred_cc.nii.gz':
        #     SUV_name= 'NK-008-2_0000.nii.gz'
        # elif file_i == 'NK-011-2_pred_cc.nii.gz':
        #     SUV_name= 'NK-011_0000.nii.gz'
        # elif file_i == 'NK-014-2_pred_cc.nii.gz':
        #     SUV_name= 'NK-014_0000.nii.gz'
        # else:
        SUV_name = str.replace(file_i, '.nii.gz', '_0000.nii.gz')
        # name = str.replace(file_i, '.nii.gz_cc.nii.gz', '')
        name = file_i
        # SUV_name = str.replace(file_i, '_pred_cc.nii.gz', '_0000.nii.gz')
        # name = str.replace(file_i, '_pred_cc.nii.gz', '')
        # print(name)
        if np.count_nonzero(mask > 0) == 0:
            continue

        image_suv = sitk.ReadImage(os.path.join(suv_dir,SUV_name))
        suv_spacing = image_suv.GetSpacing()
        suv_direction = image_suv.GetDirection()
        print(suv_spacing, suv_direction)
        suv = sitk.GetArrayFromImage(image_suv)

        no_lesion= mask.max()
        lesion_max_suv = np.max(suv[mask > 0])
        lesion_mean_suv = np.mean(suv[mask > 0])
        overall_lesion_volume = np.count_nonzero(mask > 0) * img_spacing[0] * img_spacing[1] * img_spacing[2] * 0.001

        total_Lesion_glycolysis= 0
        for pint in range(0, mask.max()):
            proi = np.zeros(shape=mask.shape, dtype=int)
            proi[mask == (pint + 1)] = 1
            if (pint + 1) not in mask:
                continue
            lesion_glycolysis = np.mean(suv[proi > 0])*np.count_nonzero(proi > 0)*img_spacing[0]*img_spacing[1]*img_spacing[2] * 0.001
            total_Lesion_glycolysis += lesion_glycolysis
            list_lesion_glycolysis.append(lesion_glycolysis)
            each_lesion_max_suv=np.max(suv[proi > 0])
            each_lesion_mean_suv=np.mean(suv[proi > 0])
            each_lesion_volume = np.count_nonzero(proi > 0)*img_spacing[0]*img_spacing[1]*img_spacing[2]* 0.001
            
            a.append({"Patient id": file_i, "Lesion No": pint + 1, 'SUVmax':each_lesion_max_suv,'SUVmean':each_lesion_mean_suv, 'TTV [cm^3]':each_lesion_volume, 'TLG [cm^3]':lesion_glycolysis})
            # b.append({"Patient id": file_i, "Lesion No": pint + 1, 'SUVmax':each_lesion_max_suv})
            # c.append({"Patient id": file_i, "Lesion No": pint + 1, 'SUVmean':each_lesion_mean_suv})
            # d.append({"Patient id": file_i, "Lesion No": pint + 1, 'MTV':each_lesion_volume})

        list_total_Lesion_glycolysis.append(list_lesion_glycolysis)
        subject_id.append(name)
        stat_list= {"Patients ID": name ,"no lesion": no_lesion,"SUVmax": lesion_max_suv,
                    "SUVmean": lesion_mean_suv, "Overall lesion volume [cm^3]" : overall_lesion_volume,
                    "Total Lesion glycolysis [cm^3]": total_Lesion_glycolysis}
        list_stat.append(stat_list)
        # a1.append(a)
        # b1.append(b)
        # c1.append(c)
    filename1 = f'Lesion_Stats_{mod}_cases_{aname}.xlsx'
    pd.DataFrame(list_stat).to_excel(os.path.join(out_dir, filename1))

    # filename2= f'lesion_glycolysis_{mod}_cases_{aname}.xlsx'
    # pd.concat([pd.DataFrame(subject_id), pd.DataFrame(list_total_Lesion_glycolysis)], axis= 1).to_excel(os.path.join(out_dir, filename2))

    filename3= f'each_lesion_Tumorburden_{mod}_cases_{aname}.xlsx'
    # pd.concat([pd.DataFrame(subject_id), pd.DataFrame(a1)], axis= 1).to_excel(os.path.join(out_dir, filename3))
    pd.DataFrame.from_dict(a).to_excel(os.path.join(out_dir, filename3))
    # filename4= f'each_lesion_SUVmax_{mod}_cases_{aname}.xlsx'
    # # pd.concat([pd.DataFrame(subject_id), pd.DataFrame(b1)], axis= 1).to_excel(os.path.join(out_dir, filename4))
    # pd.DataFrame.from_dict(b).to_excel(os.path.join(out_dir, filename4))
    # filename5= f'each_lesion_SUVmean_{mod}_cases_{aname}.xlsx'
    # # pd.concat([pd.DataFrame(subject_id), pd.DataFrame(c1)], axis= 1).to_excel(os.path.join(out_dir, filename5))
    # pd.DataFrame.from_dict(c).to_excel(os.path.join(out_dir, filename5))
    # filename6= f'each_lesion_Volume_{mod}_cases_{aname}.xlsx'
    # # pd.concat([pd.DataFrame(subject_id), pd.DataFrame(c1)], axis= 1).to_excel(os.path.join(out_dir, filename5))
    # pd.DataFrame.from_dict(d).to_excel(os.path.join(out_dir, filename6))


if __name__=="__main__":
    
    # suv_dir= '/data/MIP/fahmida_PETCT/Fahmida_PETCT/AUTOPET_III/Images/Autopet/PSMA_Image_Fixed' 
    # out_dir= '/data/MIP/fahmida_PETCT/Fahmida_PETCT/AUTOPET_III/Images/Autopet/Stats'
    # mod= 'psma' #OS or NK
    mod= 'test'
    suv_dir= '/data/MIP/Fahmida_MRI_ovary/Run-1/nnUNet_raw/Dataset102_MRI-Ovary/imagesTe'
    out_dir= '/data/MIP/Fahmida_MRI_ovary/Run-1/nnUNet_results/Dataset102_MRI-Ovary/nnUNetTrainer__nnUNetPlans__2d/Results/test_set2'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    a= 'AI'
    mask_dir = '/data/MIP/Fahmida_MRI_ovary/Run-1/nnUNet_results/Dataset102_MRI-Ovary/nnUNetTrainer__nnUNetPlans__2d/test_set2'
    lesion_level_stats(mask_dir, suv_dir,out_dir, mod, a)

    a= 'GT'
    # suv_dir= '/data/MIP/fahmida_PETCT/Belzutifan_PNETs/DOTATATE_Analysis/DOTATATE_PETCT_nnUnet_format/Post-treatment/imagesTe'
    mask_dir2 = '/data/MIP/Fahmida_MRI_ovary/Run-1/nnUNet_raw/Dataset102_MRI-Ovary/labelsTe'
    lesion_level_stats(mask_dir2, suv_dir,out_dir, mod, a)
    

    # subjects= []
    # Without_TP =[]
    # file = open(os.path.join(mask_dir, 'OS_Cases.txt'), 'r')
    # for x in file.readlines():
    #     a, b = x.strip().rstrip("/n").split(":")
    #     c = [i.strip() for i in b.split(",")]
    #     print (c)
    #     if c == ['']:
    #         reject_lesion=[]
    #     else:
    #         reject_lesion= sorted([int(x) for x in c])
    #     TP= {a.strip(): reject_lesion}
    #     Without_TP.append(TP)
    # print(Without_TP)
    #
    # lesion_level_stats_withoutFP(mask_dir, suv_dir, out_dir, Without_TP, mod)

    # scp - r /data/MIP/fahmida_PETCT/Fahmida_PETCT/check nnunet results/RUN-1/PHEO_case air@air-lambda.nci.nih.gov:/home/air/Shared_Drives/MIP_network/MIP/AIR/Projects/Project_OS_Kaplan/PHEO_cases/PHEO_corrected_annoazie/Failure Analysis/Prediction