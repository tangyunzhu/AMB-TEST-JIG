import os
import time
import datetime
import subprocess
import logging

error_flag = True

formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(message)s')

logger=logging.getLogger("AMB_Test:")
logger.setLevel(logging.DEBUG)

fh=logging.FileHandler("AMB_Test.log")
fh.setLevel(logging.DEBUG)

ch=logging.StreamHandler()
ch.setLevel(logging.INFO)

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

#--------------------------Normal Command--------------------------------------#
Enter   =   "adb shell pwd"
workDir =   "E:/adb"
CMD01   =   "e:"
CMD02   =   "adb devices"
CMD03   =   "adb root"
CMD04   =   "adb remount"
#--------------------------Speaker---------------------------------------------#
# enable speaker
CMD11   =   "adb shell tinymix 'PRI_MI2S_RX Audio Mixer MultiMedia1' 1"
CMD12   =   "adb shell tinymix 'RX3 MIX1 INP1' 'RX1'"
CMD13   =   "adb shell tinymix 'SPK DAC Switch' 1"

CMD14   =   "adb shell tinyplay /data/audio/test.wav"
#disable speaker
CMD15   =   "adb shell tinymix 'PRI_MI2S_RX Audio Mixer MultiMedia1' 0"
CMD16   =   "adb shell tinymix 'RX3 MIX1 INP1' 'ZERO'"
CMD17   =   "adb shell tinymix 'SPK DAC Switch' 0"

#---------------------------Head Jack------------------------------------------#
#enable Head Jack
CMD21   =   "adb shell tinymix 'PRI_MI2S_RX Audio Mixer MultiMedia1' 1"
CMD22   =   "adb shell tinymix 'RX1 MIX1 INP1' 'RX1'"
CMD23   =   "adb shell tinymix 'RX2 MIX1 INP1' 'RX2'"
CMD24   =   "adb shell tinymix 'RDAC2 MUX' 'RX2'"
CMD25   =   "adb shell tinymix 'HPHL' 'Switch'"
CMD26   =   "adb shell tinymix 'HPHR' 'Switch'"
CMD27   =   "adb shell tinymix 'MI2S_RX Channels' 'Two'"

CMD28   =   "adb shell tinyplay /data/audio/test.wav"
CMD29   =   "adb shell tinyplay /data/audio/record.wav"
CMD20   =   "adb shell tinyplay /data/audio/right.wav"

#---------------------------Headset Mic---------------------------------------#
#enable Headset mic capture:
CMD31   =   "adb shell tinymix 'MultiMedia1 Mixer TERT_MI2S_TX' 1"
CMD32   =   "adb shell tinymix 'DEC1 MUX' 'ADC2'"
CMD33   =   "adb shell tinymix 'ADC2 MUX' 'INP2'"
CMD34   =   "adb shell tinycap /data/audio/capture_hs.wav -D 0 -d 0 -c 1 -r 48000 -b 16 &"

#play recorde
CMD30   =   "adb shell tinyplay /data/audio/capture_hs.wav"

#disable Headset mic capture
CMD35   =   "adb shell tinymix 'MultiMedia1 Mixer TERT_MI2S_TX' 0"
CMD36   =   "adb shell tinymix 'DEC1 MUX' 'ZERO'"
CMD37   =   "adb shell tinymix 'ADC2 MUX' 'ZERO'"

#---------------------------Analog Mic---------------------------------------#
#enable Analog Mic
CMD41   =   "adb shell tinymix 'MultiMedia1 Mixer TERT_MI2S_TX' 1"
CMD42   =   "adb shell tinymix 'DEC1 MUX' 'ADC2'"
CMD43   =   "adb shell tinymix 'ADC2 MUX' 'INP3'"
CMD44   =   "adb shell tinymix 'ADC3 Volume' 8"
CMD45   =   "adb shell tinycap /data/audio/capture_amic.wav -D 0 -d 0 -c 1 -r 48000 -b 16 &"

#play the recorde
CMD40   =   "adb shell tinyplay /data/audio/capture_amic.wav"

#disable the Analog Mic
CMD46   =   "adb shell tinymix 'MultiMedia1 Mixer TERT_MI2S_TX' 0"
CMD47   =   "adb shell tinymix 'DEC1 MUX' 'ZERO'"
CMD48   =   "adb shell tinymix 'ADC2 MUX' 'ZERO'"
CMD49   =   "adb shell tinymix 'ADC3 Volume' 0"

