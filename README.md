# Item Catalog

[Udacity Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044)

## Table of Contents

- [Project Overview](#project-overview)
- [Description](#description)
- [Technologies](#technologies)
- [Repository Data](#repository-data)
- [Installation](#installation)
- [How To Run](#how-to-run)
- [Highlights](#highlights)

## Project Overview

The Item Catalog project consists of developing an application that provides a list of items within a variety of categories, as well as provides a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Description

This is a book rental application that has the book genres listed as categories and books under each genre are listed as items. A book item contains a detailed description along with price and availabilty status of the item.
It provides login and logout funcationality for a user. An authenticated user can add, delete and update a book item.
A catalog json endpoint is provided to access the list of categories and items in json fromat. 

## Technologies

- Python 3
- Flask Framework
- Google OAuth2.0
- CSS
- JQuery
- Bootstrap 5

## Repository Data

- [static](static)
  - [img](static/img): Contains images used in the application.
  - [style.css](style.css): Custom css file.
- [template](templates): HTML webpage templates.
- [.gitignore](.gitignore): Contains files to exclude from commits.
- [app.py](app.py): Main python backend application file.
- [db_setup.py](db_setup.py): Python file to setup the db.
- [populate_db_data.py](populate_db_data.py): Python file to populate the db.
- [README.md](README.md): Project Documentation file.

## Installation
As a prerequisite, installation steps are provided by udacity.

- #### Install VirtualBox and Vagrant
  Install VirtualBox from virtualbox.org to run a virtual machine. Install Vagrant to configure the VM.
  I have used VirtualBox-6.0.14 version with Vagrant-2.2.6 version.

- #### VM configuration
  Follow the Vagrant virtual machine configuration from [Udacity virtual machine configuration](https://github.com/udacity/fullstack-nanodegree-vm) to start and ssh into virtual   machine.

## How To Run

- #### Generate Google Authentication Credentials
  - Login to the [Google Cloud Platform Console](https://console.cloud.google.com/apis/credentials).
  - Create a new project with any name ex- Item Catalog Application.
  - Under Create Credentials select OAuth Client ID
  - Configure Consent Screen before proceeding
  - In Create Credentials provide Application Type as `Web Application`
  - Add `http://localhost:5000` under Authorized JavaScript origins and Authorized Redirect URIs.
  - Download the JSON file for credentials and put it inside app directory after renaming to `client_secrets.json`.

- #### RUN Application
  - Create the database: `python3 db_setup.py`
  - Populate the data in database: `python3 populate_db_data.py`
  - Run the application: `python3 app.py`
  - Access http://localhost:5000 in browser

## Highlights
- Since Google+ is deprecated, google authentication code from instructor notes did not work for me.
  I used the solution from [Udacity Knowledge Hub](https://knowledge.udacity.com/questions/43336)
