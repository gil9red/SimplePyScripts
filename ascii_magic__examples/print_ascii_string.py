#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/LeandroBarone/python-ascii_magic


# pip install ascii-magic
from ascii_magic import AsciiArt


file_name = "input.png"
my_art = AsciiArt.from_image(file_name)
print(my_art.to_ascii(columns=40, monochrome=True))
"""
                                        
                   ii                   
                 .]EE].                 
                ;JXEEXJ;                
               iqX4444Xqi               
             `tXg444444gXt`             
            +CFLdg4444gdLFC+            
           xuv. >6gEEg6> .vnx           
         `au`    :2442:    `ua`         
        ^wXc+////[!^^![////+cXw^        
       %SX4d44444GLiiLG44444d4XS%       
     `tEg44EEEEEXn^::^nXEEEEE44gEt`     
    =fPEEEEEEEEd*      *dEEEEEEEEPf=    
   i6dhhhhhhhhh6a*%ii%*a6hhhhhhhhhd6i   
   ^=^^^^^^^^^^=////////=^^^^^^^^^^=^   
"""
