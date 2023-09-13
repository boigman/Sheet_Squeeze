#Expand_short_pages.py

import png
# import ntpath
import os
import sys
import time
import re
import img2pdf
from PIL import Image
from pdf2image import convert_from_path

infile = sys.argv[1]
print("Input file: " + infile.replace("\\\\", "\\"))
outfile = infile.replace(".png", "_exp.png")

pages = convert_from_path(infile, 200)
page_count = 0
pngfiles = []
for page in pages:
    page_count += 1
    print(str(page_count).zfill(2))
    outfile = infile.replace('.pdf',str(page_count).zfill(2)+'.png')
    page.save(outfile, 'PNG')
    page.close()
    pngfiles.append(outfile)
    if page.width > page.height:
        white_row = []
        for xw in range(0, page.width * 3, 3):
            white_row.append(255)
            white_row.append(255)
            white_row.append(255)
        r = png.Reader(filename=outfile)
        xwidth, yheight, pixels, meta = r.asDirect()
        print("Converting pixels to list()...")
        tpixels = list(pixels)

        opixels = []
        oidx = 0
        for xh in range(len(tpixels),xwidth-1):
            tpixels.append(white_row)
        w = png.Writer(width=xwidth, height=len(tpixels), greyscale=False, interlace=0, bitdepth=8)
        f = open(outfile, 'wb')
        w.write(f, tpixels)
        f.close()

#exit()

dir_name = os.path.dirname(infile)
#print("Dir Name: "+dir_name)
os.chdir(dir_name)

#Backing up existing pdf file
print("Backing up existing pdf file")
os.rename(infile, infile.replace(".pdf","_bck.pdf"))
print("Writing page files to PDF")
with open(infile, "wb") as wf:
    wf.write(img2pdf.convert(pngfiles))
wf.close()
for f in pngfiles:
    #print("Del file:"+f)
    os.remove(f)

# print(os.listdir(dir_name))
# match_string = infile.replace(".pdf", "").join('.*0[0-9].\.png')
# print(match_string)
# pagefiles = [f for f in os.listdir(dir_name) if re.match(match_string, f)]
# print(pagefiles)
# #paagefiles = [f for f in os.listdir(dir_name) if re.match('.*_p[0-9]+.*\.png', f)]
# with open(outpdffile,"wb") as wf:
#     wf.write(img2pdf.convert(pagefiles))
# wf.close()
# print("Deleting temp page files")
# for f in pagefiles:
#     #print("Del file:"+f)
#     os.remove(f)
#
print("Finished")
time.sleep(5)