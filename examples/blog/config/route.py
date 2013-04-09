rule('/', 'get', 'posts#index')
rule('/login',    'get',    'login#new')
rule('/login',    'post',   'login#create')
rule('/logout',   'get',    'login#logout')

resources('posts')
