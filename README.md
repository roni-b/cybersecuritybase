LINK: https://github.com/roni-b/cybersecuritybase

Installation instructions:

1. Run database migrations with command `python manage.py migrate`

2. Create superuser with command python manage.py createsuperuser

3. Start the app with command python manage.py runserver

You will see simple blog app where you can make blogs. The blogs should be only visible to logged users and posting a new blog requires logged user.

FLAW 1:

A5:2017-Broken Access Control

https://github.com/roni-b/cybersecuritybase/blob/5eea292b5338cdb7955feffaabe8302090742ac5/app/views.py#L12

The short description states that the blogs should only be visible to logged-in users. However, currently, there is no restriction for non-logged-in users to access the /blogs page, which lists all the blogs, or specific blog sites, for example, /blog/1. The fix for this problem is actually very simple with Django as @login_required decorator before the view function ensures that only authenticated user can access certain views.

FLAW 2:

A1:2017-Injection

https://github.com/roni-b/cybersecuritybase/blob/5eea292b5338cdb7955feffaabe8302090742ac5/app/views.py#L46

The app currently employs an unsafe SQL query format for its search function, wherein user-provided parameters are directly integrated into the query. User could for example use search term ' OR 1=1 -- to show all results. To fix this vulnerability, it is necessary to use methods which uses query parameterization. These techniques ensure that user input is properly sanitized and separated from the query.

FLAW 3

A7:2017-Cross-Site Scripting (XSS)

https://github.com/roni-b/cybersecuritybase/blob/5eea292b5338cdb7955feffaabe8302090742ac5/app/views.py#L13

By default Django escapes data but it can be turned off. Now if the user creates blog with title <script>alert('XSS');</script> that javascript code is executed for everyone who is visiting the /blogs page. The fix is to not use | safe option which marks data safe. It is worth of keeping mind that first rule of web application security is never to trust user input.

FLAW 4

Cross-Site Request Forgery (CSRF)

https://github.com/roni-b/cybersecuritybase/blob/5eea292b5338cdb7955feffaabe8302090742ac5/app/views.py#L13

In the /blogs page there is a form for submitting a new blog. However the view for that page has @csrf_exempt decorator which skips the CSRF validation. The fix is to remove @csrf_exempt decorator.

FLAW 5

A6:2017-Security Misconfiguration

https://github.com/roni-b/cybersecuritybase/blob/652bddd5003c60c110b565813db218c63478d1f7/project/settings.py#L26

The most commonly seen issue is security misconfiguration and the blog app has one. In the settings.py file the DEBUG option is set to True. If we asssume that the app is in the production environment and DEBUG is set to True, it exposes sensitive information about the app and its internal workings to potential attacker such as file paths or stack traces. The fix is to set DEBUG to False. 






