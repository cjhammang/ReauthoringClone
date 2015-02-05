# Reauthoring: A Toolkit to create Liquid HTML Learning Resources

Welcome to Reauthoring, a toolkit to create learning resources in Liquid HTML
(automatically adapts to the size and type of device) with active components
such as videos and multiple choice questions. The functionality is an extension
of [Sphinx-doc](http://sphinx-doc.org) and the idea is to create HTML documents
with active components that render nicely in both computer and mobile browsers.

The best way to start is by looking at pages generated by the toolkit. Take a
look at the site created with
[this project and the toolkit](http://abelardopardo.com/Reauthoring). Check out
the link at the upper right corner of each page, it shows the source document
from which the page was obtained. Check the same URL with a mobile device
(phone, tablet).

If you liked the look and feel of that site and want to try it yourself, follow
the steps to install a few tools, get ready to type commands in a window, and
create your own set of HTML pages.

## Steps to install the Authoring Toolkit


### Install Python (2.7.9) and Sphinx (latest version)

[Install Python and Sphinx](http://sphinx-doc.org/latest/install.html)

---
 
### Install sphinx_rtd_theme

Open a command window and type:

`pip install sphinx_rtd_theme`

You may check the
[instructions to install Sphinx RTD Theme](https://github.com/snide/sphinx_rtd_theme)

---

### Create a sample site

The sample site is available through [this bitbucket reauthoring repository](https://bitbucket.org/abelardopardo/reauthoring)

1. Go to https://bitbucket.org/abelardopardo/reauthoring/downloads
  
2. Download the repository. 
  
3. Unpack the ZIP in a folder in your own computer (in which you have installed
   Sphinx). Alternatively to these steps you can clone the repository with
   `git` (if you don't know what this means, doesn't matter).
    
4. Open a command window in your computer.
  
5. Go to the folder where you downloaded and expanded the repository. There
   should be a file called `conf.py` in that folder.
       
6. Type the command `make html` in the command window
	   
7. Open the browser and look at the file _build/html/index.html that was
   created in that same folder. You should be looking at a sample of pages
   created using the authoring toolkit. Go ahead, modify them, type again the
   `make html` command and a new version is ready.

Happy designing!
