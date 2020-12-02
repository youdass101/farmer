# farmer Web Application 
This web application is a microgreens farm tracking application, where users can create plants, mediums, and trays that have been seeded, to track the progress and know when to harvest active trays. Users can view trays history, plant or medium information details and can edit and update them.
This application is built using django, HTML, css,and javascript.
In the back end, I am using the Django framework, in the front end I am using the javascript.
In Django, I used models to create and edit database, and I used form to create forms and render them to HTML. For this application currently, I have 5 models, also I created 6 forms to render on HTML. the web application is mobile-friendly using the media max-width to manipulate what to show and hide and also to change the style of elements on mobile phone.
For the HTML design page, a layout is used for the static elements.
CSS is used to style classes, ids, and elements.


# Plant Page 
On the plant page, users can view created plants details table, also users can use the filter form to search for specific plant name or sort plant table order by name, harvest days, or output grams.
## filter button 
uses the view *filter* to sort the Django model by required field value, refresh the page, and return the data sorted.
## Create plant button
When pressed a java eventlistener will display a floating form, when users press outside the form or on the "x" icon the form will be closed though, typed data will stay there unless the page is refreshed (the form is loaded from Django to HTML) in the form users can fill the plant details, and when done a create button should be pressed.  
when create is clicked java loads and get the form input and, will fetch the plant view using the post method to post the data to Django plant view. Python will check the form validity, if all data is valid the data will be created in the plant model and the view will return a JSON response to java where java will check the result message to check for error and if there is no error java will add the new plant row to plant table without reloading.

## Edit button
pressing this button will trigger an event in java which will get all data in the current row and transfer the row to form with the row gathered data, when users finish editing, the save button pressed where java will get the edited data and fetch plant view using Post method nested a type variable its value should be put. the fetched data in python will be checked and if passed the check python will get the model and change its value and save it, then will return a JSON response to java with a message. Java will rechange the row to a table data row with edited information in it.

# Medium Page
In the medium HTML page, users can view all created medium mix names and detail, also a filter can be applied to sort the table by name, coco, or soil percentage. the filter request sorted model data from the Django filter view.
## New Mix button
when pressed a javascript event will launch a function to show a floating form loaded in HTML. When form data is filled and the Create button is clicked a java event will fetch medium view using the post method to load the data, the python should get the data and validate the form, and if the form is valide python will create a new medium ad return a JSON message to the java function. The java function will check the message for an error, and then java will add the element of the created data to the table row.
# Edit button
pressing this button will trigger an event in java which will get all data in the current row and transfer the row to form with the row gathered data, when users finish editing, the save button pressed where java will get the edited data and fetch medium view using Post method nested a type variable its value should be put. the fetched data in python will be checked and if passed the check python will get the model and change its value and save it, then will return a JSON response to java with a message. Java will rechange the row to a table data row with edited information in it.

# Tray page 
Tray page, when loaded a GET request index view in Django, will render the index.html page and view plants that are not in the harvest table, the statement table will show tray details most important is the tray count, tray name, growing time in days, count to best harvest time baes on the plant data. 
## Filter 
filter button will POST to the python filter view to sort serialized data by name, start date, or end date. also if a query typed in search the filter view will filter the query from the model and return the data to the page.
## New tray 
new tray button will trigger an event in javascript to unhide a class that will pop a floating form (a Django form set in the layout) after filling the data if nothing is missing and the Create button is pressed the java will fetch index view and validate the data, then after success index will create a model object and return JSON response with a success message and render index get to reload the new data
creating a tray requires a plant name and medium, start date
the index page contains all active tray "or tray that haven't been harvested yet"
## Edit 
The edit button will trigger an onclick event in java that will save the row specific data to a variable and, unhide a form and fill it with current row data in the forms inputs field so that we can edit, after finish editing if save is pressed java will post fetch the data to edit the model in index view, also if the delete button is pressed the java will fetch Django index and delete the object then the python will return a JSON response with a message the pop for will vanish and the row if edited will be replaced with new data and if deleted will be removed without reloading the page.
## Harvest 
If pressed an onclick java will trigger a function that will display a form class which will pop on the page, user will fill the harvest weight and change the date if needed. if the harvest button is pressed in the form java will fetch Django harvest view with the data  where a harvest object will the tray id will be created in the harvest table, when succeeded the harvest function will return JSON response to java and java will hide the form and remove the tray row without reloading the page

# History 
the history page will show the harvested tray with information about the harvest weight, date, total time, count, etc ...

# views.py 
## index 
index function accepts 3 methods, POST, PUT, and default GET.
the put is mainly used to edit the tray model and return JSON response for a javascript function.
the POST will create a new tray model object and redirect to the index GET method.
Get method will request all tray objects, serialize them, and render them to the index.html page.
## login_view 
have POST and GET method.
the GET, if the user is not logged will render the login.html page else it will redirect to index.html.
The POST will get the login.html to submit form data and try to authenticate if failed it will return an error and reload login.html if succeded it will redirect to index.html 
## def logout_view
this function will log out any logged-in user, index view which will redirect to login.html
## register_view
this function has 2 methods, POST and GET.
The GET if the user logged-out will render the register.html with the registration form.
The POST will get posted data on register.html and create a new user model object, log in the created user and, then will redirect to index.html, though if creation failed it will return error alert and reload register.html with typed data.
## plants view 
this function has 2 methods, POST and GET.
the GET will get all objects in the plants model and then render them to plants.html.
The POST method have 3 nested method type: get, create, and put. POST method here mainly is fetched from javascript
-get is to request data of a specific object and return a response to javascript. 
-create will request data from javascript check if plant exist, f not it creates new object model plant and returns 201 and done message 
-put will request edit data from javascript check if changed plant name exists, if not it will edit the plant data and return a message to javascript.
## medium
this function has 2 methods, POST and GET.
the GET will get all objects in the medium model and then render them to medium.html.
The POST method has 2 nested method type: create, and put. POST method here mainly is fetched from javascript
-create will request data from javascript check if medium name exist, if not it creates new object model medium and returns 201 and done message 
-put will request edit data from javascript check if changed medium name exists, if not it will edit the medium data and return a message to javascript.
## harvest
this function have only a POST method wich will create new harvest object field for a tray with the fetched data from java scipt, and will return message of success for javascript function.
## History 
this function has a get method that will get all tray that is in the harvest and serialize them, then render the history page with the serialized data.
## Filter 
The filter function has 4 if "check" to check which page submitted the filter and for each submitted page the filter will sort the models or serialized model data based on the key field name, and in case of a search the function will search the Django model for the name in the query.

```python
First of all run the django server using the follwing command

python manage runserver
```
#
