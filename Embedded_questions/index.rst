.. _Embedded-MCQ:

=============================================
 Multiple Choice Questions Embedded in Notes
=============================================

This extension is one of the classics: multiple choice questions. It allows to
include the questions in the middle of the notes for formative assessment
purposes. Students can then answer these questions at any point in time, and
check immediately their answers. This is how you write on of these questions::

  .. eqt:: COD-integerencoding-videoeqt-eqt_11

     **Question 1** What is the representation of the number -127 in 2s
     complement with 8 bits? 

     A) :eqt:`I` `1000 0000`

     #) :eqt:`I` `1111 1111`

     #) :eqt:`C` `1000 0001`

     #) :eqt:`I` None of the above

Make sure the string that follows the `.. eqt::` directive is unique throughout
your documents. Can you spot which answer is marked as the correct one? After
processing, the result is:

.. eqt:: COD-integerencoding-videoeqt-eqt_11

   **Question 1** What is the representation of the number -127 in 2s
   complement with 8 bits? 

   A) :eqt:`I` `1000 0000`

   #) :eqt:`I` `1111 1111`

   #) :eqt:`C` `1000 0001`

   #) :eqt:`I` None of the above

Go ahead, answer it! The question is translated to the proper HTML, the right
scripts inserted, and everything handled properly as specified by the
markup.

Check the following document for an example of a file containing **only**
questions of this type.

.. toctree::
   
   sample_eqt
