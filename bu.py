import serial 
import numpy  
import matplotlib.pyplot as plt
from drawnow import *
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt2
import datetime
import pyeeg
from scipy.signal import butter, lfilter
import csv

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y.tolist()


def pwsp(y,n,fs):
    #print(y[0:10])
    #y=y/max(abs(y))
    y=y[-395*4:]
    n=len(y)
    fft=np.fft.fft(y,n)
    #fft *= np.conj(fft)
    #ps = fft.real / N**2
    #freqs = np.fft.fftfreq(time.size, 1.0/fs)
    #idx = np.argsort(freqs)
    #freq=freqs[idx]
    #power=ps[idx]
    power = (np.abs( fft )/n)**2.0
    freq = np.linspace(0,fs/2, n/2)
    maxl=len([i for i in freq if i <= 45])
    freq=freq[10:maxl]
    power=power[10:maxl]
    return [power,freq]
def makeFig(): 
    plt.subplot(411)
    plt.ylim(min(data1),max(data1))                                 #Set y min and max values
    plt.grid(True)
    t1=np.linspace(0,len(data1),len(data1))/fsc
    t1=t1[-1]-t1
    #print t
    line1=plt.plot(-t1,data1)
    plt.setp(line1, 'color', 'r', 'linewidth', 1.0)
    
    plt.subplot(412)
    #fx=np.log10(ft)*20
    line2=plt.plot(f1, ft1)
    plt.setp(line2, 'color', 'k', 'linewidth', 1.0)
    plt.margins(0) # remove default margins (matplotlib verision 2+)
    plt.axvspan(0, 4, facecolor='green', alpha=0.3)
    plt.axvspan(4, 8, facecolor='yellow', alpha=0.3)
    plt.axvspan(8, 12, facecolor='red', alpha=0.3)
    plt.axvspan(12, 25, facecolor='blue', alpha=0.3)
    plt.axvspan(25, 45, facecolor='orange', alpha=0.3)
    
    plt.subplot(413)
    plt.ylim(min(data2),max(data2))                                 #Set y min and max values
    plt.grid(True)
    line3=plt.plot(-t1,data2)
    plt.setp(line3, 'color', 'b', 'linewidth', 1.0)
    
    plt.subplot(414)
    #fx=np.log10(ft)*20
    line4=plt.plot(f2, ft2)
    plt.setp(line4, 'color', 'k', 'linewidth', 1.0)
    plt.margins(0) # remove default margins (matplotlib verision 2+)
    plt.axvspan(0, 4, facecolor='green', alpha=0.3)
    plt.axvspan(4, 8, facecolor='yellow', alpha=0.3)
    plt.axvspan(8, 12, facecolor='red', alpha=0.3)
    plt.axvspan(12, 25, facecolor='blue', alpha=0.3)
    plt.axvspan(25, 45, facecolor='orange', alpha=0.3)


    
    #ppp=pyeeg.bin_power(data1,[0.5,4,7,12,30], 500)
    #print ppp

    #plt.subplot(313)
    #line4=plt.plot(ppp)
    #plt.setp(line4, 'color', 'g', 'linewidth', 1.0)

inp=raw_input("what do you waht to do 1. record, 2 plot early data, 3 animate early data\n")
if inp=="1":
    win=2000
    data2= []
    data1= []
    w2=200
    arduinoData = serial.Serial('com6',115200) 
    plt.ion() 
    plt2.ion()
    cnt=0
    f=0
    fft=0
    plt.figure(1)

    inp=raw_input("enter File name to save data\n")
    print inp+".csv"
    with open(inp+".csv", mode='w') as data_file: 
        cf=1.0/1000
        #file_writer = csv.writer(data_file, delimiter=',')
        while True: # While loop that loops forever
            c=w2
            b = datetime.datetime.now()
            while c>0:
                c=c-1
                while (arduinoData.inWaiting()==0): 
                    pass #do nothing
                dataS = arduinoData.readline()        
                temp1 = 0
                temp2 = 0
                try:
                    datax=dataS.split(',')
                    temp1=float(datax[0])/1024
                    temp2= float(datax[1])/1024
                    data_file.write(str(temp1)+","+str(temp2)+'\n') 
                    #file_writer.writerow([temp1,temp2])
                except ValueError:
                    pass   
                data1.append(temp1)
                data2.append(temp2)
                cnt=cnt+1
                if(cnt>win):            
                    data1.pop(0)         
                    data2.pop(0) 
            fsc=395#1.0/cf
            #print(1.0/cf)
            #data1[-w2:-1] = butter_bandpass_filter(data1[-w2:-1], .05, 70, 395, order=5)
            if(len(data1)>4*395):
                [ft1,f1]=pwsp(data1,8192,fsc)
                [ft2,f2]=pwsp(data2,8192,fsc)
                drawnow(makeFig)                       #Call drawnow to update our live graph
                plt.pause(.000001)                     #Pause Briefly. Important to keep drawnow from crashing
            




if inp=="2":
    import matplotlib.pyplot as plt
    inp=raw_input("enter File name to read data\n")
    print "Reading data from file "+inp+".csv"
    data1=[]
    data2=[]
    with open(inp+'.csv', mode='r') as csv_file:
        #csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        #print csv_reader
        
        for line in csv_file:
            
            row=line.split(',')
            data1.append(float(row[0]))
            data2.append(float(row[1]))
            #print('\n'+row[0]+','+row[1])
            line_count += 1
        print('Total samples '+str(line_count)+'.')


    t=range(0,line_count)
    #t=t*(1/395.5)
    fig, axs = plt.subplots(2, 1)
    plt.plot(t, data1,t, data2)




        
