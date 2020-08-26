from threading import Thread
import time
import random
import math

start_time = time.time()

number_of_threads = 12


class KMeansError(Exception):
    pass


class ComputeDistances(Thread):
    def __init__(self, thread_number, centroids, t_points):
        Thread.__init__(self)
        self.centroids = centroids
        self.thread_number = thread_number
        self.thread_clusters = [[] for i in range(len(centroids))]
        self.am_i_still_running = True
        self.t_points = t_points
		
    def run(self):
        self.get_distances()
        self.am_i_still_running = False
		
    def get_distances(self):
        for point in self.t_points:
            #get the first distance
            d_0 = self.distance(point, self.centroids[0])
            min_j = 0
            #iterate over the remaining centroids to find which the point belongs
            for j, c in enumerate(self.centroids[1:], 1):
                d = self.distance(point, c)
                if d < d_0:
                    d_0 = d
                    min_j = j 
            self.thread_clusters[min_j].append(point)
	
    def am_i_alive(self):
        return self.am_i_still_running
			
    def distance(self, p, c):
        #define your own distance function here
        #The line below would be used for 1-dimensional data
        #return abs(p-c)
        return math.sqrt( (p[0]-c[0])**2 + (p[1]-c[1])**2)

    def kill(self):
        self.EXIT = True
		
		
class KMeans:
    def __init__(self, number_of_clusters, max_iter, tolerance, number_of_threads=-1):
        self.number_of_clusters = number_of_clusters
        self.max_iterations = max_iter
        self.tolerance = tolerance
        self.centroids = []
        self.new_centroids = []
        self.clusters = [[] for i in range(number_of_clusters)]
        self.number_of_threads = number_of_threads
        if number_of_threads <= 0:
            self.number_of_threads = number_of_clusters
		
    def initialize_centroids(self):
        """
        This uses the random sample method; it would be easy to change what happens in this method. Just
        make sure that self.centroids is set
        """
        temp_point_list = []
        for t_points in point_list:
            temp_point_list += t_points
        if self.number_of_clusters < len(temp_point_list):
            self.centroids = random.sample(temp_point_list, self.number_of_clusters)
        else:
            raise KMeansError
			
    def calculate_centroid(self, cluster):
        #The following three lines make sense when working with 1-dimensional data
        #if len(cluster) > 0:
        #	return sum(cluster)/len(cluster)
        #return 0
        if len(cluster) > 0:
            sum_x = sum(x[0] for x in cluster)
            sum_y = sum(x[1] for x in cluster)
            return (sum_x/float(len(cluster)), sum_y/float(len(cluster)))
        return 0
		
    def get_error(self, old_centroid, new_centroid):
        #The line below would be used for 1-dimensional data
        #return abs(old_centroid - new_centroid)
        return math.sqrt( (old_centroid[0] - new_centroid[0])**2 + (old_centroid[1] - new_centroid[1])**2)
		
    def get_clusters(self):
        self.initialize_centroids()
        self.new_centroids = self.centroids[:]
        for i in range(self.max_iterations):
            #make a new list for all the threads
            threads = []
            #make new clusters
            self.clusters = [[] for i in range(self.number_of_clusters)]
            for i in range(self.number_of_threads):
                cd = ComputeDistances(i, self.centroids, point_list[i])
                cd.start()
                threads.append(cd)
            #We keep looping until all the threads have finished.
            #We really should error check in the ComputeDistances class; or we could
            #set a time for computations and then kill the threads if time limit exceeded.
            #Use the cd.kill() to exit the thread and then raise an error.
            #Also note that we could use while any([t.is_alive() for t in threads]), however,
            #sometimes between the time it takes to start a thread and checking if it is alive
            #is too fast. I.e., it will give a False before it's even started and the code
            #will advance thinking that the thread has already computed what it needed.
            while any([t.am_i_alive() for t in threads]):
                pass
            #Once all the threads have finished, join the clusters together.
            for t in threads:
                for i, cluster in enumerate(t.thread_clusters):
                    self.clusters[i] = self.clusters[i] + t.thread_clusters[i]
            errors = []
            #With the new clusters, calculate new centroids and get errors.
            for i, cluster in enumerate(self.clusters):
                self.new_centroids[i] = self.calculate_centroid(cluster)
                errors.append(self.get_error(self.centroids[i], self.new_centroids[i]))
                self.centroids[i] = self.new_centroids[i]
            #If the maximum error is less than our tolerance, we have our solution.
            if max(errors) < self.tolerance:
                return self.clusters
        return self.clusters
			

"""
It is not necessary to open a CSV; this is done as an example for getting points
to perform k-means clustering.
The csv was taken from: https://www.analyticsvidhya.com/blog/2019/08/comprehensive-guide-k-means-clustering/
"""
import csv
point_list = [[] for x in range(number_of_threads)]
point_count = 0
with open('./clustering.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            #points.append([float(row[6]), float(row[8])])
            point_list[point_count].append([float(row[6]), float(row[8])])
            point_count = (point_count + 1) % number_of_threads
        line_count += 1
#Takes less than 0.06s on average to finish
kmeans = KMeans(3, 20, 0.001)
kmeans.get_clusters()
print(kmeans.centroids)
end_time = time.time()
print(end_time - start_time)
