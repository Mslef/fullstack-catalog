# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Category, Base, Item, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def createCategory(name):
    category = Category(name = name, user_id = 1)
    session.add(category)
    session.commit()
    return category

def createItem(name, description, image_url, category):
    item = Item(name = name, description = description, image_url=image_url, category = category, user_id = 1)

    session.add(item)
    session.commit()

def createAdmin(name, email):
    user = User(name = name, email = email, admin = True)
    session.add(user)
    session.commit()

#Categories
category1 = createCategory("Javascript Front End Frameworks")

createItem("jQuery", '''jQuery is a fast, small, and feature-rich JavaScript library.
    It makes things like HTML document traversal and manipulation, event handling,
    animation, and Ajax much simpler with an easy-to-use API that works across a
    multitude of browsers. With a combination of versatility and extensibility,
    jQuery has changed the way that millions of people write JavaScript.''',
    "http://upload.wikimedia.org/wikipedia/en/9/9e/JQuery_logo.svg", category1)


createItem("Angular", '''HTML is great for declaring static documents, but it falters when we try to use it for declaring dynamic views in web-applications. AngularJS lets you extend HTML vocabulary for your application. The resulting environment is extraordinarily expressive, readable, and quick to develop.''', "http://upload.wikimedia.org/wikipedia/commons/c/ca/AngularJS_logo.svg", category1)

createItem("Knockout", '''Knockout is a standalone JavaScript implementation of the Model-View-ViewModel pattern with templates. The underlying principles are therefore a clear separation between domain data, view components and data to be displayed the presence of a clearly defined layer of specialized code to manage the relationships between the view components. The latter leverages the native event management features of the JavaScript language. These features streamline and simplify the specification of complex relationships between view components, which in turn make the display more responsive and the user experience richer. Knockout was developed and is maintained as an open source project by Steve Sanderson, a Microsoft employee. As the author said, "it continues exactly as-is, and will evolve in whatever direction I and its user community wishes to take it", and stressed, "this isn't a Microsoft product".''', "http://knockoutjs.com/img/ko-logo.png", category1)

createItem("Backbone", '''Backbone.js gives structure to web applications by providing models with key-value binding and custom events, collections with a rich API of enumerable functions, views with declarative event handling, and connects it all to your existing API over a RESTful JSON interface.''',
    "http://backbonejs.org/docs/images/backbone.png", category1)

category2 = createCategory("Python Web Libraires")

createItem("Django", '''Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It's free and open source.''',
    "http://upload.wikimedia.org/wikipedia/commons/7/75/Django_logo.svg", category2)

createItem("Flask", '''Flask is a micro web application framework written in Python and based on the Werkzeug toolkit and Jinja2 template engine. It is BSD licensed. As of 2015, the latest stable version of Flask is 0.10.1. Examples of applications that make use of the Flask framework are Pinterest, LinkedIn, as well as the community web page for Flask itself. Flask is called a microframework because it does not presume or force a developer to use a particular tool or library. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. However, Flask supports extensions that can add application features as if they were implemented in Flask itself. Extensions exist for object-relational mappers, form validation, upload handling, various open authentication technologies and several common framework related tools.''', "http://upload.wikimedia.org/wikipedia/commons/3/3c/Flask_logo.svg", category2)

createItem("SQLAlchemy", '''SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL. It provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.''', "http://www.sqlalchemy.org/img/sqla_logo.png", category2)

category3 = createCategory(name = "CSS Preprocessors")

createItem("Sass", '''Sass (Syntactically Awesome Stylesheets) is a stylesheet language initially designed by Hampton Catlin and developed by Natalie Weizenbaum. After its initial versions, Weizenbaum and Chris Eppstein have continued to extend Sass with SassScript, a simple scripting language used in Sass files. Sass is a scripting language that is interpreted into Cascading Style Sheets (CSS). SassScript is the scripting language itself. Sass consists of two syntaxes. The original syntax, called "the indented syntax", uses a syntax similar to Haml. It uses indentation to separate code blocks and newline characters to separate rules. The newer syntax, "SCSS", uses block formatting like that of CSS. It uses braces to denote code blocks and semicolons to separate lines within a block. The indented syntax and SCSS files are traditionally given the extensions .sass and .scss respectively.''',
    "http://sass-lang.com/assets/img/logos/logo-b6e1ef6e.svg", category3)

