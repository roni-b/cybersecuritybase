LINK: https://github.com/roni-b/cybersecuritybase

Installation instructions:

1. Run database migrations with command `python manage.py migrate`

2. Create superuser with command `python manage.py createsuperuser`

3. Start the app with command `python manage.py runserver`

You will see simple blog app where you can make blogs. The blogs should be only visible to logged users and posting a new blog requires logged user.

FLAW 1:

A5:2017-Broken Access Control

https://github.com/roni-b/cybersecuritybase/blob/5eea292b5338cdb7955feffaabe8302090742ac5/app/views.py#L12

Broken access control refers to a security vulnerability where an application or system fails to enforce proper access restrictions, allowing unauthorized users to access or modify resources or perform actions they shouldn't have permission to do. It occurs when access controls, such as authentication and authorization mechanisms, are not effectively implemented, leading to unauthorized access, data breaches, or other security breaches. In essence, it means that users can bypass security measures and gain access to sensitive information or functionality they shouldn't be allowed to use.

The short description states that the blogs should only be visible to logged-in users. However, currently, there is no restriction for non-logged-in users to access the /blogs page, which lists all the blogs, or specific blog sites, for example, /blog/1. The fix for this problem is actually very simple with Django as @login_required decorator before the view function ensures that only authenticated user can access certain views.

FLAW 2:

A1:2017-Injection

https://github.com/roni-b/cybersecuritybase/blob/5eea292b5338cdb7955feffaabe8302090742ac5/app/views.py#L46

Injection is a cybersecurity vulnerability where malicious code or data is inserted into a program, application, or system. This can occur when user inputs are not properly validated or sanitized. Injection attacks, like SQL injection or cross-site scripting (XSS), can manipulate and exploit vulnerabilities, potentially leading to unauthorized access, data breaches, or system compromise.

The app currently employs an unsafe SQL query format for its search function, wherein user-provided parameters are directly integrated into the query. User could for example use search term ' OR 1=1 -- to show all results. To fix this vulnerability, it is necessary to use methods which uses query parameterization. These techniques ensure that user input is properly sanitized and separated from the query.

FLAW 3

A7:2017-Cross-Site Scripting (XSS)

https://github.com/roni-b/cybersecuritybase/blob/5eea292b5338cdb7955feffaabe8302090742ac5/app/views.py#L13

Cross-Site Scripting (XSS) is a cybersecurity vulnerability that allows attackers to inject malicious scripts into web pages viewed by other users. These scripts can execute within a user's browser and steal sensitive information, manipulate page content, or perform unauthorized actions on behalf of the victim. XSS attacks occur when user inputs are not properly sanitized or validated by a web application, enabling malicious code to be executed in the context of a trusted website.

By default Django escapes data but it can be turned off. Currently blogs.html has for loop which renders blog titles as a links to that blog. The title of the blog is marked as a safe HTML content which means Django isn’t using content escaping. Now if the user creates blog with title <script>alert('XSS');</script> that javascript code is executed for everyone who is visiting the /blogs page. The fix is to not use | safe option which marks data safe. It is worth of keeping mind that first rule of web application security is never to trust user input.

FLAW 4

Cross-Site Request Forgery (CSRF)

https://github.com/roni-b/cybersecuritybase/blob/5eea292b5338cdb7955feffaabe8302090742ac5/app/views.py#L13

Cross-Site Request Forgery (CSRF) is a cybersecurity attack that tricks a user into performing an unwanted action on a web application without their consent. Attackers craft malicious requests and induce users, who are already authenticated with the web application, to unknowingly submit those requests. Since the user is authenticated, the web application may mistakenly treat the malicious request as legitimate, potentially causing actions such as changing settings, making transactions, or deleting data. Preventing CSRF attacks typically involves using tokens to validate that requests come from legitimate sources. 

Django provides built-in CSRF protection to safeguard against such attacks. When you submit a form in a Django application, it includes a CSRF token that is validated on the server to confirm that the request is legitimate and coming from the same site. This helps prevent unauthorized actions and data manipulation.

The /blogs page contains a form for submitting new blog entries. However the view for that page has @csrf_exempt decorator which skips the CSRF validation. The fix is to remove @csrf_exempt decorator and Django will validate the CSRF token.

FLAW 5

A6:2017-Security Misconfiguration

https://github.com/roni-b/cybersecuritybase/blob/652bddd5003c60c110b565813db218c63478d1f7/project/settings.py#L26

Security misconfiguration refers to the state of a computer system or software application that is not set up securely according to best practices. It occurs when security settings, options, or configurations are unintentionally left in an insecure state or are not properly configured. Security misconfigurations can leave systems and applications vulnerable to exploitation by attackers.

The most commonly seen issue is security misconfiguration and the blog app has one. In the settings.py file the DEBUG option is set to True. If we asssume that the app is in the production environment and DEBUG is set to True, it exposes sensitive information about the app and its internal workings to potential attacker such as file paths or stack traces. The fix is to set DEBUG to False. 

