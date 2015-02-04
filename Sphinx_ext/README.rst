:orphan:

You may want to us this folder as a stand alone place holder for Sphinx macros. If that is
so, you need to perform a **sparse checkout** with git.
`The steps to do a sparse clone are as follows <http://stackoverflow.com/a/13738951>`_::

   git init <repo>
   cd <repo>
   git remote add -f origin <url>

This creates an empty repository with your remote. Then do::

   git config core.sparsecheckout true

Now you need to define which files/folders you want to actually check out. 
This is done by listing them in .git/info/sparse-checkout, eg::

   echo "some/dir/" >> .git/info/sparse-checkout
   echo "another/sub/tree" >> .git/info/sparse-checkout

Last but not least, update your empty repo with the state from the remote::

   git pull origin master

Source: `Post by Chronial in Stackoverflow.com <http://stackoverflow.com/a/13738951>`_
