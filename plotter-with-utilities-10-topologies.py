import os

import matplotlib.pyplot as plt
import numpy

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
for i in os.listdir("/home/lexu/Desktop/henge_experiments/2016-12-15-14:11:49+Experiment_micromix_1"):
    if i.endswith("output.log") :
        print i
        f = open("/home/lexu/Desktop/henge_experiments/2016-12-15-14:11:49+Experiment_micromix_1/"+i, 'r')
        filename = f.__getattribute__("name").split(".")[0]
        print filename
        topology1_juice = []
        topology2_juice = []
        topology3_juice = []


        topology1_latency = []
        topology2_latency = []
        topology3_latency = []


        topology1_utility = []
        topology2_utility = []
        topology3_utility = []



        reduced_topology = []
        num_workers = []
        input_at_source_1 = []
        output_at_sink_1 = []
        input_at_source_2 = []
        output_at_sink_2 = []
        input_at_source_3 = []
        output_at_sink_3 = []

        time = []
        target = []
        target_operator = []
        victim_operator = []
        victim = []
        rebalance_time = []
        rebalance_desc = []

        #sample
        #StarTopology_ill-1-1477935100,0.22572376766944544,0.38325094771997914,878356.75,0.0019923567502612123,35.0,1780,360,1477936921086
        #diamond_regular-3-1477935114,1.799076289207868,1.2240119850930646,0.0,5.0,5.0,480,240,1477936921087

        latency_index = 3
        current_utility_index = 4
        specified_utility_index = 5

        name_index = 0
        juice_index = 2
        input_index = 7
        output_index = 8
        time_index = 9
        taillatency_index = 6

        for line in f:
                line = line.split("\n")[0]
                one_line = line.split(',')
                if "/var/nimbus/storm" not in one_line[name_index] and len(one_line) > 1:
                    if "star_ill"  in one_line[name_index]:
                        topology1_juice.append(float(one_line[juice_index]))
                        topology1_utility.append(float(one_line[current_utility_index]))
                        topology1_latency.append(float(one_line[latency_index]))
                        input_at_source_1.append(float(one_line[input_index]))
                        output_at_sink_1.append(float(one_line[output_index]))
                    elif "linear_regular"  in one_line[name_index]:
                        topology2_juice.append(float(one_line[juice_index]))
                        topology2_latency.append(float(one_line[latency_index]))
                        topology2_utility.append(float(one_line[current_utility_index]))
                        time.append(float(one_line[time_index]))
                        input_at_source_2.append(float(one_line[input_index]))
                        output_at_sink_2.append(float(one_line[output_index]))
                    elif "diamond_regular"  in one_line[name_index]:
                        topology3_juice.append(float(one_line[juice_index]))
                        input_at_source_3.append(float(one_line[input_index]))
                        topology3_latency.append(float(one_line[latency_index]))
                        topology3_utility.append(float(one_line[current_utility_index]))
                        output_at_sink_3.append(float(one_line[output_index]))

                    elif len(one_line) == 1 and "Running" not in one_line[0] and is_number(one_line[0]):
                        rebalance_time.append(float(one_line[0]))
                elif "/var/nimbus/storm" in one_line[0] :
                    time_for_rebalance = line.split(" ")
                    if "-n" not in line:
                        if flag == 0:
                            string = ""
                            #print time_for_rebalance[2]
                            if time_for_rebalance[2] == "StarTopology_ill":
                                string = "T1"
                            elif time_for_rebalance[2] == "linear_regular":
                                string = "T2"
                            elif time_for_rebalance[2] == "diamond_regular":
                                string = "T3"
                            
                            else:
                                string = time_for_rebalance[2]

                            #if (len(time_for_rebalance) > 6): # TODO -- GET RID OF IT
                            str = string + " " + time_for_rebalance[6]
                            #rebalance_desc.append(string + " "+ time_for_rebalance[6]) # should give topology name space num workers
                            i = 7
                            while len(time_for_rebalance) > i:
                                str = str + " "+ time_for_rebalance[i] # should give topology name space num workers
                                i = i + 1
                            rebalance_desc.append(str)

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
                        if time_for_rebalance[2] == "star_ill":
                            rebalance_desc.append("T1")
                        elif time_for_rebalance[2] == "linear_regular":
                            rebalance_desc.append("T2")
                        elif time_for_rebalance[2] == "diamond_regular":
                            rebalance_desc.append("T3")
                        
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
        print min_length


        if min_length > len(topology1_juice):
            min_length = len(topology1_juice)
        print min_length
        if min_length > len(topology2_juice):
            min_length = len(topology2_juice)

        print min_length
        if min_length > len(topology3_juice):
            min_length = len(topology3_juice)

        print min_length


        if min_length > len(topology1_latency):
            min_length = len(topology1_latency)
        if min_length > len(topology2_latency):
            min_length = len(topology2_latency)
        if min_length > len(topology3_latency):
            min_length = len(topology3_latency)

        print min_length

        if min_length > len(topology1_utility):
            min_length = len(topology1_utility)
        if min_length > len(topology2_utility):
            min_length = len(topology2_utility)
        if min_length > len(topology3_utility):
            min_length = len(topology3_utility)

        print min_length
        time = time[0:min_length]
        topology1_juice = topology1_juice [0:min_length]
        topology2_juice = topology2_juice [0:min_length]
        topology3_juice = topology3_juice [0:min_length]


        topology1_latency = topology1_latency [0:min_length]
        topology2_latency = topology2_latency [0:min_length]
        topology3_latency = topology3_latency [0:min_length]


        topology1_utility = topology1_utility [0:min_length]
        topology2_utility = topology2_utility [0:min_length]
        topology3_utility = topology3_utility [0:min_length]