#---------------------------Digtal Mic---------------------------------------#
#enable Digitla Mic
CMD51   =   "adb shell tinymix 'MultiMedia1 Mixer TERT_MI2S_TX' 1"
CMD52   =   "adb shell tinymix 'DEC1 MUX' 'DMIC1'"
CMD53   =   "adb shell tinycap /data/audio/capture_dmic.wav -D 0 -d 0 -c 1 -r 48000 -b 16 &"
#play the recorde
CMD50   =   "adb shell tinyplay /data/audio/capture_dmic.wav"
#disable Digtal Mic
CMD55   =   "adb shell tinymix 'MultiMedia1 Mixer TERT_MI2S_TX' 0"
CMD56   =   "adb shell tinymix 'DEC1 MUX' 'ZERO'"

#------------------------------END-------------------------------------------#
   
def process_cmd(cmd,time_sleep):        #function which could run linux command on windows command line
    os.system(cmd)
    time.sleep(time_sleep)

def configureEnv():
    process_cmd(CMD01,0.2)
    os.chdir(workDir)
    print "try to connect Main board"
    while True:
        getData=subprocess.check_output(CMD02)
        print getData
        if ("ba5d1d70" in str(getData)) or ("1f580338" in str(getData)):
            break;
        time.sleep(0.06)
        logger.debug("-->%s" %getData)
        logger.warn("-->try again with [adb devices]")

    while True:
        getData=subprocess.check_output(CMD03)
        print getData
        if "already running as root" in str(getData):
            break;
        time.sleep(0.06)
        logger.debug("-->%s" %getData)
        logger.warn("-->try again with [adb root]")

    while True:
        getData=subprocess.check_output(CMD04)
        print getData
        if "remount succeeded" in str(getData):
            break;
        time.sleep(0.06)
        logger.debug("-->%s" %getData)
        logger.warn("-->try again with [adb remount]")
        

def configureFT232():
    cmd="FT_Prog_CmdLine.exe scan prog * ./AMBTemplate.xml"
    while True:
        getData=subprocess.check_output(cmd)
#        print getData
        if "programmed successfully" in str(getData):
            print "-->flash FT232 OK"
            break;
        time.sleep(0.06)
        logger.debug("-->%s" %getData)
        logger.warn("-->try again to flash the FT232")


def EnableSpeaker():                    #just enable speaker,do not play music
    for cmd in [CMD11,CMD12,CMD13]:
        process_cmd(cmd,0.06)

def DisableSpeaker():                   #just disable speaker
    for cmd in [CMD15,CMD16,CMD17]:
        process_cmd(cmd,0.06)

def EnableHeadSet():                    #just enable Headset jack, do not play music
    for cmd in [CMD21,CMD22,CMD23,CMD24,CMD25,CMD26,CMD27]:
        process_cmd(cmd,0.06)   

def EnableHeadsetMic():                 #enable Headset Mic and begin to recode
    for cmd in [CMD31,CMD32,CMD33]:
        process_cmd(cmd,0.06)    

def DisableHeadsetMic():                #just disable Headset Mic
    for cmd in [CMD35,CMD36,CMD37]:
        process_cmd(cmd,0.06)   
           
def EnableDigitalMic():                 #enable Digital Mic
    for cmd in [CMD51,CMD52]:
        process_cmd(cmd,0.06)
        
def DisableDigitalMic():                #just disable digital Mic
    for cmd in [CMD55,CMD56]:
        process_cmd(cmd,0.06)
        
def EnableAnalogMic():                  #enable Analog Mic
    for cmd in [CMD41,CMD42,CMD43,CMD44]:
        process_cmd(cmd,0.06)

def DistalbeAnalogMic():
    for cmd in [CMD46,CMD47,CMD48,CMD49]:
        process_cmd(cmd,0.06)

def playHeadSetMic():  
    global error_flag                    #play the .wav file which created by HeadSet Mic 
    time.sleep(0.8)
    getdata=subprocess.check_output(CMD30)
    print getdata
    if ("is not a riff/wave file" in str(getdata)) or ("Unable to open file" in str(getdata)) or ("Error playing" in str(getdata)):
        logger.warn("-->HeadSet Mic play error")
        error_flag = False

#    os.system(CMD30)
    
def playAnalogMic():                        #play the .wav file which created by Analog Mic
    global error_flag   
    time.sleep(0.8)         
    getdata=subprocess.check_output(CMD40)
    print getdata
    if ("is not a riff/wave file" in str(getdata)) or ("Unable to open file" in str(getdata)) or ("Error playing" in str(getdata)):
        logger.warn("-->Analog Mic play error")
        error_flag=False

#    os.system(CMD40)

def playDigitalMic():  
    global error_flag                     #play the .wav file which created by Digital Mic
    time.sleep(0.8)
    getdata=subprocess.check_output(CMD50)
    print getdata
    if ("is not a riff/wave file" in str(getdata)) or ("Unable to open file" in str(getdata)) or ("Error playing" in str(getdata)):
        logger.warn("-->Digital Mic play error")
        error_flag=False
    
#    os.system(CMD50)

