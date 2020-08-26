<h1>Threaded KMeans - Jython</h1>
<h2>Introduction</h2>
[Jython](https://www.jython.org) is the Java implementation of Python. One advantage of Jython over CPython is
the lack of the [Global Interpreter Lock](https://wiki.python.org/moin/GlobalInterpreterLock) (GIL) and thus can fully
exploit multiprocessor systems. Threading in Jython is super easy, just follow the steps:
<ol>
	<li>Import the Thread module from threading</li>
	<li>sub-class Thread</li>
	<li>Override the run function from Thread</li>
	<li>Create an instance of the class</li>
	<li>Call start()</li>
</ol>
Congratuations, you are now multithreading in Jython! Admittedly sometimes there's more than that, but that is the basic gist.
But seriously, threading in Jython is nice. I've had instances where I've cut run times of programs from 30+ minutes to under 2 mintues.
(One specific example involved searching through millions of items and then logging attributes to a database.)

One drawback of the Jython is that most packages are made for CPython. In particular, there is no pandas, numpy, or scikit learn.
However, in my experience working on very specialized problems, there is often a need to develop a large portion of your own
algorithms from scratch. Usually this arises because of some special case or because general algorithms do not give the control needed.
<h2>Basics of the Program</h2>
When devising a multithreaded program, a very challenging portion of programming is deciding how to break the work up into threads. In other
words, thinking of the best way to break the program into smaller pieces.

The part of KMeans that takes the most amount of time is evaluating all the points against new centroids and then assigning the points to the new
cluster. One key observation is that evaluating one point against all the centroids has no bearing on evaluating a different point against all the centroids.
I.e., evaluating points against centroids can be done <i>independently</i>.

The second challenging part of multithreading is deciding how to merge all the threads together. 
Our threaded kmeans will assign the cluster to which each point belongs.
Once all the threads have finished, all we have to do is merge the clusters.
