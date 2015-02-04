:orphan:

You may want to us this folder as a stand alone place holder for Sphinx macros. If that is
so, you need to perform a **sparse checkout** with git.
`The steps to do a sparse clone are as follows <http://stackoverflow.com/a/13738951>`_::

   git clone <repo>
   cd <repo>

This creates a repository with your remote. Then do::

   git config core.sparsecheckout true

Now define which files/folders you want to check out by listing them in 
 ``.git/info/sparse-checkout``::

   echo "/some/dir" >> .git/info/sparse-checkout
   echo "/another/sub/tree" >> .git/info/sparse-checkout

Update the repository with the directories just selected:: 

   git read-tree -m -u HEAD
