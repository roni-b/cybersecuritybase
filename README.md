LINK: https://github.com/roni-b/cybersecuritybase

Installation instructions:

1. Run database migrations with commands: python manage.py makemigrations and python manage.py migrate

2. Create superuser with command python manage.py createsuperuser

3. Start the app with command python manage.py runserver

You will see simple blog app where you can make blogs. The blogs should be only visible to logged users and posting a new blog requires logged user.

FLAW 1:

A01:2021-Broken Access Control 

https://github.com/roni-b/cybersecuritybase/blob/main/app/views.py#L10C16-L10C16
and https://github.com/roni-b/cybersecuritybase/blob/main/app/views.py#L28

The short description states that the blogs should only be visible to logged-in users. However, currently, there is no restriction for non-logged-in users to access the /blogs page, which lists all the blogs, or specific blog sites, for example, /blog/1. The fix for this problem is actually very simple with Django as @login_required decorator before the view function ensures that only authenticated user can access certain views.

FLAW 2:

A03:2021-Injection

https://github.com/roni-b/cybersecuritybase/blob/main/app/views.py#L40

The app currently employs an unsafe SQL query format for its search function, wherein user-provided parameters are directly integrated into the query. User could for example use search term ' OR 1=1 -- to see all blogs. To fix this vulnerability, it is necessary to use methods which uses query parameterization. These techniques ensure that user input is properly sanitized and separated from the query.

' OR 1=1 --


