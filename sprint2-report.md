# Sprint 2 Report
Video Link:

## What's New (User Facing)
* Feature 3: Display Menus, Nutritional Information, and Food Ingredients
* Feature 6: Employees’ Ability to Upload Menu/Meal Photos
* Feature 7: Managers’ Ability to Post Dietary Restrictions
* Feature 10: User Feedback System for Dining Hall Services
* Feature 11: Admin Portal to Manage Menus, Meal Plans, and Usage Reports
* Feature 25, 31, 40: Today’s Menu, Manage Meal Plan, & Meal Feedback UI

## Work Summary (Developer Facing)
During Sprint 2, we decided to split up our tasks to make sure that everyone would be able to contribute to the sprint. We worked on both frontend and backend to ensure that there would be steady progress in the overall project. On the frontend, we refined the visual design to create a more cohesive look while also creating new pages such as meal plan, today’s menu, admin portal, and feedback page. Meanwhile, the backend focused on enabling core functionality features that allowed us to focus more on authorization and permissions for features such as the admin portal, and database models. Due to the importance of databases in this project, we ensured to refine and use our models efficiently in order to complete our tasks. 

## Completed Issues/User Stories
Here are links to the issues that we completed in this sprint:
* https://github.com/Jaehong-username/dininghall-mealplan/issues/3
* https://github.com/Jaehong-username/dininghall-mealplan/issues/6
* https://github.com/Jaehong-username/dininghall-mealplan/issues/7
* https://github.com/Jaehong-username/dininghall-mealplan/issues/10
* https://github.com/Jaehong-username/dininghall-mealplan/issues/11
* https://github.com/Jaehong-username/dininghall-mealplan/issues/25
* https://github.com/Jaehong-username/dininghall-mealplan/issues/31
* https://github.com/Jaehong-username/dininghall-mealplan/issues/32
* https://github.com/Jaehong-username/dininghall-mealplan/issues/33
* https://github.com/Jaehong-username/dininghall-mealplan/issues/34
* https://github.com/Jaehong-username/dininghall-mealplan/issues/35
* https://github.com/Jaehong-username/dininghall-mealplan/issues/36
* https://github.com/Jaehong-username/dininghall-mealplan/issues/37
* https://github.com/Jaehong-username/dininghall-mealplan/issues/38
* https://github.com/Jaehong-username/dininghall-mealplan/issues/39
* https://github.com/Jaehong-username/dininghall-mealplan/issues/40

## Incomplete Issues/User Stories
Here are links to issues we worked on but did not complete in this sprint:
* https://github.com/Jaehong-username/dininghall-mealplan/issues/4: This feature was not implemented due to time constraints and overlapping tasks; managers are unable to track meal usage without having a portal implemented.
* https://github.com/Jaehong-username/dininghall-mealplan/issues/9: This feature was not fully implemented due to the complexity of user authorization in our application; in order to have a password change functionality, the server would have to send an email to the user. 

* Our group decided to discuss and plan how to approach these issues in our next sprint.

## Code Files for Review
Please review the following code files, which were actively developed during this sprint, for quality:

* [admin_data.js] https://github.com/Jaehong-username/dininghall-mealplan/blob/admin_portal/src/static/admin_data.js
* [util.js] https://github.com/Jaehong-username/dininghall-mealplan/blob/admin_portal/src/static/util.js
* [api.py] https://github.com/Jaehong-username/dininghall-mealplan/blob/admin_portal/src/api.py
* [app.py (main)] https://github.com/Jaehong-username/dininghall-mealplan/blob/main/src/app.py
* [app.py (mealplan-ui)] https://github.com/Jaehong-username/dininghall-mealplan/blob/mealplan-ui/src/app.py
* [form_classes.py (main)] https://github.com/Jaehong-username/dininghall-mealplan/blob/main/src/form_classes.py
* [form_classes.py (mealplan-ui)] https://github.com/Jaehong-username/dininghall-mealplan/blob/admin_portal/src/form_classes.py
* [form_classes.py (admin_portal)] https://github.com/Jaehong-username/dininghall-mealplan/tree/mealplan-ui/src
* [models.py (main)] https://github.com/Jaehong-username/dininghall-mealplan/blob/main/src/models.py
* [models.py (mealplan-ui)] https://github.com/Jaehong-username/dininghall-mealplan/blob/mealplan-ui/src/models.py
* [models.py (admin_portal)] https://github.com/Jaehong-username/dininghall-mealplan/blob/admin_portal/src/models.py
* [views.py (menu-UI)] https://github.com/Jaehong-username/dininghall-mealplan/blob/menu-UI/src/views.py
* [views.py (mealplan-ui)] https://github.com/Jaehong-username/dininghall-mealplan/blob/mealplan-ui/src/views.py
* [views.py (admin_portal)] https://github.com/Jaehong-username/dininghall-mealplan/blob/admin_portal/src/views.py
* [style.css (menu-UI)] https://github.com/Jaehong-username/dininghall-mealplan/blob/menu-UI/src/static/style.css
* [style.css (admin_portal)] https://github.com/Jaehong-username/dininghall-mealplan/blob/admin_portal/src/static/style.css
* [admin-portal-main.html] https://github.com/Jaehong-username/dininghall-mealplan/blob/admin_portal/src/templates/admin-portal-main.html
* [admin-portal-mealplans.html] https://github.com/Jaehong-username/dininghall-mealplan/blob/admin_portal/src/templates/admin-portal-mealplans.html
* [admin-portal-menus.html] https://github.com/Jaehong-username/dininghall-mealplan/blob/admin_portal/src/templates/admin-portal-menus.html
* [admin-portal-users.html] https://github.com/Jaehong-username/dininghall-mealplan/blob/admin_portal/src/templates/admin-portal-users.html
* [contact.html] https://github.com/Jaehong-username/dininghall-mealplan/blob/menu-UI/src/templates/contact.html
* [dashboard.html] https://github.com/Jaehong-username/dininghall-mealplan/blob/admin_portal/src/templates/dashboard.html
* [layout.html (menu-UI)] https://github.com/Jaehong-username/dininghall-mealplan/blob/menu-UI/src/templates/layout.html
* [layout.html (admin_portal)] https://github.com/Jaehong-username/dininghall-mealplan/blob/admin_portal/src/templates/layout.html
* [meal-plan.html (menu-UI)] https://github.com/Jaehong-username/dininghall-mealplan/blob/menu-UI/src/templates/meal-plan.html
* [meal-plan.html (mealplan-ui)] https://github.com/Jaehong-username/dininghall-mealplan/blob/mealplan-ui/src/templates/meal-plan.html
* [menu-details.html] https://github.com/Jaehong-username/dininghall-mealplan/blob/mealplan-ui/src/templates/menu-details.html

## Retrospective Summary
Here's what went well:
* Easy communication with team members
* Collaboration and task division within our team
* Backend functionality progress
* Effective sprint planning

Here's what we'd like to improve:
* Improve version control practices to minimize merge conflicts
* Allocate more time for working on issues before the sprint deadline
* Adding more comments to our code to ensure easy readability

Here are the changes we plan to implement in the next sprint:
* Incorporation of 2FA to secure our web app
* Merging features we’ve worked on from separate branches into one main branch
* Completing the rest of the functional requirements such as manager usage reports and changing password
* Implementing more backend features as needed
* Adding frontend features to pages lacking a specific UI, to match the overarching theme of the project
* Discussing and planning how to implement future features together
