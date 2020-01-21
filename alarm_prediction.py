import prelearning
import predicting
import os
import time
import threading
import json_to_csv
import pandas as pd
import csv

SVMscore=[]
SVMs=[]
for SVMi in range(10):
    SVMi=prelearning.SVM('TrainingData14.csv') #traning data set file input
    SVMscore.append(float(prelearning.scoring()))
    SVMs.append(SVMi)

print 'use: ',SVMscore[SVMscore.index(max(SVMscore))]
svm_model=SVMs[SVMscore.index(max(SVMscore))]

global flag1
flag1 = 0
alarm_flag = 0
global flag2
flag2 = 0
global flag3
flag3 = 0
global flag4
flag4 = 0
global flag5
flag5 = 0

def alarm_next():
    global alarm_flag
    alarm_flag = 1
    print("=============== alarm! ===============")
    time.sleep(10)
    #after Alarm
    def db_alarm_to_tower():
        os.system('python db_alarm_to_tower.py')

    def db_json_to_tower():
        os.system('python db_json_from_influx.py')

    thread1 = threading.Thread(target = db_alarm_to_tower)
    thread1.start()

    thread2 = threading.Thread(target = db_json_to_tower)
    thread2.start()

def pi1():
    #global green_flag, yellow_flag, red_flag
    #global count_none_red

    green_flag, yellow_flag, red_flag, count_none_red = 0,0,0,0

    global alarm_flag
    global flag2
    while 1:
        if alarm_flag == 1:
            print("pi1 loop complete because alarm")
            break
        #get test_set.csv file from influxdb
    #    os.system('curl -G \'http://103.22.222.214:8086/query?pretty=true\' --data-urlencode "db=labs" --data-urlencode "q=SELECT \"time_stamp\",\"temperature\",\"CO_ADvalue\",\"CO_density\",\"flame_fireADC\",\"motion_detect\" FROM \"resource\" where time > now() - 20s" > sensor_all_csv.csv')
        os.system('influx -database sensor -format csv -execute \'select CO_ADvalue, flame_fireADC, human, temperature from sensor WHERE pi = 1 AND time > now() - 1d\' > pi1.csv')

        print("Finish querying P1")

    #    filename_json = "" ##input json filename for the module json_to_csv
    #    filename_csv = "" ##input csv filename
    #    Convert_json(filename_json,filename_csv)
        filename_csv = 'pi1.csv'
        test_set = pd.read_csv(filename_csv)

        cnt={"[\'Red\']":0, "[\'Yellow\']":0, "[\'Green\']":0}

        for line in range(0,len(test_set)):

            print("line num:",line)

            a=test_set['CO_ADvalue'][line]
            b=test_set['flame_fireADC'][line]
            c=test_set['temperature'][line]
            if line > 0:
                d=(test_set['temperature'][line]-test_set['temperature'][line-1]) #dt
            else:
                d=0

            if line > 0:
                print("recap -",a,b,c,d)
                s=svm_model.predict([[float(a) ,float(b), float(c), float(d)]])
                print(s)
                # print("report =\n", cl_report)
                if __name__ == '__main__':
                    if str(s) == '[\'Red\']':
                        cnt[str(s)] += 1
                    elif str(s) == '[\'Yellow\']':
                        cnt[str(s)] += 1
                    elif str(s) == '[\'Green\']':
                        cnt[str(s)] += 1

                    if cnt['[\'Green\']'] >= 0.7*len(test_set):
                        green_flag = 1
                    elif cnt['[\'Yellow\']'] >= 0.7*len(test_set):
                        yellow_flag = 1
                    elif cnt['[\'Red\']'] >= 0.7*len(test_set):
                        if yellow_flag == 1:
                            red_flag = 1
                            flag2 = 1
                            print('#####CASE RED#####')
                            #os.system('python3 ML_alarm.py')
                        else:
                            yellow_flag = 1
                            cnt['[\'Red\']'] = 0

                    if yellow_flag == 1 and red_flag == 0:
                        count_none_red += 1

                    print("P1 report : green flag = {0}, yellow flag = {1}, red flag = {2}, none red count = {3}\r\n".format(green_flag, yellow_flag, red_flag, count_none_red))
                    if flag2 == 1:
                        break
                if flag2 == 1:
                    break
            if flag2 == 1:
                break
        if flag2 == 1:
            break

        if count_none_red >= 12:
            count_none_red = 0
            yellow_flag = 0

    if alarm_flag == 1:
        pass
    else:
        print("pi1 alarm!")
        alarm_next()
    time.sleep(5)


