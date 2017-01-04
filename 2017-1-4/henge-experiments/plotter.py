import os

import matplotlib.pyplot as plt
import numpy
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def movingaverage(interval, window_size):
    window = numpy.ones(int(window_size))/float(window_size)
    return numpy.convolve(interval, window, 'same')

def reject_outliers(data, m):
    u = numpy.mean(data)
    s = numpy.std(data)
    filtered = []
    for e in data:
        if (u - m * s < e < u + m * s):
            filtered.append(e)
        else:
            print "Does not apply"
            filtered.append(u)
    return filtered

flag = 0
desc_string = " "
for i in os.listdir("/home/lexu/Desktop/henge_experiments/henge-experiments/2016-11-15-16:02:46+Experiment1_NUM_WORKERS_10TO1/"):
    if i.endswith("output.log") :
        print i
        f = open("/home/lexu/Desktop/henge_experiments/henge-experiments/2016-11-15-16:02:46+Experiment1_NUM_WORKERS_10TO1/"+i, 'r')
        filename = f.__getattribute__("name").split(".")[0]
        print filename
        topology1_juice = []
        topology2_juice = []
        topology3_juice = []
        topology4_juice = []
        topology1_latency = []
        topology2_latency = []
        topology3_latency = []
        topology4_latency = []
        reduced_topology = []
        num_workers = []
        input_at_source_1 = []
        output_at_sink_1 = []
        input_at_source_2 = []
        output_at_sink_2 = []
        input_at_source_3 = []
        output_at_sink_3 = []
        input_at_source_4 = []
        output_at_sink_4 = []
        time = []
        target = []
        target_operator = []
        victim_operator = []
        victim = []
        rebalance_time = []
        rebalance_desc = []
        latency_index = 3
        name_index = 0
        juice_index = 2
        input_index = 4
        output_index = 5
        time_index = 6

        for line in f:
                line = line.split("\n")[0]
                one_line = line.split(',')
                if "/var/nimbus/storm" not in one_line[name_index] and len(one_line) > 1:
                    if "production-topology1"  in one_line[name_index]:
                        topology1_juice.append(float(one_line[juice_index]))
                        topology1_latency.append(float(one_line[latency_index]))
                        time.append(float(one_line[time_index]))
                        input_at_source_1.append(float(one_line[input_index]))
                        output_at_sink_1.append(float(one_line[output_index]))
                    
                    elif len(one_line) == 1 and "Running" not in one_line[0] and is_number(one_line[0]):
                        rebalance_time.append(float(one_line[0]))
                elif "/var/nimbus/storm" in one_line[0] :
                    time_for_rebalance = line.split(" ")
                    if "-n" not in line:
                        if flag == 0:
                            string = ""
                            print time_for_rebalance[2]
                            if time_for_rebalance[2] == "production-topology1":
                                string = "T1"
                            
                            else:
                                string = time_for_rebalance[2]
                            rebalance_desc.append(string + " "+ time_for_rebalance[6]) # should give topology name space num workers

                            #desc_string = " ".join((time_for_rebalance[2] , time_for_rebalance[6]))

                            #rebalance_desc.append(desc_string) # get rid of this if you have multiple rebalances
                     #       flag = 1
                     #   else:
                     #       temp = " ".join((time_for_rebalance[2], time_for_rebalance[6]))
                     #       desc_string = " ".join((desc_string,temp))
                     #       rebalance_desc.append(desc_string)
                     #       desc_string = " "
                     #       flag = 0
                    else:
                        print time_for_rebalance[2]
                        if time_for_rebalance[2] == "production-topology1":
                            rebalance_desc.append("T1")
                        
                        else:
                            rebalance_desc.append(time_for_rebalance[2])
                        rebalance_desc.append(" "+ time_for_rebalance[4]) # should give topology name space num workers
                elif len(one_line) == 1 and is_number(one_line[0]):
                    rebalance_time.append(float(one_line[0]))

        val = time[0]
        for i in range(0, len(time)):
            time[i] = (time[i] - val)/1000
        for i in range(0, len(rebalance_time)):
            rebalance_time[i] = (rebalance_time[i] - val)/1000

        min_length = len(time)

        if min_length > len(topology1_juice):
            min_length = len(topology1_juice)
       
        if min_length > len(topology1_latency):
            min_length = len(topology1_latency)


        time = time[0:min_length]
        topology1_juice = topology1_juice [0:min_length]


        topology1_latency = topology1_latency [0:min_length]


     #   print topology4_latency

        input_at_source_1 = input_at_source_1[0:min_length]
        output_at_sink_1 = output_at_sink_1[0:min_length]


        fig, ax = plt.subplots()
        ax.scatter(time, topology1_juice, edgecolors ="blue", label="T1 Latency SLO=30", marker ="D", facecolors='none', s=40,)


        ax2 = ax.twinx()
        ax2.scatter(time, topology1_latency, edgecolors ="black", label="T1 Latency", marker ="*", facecolors='none', s=40,)


        ax.set_xlabel('Time/S', fontsize=10)
        ax.set_ylabel('Juice', fontsize=10)
        ax2.set_ylabel('Latency/S', fontsize=10)
        ax.grid(True)
        fig.tight_layout()

        plt.vlines(x=600, ymax=1000 , ymin=0, label="Ten Minute Mark", colors='blue')

        linestyles = [ '--']
        for j in range(0, len(rebalance_time)):
            la = rebalance_desc[j]
            ax.vlines(x=rebalance_time[j], ymax=5 , ymin=-1,  colors='black', linestyle=linestyles[j%4], label=la,)

        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2 , loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2,prop={'size':10}) #+ lines2 #+ labels2

        #plt.xlim(0,20000)
        ax.set_ylim(0.5, 1.5)
        ax2.set_ylim(0,200)

        plt.savefig(filename+'.png', bbox_inches='tight')

        fig, ax = plt.subplots()

        x_av1 = movingaverage(output_at_sink_1, 10)


        ax.scatter(time, input_at_source_1, edgecolors = "chocolate", label= "T1 input", facecolor='none', marker = "D", s=40)
        ax.scatter(time, x_av1, edgecolors = "black", label= "T1 output" ,facecolor='none', marker = "+", s=40)


        for j in range(0, len(rebalance_time)):
            la = rebalance_desc[j]#target[j] + " " + target_operator[j] + " " + victim[j] + " " + victim_operator[j]
            ax.vlines(x=rebalance_time[j], ymax=5000 , ymin=-1,  colors='black', linestyle=linestyles[j%4], label=la,) #label=la,label="rebalance " + str(j+1),

        ax.set_xlabel('Time/S', fontsize=10)
        ax.set_ylabel('Number of Tuples', fontsize=10)

        ax.grid(True)
        fig.tight_layout()
        plt.vlines(x=600, ymax=5000 , ymin=-1, label="Ten Minute Mark", colors='blue')
        plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2,prop={'size':10})
        plt.xlim(0,60000)
        plt.ylim(1000,1500)
        plt.savefig(filename+"+tuples"+'.png', bbox_inches='tight')