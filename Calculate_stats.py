import SimpleITK as sitk
import numpy as np
import pandas as pd
import os



def get_stats(gt_arr,pred_arr, img_spacing,gt_name):
    dl = []
    dl1=[]
    dl2 = []
    dl3 = []
    gt_rois= gt_arr
    pred_rois= pred_arr

    TP = 0
    FN = 0
    FP = 0
    TN = 0

    
    a= len(np.unique(gt_rois)[1:])
    b= len(np.unique(pred_rois)[1:])
    print(a, b, np.unique(gt_rois)[1:], np.unique(pred_rois)[1:])
    if gt_rois.max() == 0:
        if pred_rois.max()==0:
            TN+=1
        else:
            for pint in range(0, pred_rois.max()):
                proi = np.zeros(shape=pred_rois.shape, dtype=int)
                proi[pred_rois == (pint + 1)] = 1
                if np.count_nonzero(proi>0)>0:
                    FP += 1
                    dd1 = {'image': gt_name, 'size': np.count_nonzero(proi>0)*img_spacing[0]*img_spacing[1]*img_spacing[2], 'outcome': 'FP'}
                    # d = pd.DataFrame(dd)
                    dl3.append(dd1)
    else:
        for gint in range(0, gt_rois.max()):
            groi = np.zeros(shape=gt_rois.shape, dtype=int)
            groi[gt_rois == (gint + 1)] = 1
            if np.count_nonzero(groi[pred_arr>0]) > 0:
                TP += 1
                dd = {'image': gt_name, 'size': np.count_nonzero(groi>0)*img_spacing[0]*img_spacing[1]*img_spacing[2], 'outcome': 'TP'}
                # d = pd.DataFrame(dd)
                dl1.append(dd)
            elif np.count_nonzero(groi[pred_arr==0]) > 0:
                FN += 1
                dd = {'image': gt_name, 'size': np.count_nonzero(groi>0)*img_spacing[0]*img_spacing[1]*img_spacing[2], 'outcome': 'FN'}
                # d = pd.DataFrame(dd)
                dl2.append(dd)

    print(TP, FN, FP, TN)
    return TP, FN, FP, TN, dl1, dl2, dl3, a, b

def maual_roi_separation(gt, pred):
    gt_ov = np.zeros(shape=gt.shape, dtype=int)
    gt_cy = np.zeros(shape=gt.shape, dtype=int)
    print(gt.shape, pred.shape)
    halfx= int(gt.shape[2]/2)

    a= np.where(gt[:, : , :halfx]==1)
    gt_ov[:, : , :halfx][a] = 1
    b= np.where(gt[:, : , halfx:]==1)
    gt_ov[:, : , halfx:][b] = 2

    a= np.where(gt[:, : , :halfx]==2)
    gt_cy[:, : , :halfx][a] = 1
    b= np.where(gt[:, : , halfx:]==2)
    gt_cy[:, : , halfx:][b] = 2


    preds_ov = np.zeros(shape=pred.shape, dtype=int)
    preds_cy = np.zeros(shape=pred.shape, dtype=int)

    halfx= int(pred.shape[2]/2)
    a= np.where(pred[:, : , :halfx]==1)
    preds_ov[:, : , :halfx][a] = 1
    b= np.where(pred[:, : , halfx:]==1)
    preds_ov[:, : , halfx:][b] = 2

    a= np.where(pred[:, : , :halfx]==2)
    preds_cy[:, : , :halfx][a] = 1
    b= np.where(pred[:, : , halfx:]==2)
    preds_cy[:, : , halfx:][b] = 2
    return gt_ov, gt_cy, preds_ov, preds_cy

