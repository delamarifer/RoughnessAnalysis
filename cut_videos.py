import os
import pathlib as path
imgs_dir2 = os.path.join("videos/")
out_dir = os.path.join( "movies/")
for vidfile in os.listdir(imgs_dir2):
     if os.path.join(imgs_dir2, vidfile).endswith(".mp4"):
        outfile = out_dir + vidfile
 
        cmd = "ffmpeg -ss 0.1 -i " + imgs_dir2 + vidfile + " -t 1 -c:v libx264 -c:a aac " + outfile
        os.system(cmd)
        print(cmd)
