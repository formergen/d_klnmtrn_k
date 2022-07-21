import glob
import os
a = glob.glob(r'G:\Collection 1\chat-bot\chat-bot\pictures\*.jpg')
a=str(a)
a=open('picsd.py', 'a', encoding='utf-8', errors='ignore').write(a)
