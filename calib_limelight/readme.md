how to use on limelight:
* to put the actual vision code on the limelight go to the limelights python editor and copy paste the code there
* be sure to edit code in limelight_code_backup.py and copy to limelight python editor as copying from the limelight python editor makes it crash somehow
* choosing a threshold:
    - take a picture of what you want to track and save it as "thr.jpg" in this folder
    - run limelight_median_thr.py and mark the object you want to track using the cursor
    - look at the resulting image to see if you like it, if not try again
    - once youre happy copy the array the program printed to the pid_vals parameter in your track_object object
    - you can change the stdv to get beter results, but be sure to also change the range in your track_object to match it
* Main.java reads the values exactly as the robot would, you can use it to see the values being sent
* uploading new libraries: 
    - to upload libraries use sftp, you can use FileZila
    - host: 10.71.12.11 (limelights IP)| username: root | password: 7112| port: 22 (sftp standard)
    - once connected go to usr/lib/python3.9/site-packages and upload the folder or file there