import SimpleITK as sitk
import argparse
import os
import warnings
warnings.filterwarnings("ignore")
import glob
def dicom_to_nifti(imagefilepath, pathout):
    if not os.path.exists(pathout):
        try:
            series_reader = sitk.ImageSeriesReader() 
            dicom_names = series_reader.GetGDCMSeriesFileNames(imagefilepath)
            series_reader.SetFileNames(dicom_names)
            dicom_img = series_reader.Execute()   
            writer = sitk.ImageFileWriter()
            writer.SetFileName(pathout)
            writer.Execute(dicom_img)
            status= "completed"
            return status
        except RuntimeError:
            print("ERROR: ", imagefilepath)
            status= "Error"
            return status 

def get_args_parser(add_help=True):
    import argparse
    parser = argparse.ArgumentParser(description="Dicom to NIFTI Conversion")
    parser.add_argument("--dicom_path", default="None", type=str, help="MRI images in DICOM format")
    parser.add_argument("--nifti_path", default="None", type=str, help="File to save MRI images in NIFTI format")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Dicom to NIFTI Conversion")
    parser.add_argument("--dicom_path", default="None", type=str, help="MRI images in DICOM format")
    parser.add_argument("--nifti_path", default="None", type=str, help="File to save MRI images in NIFTI format")
    args = parser.parse_args()
    os.makedirs(args.nifti_path, exist_ok=True)
    filelist= glob.glob(os.path.join(args.dicom_path, "*", "*.nii.gz"))
        
    for index, file_location in enumerate(filelist):
        filename = file_location.split("/")[-1]+".nii.gz"
        pathout= os.path.join(args.nifti_path, filename)
        c = dicom_to_nifti(file_location, args.nifti_path)
        
