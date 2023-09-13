'''
Sheet_Paginate.py
This is a Python utility to add page breaks to long ".png" files. The intended use is to run Sheet_Squeeze.py first on the file to remove
excess blank space. Page breaks are identified by a line at least 1/20 of the page width having the color defined by pb_color. For Sumatra,
this is #999999
'''
from PIL import Image
import png
import ntpath
import os, sys
from telnetlib import theNULL
import time
import img2pdf
import re

pb_color = "#999999"    # #999999 for Sumatra
white_row_limit = 5
top_padding = 4
infile = sys.argv[1]

infile = infile.replace("\\\\","\\")
print("Input file: "+infile)
outfile=infile
outpdffile=infile.replace("_sqz.png","_pub.pdf")

r=png.Reader(filename=infile)
xwidth, yheight, pixels, meta = r.asDirect()
print("pixels type="+str(type(pixels)))
print("Converting pixels to list()")
tpixels=list(pixels)
opixels=[]
page_breaks=[]
space_ranges=[]
oidx=0
white_row_count = 0
min_row = 99999
max_row = -99999
print("Processing...")
for xh in range(len(tpixels)):
    if xh >= 3090:
        xxx = 0
#for xh in range(50):
    white_count = 0
    pb_count = 0
    for xw in range(0,xwidth*3,3):
        try:
            curr_color = ("#"+hex(tpixels[xh][xw])+hex(tpixels[xh][xw+1])+hex(tpixels[xh][xw+2])).replace("0x","")
            if tpixels[xh][xw]>250 and tpixels[xh][xw+1]>250 and tpixels[xh][xw+2]>250:
                #jj = 1
                white_count += 1
            elif curr_color == pb_color:  #tpixels[xh][xw]>200 and tpixels[xh][xw+1]<80 and tpixels[xh][xw+2]<80:
                tpixels[xh][xw]=255
                tpixels[xh][xw+1]=255
                tpixels[xh][xw+2]=255
                pb_count += 1
            else:
                break
        except:
            print("Invalid Index: wh="+str(xh)+", xh="+str(xw))
    if pb_count > xwidth/20:
        if len(page_breaks) == 0 or xh - page_breaks[-1] > 50:
            page_breaks.append(xh)

    elif white_count==xwidth:
#        print('WhiteRow: '+str(xh))
        white_row_count += 1
        min_row=min(min_row, xh)
        max_row=max(max_row, xh)
#            print("Row "+str(xh)+" over limit")
    else:
        white_row_count = 0
        if max_row > 0 and min_row < max_row:
            print("Blank row range "+str(min_row)+" - "+str(max_row))
            space_ranges.append([min_row,max_row])
            min_row = 99999
            max_row = -99999
lastbreak = -1
pagenum = 0
breakline = 0
white_row = []
for xxw in range(0, xwidth * 3, 3):
    white_row.append(255)
    white_row.append(255)
    white_row.append(255)
if max_row > 0 and min_row < max_row:
    print("Blank row range "+str(min_row)+" - "+str(max_row))
    space_ranges.append([min_row,max_row])
for pb in page_breaks:
    print("page break at:"+str(pb))
    breakline = 0
#    for [minx,maxx] in space_ranges:
#        if maxx<pb:
#            breakline = maxx
#        else:
#            break
    breakline = pb
    opixels=tpixels[lastbreak+1:breakline+1]
# program change 4/24/18 - add top padding to page
    for pad in range(0,top_padding):
        opixels.insert(0,tpixels[breakline])
# end if program change 4/24/18
    lastbreak = breakline
    pagenum +=1
#program change 9/13/2023 - append blank rows to short pages
    if xwidth > len(opixels):
        opheight = len(opixels)
        print("Adding "+str(xwidth - opheight)+" blank rows")
        for zh in range(0, xwidth - opheight):
            opixels.append(white_row)
    outfile=infile.replace(".png","_p"+"{0:02d}".format(pagenum)+".png")
    w = png.Writer(width=xwidth, height=len(opixels), greyscale=False, interlace=0, bitdepth=8)
    f=open(outfile, 'wb')
    w.write(f, opixels)
    f.close()
    print(str(len(opixels))+" lines written to: "+outfile.replace("\\\\","\\"))
opixels=tpixels[lastbreak+1:len(tpixels)]
if xwidth > len(opixels):
    opheight = len(opixels)
    print("Adding " + str(xwidth - opheight) + " blank rows")
    for zh in range(0, xwidth - opheight):
        opixels.append(white_row)
lastbreak = breakline
pagenum +=1
outfile=infile.replace(".png","_p"+"{0:02d}".format(pagenum)+".png")
w = png.Writer(width=xwidth, height=len(opixels), greyscale=False, interlace=0, bitdepth=8)
f=open(outfile, 'wb')
w.write(f, opixels)

f.close()
print(str(len(opixels))+" lines written to: "+outfile.replace("\\\\","\\"))

dir_name = os.path.dirname(outpdffile)
#print("Dir Name: "+dir_name)
os.chdir(dir_name)

print("Writing page files to PDF")
pagefiles = [f for f in os.listdir(dir_name) if re.match('.*_p[0-9]+.*\.png', f)]
with open(outpdffile,"wb") as wf:
    wf.write(img2pdf.convert(pagefiles))
wf.close()
print("Deleting temp page files")
for f in pagefiles:
    print("Del file:"+f)
    os.remove(f)

print("Finished")
time.sleep(5)