def pi2():
    #global green_flag, yellow_flag, red_flag
    #global count_none_red

    green_flag, yellow_flag, red_flag, count_none_red = 0,0,0,0

    global alarm_flag
    global flag2
    while 1:
        if alarm_flag == 1:
            print("pi2 loop complete because alarm")
            break
        #get test_set.csv file from influxdb
    #    os.system('curl -G \'http://103.22.222.214:8086/query?pretty=true\' --data-urlencode "db=labs" --data-urlencode "q=SELECT \"time_stamp\",\"temperature\",\"CO_ADvalue\",\"CO_density\",\"flame_fireADC\",\"motion_detect\" FROM \"resource\" where time > now() - 20s" > sensor_all_csv.csv')
        os.system('influx -database sensor -format csv -execute \'select CO_ADvalue, flame_fireADC, human, temperature from sensor WHERE pi = 2 AND time > now() - 1d\' > pi2.csv')

        print("Finish querying P2")

    #    filename_json = "" ##input json filename for the module json_to_csv
    #    filename_csv = "" ##input csv filename
    #    Convert_json(filename_json,filename_csv)
        filename_csv = 'pi2.csv'
        test_set = pd.read_csv(filename_csv)

        cnt={"[\'Red\']":0, "[\'Yellow\']":0, "[\'Green\']":0}

        for line in range(0,len(test_set)):

            print("line num:",line)

            a=test_set['CO_ADvalue'][line]
            b=test_set['flame_fireADC'][line]
            c=test_set['temperature'][line]
            if line > 0:
                d=(test_set['temperature'][line]-test_set['temperature'][line-1]) #dt
            else:
                d=0

            if line > 0:
                print("recap -",a,b,c,d)
                s=svm_model.predict([[float(a) ,float(b), float(c), float(d)]])
                print(s)
                # print("report =\n", cl_report)
                if __name__ == '__main__':
                    if str(s) == '[\'Red\']':
                        cnt[str(s)] += 1
                    elif str(s) == '[\'Yellow\']':
                        cnt[str(s)] += 1
                    elif str(s) == '[\'Green\']':
                        cnt[str(s)] += 1

                    if cnt['[\'Green\']'] >= 0.7*len(test_set):
                        green_flag = 1
                    elif cnt['[\'Yellow\']'] >= 0.7*len(test_set):
                        yellow_flag = 1
                    elif cnt['[\'Red\']'] >= 0.7*len(test_set):
                        if yellow_flag == 1:
                            red_flag = 1
                            flag2 = 1
                            print('#####CASE RED#####')
                            #os.system('python3 ML_alarm.py')
                        else:
                            yellow_flag = 1
                            cnt['[\'Red\']'] = 0

                    if yellow_flag == 1 and red_flag == 0:
                        count_none_red += 1

                    print("P2 report : green flag = {0}, yellow flag = {1}, red flag = {2}, none red count = {3}\r\n".format(green_flag, yellow_flag, red_flag, count_none_red))
                    if flag2 == 1:
                        break
                if flag2 == 1:
                    break
            if flag2 == 1:
                break
        if flag2 == 1:
            break

        if count_none_red >= 12:
            count_none_red = 0
            yellow_flag = 0

    if alarm_flag == 1:
        pass
    else:
        print("pi2 alarm!")
        alarm_next()
    time.sleep(5)

