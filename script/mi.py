from random import random
from time import time

from core import *

if __name__ == '__main__':
    save_path = '../data/mi'
    create_dir(save_path)
    typelists = ['R3ADEV','R3ASTA','R3DDEV','R3DSTA','R3PDEV','R3PSTA','R3LDEV','R3LSTA','R3DEV','R3STA','R3GDEV','R3GSTA','R2DSTA','R1DPC','R1DMAC','WiFiPC','R1CLDEV','R1CLSTA','R1CDEV','R1CSTA','R1DDEV','R1DSTA','R2DDEV','R1DANSTA','R1DANDEV','R1DIP','WiFiAN','R1CUSB','R2DUSB','R1DUSB','R1DUSB2','R4STA','R4CSTA','TFTPPC','R4ASTA','R4ACSTA','R4CMSTA','D01STA','R2100STA','RM2100STA','R3600STA','RM1800STA','RA67STA','RA69STA','RA72STA','R1350STA','R2350STA','RA70STA','RA81STA','RA80STA','RB03STA','RA71STA','RA70DEV','RB04STA']
    tem_url = 'https://api.miwifi.com/upgrade/log/latest?typeList={type}&callback=jQuery151{num}_{time1}&_={time2}'

    for type in tqdm(typelists,desc='types'):
        num = str(random.random()).replace('.', '').zfill(18)
        time1 = int(time() * 1000)
        time2 = int(time() * 1000)

        req_url = tem_url.format(type=type, num=num, time1=time1, time2=time2)

        download_pattern = '"url":"(http://[^"]+.bin)"'
        Download([req_url],download_pattern,save_path)