createItem("Less", '''Less (sometimes stylized as LESS) is a dynamic stylesheet language that can be compiled into Cascading Style Sheets (CSS), or can run on the client-side and server-side. Designed by Alexis Sellier, Less is influenced by Sass and has influenced the newer "SCSS" syntax of Sass, which adapted its CSS-like block formatting syntax. Less is open-source. Its first version was written in Ruby, however in the later versions, use of Ruby has been deprecated and replaced by JavaScript. The indented syntax of Less is a nested metalanguage, as valid CSS is valid Less code with the same semantics. Less provides the following mechanisms: variables, nesting, mixins, operators and functions; the main difference between Less and other CSS precompilers being that Less allows real-time compilation via less.js by the browser.''',
    "http://upload.wikimedia.org/wikipedia/commons/8/81/LESS_Logo.svg", category3)

category4 = createCategory(name = "CSS Frameworks")

createItem("Bootstrap", '''Bootstrap is a free and open-source collection of tools for creating websites and web applications. It contains HTML- and CSS-based design templates for typography, forms, buttons, navigation and other interface components, as well as optional JavaScript extensions. The bootstrap framework aims to ease web development. Bootstrap is a front end, that is an interface between the user and the server-side code which resides on the "back end" or server. And it is a web application framework, that is a software framework which is designed to support the development of dynamic websites and web applications.''',
    "http://upload.wikimedia.org/wikipedia/commons/e/ea/Boostrap_logo.svg", category4)

createItem("Foundation", '''Foundation is a responsive front-end framework. Foundation provides a responsive grid and plenty of HTML and CSS UI components, templates, and code snippets, including typography, forms, buttons, navigation and other interface components, as well as optional JavaScript extensions. Foundation is maintained by zurb.com  and is an open source project.''',
    "http://foundation.zurb.com/assets/img/zurb-logo.svg", category4)

category5 = createCategory(name = "PHP frameworks")

createItem("Laravel", '''Laravel is a free, open source PHP web application framework, designed for the development of model-view-controller (MVC) web applications. Laravel is released under the MIT License, with its source code hosted on GitHub. According to a December 2013 developers survey on PHP frameworks popularity, Laravel was listed as the most popular PHP framework of 2013, followed by Phalcon, Symfony2, CodeIgniter and others. As of August 2014, Laravel is the most popular and watched PHP project on GitHub.''',
    "http://upload.wikimedia.org/wikipedia/commons/3/3d/LaravelLogo.png", category5)

category6 = createCategory(name = "SQL Databases")

createItem("MySQL", '''MySQL is (as of July 2013) the world's second most widely used relational database management system (RDBMS) and most widely used open-source RDBMS. It is named after co-founder Michael Widenius's daughter, My. The SQL acronym stands for Structured Query Language. The MySQL development project has made its source code available under the terms of the GNU General Public License, as well as under a variety of proprietary agreements. MySQL was owned and sponsored by a single for-profit firm, the Swedish company MySQL AB, now owned by Oracle Corporation.''', "http://upload.wikimedia.org/wikipedia/en/6/62/MySQL.svg", category6)

createItem("SQLite", '''SQLite is a relational database management system contained in a C programming library. In contrast to many other database management systems, SQLite is not a client-server database engine. Rather, it is embedded into the end program. SQLite is ACID-compliant and implements most of the SQL standard, using a dynamically and weakly typed SQL syntax that does not guarantee the domain integrity. SQLite is a popular choice as embedded database software for local/client storage in application software such as web browsers. It is arguably the most widely deployed database engine, as it is used today by several widespread browsers, operating systems, and embedded systems, among others.[6] SQLite has bindings to many programming languages.''',
    "http://upload.wikimedia.org/wikipedia/commons/3/38/SQLite370.svg", category6)

createItem("PostgreSQL", '''PostgreSQL, often simply "Postgres", is an object-relational database management system (ORDBMS) with an emphasis on extensibility and standards-compliance. As a database server, its primary function is to store data securely, supporting best practices, and to allow for retrieval at the request of other software applications. It can handle workloads ranging from small single-machine applications to large Internet-facing applications with many concurrent users. Recent versions also provide replication of the database itself for availability and scalability.''', "http://upload.wikimedia.org/wikipedia/commons/2/29/Postgresql_elephant.svg", category6)
