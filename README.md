noodle
======

A Python Web Framework

## [文档](https://github.com/jungledrum/noodle/wiki/%E8%93%9D%E5%9B%BE)

主要仿照rails和django的一款快速开发框架，MVC对应django中的MTV。
模板采用Mako，ORM采用SQLAlchemy，使用Werkzeug库用于处理HTTP。最终会设计成插件的形式，小则如flask，webpy一样轻量级，由用
户随意替换去除ORM，模板等，大则如django，集成常用插件帮助用户快速构建应用。
目前实现的功能主要是request，response，session，cookie，路由，防止CSRF等基本功能，ORM和模板的简单集成，多线程的支持。

练手之作，无创新之处，未来大概也是为了自己用着趁手，改起来也方便。
