import sys

input_file = open(sys.argv[1], 'r')

line = input_file.readline()
split_line = line.split()

# V is the number of videos
# E the number of endpoints
# R the number of requests
# C the number of caches
# X the capacity of each cache
V = int(split_line[0])
E = int(split_line[1])
R = int(split_line[2])
C = int(split_line[3])
X = int(split_line[4])

sizes = []
line = input_file.readline()
sizes = map(int, line.split())

# For each endpoint, we are going to have an entry with the endpoint
# ID, the latency to the datacenter, and a list of the latencies to
# each of the caches that the endpoint connects to
endpoints = []
for idx in xrange(E):
    line = input_file.readline().split()
    latency_to_datacenter = int(line[0])
    number_of_caches = int(line[1])
    caches_latencies = []
    for jdx in xrange(number_of_caches):
        line = input_file.readline().split()
        cache_id = int(line[0])
        cache_latency = int(line[1])
        caches_latencies.append((cache_id, cache_latency))
    endpoints.append((idx, latency_to_datacenter, caches_latencies))

# These will be used later to aggregate the total saved time for each
# video
requests = {}
requests_for_video = {}
for idx in xrange(V):
    requests_for_video[idx] = {}
    for jdx in xrange(C):
        requests_for_video[idx][jdx] = (0, [])

for idx in xrange(E):
    requests[idx] = []

# We are going to group the requests by endpoints. So, each request gets appointed
# to the corresponding endpoint. For each request, we are going to have an entry
# with the video ID, the number of requests for the video, and an increasing ID
# that will be used later to track the requests
for idx in xrange(R):
    line = input_file.readline().split()
    endpoint_id = int(line[1])
    video_id = int(line[0])
    number_of_requests = int(line[2])
    requests[endpoint_id].append((video_id, number_of_requests, idx))

caches = {}
for idx in xrange(C):
	caches[idx] = []

# For each cache server, we are going to have a list with the endpoints that
# connect to the cache, along with the gain for each endpoint
for endpoint in endpoints:
    endpoint_id = endpoint[0]
    datacenter_latency = endpoint[1]
    endpoint_cache_list = endpoint[2]
    for cache in endpoint_cache_list:
        cache_id = cache[0]
        cache_latency = cache[1]
        gain = datacenter_latency - cache_latency
        caches[cache_id].append((endpoint_id, gain))

# We are going to create the list of the requests to the caches. To do that,
# we are going to go through each of the caches, go through each of the endpoints
# that connect to that cache, and then go through each of the requests associated
# with that endpoint. Then, we will update the total saved time by storing
# that video to the cache, and the IDs of the requests for that video
cache_requests = []
for cache_id, endpoints in caches.iteritems():
    for endpoint in endpoints:
        endpoint_id = endpoint[0]
        endpoint_requests = requests[endpoint_id]
        for request in endpoint_requests:
            video_id = request[0]
            number_of_requests = request[1]
            time_saved = endpoint[1]
            request_id = request[2]
            previous_time_saved, previous_requests = requests_for_video[video_id][cache_id]
            new_time_saved = previous_time_saved + number_of_requests * time_saved
            new_requests = previous_requests + [request_id]
            requests_for_video[video_id][cache_id] = (new_time_saved, new_requests)

# Create the final list where we store the cache ID, the IDs of the requests,
# the total saved time, and the video ID
for video_id, requests in requests_for_video.iteritems():
    for cache_id, request in requests.iteritems():
        time_saved = request[0]
        requests_ids = request[1]

        # Check whether the list of requests IDs is empty
        if (requests_ids):
            cache_requests.append((cache_id, requests_ids, video_id, time_saved))

# We are going to sort the list in descending order based on the metric
# that we are being graded, which is the number of seconds saved normalized
# by the video size
sorted_list = sorted(cache_requests, key = lambda request: request[3] / (1.0 * sizes[request[2]]), reverse = True)

# A logical array to keep track of which requests have been fullfiled
satisfied_requests = {}
for idx in xrange(R):
    satisfied_requests[idx] = 0

# Initialize all the caches to the initial size
cache_sizes = {}
for idx in xrange(C):
    cache_sizes[idx] = X

# We'll now create a list with the videos that should be stored to
# each cache
results = set([])
for cache_request in sorted_list:
    cache_id = cache_request[0]
    requests_ids = cache_request[1]
    video_id = cache_request[2]
    video_size = sizes[video_id]

    # If the request has not been satisfied and the video can be stored to the cache
    if (satisfied_requests[requests_ids[0]] == 0) and (cache_sizes[cache_id] - video_size >= 0):
        cache_sizes[cache_id] -= video_size
        for request_id in requests_ids:
            satisfied_requests[request_id] = 1
        results.add((cache_id, video_id))

# We'll use a dictionary to help us write the results to a file
output = {}
for idx in xrange(C):
	output[idx] = []

for result in results:
	cache_id = result[0]
	video_id = result[1]
	output[cache_id].append(video_id)

# We'll simply count the number of cache servers used. This is required
# for the output formatting
count = 0
for cache_id in output.keys():
	cache_videos = output[cache_id]

    # Check whether the list of videos is empty
	if cache_videos:
		count = count + 1

# Write the results in the file "output_" + the name of the input file
output_file = open("output_" + sys.argv[1] + ".txt", 'w')
output_file.write(str(count) + "\n")
for cache_id in output.keys():
    cache_videos = output[cache_id]

    # Check whether the list of videos is empty
    if cache_videos:
        cache_string = str(cache_id)
        for video_id in cache_videos:
            cache_string += ' ' + str(video_id)
        output_file.write(cache_string + "\n")
