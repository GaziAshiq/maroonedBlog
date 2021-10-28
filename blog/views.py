from .models import News, Tag
from .forms import NewsPublishForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render


# Create your views here.
def home(request):
    featured_post = News.objects.filter(status=True).order_by('-created_on')[0:3]
    return render(request, 'blog/index.html', {'home': 'Welcome to Marooned', 'featured_post': featured_post})


class NewsListView(ListView):
    queryset = News.objects.filter(status=1).order_by('-created_on')
    context_object_name = 'news_list'
    paginate_by = 5


class NewsDetailView(DetailView):
    model = News
    context_object_name = 'post'


class NewsCreateView(LoginRequiredMixin, CreateView):
    # model = News
    # fields = ['title', 'slug', 'cover_photo', 'summary', 'content', 'tags']

    # using form_class so i can use summernote
    form_class = NewsPublishForm
    template_name = 'blog/news_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NewsCreateView, self).form_valid(form)


class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News

    form_class = NewsPublishForm
    template_name = 'blog/news_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NewsUpdateView, self).form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    success_url = '/blog/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class UserPostListView(ListView):
    model = News
    template_name = 'blog/user_posts.html'
    context_object_name = 'news_list'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return News.objects.filter(author=user).order_by('-created_on')


class TagListView(ListView):
    queryset = Tag.objects.all()
    template_name = 'blog/tags.html'
    context_object_name = 'tag_list'


def tag_detail(request, slug):
    tag = Tag.objects.get(tag_slug__iexact=slug)
    return render(request, 'blog/tag_detail.html', context={'tag': tag})
