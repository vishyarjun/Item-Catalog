# Item Catalog

This project is a **Car Sales** item catalog website that list out cars from various brands/categories available for sale along with its details. Logged In users can Add, Edit, Delete Car for sales.
## Design
1. This projects makes use of following tables
    **Tables**
          - sales_categories - contains all the categories/brands of cars available for sale
           - sales_items - lists all the cars available for sale with price
           - user_details - stores all logged in user details
2. The websites consists of a Home page where any user can view all the cars listed and available for sales
3. A list of categories/ brands are available below the Home Tab
4. Clicking on each brand/category list out all the cars that belongs to the category
5. A user needn't login to view all the details
6. To add, edit or delete an item, a user must be logged in
7. To login, Clik Login button on the right top and Login with facebook
8. A logged in user needs to select a particular category inorder to add, edit and delete an item
9. Once a category is selected, Add button will be available on the right top of the page
10. Edit Item and Delete Item button will be only visible for the items that has been created by the same user.
11. For the item created by different user, edit item and delete item will not be visible.
12. **JSON End Points**
    - To view JSON end point clik on a particular category and add `/JSON` to the URL
### Pre-Requirements
1. Linux VM with vagrant. [Click here if not installed](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)
2. News Tables needs to be loaded. Implement the following steps if not already installed
    - [Click here to download](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
    - After downloading, unzip and place the `newsdata.sql` inside vagrant.
    - run the command `psql -d news -f newsdata.sql` and load the data.
3. Create a githib account and Install git in the local machine. [Click here, if not already installed](http://product.hubspot.com/blog/git-and-github-tutorial-for-beginners)
## Installation Steps
1. Fork the github repository. The original repository can be found [here](https://github.com/vishyarjun/Item-Catalog.git)
2. Open Terminal and change directory to Vagrant
3. Clone it to local repository using  `git clone <fork repository url>`
6. Run `vagrant up` and `vagrant ssh`
6. Run the command `cd /vagrant/Item-Catalog`
7. Run `python database_setup.py`
8. Run `python lotofitems.py`
### FAQ
1. __How do I run the project?__
 - Run `python application.py`
 - Verify if the local host is up and running
 - Open a web browser
 - type `http://localhost:5000/sales`
 - hit enter

### Reference
1 [stackoverflow](www.stackoverflow.com)
2 [W3Schools](https://www.w3schools.com)
3 [SQLAlchemy](http://docs.sqlalchemy.org/en/latest/)
4 [Flask](http://flask.pocoo.org/docs/0.12/)
