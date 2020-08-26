<h1>Threaded KMeans - Jython</h1>
<h2>Introduction</h2>
<p>
<a href="https://www.jython.org">Jython</a> is the Java implementation of Python. One advantage of Jython over CPython is

the lack of the <a href="https://wiki.python.org/moin/GlobalInterpreterLock">Global Interpreter Lock</a> (GIL) and thus can fully
exploit multiprocessor systems. Threading in Jython is super easy, just follow the steps:
<ol>
	<li>Import the Thread module from threading</li>
	<li>sub-class Thread</li>
	<li>Override the run function from Thread</li>
	<li>Create an instance of the class</li>
	<li>Call start()</li>
</ol>
</p>

<p>
Congratuations, you are now multithreading in Jython! Admittedly sometimes there's more than that, but that is the basic gist.
But seriously, threading in Jython is nice. I've had instances where I've cut run times of programs from 30+ minutes to under 2 mintues.
(One specific example involved searching through millions of items and then logging attributes to a database.)
</p>

<p>
One drawback of the Jython is that most packages are made for CPython. In particular, there is no pandas, numpy, or scikit learn.
However, in my experience working on very specialized problems, there is often a need to develop a large portion of your own
algorithms from scratch. Usually this arises because of some special case or because general algorithms do not give the control needed.
</p>
<h2>Basics of the Program</h2>
<p>
When devising a multithreaded program, a very challenging portion of programming is deciding how to break the work up into threads. In other
words, thinking of the best way to break the program into smaller pieces.
</p>

<p>
The part of KMeans that takes the most amount of time is evaluating all the points against new centroids and then assigning the points to the new
cluster. One key observation is that evaluating one point against all the centroids has no bearing on evaluating a different point against all the centroids.
I.e., evaluating points against centroids can be done <i>independently</i>.
</p>

<p>
The second challenging part of multithreading is deciding how to merge all the threads together. 
Our threaded kmeans will assign the cluster to which each point belongs.
Once all the threads have finished, all we have to do is merge the clusters.
Once we have the clusters merged together, we calculate new centroids, and then keep repeating until the centroids stop moving or reach the maximum number
of iterations.
</p>
<h2>Code Highlights</h2>
<p>
We first start by importing the Thread module from threading. We will also use the square root function from math, so import that package as well.
We also import random since we use random.sample to get starting random centroids.
</p>

<p>
The ComputeDistances class subclasses Thread. This class will be a thread, and will be our workhorse for the KMeans algorithm.
One way to use thre Thread module is override the run function. When an instance of ComputeDistances calls the function start(), it starts the run() function.
Notice that it is not start() that is overridden, but run. Inside the run function we define what work we want to do.
I usually reserve this space for calls to other functions as opposed to writing everything inside run() to make the code easiers to follow.
Each ComputeDistances will take a portion of the global name points. There's usually a point in which adding more threads doesn't make the program any faster, and
I wish I had a fail-safe way of getting the magic number of threads needed to maximize the speed of programs.
Trial and error seems to work best, as it will differ (often wildly) between systems. (I've used anywhere between 4 and 50 threads.)
The number of threads in the program is not dependent on the number of clusters desired.
</p>

<p>
One thing to note is that each thread is accessing the global list points. This might be causing
some sychronization across the threads and may cause added overhead.
Another option would be to pass a copy of the points to each thread. But this has the drawback of 
taking more memory. 
</p>
