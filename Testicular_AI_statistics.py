import SimpleITK as sitk
import numpy as np
import pandas as pd
import os


def get_stats(gt_rois,pred_rois):

    TP_1 = 0
    FN_1 = 0
    FP_1 = 0
    TN_1 = 0
    TP_2 = 0
    FN_2 = 0
    FP_2 = 0
    TN_2 = 0
    TP_other = 0
    FN_other = 0 
    FP_other = 0
    print(np.unique(gt_rois),np.unique(pred_rois))
    a= np.unique(gt_rois)
    b= np.unique(gt_rois)
    a1 = gt_rois.max()
    b1= pred_rois.max()
    if gt_rois.max() == 0:
        if pred_rois.max()==0:
            TN_1+=1
            TN_2+=1
    else:
        for gint in np.unique(gt_rois):
            
            if gint ==0:
                continue
            print(gint)
            groi = np.zeros(shape=gt_rois.shape, dtype=int)
            groi[gt_rois == gint] = gint
            print(np.unique(groi), np.count_nonzero(groi))
            if np.count_nonzero(groi[pred_rois==gint]) > 0:
                print(gint, np.count_nonzero(groi[pred_rois==gint]))
                if gint ==1:
                    TP_1 += 1
                if gint ==2:
                    TP_2 +=1
                if gint>2:
                    TP_other = gint

            else:
                if gint ==1:
                    FN_1 += 1
                if gint ==2:
                    FN_2 +=1
                if gint>2:
                    FN_other = gint


        for pint in np.unique(pred_rois):
            if pint ==0:
                continue
            proi = np.zeros(shape=pred_rois.shape, dtype=int)
            proi[pred_rois == pint] = pint
            if np.count_nonzero(proi[gt_rois == pint]) > 0:
                continue
            else:
                if pint ==1:
                    FP_1 += 1
                if pint ==2:
                    FP_2 +=1
                if pint>2:
                    FP_other = pint

    return TP_1, FN_1, FP_1, TN_1, TP_2, FN_2, FP_2, TN_2, TP_other, FN_other, FP_other, a, b, a1,b1

if __name__ == "__main__":
    for jk, nametreat in enumerate(["Dataset101_MRI-testie", "Dataset102_MRI-testie"]):

        gtDir = f'/nnUNet_raw/{nametreat}/labelsTe'
        suv_dir= f'/nnUNet_raw/{nametreat}/imagesTe'
        eval_data = []

        mainDir = f'/nnUNet_results/{nametreat}/nnUNetTrainer__nnUNetPlans__3d_fullres/test_set/'
        if not os.path.exists(mainDir):
            continue
        result= f'/nnUNet_results/{nametreat}/nnUNetTrainer__nnUNetPlans__3d_fullres/Results/test_set/'
        if not os.path.exists(result):
            os.makedirs(result)        
        print("reading file folder ",mainDir)
        eval_data= [f for f in sorted(os.listdir(mainDir)) if f.endswith('.nii.gz')]
        print(f"Number of files in the folder ",len(eval_data))
        df = []
        dfl1 = []
        dfl2 = []
        dfl3 = []

        for i, file_i in enumerate(eval_data):
            # if file_i not in ["id-014_2013-11-06.nii.gz", "id-024_2015-04-21.nii.gz", "id-024_2014-08-06.nii.gz"]:
            #     continue
            print("reading file: ",file_i)
            
            gt_name= file_i.replace('_0000', '')
            if not os.path.exists(os.path.join(gtDir,gt_name)):
                print(os.path.join(gtDir,gt_name))
                continue
            image = sitk.ReadImage(os.path.join(mainDir,file_i))
            pet_origin = image.GetOrigin()
            img_spacing = image.GetSpacing()
            preds = sitk.GetArrayFromImage(image)
    
            

            if not os.path.exists(os.path.join(gtDir,gt_name)):
                print(os.path.join(gtDir,gt_name))
                continue

            image_gt = sitk.ReadImage(os.path.join(gtDir,gt_name))
            mask_origin = image_gt .GetOrigin()
            gt = sitk.GetArrayFromImage(image_gt)

            intersect_tr = np.count_nonzero(preds[gt>0]>0)
            total_pred_tr = np.count_nonzero(preds>0)
            total_gt_tr = np.count_nonzero(gt>0)
            combo_tr = preds+gt
            union_tr = np.count_nonzero(combo_tr>0)
            if total_pred_tr==0 and total_gt_tr==0:
                dice_tr =  np.nan
                iou_tr = np.nan
            else:
                dice_tr = 2*intersect_tr/(total_pred_tr+total_gt_tr)
                iou_tr = intersect_tr/union_tr

            TP_1, FN_1, FP_1, TN_1, TP_2, FN_2, FP_2, TN_2, TP_other, FN_other, FP_other, a, b, a1,b1= get_stats(gt.astype('uint8'), preds.astype('uint8'), img_spacing,gt_name)



            d_slide = {'image': gt_name, 'gt_testies': a,'pred_testies': b, 'gt_testies_list': a1,'pred_testies_list': b1,
                    'dice_tr': dice_tr, 'iou_tr': iou_tr,
                    'TP_1': TP_1, 'TN_1': TN_1, 'FN_1':FN_1, 'FP_1': FP_1,
                    'TP_2': TP_2, 'TN_2': TN_2, 'FN_2':FN_2, 'FP_2': FP_2,
                    "TP_other": TP_other, "FN_other" :FN_other , "FP_other" : FP_other}

            df.append(d_slide)
    filename5 = f'test_case_stats_cc.xlsx'
    pd.DataFrame.from_dict(df).to_excel(os.path.join(result, filename5))

