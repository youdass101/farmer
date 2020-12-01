# farmer
This web application is a microgreens farm tracking application, where users can create plants, mediums, and trays that have been seeded to track the progress and know when to harvest active trays. Users can view trays history, plant or medium information details and can edit them.
this application is built using django, HTML, css,and java script

# Plant
On the plant page, users can view created plants detail table, also users can use the filter form to search for specific plant name or sort plant table order by name, harvest days, or output grams.
## filter button 
uses the view *filter* to sort the Django model by required field value, refresh the page, and return the data sorted.
## Create plant 
When pressed a java eventlistener will display a floating form, when users press outside the form or on the "x" icon the form will be closed but and typed data will stay there unless the page is refreshed (the form is loaded from Django to HTML) in the form users can fill the plant details, and when done a create button should be pressed.  
when create is clicked java loads and get the form input and, will fetch the plant view using the post method to post the data to Django plant view. Python will check the form validity, if all data is valid the data will be created in the plant model and the view will return a JSON response to java where java will check the result message to check for error and if there is no error java will add the new plant row to plant table without reloading.

## Edit
pressing this button will trigger an event in java which will get all data in the current row and transfer the row to form with the row gathered data, when users finish editing, the save button pressed where java will get the edited data and fetch plant view using Post method nested a type variable its value should be put. the fetched data in python will be checked and if passed the check python will get the model and change its value and save it, then will return a JSON response to java with a message. Java will rechange the row to a table data row with edited information in it.

# Medium 
In the medium HTML page, users can view all created medium mix names and detail, also a filter can be applied to sort the table by name, coco, or soil percentage. the filter request sorted model data from the Django filter view.
## New Mix
when pressed a javascript event will launch a function to show a floating form loaded in HTML. When form data is filled and the Create button is clicked a java event will fetch medium view using the post method to load the data, the python should get the data and validate the form, and if the form is valide python will create a new medium ad return a JSON message to the java function. The java function will check the message for an error, and then java will add the element of the created data to the table row.
# Edit 
pressing this button will trigger an event in java which will get all data in the current row and transfer the row to form with the row gathered data, when users finish editing, the save button pressed where java will get the edited data and fetch medium view using Post method nested a type variable its value should be put. the fetched data in python will be checked and if passed the check python will get the model and change its value and save it, then will return a JSON response to java with a message. Java will rechange the row to a table data row with edited information in it.

# Tray 
creating a tray requires a plant name and medium, start date
the index page contains all active tray "or tray that haven't been harvested yet"





```python
First of all run the django server using the follwing command

python manage runserver
```
#
