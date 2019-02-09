# Item Catalog

### Project Overview
> You will develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

Source of project overview is from Udacity's [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

### Why This Project?
> Modern web applications perform a variety of functions and provide amazing features and utilities to their users; but deep down, it’s really all just creating, reading, updating and deleting data. In this project, you’ll combine your knowledge of building dynamic websites with persistent data storage to create a web application that provides a compelling service to your users.

Source of why this project is from Udacity's [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

### What Will I Learn?
> You will learn how to develop a RESTful web application using the Python framework Flask along with implementing third-party OAuth authentication. You will then learn when to properly use the various HTTP methods available to you and how these methods relate to CRUD (create, read, update and delete) operations.

Source of what will I learn is from Udacity's [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

### How to Run?

#### PreRequisites
  * [Python ~2.7](https://www.python.org/)
  * [Vagrant](https://www.vagrantup.com/)
  * [VirtualBox](https://www.virtualbox.org/)

#### Setup Project:
1. Install Vagrant and VirtualBox
2. Download or Clone [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository.
3. Find the catalog folder and replace it with the content of this current repository, by either downloading or cloning it from
[Here](https://github.com/dgethner/Item-Catalog).


#### Starting The Application
  1. Launch your terminal
  2. Change directory into the following file path on your computer
  > fullstack-nanodegree-vm-master/vagrant/catalog

  3. Run the following command to set-up for your VM
  ```
    $ vagrant up
  ```
  4. Run the following command to login to your VM
  ```
    $ vagrant ssh
  ```
  5. Change directory in your VM to the catalog folder
  ```
    $ cd /vagrant/catalog
  ```
  6. Run the following command to populate the database
  ```
    $ python lotsofcars.py
  ```
  7. Run the following command to run the application
  ```
    $ python catalog.py
  ```
  8. Access and test your application by visiting [http://localhost:8000](http://localhost:8000).

### How to Access API Endpoints

* Return JSON for all the Car Types
> http://localhost:8000/cartype/JSON
* Return JSON of all the Models for a Car Type (change carType_id as needed)
> http://localhost:8000/cartype/<int:carType_id>/JSON
* Return JSON for all Car Models
> http://localhost:8000/item/JSON
* Return JSON for a Car Model (change carType_id & model_id as needed)
> http://localhost:8000/cartype/cartype/<int:carType_id>/item/<int:model_id>/JSON
