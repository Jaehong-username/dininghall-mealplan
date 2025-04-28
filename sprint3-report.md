# Sprint 3 Report
Video Link: https://www.youtube.com/watch?v=6i1-M_h9Gwo

## What's New (User Facing)
* Feature 4: Let Managers Track Meal Usage
* Feature 6: Let Employees Upload Photos of Today's Meals
* Feature 10: User Feedback System for Dining Hall Services
* Feature 11: Finishing Admin Portal to Manage Menus, Meal Plans, and Usage Reports
* Feature 46: Two Factor Authentication
* Feature 48: Update Models with Consistent Primary Keys

## Work Summary (Developer Facing)
During Sprint 3, we decided to split up our tasks to make sure that everyone would be able to contribute to the sprint. Since we already finished most of our issues, only a few remained. We mainly focused on finishing partially completed features, such as the admin dashboard, in the backend. Additionally, we worked the front end, polishing up the overall theme of our application. We also added new pages for image uploads, displaying the statistics of meals, and two-factor authentication checks. This backend helped focus on displaying and updating database information. It also helped with creating a more secure application for our users.

## Completed Issues/User Stories
Here are links to the issues that we completed in this sprint:
* https://github.com/Jaehong-username/dininghall-mealplan/issues/5
* https://github.com/Jaehong-username/dininghall-mealplan/issues/6
* https://github.com/Jaehong-username/dininghall-mealplan/issues/10
* https://github.com/Jaehong-username/dininghall-mealplan/issues/11
* https://github.com/Jaehong-username/dininghall-mealplan/issues/46
* https://github.com/Jaehong-username/dininghall-mealplan/issues/48

## Incomplete Issues/User Stories
Here are links to issues we worked on but did not complete in this sprint:
* https://github.com/Jaehong-username/dininghall-mealplan/issues/9 : This feature was not fully implemented due to the complexity of user authorization in our application; in order to have a password change functionality, the server would have to send an email to the user. We worked more on 2FA.
* https://github.com/Jaehong-username/dininghall-mealplan/issues/10 : Sending user comments and feedback to the database is limited due to some backend errors that our team hasn’t been able to resolve. Hence, the meal feedback list doesn’t update itself on the fly.

## Code Files for Review
Due to technical difficulties with merging, we have our final files under the project-final branch instead of main.
Please review the following code files, which were actively developed during this sprint, for quality:

- **src folder**
    * [api.py](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/api.py)
    * [app.py](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/app.py)
    * [form_classes.py](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/form_classes.py)
    * [models.py](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/models.py)
    * [views.py (menu-UI)](https://github.com/Jaehong-username/dininghall-mealplan/blob/menu-UI/src/views.py)
    * [views.py](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/views.py)
    * [views_temp.py (post)](https://github.com/Jaehong-username/dininghall-mealplan/blob/post/views_temp.py)
    * [models_temp.py (post)](https://github.com/Jaehong-username/dininghall-mealplan/blob/post/models_temp.py)
    * [form_classes_temp.py (post)](https://github.com/Jaehong-username/dininghall-mealplan/blob/post/form_classes_temp.py)
 
- **static folder**
    * [admin_data.js](https://github.com/Jaehong-username/dininghall-mealplan/tree/project-final/src/static)
   * [dynamic.js](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/static/dynamic.js)
    * [style.css](https://github.com/Jaehong-username/dininghall-mealplan/blob/post/src/static/dynamic.js)
    * [util.js](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/static/util.js)
      
- **templates folder**
    * [2fa.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/2fa.html)
    * [admin-portal-main.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/admin-portal-main.html)
    * [admin-portal-mealplans.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/admin-portal-mealplans.html)
    * [admin-portal-menus.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/admin-portal-menus.html)
    * [admin-portal-users.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/admin-portal-users.html)
    * [admin-portal.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/admin-portal.html)
    * [contact.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/contact.html)
    * [dashboard.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/dashboard.html)
    * [dining-halls.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/dining-halls.html)
    * [feedback-page.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/feedback-page.html)
    * [forgot-password.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/forgot-password.html)
    * [home.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/home.html)
    * [layout.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/layout.html)
    * [login.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/login.html)
    * [meal-data.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/meal-data.html)
    * [meal-feedback-list.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/meal-feedback-list.html)
    * [meal-plan.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/meal-plan.html)
    * [meal-details.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/menu-details.html)
    * [menu-options.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/menu-options.html)
    * [post-meal.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/post-meal.html)
   * [register.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/register.html)
    * [verify-otop.html](https://github.com/Jaehong-username/dininghall-mealplan/blob/project-final/src/templates/verify-otp.html)

## Retrospective Summary
Here's what went well:
* Easy communication with team members
* Collaboration and task division within our team
* Main backend features completed
* Main frontend polishing UI finished

Here's what we'd like to improve (our current limitations):
* Sending user comments and feedback to the database is limited due to some backend errors that our team hasn’t been able to resolve. Hence, the meal feedback list doesn’t update itself on the fly.
* Updating current password (changing password) features
* Cleaning up models if needed and making additions as needed

Here are the changes we would like to implement as possible future improvements or new modules:
* Resolving the issues related to sending Comment and Feedback data to the database is a priority, as this is one of the core functionalities to help students make informed decisions about choosing school meals. Hence, each meal’s student feedback doesn’t get dynamically updated.
* Working on each school meal feedback page to display the photo and its dietary and restriction information according to the database.
* Adding more variety of pictures to our web application to give users a more pleasant and user-friendly design.