def pi3():
    #global green_flag, yellow_flag, red_flag
    #global count_none_red

    green_flag, yellow_flag, red_flag, count_none_red = 0,0,0,0

    global alarm_flag
    global flag3
    while 1:
        if alarm_flag == 1:
            print("pi3 loop complete because alarm")
            break
        #get test_set.csv file from influxdb
    #    os.system('curl -G \'http://103.22.222.214:8086/query?pretty=true\' --data-urlencode "db=labs" --data-urlencode "q=SELECT \"time_stamp\",\"temperature\",\"CO_ADvalue\",\"CO_density\",\"flame_fireADC\",\"motion_detect\" FROM \"resource\" where time > now() - 20s" > sensor_all_csv.csv')
        os.system('influx -database sensor -format csv -execute \'select CO_ADvalue, flame_fireADC, human, temperature from sensor WHERE pi = 3 AND time > now() - 1d\' > pi3.csv')

        print("Finish querying P3")

    #    filename_json = "" ##input json filename for the module json_to_csv
    #    filename_csv = "" ##input csv filename
    #    Convert_json(filename_json,filename_csv)
        filename_csv = 'pi3.csv'
        test_set = pd.read_csv(filename_csv)

        cnt={"[\'Red\']":0, "[\'Yellow\']":0, "[\'Green\']":0}

        for line in range(0,len(test_set)):

            print("line num:",line)

            a=test_set['CO_ADvalue'][line]
            b=test_set['flame_fireADC'][line]
            c=test_set['temperature'][line]
            if line > 0:
                d=(test_set['temperature'][line]-test_set['temperature'][line-1]) #dt
            else:
                d=0

            if line > 0:
                print("recap -",a,b,c,d)
                s=svm_model.predict([[float(a) ,float(b), float(c), float(d)]])
                print(s)
                # print("report =\n", cl_report)
                if __name__ == '__main__':
                    if str(s) == '[\'Red\']':
                        cnt[str(s)] += 1
                    elif str(s) == '[\'Yellow\']':
                        cnt[str(s)] += 1
                    elif str(s) == '[\'Green\']':
                        cnt[str(s)] += 1

                    if cnt['[\'Green\']'] >= 0.7*len(test_set):
                        green_flag = 1
                    elif cnt['[\'Yellow\']'] >= 0.7*len(test_set):
                        yellow_flag = 1
                    elif cnt['[\'Red\']'] >= 0.7*len(test_set):
                        if yellow_flag == 1:
                            red_flag = 1
                            flag3 = 1
                            print('#####CASE RED#####')
                            #os.system('python3 ML_alarm.py')
                        else:
                            yellow_flag = 1
                            cnt['[\'Red\']'] = 0

                    if yellow_flag == 1 and red_flag == 0:
                        count_none_red += 1

                    print("P3 report : green flag = {0}, yellow flag = {1}, red flag = {2}, none red count = {3}\r\n".format(green_flag, yellow_flag, red_flag, count_none_red))
                    if flag2 == 1:
                        break
                if flag3 == 1:
                    break
            if flag3 == 1:
                break
        if flag3 == 1:
            break

        if count_none_red >= 12:
            count_none_red = 0
            yellow_flag = 0

    if alarm_flag == 1:
        pass
    else:
        print('pi3 alarm!')
        alarm_next()
    time.sleep(5)

def pi4():
    #global green_flag, yellow_flag, red_flag
    #global count_none_red

    green_flag, yellow_flag, red_flag, count_none_red = 0,0,0,0

    global alarm_flag
    global flag4
    while 1:
        if alarm_flag == 1:
            print("pi4 loop complete because alarm")
            break
        #get test_set.csv file from influxdb
    #    os.system('curl -G \'http://103.22.222.214:8086/query?pretty=true\' --data-urlencode "db=labs" --data-urlencode "q=SELECT \"time_stamp\",\"temperature\",\"CO_ADvalue\",\"CO_density\",\"flame_fireADC\",\"motion_detect\" FROM \"resource\" where time > now() - 20s" > sensor_all_csv.csv')
        os.system('influx -database sensor -format csv -execute \'select CO_ADvalue, flame_fireADC, human, temperature from sensor WHERE pi = 4 AND time > now() - 1d\' > pi4.csv')
        print("Finish querying P4")

    #    filename_json = "" ##input json filename for the module json_to_csv
    #    filename_csv = "" ##input csv filename
    #    Convert_json(filename_json,filename_csv)
        filename_csv = 'pi4.csv'
        test_set = pd.read_csv(filename_csv)

        cnt={"[\'Red\']":0, "[\'Yellow\']":0, "[\'Green\']":0}

        for line in range(0,len(test_set)):

            print("line num:",line)

            a=test_set['CO_ADvalue'][line]
            b=test_set['flame_fireADC'][line]
            c=test_set['temperature'][line]
            if line > 0:
                d=(test_set['temperature'][line]-test_set['temperature'][line-1]) #dt
            else:
                d=0


            if line > 0:
                print("recap -",a,b,c,d)
                s=svm_model.predict([[float(a) ,float(b), float(c), float(d)]])
                print(s)
                # print("report =\n", cl_report)
                if __name__ == '__main__':
                    if str(s) == '[\'Red\']':
                        cnt[str(s)] += 1
                    elif str(s) == '[\'Yellow\']':
                        cnt[str(s)] += 1
                    elif str(s) == '[\'Green\']':
                        cnt[str(s)] += 1

                    if cnt['[\'Green\']'] >= 0.7*len(test_set):
                        green_flag = 1
                    elif cnt['[\'Yellow\']'] >= 0.7*len(test_set):
                        yellow_flag = 1
                    elif cnt['[\'Red\']'] >= 0.7*len(test_set):
                        if yellow_flag == 1:
                            red_flag = 1
                            flag4 = 1
                            print('#####CASE RED#####')
                            #os.system('python3 ML_alarm.py')
                        else:
                            yellow_flag = 1

                    if yellow_flag == 1 and red_flag == 0:
                        count_none_red += 1
                        cnt['[\'Red\']'] = 0

                    print("P4 report : green flag = {0}, yellow flag = {1}, red flag = {2}, none red count = {3}\r\n".format(green_flag, yellow_flag, red_flag, count_none_red))
                    if flag2 == 1:
                        break
                if flag4 == 1:
                    break
            if flag4 == 1:
                break
        if flag4 == 1:
            break

        if count_none_red >= 12:
            count_none_red = 0
            yellow_flag = 0

    if alarm_flag == 1:
        pass
    else:
        print('pi4 alarm!')
        alarm_next()
    time.sleep(5)



