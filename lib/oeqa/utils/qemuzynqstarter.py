# Provide a Qemusynqstarter class, which will be used by oeqa qemurunner.py whenever
# whenever a bitbake -c testimage <image> is called with MACHINE set to qemuzynq 

import bb
import subprocess
import os

class Qemuzynqstarter:

    def __init__(self):
        self.server_ip = "127.0.0.1"
        self.user = "root" 
        self.port = 2226
        self.ip = "127.0.0.1"

    def launch(self, nativesysroot = None, deploydir = None, qemuparams = None, machine = None, rootfs = None):
        kernelimagetype = "uImage"
        kernelimage = os.path.join(deploydir, kernelimagetype)
        dtbfile = "%s-%s.dtb" % (kernelimagetype, machine)
        dtbpath = os.path.join(deploydir, dtbfile)
        zynqqemuparams = "-redir tcp:2226:10.0.2.15:22 -kernel %s -initrd %s -M xilinx-zynq-a9 -serial null %s -dtb %s -no-reboot -nographic -m 1024 --append \"earlyprintk root=/dev/ram rw console=ttyPS0\"" % (kernelimage, rootfs, qemuparams, dtbpath)
        
        qemubinary = os.path.join(nativesysroot, "qemu-system-arm")
        launch_cmd = '%s %s' % (qemubinary, zynqqemuparams)
        bb.note("Qemuzynqstarter launch_cmd: %s" % launch_cmd)
        process = subprocess.Popen(launch_cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,preexec_fn=os.setpgrp)
        
        bb.note("qemu-system-arm started, pid is %s" % process.pid)

        
        return process
