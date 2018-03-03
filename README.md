Introduction

This tool allows a user to cut an object out of one image and paste it into another.  The tool helps the user trace the object by providing a "live wire" that automatically snaps to and wraps around the object of interest.  


Description

This program is based on the paper Intelligent Scissors for Image Composition, by Eric Mortensen and William Barrett, published in the proceedings of SIGGRAPH 1995.  The way it works is that the user first clicks on a "seed point" which can be any pixel in the image.  The program then computes a path from the seed point to the mouse cursor that hugs the contours of the image as closely as possible.  This path, called the "live wire", is computed by converting the image into a graph where the pixels correspond to nodes.  Each node is connected by links to its 8 immediate neighbors.  Note that we use the term "link" instead of "edge" of a graph to avoid confusion with edges in the image.  Each link has a cost relating to the derivative of the image across that link.  The path is computed by finding the minimum cost path in the graph, from the seed point to the mouse position.  The path will tend to follow edges in the image instead of crossing them, since the latter is more expensive.  The path is represented as a sequence of links in the graph. 

Cost Function

The cost function we use here is a bit different than what's described in the paper. The image is represented as a graph.  Each pixel (i,j) is represented as a node in the graph, and is connected to its 8 neighbors in the image by graph links (labeled from 0 to 7), as shown in the following figure. To simplify the explanation, let's first assume that the image is grayscale instead of color (each pixel has only a scalar intensity, instead of a RGB triple) as a start. The same approach is easily generalized to color images.
Computing cost for grayscale images
Among the 8 links, two are horizontal (links 0 and 4), two are vertical (links 2 and 6), and the rest are diagonal. The magnitude of the intensity derivative across the diagonal links, e.g. link1, is approximated as:

D(link1)=|img(i+1,j)-img(i,j-1)|/sqrt(2)

The magnitude of the intensity derivative across the horizontal links, e.g. link 0, is approximated as:

D(link 0)=|(img(i,j-1) + img(i+1,j-1))/2 - (img(i,j+1) + img(i+1,j+1))/2|/2

Similarly, the magnitude of the intensity derivative across the horizontal links, e.g. ln2, is approximated as:

D(link2)=|(img(i-1,j)+img(i-1,j-1))/2-(img(i+1,j)+img(i+1,j-1))/2|/2.

We compute the cost for each link, cost(link), by the following equation:

cost(link)=(maxD-D(link))*length(link)


where maxD is the maximum magnitude of derivatives across links over in the image, e.g., maxD = max{D(link) | forall link in the image}, length(link) is the length of the link. For example, length(link 0) = 1, length(link 1) = sqrt(2) and length(link 2) = 1.  If a link lies along an edge in an image, we expect that the intensity derivative across that link is large and accordingly, the cost of link is small. 

Cost for an RGB image

As in the grayscale case, each pixel has eight links. We first compute the magnitude of the intensity derivative across a link, in each color channel independently, denoted as 

( DR(link),DG(link),DB(link) ). 

Then the magnitude of the color derivative across link is defined as

D(link) = sqrt( (DR(link)*DR(link)+DG(link)*DG(link)+DB(link)*DB(link))/3 ).

Then we compute the cost for link link in the same way as we do for a gray scale image:

cost(link)=(maxD-D(link))*length(link).

Notice that cost(link 0) for pixel (i,j) is the same as cost(link 4) for pixel (i+1,j). Similar symmetry property also applies to vertical and diagonal links.

Computing the Minimum Cost Path

The pseudo code for the shortest path algorithm in the paper is a variant of Dijkstra's shortest path algorithm, which is described in any of the classic algorithm books (including text books used in data structures courses like 271). Here is some pseudo code which is equivalent to the algorithm in the SIGGRAPH paper, but we feel is easier to understand.

procedure LiveWireDP
input: seed, graph 

output: a minimum path tree in the input graph with each node pointing to its predecessor along the minimum cost path to that node from the seed.  Each node will also be assigned a total cost, corresponding to the cost of the the minimum cost path from that node to the seed. 

comment: each node will experience three states: INITIAL, ACTIVE, EXPANDED sequentially. the algorithm terminates when all nodes are EXPANDED. All nodes in graph are initialized as INITIAL. When the algorithm runs, all ACTIVE nodes are kept in a priority queue, pq, ordered by the current total cost from the node to the seed. 

    Begin:

      initialize the priority queue pq to be empty;
      initialize each node to the INITIAL state;
      set the total cost of seed to be zero and make seed the root of the minimum path tree ( pointing to NULL ) ;
      insert seed into pq; 

      while pq is not empty 

        extract the node q with the minimum total cost in pq;
        mark q as EXPANDED; 

        for each neighbor node r of q  

          if  r has not been EXPANDED

            if  r is still INITIAL

              make q be the predecessor of r ( for the the minimum path tree );

              set the total cost of r to be the sum of the total cost of q and link cost from q to r as its total cost;

              insert r in pq and mark it as ACTIVE;

            else if  r is ACTIVE, e.g., in already in the pq 

              if the sum of the total cost of q and link cost between q and r is less than the total cost of r

                update q to be the predecessor of r ( for the minimum path tree );

                update the total cost of r in pq;

    End

