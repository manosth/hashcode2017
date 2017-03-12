# Google Hashcode 2017 Online Qualification Round
This code was developed by the team Veni Vidi Vsync during the Online Qualification Round of Google Hashcode 2017.
The members of the team are:
  - <a href="https://github.com/manosth">Emmanouil Theodosis</a>
  - <a href="https://github.com/abenetopoulos">Achilles Benetopoulos</a>
  - <a href="https://github.com/YannisSach">Yannis Sachinoglou</a>
  - Andreas Maggiori

Our approach, although very simple, ranked fairly well: our team ranked #170 on a worlwide scale from 2815 participating teams, and #3 on a national scale.
<br>
<br>
The problem PDF is included in the repo, as well as the input files and the output files produced by our code (since one test case, 'kittens.in', takes quite a while to produce an output).
<br>
<br>
Also included some visualizations of how our code performed in each of the test cases, highlighting the connections between the endpoints, the cache servers, and the datacenter, as well as the hit rate of each cache.

## Problem Formulation
We are given cache servers, users (endpoints), videos, and requests that the users make to watch specific videos. We are also given relations between users and cache servers: which user is connected with which cache servers.
<br>
<br>
When a video is transfered to a user from the datacenter, there is a significant delay. However, if that video is stored in a cache server that the user has access to, that delay is shorter. 
<br>
<br>
With this information, we are required to find ways to select which videos to store to the caches, in order to minimize the total delay (or maximize the time saved) of satisfying every request of the users.

## Idea Roadmap
To solve this problem, we decided to create a list of requests made to caches. However, a user makes a request for a video, regardless of which cache satisfies that request. This means that, for each request a user has, there are going to be C entries in our list, where C is the number of caches that the user is connected to. 
<br>
<br>
However, note that we need to <b>aggregate</b> the number of requests for this video. This is because a single user might make 2000 requests for a video, and 4 other users might make 1000 requests each for another video. If we don't aggregate the number of requests, then the first request will be satisfied, even though storing the second video will lead to better results.
<br>
<br>
After that list is constructed, we sort the list, and we start satisfying requests until we exhaust the list.

## Implementation
As an implementation language we chose Python. Python is an excellent choice for hackathons because of its simplicity, which makes implementation very easy and fast, allowing you to test more approaches. The code is fairly well-documented, with comprehensive names to aid in understanding. There are also several comments that aim to help readers understand the process.
