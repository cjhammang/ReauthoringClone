Steps to install the Authoring Toolkit
======================================

1. Install Python (2.7.9) and Sphinx (latest version)

   http://sphinx-doc.org/latest/install.html#windows-install-python-and-sphinx
 
2. Install sphinx_rtd_theme

   Open a command window and type:

   pip install sphinx_rtd_theme
   https://github.com/snide/sphinx_rtd_theme

3. How to create the sample site

   - Go to https://bitbucket.org/abelardopardo/reauthoring/downloads
   - Download the repository.
    - Unpack the ZIP in a folder in your own computer (in which you have installed Sphinx)
    - Open a command window in windows
    - Go to the folder where you downloaded the repository. There should be a file called 
      conf.py in that folder.
    - Type the command "make html" in the command window
    - Open the browser and look at the file _build/html/index.html that was created in that 
      same folder. You should be looking at a sample of a set of pages created using the
      authoring toolkit. 

Happy designing!
