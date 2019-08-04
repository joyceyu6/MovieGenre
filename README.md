# MovieGenre Application on Linux Server - User Manual
## Project Description
The purpose of the project was to take a Ubuntu Linux server instance on `Amazon Lightsail` to host my existing web application . The server was secured from a number of attack vectors, a database server (`PostgreSQL`) was installed and configured, and my existing web application (`MovieGenre` from the `Catalog` project) was deployed onto it.

## How to run the web application
Type in below IP address or URL in your web browser:
### IP address 
[http://54.244.56.151](http://54.244.56.151)

### URL 
[54.244.56.151.xip.io](54.244.56.151.xip.io)

## SSH log into server from client terminal:
A superuser named `grader` was created and can access server with the private key submitted with this project. For example, below command in shell can get myself login as `grader`:
```shell
ssh grader@54.244.56.151 -p 2200 -i ~/.ssh/grader_private_key
```


## Summary of software installed
* Installed `git`
  ```shell 
  git initi
  ```

* Installed `flask`
  ```shell
  sudo -H pip install flask
  ```
* Installed `oauth2client`
  ```shell 
  sudo -H pip install oauth2client
  ```
* Installed `requests`
  ```shell
  sudo -H pip install requests
  ```
* Installed `sqlalchemy`
  ```shell
  sudo -H pip install sqlalchemy

* Installed `Postgre` related libraries
  ```shell
  sudo apt-get install  postgresql-server-dev-10
    ```
  ```shell
  sudo -H pip install psycopg2
  ```

## Summary of configurations made
* All currently installed packages were listed and updated with below command:
  ```shell 
  sudo apt-get update
  ```
  ```shell 
  sudo apt-get upgrade
  ```
* Changed the SSH port from 22 to 2200
*  Configured the Uncomplicated Firewall (`UFW`) to only allow incoming connections for `SSH` (port 2200), `HTTP` (port 80), and `NTP` (port 123)
*  Created a new user account named `grader` with `sudo` permission
*  Created an SSH key pair for `grader` using the `ssh-keygen` tool
*  Configured the local local timezone to `UTC`
*  Installed and configured Apache to serve a `Python` `mod_wsgi` application
*  Configured Apache to handle requests using the `WSGI` module
*  Installed and configured `PostgreSQL`
*  Create a new database user named `catalog` that has limited permissions to my  application database
   *  Database user `catalog` is not a superuser, neither can it create more roles
*  Created `catalogdb` database


## List of third-party resources 
* [Configuring Linux Web Servers](https://classroom.udacity.com/courses/ud299) course from Udacity

* [How To Install and Use PostgreSQL on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04)

## Addtional notes
- Because HTTPS (port 443) was closed per project requirement, `Facebook login` function does not work any more