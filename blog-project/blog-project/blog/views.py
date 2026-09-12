from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from .models import BlogPost, Category, Comment
from .forms import BlogPostForm, CommentForm


class HomeView(ListView):
    """Show all published blog posts - title, author, excerpt.
    Supports optional search (?q=) and category filter (?category=<id>).
    """
    model = BlogPost
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '').strip()
        category_id = self.request.GET.get('category', '').strip()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class PostDetailView(DetailView):
    """Show full details of a single blog post, its comments, and a comment form."""
    model = BlogPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related('author')
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        """Handle new comment submissions on the post detail page."""
        self.object = self.get_object()
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to comment.')
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment was posted.')
            return redirect('post_detail', pk=self.object.pk)

        context = self.get_context_data(comment_form=form)
        return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, CreateView):
    """Only authenticated users can create a post."""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post was published successfully!')
        return super().form_valid(form)


class OwnerRequiredMixin(UserPassesTestMixin):
    """Only the post's author may edit/delete it."""
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You are not allowed to modify someone else's post.")
        return redirect('post_detail', pk=self.kwargs['pk'])


class PostUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Your post was updated successfully!')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'Your post was deleted.')
        return super().form_valid(form)


@login_required
def my_posts(request):
    """Show only the posts created by the logged-in user."""
    posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'blog/my_posts.html', {'posts': posts})


@login_required
@require_POST
def like_toggle(request, pk):
    """Toggle a like on a post for the current user."""
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', pk=pk)
