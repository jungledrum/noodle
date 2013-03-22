
class PostsController(ControllerBase):
    
  def index(self):
    posts = Post.all()
    return render('index.html', {'posts':posts})

  def new(self):
    return render('new.html', {})
  
  def create(self):
    title = params['title']
    author = params['author']
    content = params['content']

    post = Post(title, author, content)
    post.save()

    return redirect('/')

  def show(self):
    id = path_params[':id']
    post = Post.find(id)

    return render('show.html', {'post':post})

  def edit(self):
    id = path_params[':id']
    post = Post.find(id)
    
    return render('edit.html', {'post':post})

  def update(self):
    id = path_params[':id']
    title = params['title']
    author = params['author']
    content = params['content']

    post = Post.find(id)
    post.update({'title':title, 'author':author, 'content':content})

    return redirect('/')

  def destroy(self):
    body = '---destroy---'
    response = Response(body, mimetype='text/html')
    return response