#        print topology4_utility

        input_at_source_1 = input_at_source_1[0:min_length]
        output_at_sink_1 = output_at_sink_1[0:min_length]
        input_at_source_2 = input_at_source_2[0:min_length]
        output_at_sink_2 = output_at_sink_2[0:min_length]
        input_at_source_3 = input_at_source_3[0:min_length]
        output_at_sink_3 = output_at_sink_3[0:min_length]
 
        fig, ax = plt.subplots()

        ax.scatter(time, topology1_juice, edgecolors ="blue", label="T1 Juice", marker ="D", facecolors='none', s=40,)
        ax.scatter(time, topology2_juice, edgecolors ="green", label="T2 Juice Latency-SLO=70 Utility=35", marker =">", facecolors='none', s=40,)
        ax.scatter(time, topology3_juice, edgecolors ="red", label="T3 Juice Latency-SLO=70 Utility=35", marker="h", facecolors='none', s=40, )
 #       ax.scatter(time, topology4_juice, edgecolors ="c", label="T4 Juice Latency-SLO=70 Utility=35", marker="s", facecolors='none', s=40,)
 #       ax.scatter(time, topology5_juice, edgecolors ="m", label="T5 Juice Latency-SLO=50 Utility=35", marker =">", facecolors='none', s=40,)
 #       ax.scatter(time, topology6_juice, edgecolors ="black", label="T6 Juice SLO=1 Utility=5", marker="h", facecolors='none', s=40, )
 #       ax.scatter(time, topology7_juice, edgecolors ="darkorange", label="T7 Juice SLO=1 Utility=5", marker="s", facecolors='none', s=40,)
 #       ax.scatter(time, topology8_juice, edgecolors ="#456648", label="T8 Latency SLO=50 Utility=35", marker =">", facecolors='none', s=40,)
 #       ax.scatter(time, topology9_juice, edgecolors ="y", label="T9 Juice SLO=1 Utility=5", marker="h", facecolors='none', s=40, )
 #       ax.scatter(time, topology10_juice, edgecolors ="#886F4C", label="T10 Juice SLO=1 Utility=5", marker="s", facecolors='none', s=40,)


        ax2 = ax.twinx()
        #ax2.scatter(time, topology1_latency, edgecolors ="green", label="T1 Latency", marker ="*", facecolors='none', s=40,)
        #ax2.scatter(time, topology2_latency, edgecolors ="#1f78b4", label="T2 Latency", marker ="<", facecolors='none', s=40,)
        #ax2.scatter(time, topology3_latency, edgecolors ="#b2df8a", label="T3 Latency", marker="D", facecolors='none', s=40, )


        ax.set_xlabel('Time/s', fontsize=10)
        ax.set_ylabel('Juice', fontsize=10)
        ax2.set_ylabel('Latency/ms', fontsize=10)

        #
        ax.grid(True)
        fig.tight_layout()


        #plt.vlines(x=600, ymax=1000 , ymin=0, label="Ten Minute Mark", colors='blue')

        #clrs = ["b", "g", "r", "c", "m", "y", "k"]
        clrs = ["k", "k", "k", "k", "k", "k", "k"]
        linestyles = [ '--' , '-.' , 'solid', 'dotted']
        for j in range(0, len(rebalance_time)):
            #if (rebalance_time[j] >= 35000 and rebalance_time[j] <= 105000):# and ("T2" in rebalance_desc[j]):
           #if "T1" in rebalance_desc[j]:
			la = rebalance_desc[j]
			ax.vlines(x=rebalance_time[j], ymax=6 , ymin=-1,  colors=clrs[j%7], linestyle= 'solid', label=la)

        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines  + lines2, labels + labels2  , loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2,prop={'size':4}) #, label=la,)#linestyles[j%4]

        #ax2.set_yscale('log')
        #plt.xlim(0,23000)

        #ax.set_ylim(0.95, 1.05)
       # ax2.set_ylim(0,200)

        ax.set_ylim(0.9,1.1)
        plt.xlim(0,20000)

        plt.savefig(filename+'.png', bbox_inches='tight')


