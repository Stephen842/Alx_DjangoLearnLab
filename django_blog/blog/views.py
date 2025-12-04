from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import UserRegisterForm, PostForm, CommentForm


# Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('home')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
        'title': 'Django Blog - Register Now'
    }
    return render(request, 'blog/register.html', context)

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, f'Welcome {username}!')
                return redirect('home')
            
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form,
        'title': 'Django Blog - Login Now',
    }
    return render(request, 'blog/login.html', context)

# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('home')

# Profile view
@login_required
def profile_view(request):
    if request.method == 'POST':
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        messages.success(request, 'Profile updated successfully!')

    context = {
        'title': 'Django Blog - User Profile',
    }
    return render(request, 'blog/profile.html', context)


# Landing page view
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 12


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.order_by('-created_at')
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid() and request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=self.object.pk)
        
        context = self.get_context_data(comment_form=form)
        return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html' # used for both create & update

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html' # used for both create & update

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    

# Edit Comment
@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.author:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post-detail', pk=comment.post.id)
        
    return redirect('post-detail', pk=comment.post.id)


# Delete Comment
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        return HttpResponseForbidden()
    
    post_id = comment.post.id
    comment.delete()
    return redirect('post-detail', pk=post_id)