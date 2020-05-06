from PIL import Image
import png
#import ntpath
#import os 
import sys
import time

white_row_limit = 5
vbar_row_limit = 10

infile = sys.argv[1]
print("Input file: "+infile.replace("\\\\","\\"))
outfile=infile.replace(".png","_sqz.png")

r=png.Reader(filename=infile)
xwidth, yheight, pixels, meta = r.asDirect()
#print("pixels type="+str(type(pixels)))
print("Converting pixels to list()...")
tpixels=list(pixels)
opixels=[]
oidx=0
white_row_count = 0
vbar_row_count = 0
min_row = 99999
max_row = -99999
min_vbar_row = 99999
max_vbar_row = -99999
line_break = 99999
print("Processing...")
#w = png.Writer(width=len(tpixels[0]), height=len(tpixels), greyscale=False, interlace=0, bitdepth=8)    
#f=open(outfile+'x.png', 'wb')
#w.write(f, tpixels)
#f.close()
for xh in range(len(tpixels)):
#for xh in range(350):
    white_count = 0
    black_lines = []
    white_lines = []
    bline_len = 0
    wline_len = 0
    min_dark_col = 99999
    max_dark_col = -99999
    left_bar_count = 0
    if xh > 1071 and xh < 1100:
        xxx = 0
    if xh == 1511:
        xxx = 0
    for xw in range(0,xwidth*3,3):
        try:
#            if tpixels[xh][xw]==255 and tpixels[xh][xw+1]==255 and tpixels[xh][xw+2]==255:
            if tpixels[xh][xw]>250 and tpixels[xh][xw+1]>250 and tpixels[xh][xw+2]>250:
                #jj = 1
                white_count += 1
                tpixels[xh][xw]=255
                tpixels[xh][xw+1]=255
                tpixels[xh][xw+2]=255
            else:
                min_dark_col = min(min_dark_col, xw)
                max_dark_col = max(max_dark_col, xw)
#                if (max_dark_col - min_dark_col)/3 > 5 or xw/3 > 50:
#                    break
            if (tpixels[xh][xw]==255 and tpixels[xh][xw+1]==255 and tpixels[xh][xw+2]==255) or (tpixels[xh][xw]==0 and tpixels[xh][xw+1]==0 and tpixels[xh][xw+2]==0):
                if tpixels[xh][xw]==255 and tpixels[xh][xw+1]==255 and tpixels[xh][xw+2]==255:
                    if bline_len>0:
                        black_lines.append(bline_len)
                        bline_len = 0 
                    wline_len +=1
                else:
                    if wline_len>0:
                        white_lines.append(wline_len)
                        wline_len = 0
                    bline_len +=1
            else:
                black_lines = []
                white_lines = []
        except:
            print("Invalid Index: wh="+str(xh)+", xh="+str(xw))
# Detect dashed line (line break) - Lots of pure white and black segments approximately equal in number            
    if (len(black_lines)>50 and len(white_lines)>50 and abs(len(black_lines) - len(white_lines))<4
            and black_lines[0]<20 and white_lines[0]<20):
        print("Line break at: "+str(xh))
        line_break = xh
        white_count=xwidth
    if white_count==xwidth:
#        print('WhiteRow: '+str(xh))
        white_row_count += 1
        vbar_row_count = 0
        if max_vbar_row > 0 and min_vbar_row < max_vbar_row:
            print("VBar Rows "+str(min_vbar_row)+" - "+str(max_vbar_row)+ " squeezed out")
            min_vbar_row = 99999
            max_vbar_row = -99999
        if white_row_count < white_row_limit:
            opixels += [tuple(tpixels[xh])]
        else:
            min_row=min(min_row, xh)
            max_row=max(max_row, xh)
#            print("Row "+str(xh)+" over limit")
    elif xwidth - white_count < 10 and max_dark_col/3 < 50 and (max_dark_col - min_dark_col) >= 0  and (max_dark_col - min_dark_col)/3 < 5 :
        vbar_row_count += 1
        white_row_count = 0
        if max_row > 0 and min_row < max_row:
            print("White Rows "+str(min_row)+" - "+str(max_row)+ " squeezed out")
            min_row = 99999
            max_row = -99999
        if vbar_row_count < vbar_row_limit:
            opixels += [tuple(tpixels[xh])]
        else:
            min_vbar_row=min(min_vbar_row, xh)
            max_vbar_row=max(max_vbar_row, xh)
    else:
        white_row_count = 0
        vbar_row_count = 0
        if max_row > 0 and min_row < max_row:
            print("White Rows "+str(min_row)+" - "+str(max_row)+ " squeezed out")
            min_row = 99999
            max_row = -99999
        elif max_vbar_row > 0 and min_vbar_row < max_vbar_row:
            print("VBar Rows "+str(min_vbar_row)+" - "+str(max_vbar_row)+ " squeezed out")
            min_vbar_row = 99999
            max_vbar_row = -99999
        if line_break < xh: #Mark as line break line with red dash
            for xw in range(0,10*3,3):
                tpixels[xh][xw]=255
                tpixels[xh][xw+1]=0
                tpixels[xh][xw+2]=0
            line_break = 99999
            
        opixels += [tuple(tpixels[xh])]

if max_row > 0 and min_row < max_row:
    print("White Rows "+str(min_row)+" - "+str(max_row)+ " squeezed out")
    min_row = 99999
    max_row = -99999
elif max_vbar_row > 0 and min_vbar_row < max_vbar_row:
    print("VBar Rows "+str(min_vbar_row)+" - "+str(max_vbar_row)+ " squeezed out")
    min_vbar_row = 99999
    max_vbar_row = -99999
w = png.Writer(width=xwidth, height=len(opixels), greyscale=False, interlace=0, bitdepth=8)    
f=open(outfile, 'wb')
w.write(f, opixels)
f.close()
print(str(len(opixels))+" lines written to: "+outfile.replace("\\\\","\\"))
print(str(len(tpixels)-len(opixels))+" lines squeezed out")
print("Finished")
time.sleep(5)