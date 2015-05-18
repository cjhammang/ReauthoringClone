**********************************
Embedding Youtube Videos in a page
**********************************

This extension is to simplify the inclusion of videos already existing in
YouTube as part of your notes. The videos are included in the way you usually
see them in regular web pages. Here is an example of the markup you would use
in your source files::

  .. embedded-video:: SeoW3YNo3Zs

The string following the two colons is the identifier that YouTube attaches to
any video. You may find this identifier as part of the URL that appears in your
browser when watching it. Here is the result:

.. embedded-video:: SeoW3YNo3Zs

You can also select just a segment of the video to be presented by optionally specifying a start and end time (in seconds).  The player will start playing at the given time, and will stop at the end time.  Here is an example of the markup you would use to specify only the start of the video segment (at 120 seconds or 2 minutes)::

  .. embedded-video:: SeoW3YNo3Zs 120  
  
Here is an example that specify both the start and the end of the segment::

  .. embedded-video:: SeoW3YNo3Zs 120 140
  
The result of this last command is:

.. embedded-video:: SeoW3YNo3Zs 120 140

If you create and upload your own videos in YouTube, remember that the platform
collects some interesting data about how the videos are used. The following
document is an example of a file containing several videos.

.. toctree::

   sample_video