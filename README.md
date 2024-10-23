# PROJECT NAME: Demo Credit

**Table of Contents**
- [Project Description / Implementation-Details](#project-description**implementation-details**)
- [API Documentation](#api-docs)
- [E-R Diagram](#e-r-diagram)
- [Installation](#installation)
- [Execution/Usage](#execution--usage)
- [Technologies](#technologies)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [Contributors](#contributors)
- [Author](#author)
- [Change log](#change-log)


## Project Description: 
Demo Credit is a mobile lending app that requires wallet functionality. This is needed as borrowers need a wallet to receive the loans they have been granted and also send the money for repayments.

## Implementation Details
  ### STEP 1: Understanding the project idea
- What is the project about ? 
    You are required to build an MVP wallet service application called Demo Credit.

- What is an MVP ?
    A minimum viable product (MVP) is the release of a new product (or a major new feature) that is used to validate customer needs and demands prior to developing a more fully featured product.

  ### STEP 2: Understanding the project functionality
- What tasks should the project accomplish ?

    The application should be able to carry out the following:
    -   A user can create an account.
    -   A user can fund their account.
    -   A user can transfer funds to another user’s account.
    -   A user can withdraw funds from their account.
    -   A user with records in the Lendsqr Adjutor Karma blacklist should never be onboarded.
    
  ### STEP 3: Considering the requirements
- What are the requirements for this project ?

    The application would benefit greatly from having the following:
    -   A web framework to handle tasks like authentication, routing, serialization etc.
    -   A database/DBMS to store users and all the necessary information.
    -   The Adjutor API is needed in order to implement the Karma blacklist functionality during sign-up.
    
  ### STEP 4: Development approach
-   How can we approach the development of this project ?

    The development of this project is broken down into two major parts:
    -   WEB-APPLICATION DEVELOPMENT (MINIMAL DESIGN SETUP)
    -   API DEVELOPMENT
    
    #### I. WEB-APPLICATION DEVELOPMENT
    I decided to proceed with building out a minimal web application first as i believed it would provide me with a much better understanding of how to go about developing the web API.
    
    A lot of the implementation details where carried out using the Django web framework, which is an extremely high-level, popular and fully featured server-side web framework, written in Python.
    
    The approach taken is outlined as follows:
    
    **DATABASE DESIGN**:
    I started the project by considering the database design in terms of how many database tables I would need and how these tables would be related to one another. I concluded that I would need three seperate database tables named "Users", "Savings" and "Transactions" to store all the necessary data required for the entire application.
    
    The "Users" table would be used to store the information of all the users who successfully signed-up on the platform (the exception being those who were found on the Karma blacklist via the Adjutor API). It would contain fields including (but not limited to) the first name, last name, email address etc.
    
    The "Savings" table would be used to hold all the wallet details of the users on Demo Credit. These details include the first name, last name, account balance and a user-id that points to the owner of the wallet. This simply means that each record/row on the "Savings" table would be linked to a record on the "User" table (via a foreign-key relationship) and represent the wallet of a particular user on the platform.
    
    The "Transactions" table would be used to hold the records of all the transactions that have occurred on the application. Each individual record would contain the details of a particular transaction, the time the transaction took place, as well as the savings-wallet on which that transaction occurred. This simply means that each individual transaction would ensure a foreign-key relationship with a record on the "Savings" table seeing as a savings-record can have more than one transaction records associated with it. This makes sense because in the real-world a savings account in a bank can have multiple transactions associated with it.
    
    The source code for the implementation is located in the "models.py" module of the "wallet" directory in the BASE directory of this application (LENDSQR - same location as this README file).
    
    **FILE PATH** : "LENDSQR/wallet/models.py"
    
    **USER INPUT AND FORMS**:
    I then began to consider how I planned on collecting user data, as well as data-processing and validation. From the sign up process, I knew that I would require the standard user information necessary for validation. This also included asking for an email address which I would then use to verify if the user had already been blacklisted via the Adjutor API. Once these details had been verified and confirmed valid, an account would be created and the user would then be able to log into their newly created account on the platform using those validated credentials.
    
    Once the user is logged in, the next step would be to provide them with a means with which they could create a savings-wallet, as this isn't something that is created automatically upon sign-up. This makes sense because a user shouldn't have a wallet created automatically unless the user really wanted one. I provided the users with two options, one with which they could have a wallet quickly created using their default credentials without much hassle, and another that displays a form with which they could provide custom credentials used to create their wallets.
    
    Once a wallet has been created for a user, they would then be redirected to their homepage where they would have access to different wallet information such as their wallet balance (which has a default value of 0.00 naira upon creation),links to forms for processing funds, and few of their previous transaction details (if any).
    There would be three different button links on the homepage that would enable the user achieve the remaining tasks in step 2 above (Understanding the project functionality), one containing a form for funding user wallets, and the other two for withdrawals and transfers respectively.
    
    The data type of these forms would be restricted to numerical data (specifically decimals) via validation, as this is the recommended data type to use when working with monetary values or currencies.
    
    The source code for the implementation is located in the "forms.py" module of the "wallet" directory in the BASE directory of this application (LENDSQR - same location as this README file).
    
    **FILE PATH** : "LENDSQR/wallet/forms.py"
    
    **URL ROUTES & TEMPLATES**:
    As far as the routes are concerned, each task i.e funding an account, transfers, and withdrawals will all have their own specific url and html-template associated with them. Each template will render the appropriate form needed to carry out the operation. The homepage would be dynamic, containing the appropriate wallet information belonging to the currently logged-in users, as well as a link to a route that displays their past wallet transactions.
    
    The source code for the implementation is located in the "urls.py" module, as well as the "templates" folder of the "wallet" directory in the BASE directory of this application (LENDSQR - same location as this README file).
    
    **URLS FILE PATH** : "LENDSQR/wallet/urls.py"
    
    **TEMPLATES FILE PATH** : "LENDSQR/wallet/templates/wallet"
    
    **TESTS (UNIT AND INTEGRATION)**:
    Last but definitely not least, I will have to test that the core functionality of the application works as expected, including verifying that each form validates the required input, as well as ensuring that all aspects of the application work together as a whole.
    
    The source codes for the implementation (which is divided into three seperate modules) is located in the "tests" folder of the "wallet" directory in the BASE directory of this application (LENDSQR - same location as this README file).
    
    **FILE PATH** : "LENDSQR/wallet/tests"
    
    #### II. API DEVELOPMENT
    Once I had concluded the development of the minimal web application, I proceeded to begin working on the actual web API as I now had a much better understanding of how its implementation should be carried out.
    
    A lot of the implementation details where carried out using the third-party python package called django rest-framework, which is a powerful and flexible toolkit that works hand-in-hand with the django web-framework and is used for building web APIs.
    
    The approach taken is outlined as follows:
    
    **DATABASE DESIGN**:
    The database design for the API is the same as the one for the web application above as they both make use of the same underlying back-end database.
    
    The source code for the implementation is located in the "models.py" module of the "wallet" directory in the BASE directory of this application (LENDSQR - same location as this README file).
    
    **FILE PATH** : "LENDSQR/wallet/models.py"
    
    **AUTHENTICATION**:
    I also implemented a token authentication setup using django rest-framework which ensures that all requests made via API endpoints that require authentication provide a token via the http "AUTHORIZATION" header before they can be granted access to a restricted resource. 
    
    This setting can also be viewed at the bottom of the project's "settings.py" module located in a directory with the same name as the base directory (LENDSQR).
    
    **FILE PATH** : "LENDSQR/LENDSQR/settings.py"
    
    **PERMISSIONS**:
    On a project-level, I implemented an 'AllowAny' permissions setup using django rest-framework which grants unrestricted resource access to non-authorized users via the API.
    
    This setting, like that of authentication, can also be viewed at the bottom of the project settings module located in a directory with the same name as the BASE directory (LENDSQR). Another 'IsAuthenticated' permissions setup was applied to specific endpoints, requiring that the HTTP requests made on those endpoints provided some sort of authentication (token authentication to be specific).
    
    **SERIALIZERS**:
    Serializers marshal between complex types like model instances, and python primitives. Basically what this means is that they enable us to take our database records which take the form of model instances (i.e objects) in python, to be converted to primitive data types which can then be rendered to different content-types in a HTTP response. They also enable parsed data in a HTTP request to be validated and either used to create or update a database record. 
    The process of marshalling between python primitives and request and response content is handled by parsers and renderers.
    
    I took the time to consider as well as create all the serializers necessary to carry out all the operations needed for this project, one for each function.
    
    The source code for the implementation is located in the "serializers.py" module of the "api" directory in the BASE directory of this application (LENDSQR - same location as this README file).
    
    **FILE PATH** : "LENDSQR/api/serializers.py"
    
    **ENDPOINTS**:
    Arguably the most standout feature of every API, endpoints are very crucial to API development seeing as they provide the entry-point to access specific data/resources located on a database.
    
    There are nine (8) different endpoints on this API, most of which require authentication before further access can be granted.
    
    The endpoints are listed and described as follows:

    -   "/api/register/": 
        This "POST" endpoint provides a means for users to create an account.

    -   "/api-dj-rest-auth/login/":
        This "POST" endpoint provides a means for users to receive tokens upon successful logins.

    -   "/api/create-savings/":
        This "POST" endpoint provides a means for users to create a savings-wallet.

    -   "/api/savings-details/":
        This "GET" endpoint provides a means for users to view their savings-wallet details.

    -   "/api/fund-savings/":
        This "PUT" endpoint provides a means for users to fund their savings-wallet.

    -   "/api/withdraw-funds/":
        This "PUT" endpoint provides a means for users to withdraw funds from their savings-wallet.

    -   "/api/transfer-funds/":
        This "PUT" endpoint provides a means for users to transfer funds from their savings-wallet.

    -   "/api/transactions/":
        This "GET" endpoint provides a means for users to view all past transactions on their savings-wallet.
        
    -   "/api-dj-rest-auth/logout/":
        This "POST" endpoint provides a means for users to logout successfully.
    
    The source code for the implementation is located in the "urls.py" module of the "api" directory in the BASE directory of this application (LENDSQR - same location as this README file).
    
    **FILE PATH** : "LENDSQR/api/urls.py"
    
    *NOTE*: Read the next section to get the link to the full **API documentation**.

    **TESTS**:
    Again, last but definitely not least, I will have to test that the core functionality of the API works as expected, including but not limited to ensuring that authenticated endpoints validate tokens, verifying that each of the endpoints validate the required HTTP POST/PUT data via serializers and return the correct response data/errors, as well as ensuring that all the tasks mentioned in step 2 of this project description (Understanding the project functionality) can be accomplished.
    
    The source code for the implementation is located in the "tests.py" module of the "api" directory in the BASE directory of this application (LENDSQR - same location as this README file).
    
    **FILE PATH** : "LENDSQR/api/tests.py"
    

## API Documentation

Please visit the following link for the full API documentation:

- [API-Docs](https://documenter.getpostman.com/view/26490359/2sAY4rDj6T)


## E-R Diagram

- [E-R short link] (https://dbdesigner.page.link/kGtYFrwBWLFmSkjeA)

- [E-R embedded link] (<iframe width="100%" height="500px" allowtransparency="true" allowfullscreen="true" scrolling="no" title="Embedded DB Designer IFrame" frameborder="0" src='https://erd.dbdesigner.net/designer/schema/1726037797-demo-credit?embed=true'></iframe>)


##  Installation (Django)

On macOS and Linux:

```sh
$ python -m pip install Django
```

On Windows:

```sh
...\> py -m pip install Django
```


## Execution/Usage

To use the Demo Credit web-application, click the link below and sign up in order to create an account and get started:

- [Project-Link](https://tonye-onuoha-lendsqr-be-test.onrender.com)


## Technologies

Demo Credit uses the following technologies and tools:

- [Python](https://www.python.org/): ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) - Programming language

- [Django] (https://www.djangoproject.com/) - Web framework

- [Django-Rest-Framework] (https://www.django-rest-framework.org/) - for building Web APIs

- [MySQL] (https://www.mysql.com/) - Database management system (Development only)

- [PostgreSQL] (https://www.postgresql.org/) - Database management system (Production only)

- [CSS] Cascading Style Sheets - For templates styling

- [HTML] Hypertext Markup Language - For templates structure


## Dependencies

- Please refer to the **requirements.txt** file in this same directory for all the project's dependencies.


## Contributors

Here's the list of people who have contributed to Demo Credit:

- Tonye Hugo Onuoha – [GitHub](https://github.com/Tonye-Onuoha)


## Author

Tonye Hugo Onuoha – [Email] : tonyeonuoha@gmail.com


## Change log

Below are the most recent changes made throughout the entire project:

-   commit f0372a282378c0d2a871c8623277f3bf5c2fca74 (HEAD -> master)
    Author: Tonye Hugo Onuoha <tonyeonuoha@gmail.com>
    Date:   Wed Oct 23 04:05:22 2024 -0700

    -   Updated README file


-   commit 1bceeb79092a56d03905e25d30518b2060aa6b3f (origin/master)
    Author: Tonye Hugo Onuoha <tonyeonuoha@gmail.com>
    Date:   Wed Oct 23 03:43:41 2024 -0700

    -   Added README file

-   commit ad9070221b4c04812705d1c30b226a93451a975d (HEAD -> master, origin/master)
    Author: Tonye Hugo Onuoha <tonyeonuoha@gmail.com>
    Date:   Tue Oct 22 03:02:15 2024 -0700

    -   Updated CSS file, login template and create_default template

-   commit 5905a704ff70343654cedb1f0febcb9263215fbd (HEAD -> master, origin/master)
    Author: Tonye Hugo Onuoha <tonyeonuoha@gmail.com>
    Date:   Mon Oct 21 04:01:37 2024 -0700

    -   Updated requirements.txt

-   commit 36e239afb7d4fc75f3661ea6116e66b2bd35ffe5 (HEAD -> master, origin/master)
    Author: Tonye Hugo Onuoha <tonyeonuoha@gmail.com>
    Date:   Mon Oct 21 03:46:30 2024 -0700

    -   Added requirements.txt file

-   commit c0b5039beb4dc0a2ce46ef5576584f0c3247f1a2
    Author: Tonye Hugo Onuoha <tonyeonuoha@gmail.com>
    Date:   Mon Oct 21 03:39:52 2024 -0700

    -   Configured settings for deployment and added comments to the other modules

-   commit 007d832de8b996427c4bbfbf13ebdacf4a766e85
    Author: Tonye Hugo Onuoha <tonyeonuoha@gmail.com>
    Date:   Mon Oct 21 02:56:37 2024 -0700

    -   Added django-corsheaders app

-   commit f00db0d466943897195614908344ec2a165d5c12 (HEAD -> master, origin/master)
    Author: Tonye Hugo Onuoha <tonyeonuoha@gmail.com>
    Date:   Mon Oct 21 02:35:46 2024 -0700

    -   Added API tests

-   commit bac136e95e92da39065af30c696e300f3eb167d3
    Author: Tonye Hugo Onuoha <tonyeonuoha@gmail.com>
    Date:   Sun Oct 20 08:46:35 2024 -0700

    -   Formatted settings module

-   commit 16605fd7837ba8fa63bab2e6427a4d56203f05f4 (HEAD -> master)
    Author: Tonye Hugo Onuoha <tonyeonuoha@gmail.com>
    Date:   Sun Oct 20 08:18:04 2024 -0700

    -   Switched to MySQL database for development and also modified some templates

-   commit 4f9c730d962b677c06d449c055872aa59ebf1d22 (HEAD -> master, origin/master)
    Author: Tonye Hugo Onuoha <tonyeonuoha@gmail.com>
    Date:   Sat Oct 19 01:10:22 2024 -0700

    -   Formatted templates and modules

-   commit 90b63d2b8e2f1d8b5a522252f93da6ef2e9431e0
    Author: Tonye Hugo Onuoha <tonyeonuoha@gmail.com>
    Date:   Fri Oct 18 05:51:23 2024 -0700

    -   Created views for api app

-   commit e255d98f16c7fecd262c5e76e1fd597b65d73e68
    Author: Tonye Hugo Onuoha <tonyeonuoha@gmail.com>
    Date:   Fri Oct 18 05:11:11 2024 -0700

    -   Added url patterns for api app

-   commit ba818f61b19d96b1570c92a0f7bc08cf811d60ab
    Author: Tonye Hugo Onuoha <tonyeonuoha@gmail.com>
    Date:   Fri Oct 18 04:35:00 2024 -0700

    -   Created serializers for api app



For more enquries, please contact me with this phone number +2349054466479.