#plotting utilities

        fig, ax = plt.subplots()
        ax.scatter(time, topology1_utility, edgecolors ="green", label="T1 Utility", marker ="D", facecolors='none', s=40,)
        ax.scatter(time, topology2_utility, edgecolors ="green", label="T2 Latency SLO=50 Utility=35", marker =">", facecolors='none', s=40,)
        ax.scatter(time, topology3_utility, edgecolors ="red", label="T3 Latency SLO=1 Utility=35", marker="h", facecolors='none', s=40, )


        ax.set_xlabel('Time/S', fontsize=10)
        ax.set_ylabel('Utility', fontsize=10)
        ax.grid(True)
        fig.tight_layout()

        xlim_start = 0
        xlim_end = 5000
        linestyles = [ '--' , '-.' , 'solid', 'dotted']
        for j in range(0, len(rebalance_time)):
            if (rebalance_time[j] >=xlim_start and rebalance_time[j] <= xlim_end):
                la = rebalance_desc[j]
                ax.vlines(x=rebalance_time[j], ymax=250 , ymin=-1,  colors=clrs[j%7], linestyle= 'solid', label=la,)#linestyles[j%4]

        sum =[]
        temp_time = []
        for j in range(0, len(time)):
            if (time[j] >=xlim_start and time[j] <= xlim_end):
                temp_time.append(time[j])
                print topology1_utility[j]
                print topology2_utility[j]
                print topology3_utility[j]

                sum.append((topology1_utility[j] + topology2_utility[j] + topology3_utility[j]))#/10.0

        ax.scatter(temp_time, sum, edgecolors ="red", label="Sum", marker="h", facecolors='r', s=80,)

        lines, labels = ax.get_legend_handles_labels()
        ax.legend(lines, labels , loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2,prop={'size':10})

        plt.xlim(xlim_start,xlim_end)
        ax.set_ylim(-1,16)
        #ax.set_ylim(185,205)
        plt.savefig(filename+'-utilities.png', bbox_inches='tight')
# plotting input and output tuples
        fig, ax = plt.subplots()

        ax.scatter(time, input_at_source_1, edgecolors = "green", label= "T1 input", facecolor='none', marker = "D", s=40)
      #  ax.scatter(time, output_at_sink_1, edgecolors = "blue", label= "T1 output" ,facecolor='none', marker = "+", s=40)
        ax.scatter(time, input_at_source_2, edgecolors = "red", label= "T2 input",facecolor='none', marker = ">", s=40)
      #  ax.scatter(time, output_at_sink_2, edgecolors = "blue", label= "T2 output" ,facecolor='none', marker = "<",s=40)
        ax.scatter(time, input_at_source_3, edgecolors = "teal", label= "T3 input", facecolor='none', marker = "x",s=40)
      #  ax.scatter(time, output_at_sink_3, edgecolors = "green", label= "T3 output", facecolor='none', marker = "h", s=40)
      

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
        #plt.ylim(0,100000)
        #plt.ylim(0,20000)
        plt.ylim(0,5000)
        plt.savefig(filename+"+tuples"+'.png', bbox_inches='tight')
