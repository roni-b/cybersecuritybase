from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from .forms import BlogForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user

def home(request):
    return render(request, 'app/index.html')

#@login_required
def blogs(request):
    # if request.method == 'POST':
    #     form = BlogForm(request.POST)
    #     if form.is_valid():
    #         new_blog = form.save(commit=False)
    #         user = get_user(request)
    #         new_blog.author = user
    #         new_blog.save()
    #         return redirect('blogs')
    #     else:
    #         print(form.errors)
    #         form = BlogForm()

    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        user = get_user(request)
        new_blog = Blog(title=title, content=content, author=user)
        new_blog.save()

    bloglist = Blog.objects.all()
    return render(request, 'app/blogs.html', {'bloglist': bloglist})

#@login_required
def blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'app/blog.html', {'blog': blog})

#@login_required
def search(request):
    query = request.GET.get('q', '')
    results = []
    sql_query = f"""
        SELECT * FROM app_blog
        WHERE lower(title) LIKE '%{query.lower()}%' OR lower(content) LIKE '%{query.lower()}%'
    """

    results = Blog.objects.raw(sql_query)

    context = {
        'query': query,
        'results': results
    }

    return render(request, 'app/search_results.html', context)