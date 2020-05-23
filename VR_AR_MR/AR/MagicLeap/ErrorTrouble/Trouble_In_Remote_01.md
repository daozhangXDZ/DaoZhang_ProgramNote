# Error running MLDB install Building for Magic Leap

**Error:**

Failed to start Zero Iteration (ZI) server on the physical device 
'G821FM101258'. - com.magicleap.vdf.core.MLException: Command 
"[C:\Users\cypri\MagicLeap\mlsdk\v0.18.0\tools\mldb\mldb.exe, -s, 
G821FM101258, install, -u, 
C:\Users\cypri\MagicLeap\mlsdk\v0.18.0\VirtualDevice\device\com.magicleap.zi_server.mpk]"
exited with non-zero code: 1 error: Manifest for 
/data/local/tmp/com.magicleap.zi_server.mpk not valid 



**Resolve**

I'm getting the same exact error, so I'm glad you posted this.

I even tried copying the .mpk file along with the cert files directly  into my SDK folder and installing it manually through the command line  and it still wouldn't work.

Turned out I just needed to update my headset to the latest version.  Just go to settings on your Magic Leap One and update it. After the  updates install and your headset reboots, you need to plug your  controller into the Lightpack to update it to the same version as the  headset. 

Hope this works for you too! 