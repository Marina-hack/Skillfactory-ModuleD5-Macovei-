from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Post
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm


class News(ListView):
    model = Post
    ordering = '-datetime_post_creation' #сортировка по дате создания
    # queryset = Post.objects.post_by('name')
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        # context['time_now'] = datetime.utcnow()
        return context

 
class BreakingNews(DetailView):
    model = Post
    template_name = 'breaking_news.html'
    context_object_name = 'breaking_news'


class Articles(DetailView):
    model = Post
    template_name = 'articles.html'
    context_object_name = 'articles'


class PostCreate(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    permission_required = ('news.add_post',)
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news')


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news')


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news')