if __name__ == "__main__":

    for jk, nametreat in enumerate(["Dataset107_MRI-Ovary-Cyst"]):
        gtDir = f'nnUNet_raw/{nametreat}/labelsTe'
        suv_dir= f'nnUNet_raw/{nametreat}/imagesTe'
        eval_data = []

        mainDir = f'/nnUNet_results/Dataset101_MRI-Ovary-Cyst/nnUNetTrainer__nnUNetPlans__3d_fullres/test/'
        if not os.path.exists(mainDir):
            continue
        result= f'nnUNet_results/Dataset101_MRI-Ovary-Cyst/nnUNetTrainer__nnUNetPlans__3d_fullres/Results/test/'
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
            print("reading file: ",file_i)
            
            gt_name= file_i.replace('_0000', '')
            if not os.path.exists(os.path.join(gtDir,gt_name)):
                print(os.path.join(gtDir,gt_name))
                continue
            pred_image = sitk.ReadImage(os.path.join(mainDir,file_i))
            
            img_spacing = pred_image.GetSpacing()
            preds_mask = sitk.GetArrayFromImage(pred_image)

            if not os.path.exists(os.path.join(gtDir,gt_name)):
                print(os.path.join(gtDir,gt_name))
                continue

            image_gt = sitk.ReadImage(os.path.join(gtDir,gt_name))
            mask_origin = image_gt .GetOrigin()
            gt = sitk.GetArrayFromImage(image_gt)
            gt_ov, gt_cy, preds_ov, preds_cy= maual_roi_separation(gt, preds_mask)

            intersect_ov = np.count_nonzero(preds_ov[gt_ov>0]>0)
            total_pred_ov = np.count_nonzero(preds_ov>0)
            total_gt_ov = np.count_nonzero(gt_ov>0)
            combo_ov = preds_ov+gt_ov
            union_ov = np.count_nonzero(combo_ov>0)
            if total_pred_ov==0 and total_gt_ov==0:
                dice_ov =  np.nan
                iou_ov = np.nan
            else:
                dice_ov = 2*intersect_ov/(total_pred_ov+total_gt_ov)
                iou_ov = intersect_ov/union_ov

            TP_ov, FN_ov, FP_ov, TN_ov, dl1_ov, dl2_ov, dl3_ov, a_ov, b_ov= get_stats(gt_ov.astype('uint8'), preds_ov.astype('uint8'), img_spacing,gt_name)
            
            # calculating stats for only cyst
            halfx= int(gt.shape[2]/2)
            a= np.where(gt[:, : , :halfx]==2)
            gt_ov[:, : , :halfx][a] = 1
            b= np.where(gt[:, : , halfx:]==2)
            gt_ov[:, : , halfx:][b] = 2

            intersect_cy = np.count_nonzero(preds_cy[gt_cy>0]>0)
            total_pred_cy = np.count_nonzero(preds_cy>0)
            total_gt_cy = np.count_nonzero(gt_cy>0)
            combo_cy = preds_cy+gt_cy
            union_cy = np.count_nonzero(combo_cy>0)
            if total_pred_cy==0 and total_gt_cy==0:
                dice_cy =  np.nan
                iou_cy = np.nan
            else:
                dice_cy = 2*intersect_cy/(total_pred_cy+total_gt_cy)
                iou_cy = intersect_cy/union_cy
            
        
            TP_cy, FN_cy, FP_cy, TN_cy, dl1_cy, dl2_cy, dl3_cy, a_cy, b_cy= get_stats(gt_cy.astype('uint8'), preds_cy.astype('uint8'), img_spacing,gt_name)


            d_slide = {'image': gt_name, 'gt_lesion_no_ov': a_ov,'pred_lesion_no_ov': b_ov,'gt_lesion_no_cy': a_cy,'pred_lesion_no_cy': b_cy,
                    'dice_ov': dice_ov, 'iou_ov': iou_ov, 'dice_cy': dice_cy, 'iou_cy': iou_cy, 
                    'TP_ov': TP_ov, 'TN_ov': TN_ov, 'FN_ov':FN_ov, 'FP_ov': FP_ov,
                    'TP_cy': TP_cy, 'TN_cy': TN_cy, 'FN_cy':FN_cy, 'FP_cy': FP_cy}

            df.append(d_slide)
        filename5 = f'test_case_stats_cc.xlsx'
        pd.DataFrame.from_dict(df).to_excel(os.path.join(result, filename5))

