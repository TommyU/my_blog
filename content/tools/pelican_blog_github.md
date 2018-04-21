Title: github 博客搭建过程
Date: 2015-12-01 10:20
Category: 
Tags: tools
Slug:github-blog-by-pelican
Authors: Tommy.Yu
Summary: blogs
# github 博客搭建过程(pelican)

## 准备工作

### github account
注册帐号， 然后依照这个[指引](https://pages.github.com/)创建一个新的仓库，注意命名（username.github.io）;

### peclian

这是一个基于python2.7(及以上)的静态页生成工具。注意，是静态页。github博客貌似只支持**静态页**。

- install

```
pip install pelican
pip install markdown
```

- 创建blog项目路径，并初始化

```
mkdir my_blog
cd my_blog
pelican-quickstart
```

这样子就会在my_blog路径下敏初始化网站的静态页面结构（初始版），结构如下：

```
├── content  # markdown文件所存放的路径。
├── develop_server.sh  
├── fabfile.py  
├── Makefile  
├── output  #实际生成静态html项目的路径。
├── pelicanconf.py  #配置文件
└── publishconf.py  
```

> 注意，在生成向导中选择好自己的github域名，即:What is your URL prefix? (see above example; no trailing slash) http://username.github.io 。 同时： Do you want to upload your website using GitHub Pages? (y/N) Y

### pelican-themes

pelican搭配使用的主题，大多基于bootstrap进行一定的定制，可以根据喜好选择[相应的风格](http://www.pelicanthemes.com/).

- 下载并注册主题

```
cd ../
git clone https://github.com/getpelican/pelican-themes.git
cd pelican-themes
pelican-themes -i pelican-bootstrap3
```

- 启用主题，编辑上面的pelicanconf.py文件， 添加以下代码

```
THEME='pelican-bootstrap3'
```

### pelican plugins

- 下载插件

```
git clone https://github.com/getpelican/pelican-plugins.git pelican-plugins
```

- adding in pelicanconf.py
   1. 搜索插件依赖库
```shell
pip install beautifulsoup4
```

```pyhton
PLUGIN_PATHS = ['/path/to/git/pelican-plugins', ]
PLUGINS = ['i18n_subsites', ]
JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n', 'tipue_search'],
}
```
>obviously you need to change the '/path/to/git/ part ;)



## 创建第一个页面

```
cd ../my_blog/content
vi hello.md
```

添加以下代码：

```
Title: hello world
Date: 2015-12-03 10:20
Category: Markdown
Tags: Markdown
Slug: my-super-post
Authors: your name
Summary: pelican markdown demo
# hello world
```
保存，退出编辑。

执行以下指令生成html,并运行本地的服务（可以在http://localhost:8000查看效果）
```
cd ../
pelican content/
cd output
python -m pelican.server
```

## 部署

### 手工
上传代码到github对应的仓库

```
git clone git@github.com:username/username.github.io.git
```
> 下载仓库代码(注意username的替换）

在pelican content生成html后， output目录结构（只到3层），如下：

```
├── output  
│   ├── archives.html  
│   ├── author  
│   │   └── your-name.html  
│   ├── authors.html  
│   ├── categories.html  
│   ├── category  
│   │   └── markdown.html  
│   ├── index.html  
│   ├── my-super-post.html  
│   ├── tag  
│   │   └── markdown.html  
│   ├── tags.html  
│   └── theme  
│       ├── css  
│       ├── fonts  
│       ├── js  
│       └── tipuesearch  
```

将output目录下的文件全部拷贝到本地的username.github.io 路径

```
cp -R output/*  username.github.io/
cd username.github.io/
git add .
git commit -a -m 'init'
git push -u origin master
```

打开地址： http://username.github.io 查看效果。

### 自动化
**利用MakeFile一键部署**

生成html，拷贝到git本地目录，然后git commit可以写脚本完成。然而在pelican这里有一个现成的MakeFile文件可以用。 修改下MakeFile，我的demo如下： publish段：增加了cp指令一行，即将生成的html拷贝到本地git路径下。
    
- publish section

```
publish:
        $(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS)
        cp -R $(OUTPUTDIR)/* $(GIT_LOCAL_DIR) 
```

- github section
github段:没用ghp-import指令，懒得安装这个多余的包。作为弥补，修改了publish段，如上。同时增加cd到git路径指令。
```
github: publish
        #ghp-import -m "Generate Pelican site" -b $(GITHUB_PAGES_BRANCH) $(OUTPUTDIR)
        cd $(GIT_LOCAL_DIR)&&git add .&&git commit -a -m '+'&&git push origin $(GITHUB_PAGES_BRANCH)
```
- 部署

```shell
make github 
```
这样以后可以专注于写作。

## 关于搜索功能

由于是静态站，所以搜索的实现落在了客户端。
思路有不外乎：
1. 解析index.html页面并操作dom元素
2. 利用插件生成xml/json格式的sitemap，然后ajax请求这些资源并解析，渲染页面。

我的实现方式是2，利用插件tipue_json在生成html时附带生成一个json文件。
拷贝index.html页，命名为search.html，做少量修改（略）, 然后在里面加入下面这段代码：

```js
<script type="text/javascript">
$(function(){
        do_search();
});

function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function do_search(){
        var result_tmplate="<article><h2><a href='{{url}}'>{{title}}</a></h2></article>";
        var search_target = getParameterByName('q');
        var found_something=false;
        $("#tipue_search_input").val(search_target);
        $.ajax({
          dataType: "json",
          url: "/tipuesearch_content.json",
          success: function(data){
                console.log(data);

                for(var i=0;i<data.pages.length;i++)
                {
                        if(data.pages[i].title.indexOf(search_target)!=-1)
                        {
                                var result_html = result_tmplate.replace("{{title}}", data.pages[i].title).replace("{{url}}", data.pages[i].url)
                                $("#search_result").append(result_html);
                                found_something=true;
                        }
                }
                if(!found_something)
                {
                        $("#search_result").append("<h2>抱歉! 没有找到任何匹配的文章哦。。。</h2>");
                }
          }
        });
}
</script>
```

## 其他
可以根据添加评论系统，第三方图片接入等等。
ps:关于自带的disqus代码可能不是最新的。需要自己更新下，修改下theme主题插件的相关模板。
试用了uyan（友言）和disqus，发现ab测试下，uyan快100毫秒。不过发现了一个虫（删掉文章后，相关文章链接仍然被收藏并显示出来了），最后还是选择了disqus。