def pi5():
    #global green_flag, yellow_flag, red_flag
    #global count_none_red

    green_flag, yellow_flag, red_flag, count_none_red = 0,0,0,0

    global alarm_flag
    global flag5
    while 1:
        if alarm_flag == 1:
            print("pi5 loop complete because alarm")
            break
        #get test_set.csv file from influxdb
    #    os.system('curl -G \'http://103.22.222.214:8086/query?pretty=true\' --data-urlencode "db=labs" --data-urlencode "q=SELECT \"time_stamp\",\"temperature\",\"CO_ADvalue\",\"CO_density\",\"flame_fireADC\",\"motion_detect\" FROM \"resource\" where time > now() - 20s" > sensor_all_csv.csv')
        os.system('influx -database sensor -format csv -execute \'select CO_ADvalue, flame_fireADC, human, temperature from sensor WHERE pi = 5 AND time > now() - 1d\' > pi5.csv')

        print("Finish querying P5")

    #    filename_json = "" ##input json filename for the module json_to_csv
    #    filename_csv = "" ##input csv filename
    #    Convert_json(filename_json,filename_csv)
        filename_csv = 'pi5.csv'
        test_set = pd.read_csv(filename_csv)

        cnt={"[\'Red\']":0, "[\'Yellow\']":0, "[\'Green\']":0}

        for line in range(0,len(test_set)):

            print("line num:",line)

            a=test_set['CO_ADvalue'][line]
            b=test_set['flame_fireADC'][line]
            c=test_set['temperature'][line]
            if line > 0:
                d=(test_set['temperature'][line]-test_set['temperature'][line-1]) #dt
            else:
                d=0

            if line > 0:
                print("recap -",a,b,c,d)
                s=svm_model.predict([[float(a) ,float(b), float(c), float(d)]])
                print(s)
                # print("report =\n", cl_report)
                if __name__ == '__main__':
                    if str(s) == '[\'Red\']':
                        cnt[str(s)] += 1
                    elif str(s) == '[\'Yellow\']':
                        cnt[str(s)] += 1
                    elif str(s) == '[\'Green\']':
                        cnt[str(s)] += 1

                    if cnt['[\'Green\']'] >= 0.7*len(test_set):
                        green_flag = 1
                    elif cnt['[\'Yellow\']'] >= 0.7*len(test_set):
                        yellow_flag = 1
                    elif cnt['[\'Red\']'] >= 0.7*len(test_set):
                        if yellow_flag == 1:
                            red_flag = 1
                            flag5 = 1
                            print('#####CASE RED#####')
                            #os.system('python3 ML_alarm.py')
                        else:
                            yellow_flag = 1
                            cnt['[\'Red\']'] = 0

                    if yellow_flag == 1 and red_flag == 0:
                        count_none_red += 1

                    print("P5 report : green flag = {0}, yellow flag = {1}, red flag = {2}, none red count = {3}\r\n".format(green_flag, yellow_flag, red_flag, count_none_red))
                    if flag2 == 1:
                        break
                if flag5 == 1:
                    break
            if flag5 == 1:
                break
        if flag5 == 1:
            break

        if count_none_red >= 12:
            count_none_red = 0
            yellow_flag = 0

    if alarm_flag == 1:
        pass
    else:
        print('pi5 alarm!')
        alarm_next()
    time.sleep(5)


thread_pi1 = threading.Thread(target = pi1)
thread_pi1.start()

thread_pi2 = threading.Thread(target = pi2)
thread_pi2.start()

thread_pi3 = threading.Thread(target = pi3)
thread_pi3.start()

thread_pi4 = threading.Thread(target = pi4)
thread_pi4.start()

thread_pi5 = threading.Thread(target = pi5)
thread_pi5.start()
