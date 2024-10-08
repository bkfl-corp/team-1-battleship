'''
Name: Runs animations.
Description: Provides strong types for animations for battleship.
Inputs: N/A
Outputs: N/A
Authors: James Hurd, Joshua Lee, Will Whitehead, Trent Gould, Ky Le
Created: 09/29/24
'''

#used for clearing the screen to emulate the 'refresh' that happens when frames are drawn
import os
#used to delay frame progression or else the animations would run by too fast
import time

from animation import AnimationType

#manages and runs various animations.
class Animator:
    def __init__(self):

        #frames for winning animation.
        self._you_win_anim = [ 
                                "=+=+=+=\nYou Win\n+=+=+=+",
                                "+=+=+=+\nYou Win\n=+=+=+=",
                            ]

        #frames for miss animation. 
        self._miss_anim = [
                            """
                                                
                                               O
                                   |>           
                                ___|___         
                            ,,,,\\_____/,,,,,,,,,
                            ,,-'''-,,-'''-,,-'''
                            """,
                            """
                                                
                                        O       
                                   |>           
                                ___|___         
                            ,,,,\\_____/,,,,,,,,,
                            ,,-'''-,,-'''-,,-'''
                            """,
                            """
                                 MISS!          
                              O                 
                                   |>           
                                ___|___         
                            ,,,,\\_____/,,,,,,,,,
                            ,,-'''-,,-'''-,,-'''
                            """,
                            """
                                 MISS!          
                                                
                                   |>           
                                ___|___         
                            ,,,,\\_____/,,,,,,,,,
                            ,,-'''-,,-'''-,,-'''
                            """,
                        ]
       
        #frames for hit animation.
        self._hit_anim = [
                            """
                                                
                                                
                                   |>           
                                ___|___        O 
                            ,,,,\\_____/,,,,,,,,,
                            ,,-'''-,,-'''-,,-'''
                            """,
                            """
                                                
                                                
                                   |>           
                                ___|___ O       
                            ,,,,\\_____/,,,,,,,,,
                            ,,-'''-,,-'''-,,-'''
                            """,
                            """
                                  HIT!          
                                                
                             '.  \\ | /  ,'      
                               `. `.' ,'        
                            ,,( .`.|,' .),,,,,,,
                            ,,-'''-,,-'''-,,-'''
                            """,
                            """
                                  HIT!          
                                                
                                                
                               `. `.' ,'        
                            ,,( .`.|,' .),,,,,,,
                            ,,-'''-,,-'''-,,-'''
                            """
                        ]

    #public method to play animation.
    def play(self, anim):
        
        #render the correct animation based on the type passed in.
        match anim:
            case AnimationType.HIT:
                Animator._run_animation(self._hit_anim)

            case AnimationType.MISS:
                Animator._run_animation(self._miss_anim)

            case AnimationType.WIN:
                Animator._run_animation(self._you_win_anim*5)

    #animation renderer. 
    @staticmethod
    def _run_animation(frames):
        for frame in frames: #loop as desired
            #clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
            print(frame)
            #wait a brief moment
            time.sleep(0.25)
