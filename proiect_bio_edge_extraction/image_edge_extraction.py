import numpy as np
import argparse
import glob
import cv2
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os
import ntpath
import PIL
from PIL import Image
import shutil
import sys
from os import path
from os import makedirs
import time
import datetime

directory = r'C:\Users\IBM_ADMIN\Desktop\Master MPI\BIO\proiect_bio_edge_extraction'
old_images_dir = r'C:\Users\IBM_ADMIN\Desktop\Master MPI\BIO\proiect_bio_edge_extraction\old_converted_images'
output_path = r''
time_details_file = r'C:\Users\IBM_ADMIN\Desktop\Master MPI\BIO\proiect_bio_edge_extraction\LogFile.txt'

def auto_canny(image, sigma=0.45):
	# compute the median of the single channel pixel intensities
	v = np.median(image)

	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)

	# return the edged image
	return edged



def convert_and_get_bmp_location():

    root = tk.Tk()
    root.withdraw()

    dirname = tk.filedialog.askdirectory(parent=root,initialdir=directory,title='Please select a directory')

    count_files = []
    bmp_files = []
    start = time.time()
    for root, dirs, files in os.walk(dirname):
            for file in files:
                    if file.endswith(".png") or file.endswith(".PNG") or file.endswith(".jpg") or file.endswith(".JPG") or file.endswith(".JPEG") or file.endswith(".jpeg"):
                        count_files.append(file)
                        print(file)
                        file_name = os.path.splitext(file)[0]
                        old_image_path = os.path.join(dirname, file)
                        new_image_path = os.path.join(old_images_dir,file)
                        im = Image.open(old_image_path)
                        rgb_im = im.convert('RGB')
                        rgb_im.save(dirname+"/"+file_name+".bmp")
                        shutil.move(old_image_path,new_image_path)

    print("\n\n----------------------------------------->Done!<-----------------------------------------\n\n -> %d file(s) were successfully converted to .JPG format.\n -> Original files can be found in the following location: " %len(count_files) + old_images_dir)
    end = time.time()
    timer = end-start
    with open(time_details_file, "w") as myfile:
            myfile.write("%s  : %d images were converted in %f seconds \n" %(str(time.strftime("%d/%b/%y %H:%M:%S")),len(count_files),round(timer, 3)))
    
    if len(count_files)==0:
        messagebox.showinfo("Conversion status", "No files to be converted into BMP!")
    elif len(count_files)==1:
        messagebox.showinfo("Conversion Completed!", "\n %d file has been successfully converted to .BMP format!\n " %len(count_files))
    elif len(count_files)==1:
        messagebox.showinfo("Conversion Completed!", "\n %d files have been successfully converted to .BMP format!\n " %len(count_files))

    for root, dirs, files in os.walk(dirname):
            for file in files:
                if file.endswith(".bmp") or file.endswith(".BMP"):
                        bmp_files.append(os.path.join(dirname, file))
                     
    return bmp_files


def loop_show_images(output_path):
        # loop over the images
        for imagePath in bmp_files:
                start = time.time()
                # load the image, convert it to grayscale, and blur it slightly
                image = cv2.imread(imagePath)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (3, 3), 0)

                # apply Canny edge detection using a wide threshold, tight
                # threshold, and automatically determined threshold
                wide = cv2.Canny(blurred, 10, 200)
                tight = cv2.Canny(blurred, 225, 250)
                auto = auto_canny(blurred)

                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(wide,'Wide',(10,30), font, 1, (255,255,255),1,cv2.LINE_AA)
                cv2.putText(tight,'Tight',(10,30),font,1, (255,255,255),1,cv2.LINE_AA)
                cv2.putText(auto,'Auto',(10,30), font,1, (255,255,255),1,cv2.LINE_AA)

                wide_transf = cv2.cvtColor(wide,cv2.COLOR_GRAY2RGB)
                tight_transf = cv2.cvtColor(tight,cv2.COLOR_GRAY2RGB)
                auto_transf = cv2.cvtColor(auto,cv2.COLOR_GRAY2RGB)

                end = time.time()
                timer = end - start
                imagePath_simplified = ntpath.basename(imagePath)
                imageName = os.path.splitext(imagePath_simplified)[0]
                
                with open(time_details_file, "a") as myfile:
                    myfile.write("%s  : Image %s edge extracted in %f seconds \n" %(str(time.strftime("%d/%b/%y %H:%M:%S")),imageName,round(timer,3)))

                # show the images
                
                cv2.imshow("Output", np.hstack([image,wide_transf, tight_transf, auto_transf]))
                #output_path = r'C:\Users\IBM_ADMIN\Desktop\Master MPI\BIO\proiect_bio_edge_extraction\output'
                
                full_output_image_path = os.path.join(output_path,imageName)
                

                start2 = time.time()
                #write images into the output folder
                cv2.imwrite(full_output_image_path+"_wide_method.png",wide)
                cv2.imwrite(full_output_image_path+"_tight_method.png",tight)
                cv2.imwrite(full_output_image_path+"_auto_method.png",auto)

                end2 = time.time()
                timer2 = end2 - start2
                with open(time_details_file, "a") as myfile:
                    myfile.write("%s  : Output of image %s saved into output folder in %f seconds \n" %(str(time.strftime("%d/%b/%y %H:%M:%S")),imageName,round(timer2,3)))

                print("\n\n----------------------------------------->Done!<-----------------------------------------\n\n %s edge extraction can be found here: " %imagePath_simplified + output_path)
                cv2.waitKey(0)

        if cv2.waitKey(39):
           messagebox.showinfo("Complete!", "Operation completed successfully!")
           cv2.destroyAllWindows()
           sys.exit()


def callback(root,entry):
    
    value = entry.get()
    root.destroy()
    output_path = value
    if os.path.exists(value):
       loop_show_images(output_path)
    else:
       messagebox.showerror("Invalid Directory", "Please fill the form with a valid directory path!")
       build_output_directory_popup()
       
    
def callback1(root):
    output_path = tk.filedialog.askdirectory(parent=root,initialdir=directory,title='Select output directory')
    root.destroy()
    loop_show_images(output_path)
        

def build_output_directory_popup():
    root = tk.Tk()
    root.title("Select Output Directory")
    #root.geometry("160x100")

    w = 300
    h = 130
# get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed

    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    tk.Label(root, 
         text="""Enter Output directory:
""",
         justify = tk.LEFT,
         padx = 20,pady=5, font="Helvetica 10 bold").pack(side=tk.TOP)
    # Create single line text entry box
    entry = tk.Entry(root, width=30)
    entry.pack()
    
    # Print the contents of entry widget to console
    button2 = tk.Button(root, text='BROWSE', width=8, font="Helvetica 8 bold", command=lambda: callback1(root))
    button2.pack(side=tk.BOTTOM)
    button = tk.Button(root, text='SEARCH', width=8, font="Helvetica 8 bold", command=lambda: callback(root,entry))
    button.pack(side=tk.BOTTOM)
    

    root.mainloop()


bmp_files = convert_and_get_bmp_location()
build_output_directory_popup()







                                  
