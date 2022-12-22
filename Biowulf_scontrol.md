
```sh
scontrol show node=cn4219

You can run the scontrol command to see resources available on a node. For instance:

=> scontrol show node=cn1092
NodeName=cn1092 Arch=x86_64 CoresPerSocket=8
   CPUAlloc=64 CPUTot=64 CPULoad=6.96
   AvailableFeatures=cpu64,core32,g256,ssd3200,e7543p,ibhdr200,gpua100
   ActiveFeatures=cpu64,core32,g256,ssd3200,e7543p,ibhdr200,gpua100
   Gres=gpu:a100:4(S:0-3),lscratch:3200
   NodeAddr=cn1092 NodeHostName=cn1092 Version=21.08.8-2
   OS=Linux 3.10.0-862.14.4.el7.x86_64 #1 SMP Wed Sep 26 15:12:11 UTC 2018
   RealMemory=253400 AllocMem=204800 FreeMem=99636 Sockets=4 Boards=1
   State=ALLOCATED ThreadsPerCore=2 TmpDisk=3601900 Weight=10000 Owner=N/A MCS_label=N/A
   Partitions=interactive,gpu
   BootTime=2022-12-09T13:07:40 SlurmdStartTime=2022-12-11T11:47:25
   LastBusyTime=2022-12-21T14:20:58
   CfgTRES=cpu=64,mem=253400M,billing=64,gres/gpu=4,gres/gpu:a100=4,gres/lscratch=3200
   AllocTRES=cpu=64,mem=200G,gres/gpu=4,gres/gpu:a100=4
   CapWatts=n/a
   CurrentWatts=0 AveWatts=0
   ExtSensorsJoules=n/s ExtSensorsWatts=0 ExtSensorsTemp=n/s


“AvailableFeatures” shows you the resources available on the node. For instance the above command shows cn1092 is a GPU A100, has a 32 core CPU as well as 256 Gb of RAM.
```
