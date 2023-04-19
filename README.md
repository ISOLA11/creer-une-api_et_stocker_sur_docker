1 - Create some graph for RATP dataset
For this question, you need to use the first dataset (the one from RATP).

Objective
Create a bar chart that represents the TOP 10 stations with the biggest traffic
Create a Pie chart that represents trafic per cities (to make it clear, you can take only the TOP 5)
Organize those two chart on the same row (they have to be side by side)
2 - Create some graph for IDF dataset
For this question, you need to use the first dataset (the one from IDF).

Objective
Create a bar chart that represents the number of stations per exploitant
Create a chart that represents the number of stations per ligne
3 - Add some global filters
Add some global filter to your dashboard, use some dropdown selection filter.
Objective
One filter for réseau (field from the RATP dataset)
One filter for exploitant (field from the IDF dataset)
4 - Create an interactive map
In the second dataset, you have many ways to retrieve latitude and longitude, however, you don't have explicit columns lat & lon (or anything similar). 
Objective
Add a Map to your dashboard to visualize the position of the stations.

5 - Containerize your plotly dash application
Objective
Create a Dockerfile in which you define how the docker image must be build in order to run your application
Build your docker image : docker build -t your_image .
Run a container : be careful you need to expose port 8050 which is the port used by plotly dash