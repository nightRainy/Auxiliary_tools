# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#@author:知世

import os
import pexpect
import sys
import glob

passd="firmadyne"


def myinit():
    if(len(sys.argv)==1):
        sys.exit("[+]Usage:sudo ./fastrun.py xxx.bin") 
    if not os.path.isfile(sys.argv[1]):
        sys.exit("[+]Please input the right file name")

def clear():
    print("[*]clear prev file")
    print("[*]Step1:Clear the images*")
    if not os.path.exists("images"):
        print("[+]Not find the images directory")
    else:
        images=glob.glob(os.path.join("images","*.tar.gz"))
        for i in images:
            os.remove(i)
        print("[*]Done!")
    if not os.path.exists("scratch"):
        print("[+]Not find the scratch directory")
    else:
        if os.system("rm -rf scratch*"):
            sys.exit("Clear scratch failed")
        print("[*]Done!")


def fake_extractor():
    print("[*]Step3:extracting now ...")
    sys.argv[1].strip(';').strip('&&').strip('||')
    command="sudo ./sources/extractor/extractor.py -b router -sql 127.0.0.1 -np -nk " +sys.argv[1] +" images"
    if os.system(command):
        sys.exit('[+]EXtractor failed')
    print('[*]Done!')

def get_arch():
    print("[*]Step4:getting arch now...")
    get="sudo ./scripts/getArch.sh ./images/1.tar.gz "
    arch= pexpect.spawn(get,timeout=None)
    index=arch.expect(["firmadyne:",pexpect.EOF,pexpect.TIMEOUT])
    if (index == 0):
        print("[*]sendline password")
        arch.sendline(passd)
    else:
        arch.close()
        sys.exit('[+]get arch failed!')
    arch.expect(pexpect.EOF)
    print("[*]Done!")

def make_images():
    print("[*]Step5:making image now")
    make='sudo ./scripts/makeImage.sh 1'
    images=pexpect.spawn(make,timeout=None)
    index=images.expect(["firmadyne:",pexpect.EOF,pexpect.TIMEOUT])
    if(index==0):
        print("[*]sendline password")
        images.sendline(passd)
    else:
        images.close()
        sys.exit("[+]make images failed!")
    images.expect(pexpect.EOF)
    print("[*]Done!")


def set_net():
    print("[*]Step6:Setting inferNetwork now")
    myset="sudo ./scripts/inferNetwork.sh 1"
    net=pexpect.spawn(myset,timeout=None)
    index=net.expect(["firmadyne",pexpect.EOF,pexpect.TIMEOUT])
    if(index==0):
        print("[*]sendline password")
        net.sendline(passd)
    else:
        net.close()
        sys.exit("[+]make images failed!")
    net.expect(pexpect.EOF)
    print("[*]Done!")

def run():
    print("[*]Step7:Running now!")
    myrun="sudo ./scratch/1/run.sh"
    index=pexpect.spawn(myrun,timeout=None)
    index.interact()
    print("[*]Done!")


if __name__=='__main__':
    clear()
    fake_extractor()
    get_arch()
    make_images()
    set_net()
    run()





