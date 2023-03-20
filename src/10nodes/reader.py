import threading;
import time;
import random;
import requests;
import json;


NODES = 10;

reqList = [];

def transRequest(filename, port):
    f = open(filename, "r");
    f1 = f.readlines();
    for line in f1:
        args = line.split();
        requestData = '{"id": "' + args[0] + '", "amount":' + args[1] + '}';
        url =  "http://127.0.0.1:" + str(port) + "/newTransaction";
        reqList.append((url, requestData));    
    return;

if __name__ == '__main__':
    startTimestamp = time.time();
    threads = []
    transactions =0;
    for i in range(NODES):
        myFile = 'transactions' + str(i) + '.txt';
        myPort = 5000;
        myPort += i;
        threads.append(threading.Thread(target = transRequest, args = (myFile,myPort,)));
        
    for i in range(NODES):
        threads[i].start();
        
    for i in range(NODES):
        threads[i].join();
    
    random.shuffle(reqList);
    for request in reqList:
        response = requests.post(request[0], data = request[1]);
        if response.status_code == 200:
            transactions += 1;
        time.sleep(0.2);
    
    endTimestamp = time.time();
    duration = endTimestamp - startTimestamp;
    throughput = transactions / duration;
    print("All transactions done in %d seconds" %duration )
    print("Throughput %f" %throughput)
    response = requests.get("http://127.0.0.1:5000/printChain");
    responseDict = json.loads(response.json());
    noBlocks = int(responseDict['length']) - 1;
    avgBlockTime = duration / noBlocks;
    print("The average duration of block mining was %f seconds" %avgBlockTime);
    
