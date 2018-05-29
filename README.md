# Game of Thrones Data Visualisation: "The Timeline of Ice and Fire"

*A narrative of character changes across episodes in Game of Thrones TV series*

### Vaporwave Group
* Rahul Anand 
* Priyanka Sawant 
* Itay Feldman
* Dan Kennedy

> Game of Thrones is an epic series, with a vast cast and sprawling plotline. This visualisation encapsulates the entire saga: the rise and fall of characters, families and houses, the pivotal quotes and the gruesome means of death. 
Drawing from an API of Ice and Fire (anapioficeandfire.com), as well as publicly available imdb data and web pages, the application creates new connections between detailed character data and information on the TV series. 

### To run the application:

The application runs on four servers, which each provide data to the application via a custom REST api. 

Run the servers with:

* In the **imdb folder**: ``python3 run.py``

* In the **IaF folder**: ``python3 run.py``

* In the **images folder**: ``python3 main.py``

* In the **analytics folder**: ``python3 main.py``

Then run the main application 

* In the **ui folder**: ``python3 -m http.server``






