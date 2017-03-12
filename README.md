# Google Hashcode 2017 Online Qualification Round
This code was developed by the team Veni Vidi Vsync during the Online Qualification Round of Google Hashcode 2017.
The members of the team are:
  - <a href="https://github.com/manosth">Emmanouil Theodosis</a>
  - <a href="https://github.com/abenetopoulos">Achilles Benetopoulos</a>
  - <a href="https://github.com/YannisSach">Yannis Sachinoglou</a>
  - Andreas Maggiori

This approach, although very simple, ranked fairly well: our team ranked #170 on a worlwide scale from 2815 participating teams, and #3 on a national scale.

## Problem Formulation
We are given cache servers, users (endpoints), videos, and requests that the users make to watch specific videos. We are lso given relations between users and cache servers: which user is connected with which cache servers. When a video is transfered to a user, there is a delay. However, if that video is stored in a cache server, that delay is shorter. With this information, we are required to find ways to select which videos to store to the caches, in order to minimize the total delay (or maximize the time saved).

## Idea Roadmap
To solve this problem, we decided to create a list of requests made to caches. However, a user makes a request for a video, regardless of which cache satisfies that request. This means that, for each request a user has, there are going to be C entries in our list, where C is the number of caches that the user is connected to. 
However, note that we need to <b>aggregate</b> the number of requests for this video. This is because a single user might make 2000 requests for a video, and 4 other users might make 1000 requests each for another video. If we don't aggregate the number of requests, then the first request will be satisfied, even though storing the second video will lead to better results.

After that list is constructed, we sort the list, and we start satisfying requests until we exhaust the list.

## Implementation
As an implementation language we chose Python.
