#used for clearing the screen to emulate the 'refresh' that happens when frames are drawn
import os
#used to delay frame progression or else the animations would run by too fast
import time
def run_anim(anim_obj, loop_count):
    for i in range(loop_count): #loop as desired
        for frame in anim_obj.frame_order: #run through each frame of the animation
            #clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
            print(anim_obj.frames[frame])
            #wait a brief moment
            time.sleep(0.25)

class anim_obj:
    def __init__(self, frames, frame_order):
        self.frames = frames
        self.frame_order = frame_order


frame1 = "=+=+=+=\nYou Win\n+=+=+=+"
frame2 = "+=+=+=+\nYou Win\n=+=+=+="
you_win_anim = anim_obj([frame1, frame2],[0,1])

frame1 ="""
                    
                   O
       |>           
    ___|___         
,,,,\_____/,,,,,,,,,
,,-'''-,,-'''-,,-'''
"""
frame2 ="""
                    
            O       
       |>           
    ___|___         
,,,,\_____/,,,,,,,,,
,,-'''-,,-'''-,,-'''
"""

frame3 ="""
     MISS!          
  O                 
       |>           
    ___|___         
,,,,\_____/,,,,,,,,,
,,-'''-,,-'''-,,-'''
"""

frame4 ="""
     MISS!          
                    
       |>           
    ___|___         
,,,,\_____/,,,,,,,,,
,,-'''-,,-'''-,,-'''
"""

miss_anim = anim_obj([frame1, frame2, frame3, frame4], [0,1,2,3])

frame1 ="""
                    
                    
       |>           
    ___|___        O 
,,,,\_____/,,,,,,,,,
,,-'''-,,-'''-,,-'''
"""
frame2 ="""
                    
                    
       |>           
    ___|___ O       
,,,,\_____/,,,,,,,,,
,,-'''-,,-'''-,,-'''
"""

frame3 ="""
      HIT!          
                    
 '.  \ | /  ,'      
   `. `.' ,'        
,,( .`.|,' .),,,,,,,
,,-'''-,,-'''-,,-'''
"""

frame4 ="""
      HIT!          
                    
                    
   `. `.' ,'        
,,( .`.|,' .),,,,,,,
,,-'''-,,-'''-,,-'''
"""

hit_anim = anim_obj([frame1, frame2, frame3, frame4], [0,1,2,3])

#examples below to run animations
#run_anim(hit_anim, 1)
#run_anim(miss_anim, 1)
#run_anim(you_win_anim, 5)
