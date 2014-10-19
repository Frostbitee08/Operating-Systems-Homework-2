'''
OPERATING SYSTEMS - HOMEWORK 2
PROCESS MANAGEMENT SIMULATION SYSTEM

Zachary Vanderzee
Rocco Del Priore
Caitlin Connerney
'''

import random
import operator
import sys

m = 1 				#Number of Cores used
n = 12				#Number of Processes ran
timeLimit = 100		#Time limit given for Algoritms like Round Robin

# Process Class
class process:
	# Constructor for a Process
	def __init__(self, p, t, b, i):
		self.pid 	= p      		# Process ID
		self.time = t 				# Time it takes to complete 20-200ms or 200-3000ms
		self.turn = 0					# Total Time taken to complete
		self.wait = 0					# Time spent in Queue or time spent waiting for input
		self.priority = 0			# Priority Level
		self.bursts = b 			# Bursts it takes to complete
		self.inter = i 				# Interactive Process or not

	# Simple print function for debugging
	def printP(self):
		print(self.pid,self.time,self.turn,self.wait,self.priority,self.bursts,self.inter)
	
	# Returns whether a process has finished or not
	def done(self):
		if self.bursts == 0:
			True
		else:
			False

# Print Function to handle all the if statements when printing
# Case 1: Process entry 
# Case 2: Context switch
# Case 3: Process CPU burst completion
# Case 4: Process termination
# Case 5: Aging event
def printProcess(time,case,p):
	if case == 1:
		if p.inter:
			print "[time",time,"ms] Interactive process ID",p.pid,"entered ready queue (requires",p.time,"ms CPU time)"
		else:
			print "[time",time,"ms] CPU-bound process ID",p.pid,"entered ready queue (requires",p.time,"ms CPU time)"
	elif case == 2:
		print "To be implimented"
	elif case == 3:
		print "To be implimented"
	elif case == 4:
		if p.inter:
			print "[time",time,"ms] Interactive process ID",p.pid,"has terminated (turnaround time", p.turn, "ms wait time", p.wait,"ms)"
		else:
			print "[time",time,"ms] CPU-bound process ID",p.pid,"has terminated (turnaround time", p.turn, "ms wait time", p.wait,"ms)"
	else:
		print "To be implimented"

#	Shortest Job First without Preemption algorithm
# Takes in a list of processes and puts them into a que to run
def SJFN( processes ):
	# Put all processes in Queue
	queue = []
	waiting = []
	procs = 0
	for p in processes:
		queue.append(p)
		if p.inter:
			procs += 1
	# Sort the list by the completion time
	for p in queue:
		printProcess(0,1,p)
	queue.sort(key=operator.attrgetter('time'))	
	# Simulate processing
	time = 0
	current = 0
	while len(queue)+len(waiting) > 0:
		if(current == 0):
			current = queue.pop(0)
		elif(time - current.wait == current.time):
			if(current.inter):
				current.wait=random.randint(1000,4501)
				waiting.append(current)
				current=0
			else
				if(current.bursts > 1):
					current.bursts-=1
					current.wait = random.randint(1200,3201)
				else
					current = 0
		if(waiting[0].wait == 0):
			p = waiting.pop(0)
			p.wait = time
			queue.append(p)

		
		time += 1

'''
#	Shortest Job First with Preemption algorithm
# Takes in a list of processes and puts them into a que to run
def	SJFP( processes, time ):'''


# Round Robin algorithm
# Takes in a list of processes and puts them into a que to run
def RR( processes):
	# Put all processes in Queue
	queue = []
	for process in processes:
		queue.append(process)
		pType = ""
		if process.inter:
			pType = "Interactive"
		else:
			pType = "CPU-bound"
		printProcess(0, 1, process)

	totalTime = 0											#This is the total time spent on the operation
	while len(queue) > 0:									#While there are active processes run
		for process in queue:								#Each Round Robin loop
			timeDifference = process.time-process.turn
			if timeDifference > timeLimit:
				process.turn +=timeLimit
				totalTime += timeLimit;
			else:
				process.turn = process.time
				totalTime += timeDifference;
				queue.remove(process)
				printProcess(totalTime, 4, process)


#	Preemptive Priority alorithm
# Takes in a list of processes and puts them into a que to run
#NOTE Current Implmentation is not preemptive
def PP( processes, time ):
	# Put all processes in Queue
	queue = []
	for p in processes:
		queue.append(p)
	# Sort the list by the completion time
	queue.sort(key=operator.attrgetter('priority'))
	for p in queue:
		printProcess(0,1,p)
	# Simulate processing
	time = 0
	while len(queue) != 0:
		p = queue.pop(0)
		p.wait = time
		time += p.time
		p.turn = time
		printProcess(time,4,p)


# Function to incrememnt the times for the process in the queue
def inc( processes ):
	for p in processes:
		turn += 1


#	Simulate takes in 2 parameters and runs simulates all scheduling algorithms
#		int m = number of CPUs. Should be be 1 or 4
#		int n = number of Processes. The default value is 12
'''def simulate( m, n ):

'''

def main():
	# Just some test stuff
	processes = []
	for pid in range(1,13):
		q = random.randint(1,101)
		if q < 21:
			processes.append(process(pid,random.randint(200,3001),8,False))
		else:
			processes.append(process(pid,random.randint(20,201),1,True))
	SJFN(processes)

if __name__ == '__main__': 
	#First arguement is number of cores, m, Second is number of processes ran, n, third is time limit, time
	skip = 1;
	for arguement in sys.argv:
		if skip == 1:
			skip = 0
		elif arguement[0] == 'm' and len(arguement)>2:
			m = int(arguement[2:len(arguement)])
		elif arguement[0] == 'n' and len(arguement)>2:
			n = int(arguement[2:len(arguement)])
		elif arguement[0:4] == "time" and len(arguement)>5:
			timeLimit = int(arguement[5:len(arguement)])
		pass

	main()