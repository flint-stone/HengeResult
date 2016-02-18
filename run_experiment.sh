#!/bin/sh
#echo "setting env vars..."
#setenv STORM_DIR /var/storm
#setenv STORM_SRC_DIR /proj/CS525/storm
#setenv PATH ${PATH}:${HOME}/bin:$STORM_DIR/zookeeper-3.4.6/bin:/var/storm/storm_0/bin/
#ssh node-2 "sudo killall java"
echo "starting storm topology...";

#echo "sleep 570";
#sleep 300;
#echo "rebalancing...";
#java  Client;
#ssh node-6 "sudo killall java"
#ssh node-7 "sudo killall java"
#ssh node-8 "sudo killall java"
#ssh node-9 "sudo killall java"
#filename="/tmp/ElasticityScheduler_Nodelist";
#echo "killing nodes ...";
#while read -r line
#do
#    name=$line
#    ssh $name "sudo killall java";
#done < "$filename"
#echo  "sleep 10 min"
#sleep 1200
#sudo cp /tmp/ElasticityScheduler* .
#sudo cp /tmp/EvenScheduler* .
#echo "done...killing topology"
#/
cd /var/nimbus/storm
sudo bin/storm jar examples/storm-starter/storm-starter-0*.jar storm.starter.PageLoadTopology production-topology1 remote  && sudo bin/storm jar examples/storm-starter/storm-starter-0*.jar storm.starter.PageLoadTopology_LessSLO production-topology2 remote && sudo bin/storm jar examples/storm-starter/storm-starter-0*.jar storm.starter.ProcessingTopology production-topology3 remote && sudo bin/storm jar examples/storm-starter/storm-starter-0*.jar storm.starter.ProcessingTopology_LessSLO production-topology4 remotear/storm/storm_0/bin/storm kill test1
sleep 10800
sudo bin/storm kill production-topology1
sudo bin/storm kill production-topology2
sudo bin/storm kill production-topology3
sudo bin/storm kill production-topology4

#sudo killall java

foldername=$(date +%Y%m%d-%T)
mkdir -p ~/henge-experiments/HengeResult/"$foldername"
sudo cp /tmp/*.log ~/henge-experiments/HengeResult/"$foldername"/


#sudo killall java