def detectTinycapPID(MicType):
    if MicType  == "_HeadSet":
        logger.debug("-->start to Headset Mic recode --->")
        process=subprocess.Popen(CMD34,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #    os.system(CMD34)
    elif MicType == "_AnalogMic":
        logger.debug("-->start to Analog Mic recode --->")
        process=subprocess.Popen(CMD45,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #    os.system(CMD45)
    else :
        logger.debug("-->start to Digital Mic recode --->")
        process=subprocess.Popen(CMD53,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #    os.system(CMD53)
    print "Mic type is : " + str(MicType)
    print "-->Start to recode[^_^]"
    time.sleep(2)
    output=subprocess.check_output("adb shell ps")  #get all the process in the andriod
    f=open("pid.txt","a")                           #new a file named pid.txt
    f.write(output)                                 #save data to the file
    f.write('\n')
    f.close()                                       #close the file 
    tinycapPID=0 
    
    file=open("pid.txt",'r')                        #read the data from the file by lines
    while True:
        line=file.readline()
        if "tinycap" in line:
            logger.debug("-->%s" %line)
            line_pid=line.split(" ")
            if line_pid[6]>tinycapPID:
                tinycapPID=line_pid[6]
        if not line:                                #when read all the lines from the file,close file and beak;
            file.close()
            break
    logger.debug("-->tinycapPID is : %s" %str(tinycapPID))
    os.system("del pid.txt")                        #delete the file
    

    raw_data=raw_input("-->Press [Enter] to Stop")
    time.sleep(0.1)
    #    print raw_data
    killCmd="adb shell kill -2 "+str(tinycapPID)    #
    os.system(killCmd)
    logger.debug("-->kill the tinycap PID")
    process.kill()
    logger.debug("-->kill the tinycap subprocess")
    
def AnalogMicTest():
    logger.debug("-->Analog Mic test")
    logger.debug("-->begin to enable Analog Mic")
    EnableAnalogMic()
    logger.debug("-->begin to recode and process the PID")
    detectTinycapPID("_AnalogMic")
    logger.debug("-->begin to disable the Analog Mic")
    DistalbeAnalogMic
    logger.debug("-->begin to play the .wav file")
    time.sleep(1)
    playAnalogMic()
    logger.debug("-->delte the capture_amic.wav")
    cmd="adb shell rm -f /data/audio/capture_amic.wav"
#    os.system(cmd)
    logger.debug("-->Analog Mic test completed")

def DigitalMicTest():
    logger.debug("-->Digital Mic test")
    logger.debug("-->begin to enable Digital Mic")
    EnableDigitalMic()
    logger.debug("-->begin to recode and process the PID")
    detectTinycapPID("_DigitalMic")
    logger.debug("-->begin to disable the Digital Mic")
    DisableDigitalMic()
    time.sleep(1)
    logger.debug("-->begin to play the .wav file")
    playDigitalMic()
    logger.debug("-->delte the capture_dmic.wav")
    cmd="adb shell rm -f /data/audio/capture_dmic.wav"
#    os.system(cmd)
    logger.debug("-->Digital Mic test completed")    
    
def HeadSetMicTest():
    logger.debug("-->HeadSet Mic test")
    logger.debug("-->begin to enable headset Mic")
    EnableHeadsetMic()
    logger.debug("-->begin to recode and process the PID")
    detectTinycapPID("_HeadSet")
    logger.debug("-->begin to disable the headset Mic")
    DisableHeadsetMic()
    logger.debug("-->begin to play the .wav file")
    time.sleep(1)
    playHeadSetMic()
    logger.debug("-->delte the capture_hs.wav")
    cmd="adb shell rm -f /data/audio/capture_hs.wav"
#    os.system(cmd)
    logger.debug("-->HeadSet Mic test completed")


configureEnv()      #configure the test enverment
while True:
#    configureEnv()      #configure the test enverment
    start=datetime.datetime.now()
    configureFT232()    #flash the ADBTemplate.xml to product
    #speaker test
    EnableSpeaker()
       
    os.system(CMD29)
    DisableSpeaker()

    #enable hearset
    EnableHeadSet()

    #recode test[HeadSet Mic, Analog Mic, Digital Mic]   
    #HeadSet Mic test
    HeadSetMicTest()
    
    #Analog Mic test
    AnalogMicTest()
    
    #Digital Mic test
    DigitalMicTest()    
    
    
    print "******************************"
    print "*                            *"
    if error_flag==True:
        print "*        Test   Over         *"
    else:
        print "*        Test   FAIL         *"
    print "*                            *"
    print "******************************"
    print " "
    print " "
    end = datetime.datetime.now()
    print "Test time is : %s s" %str(end-start)
    
#    os.system("adb shell reboot")
    
    data=raw_input("Press [Enter] to continue...")
    error_flag=True
    

