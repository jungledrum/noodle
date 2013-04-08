from noodle.controller_base import *

class PostsController(ControllerBase):

    before_filter = {'check'}
    after_filter = {'log'}

    def check(self):
        if not session.has_key('username'):
            return redirect('/login')

    def log(self):
        # print 'after_filter'
        pass
        
        
    def index(self):
        posts = Post.all()
        return render('index.html', posts=posts)

    def new(self):
        return render('new.html')
    
    def create(self):
        title = params['title']
        author = params['author']
        content = params['content']

        post = Post(title, author, content)
        post.save()

        response = redirect('/')

        return response

    def show(self):
        id = params['id']
        post = Post.find(id)

        return render('show.html', post=post)

    def edit(self):
        id = params['id']
        post = Post.find(id)
        
        return render('edit.html', post=post)

    def update(self):
        id = params['id']
        title = params['title']
        author = params['author']
        content = params['content']

        post = Post.find(id)
        post.update({'title':title, 'author':author, 'content':content})

        return redirect('/')

    def destroy(self):
        id = params['id']
        post = Post.find(id)
        post.destroy()
        return redirect('/')
