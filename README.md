Sat Sep 29 10:37:33 EDT 2018


# License Notes on various parts:

  - png/* art/* (see AUTHORS file):

    - some files taken from gfpoken/png or gfpoken/art
      - licensed GPL v2
      - then scaled up to 64 x 64 pixels
        - is this really any kind of change needing a copyright?
          don't think so...

    - some png/ files modified by me 
      - changes can go under GPL v2 or Unlicense
        see bits-of-gfpoken project...

    - some made by me (in png/)
      - nothing major but they can all go under Unlicense
        solid color background files, a few cubes and ...

  - code created by me *.py
    - all under Unlicense

  - document and administrivia files
    - this README.md, TODO.md and AUTHORS
      - all under Unlicense


# General Information:

ngfp aka new gfpoken aka gfpoken-in-python is my learning project for python, 
pyglet and many other things (I'm not that familiar with git or Debian 
packaging and ...).  So be gentle with me here ok?  :)


To make spacing consistent I've used:

  to see what the changes would look like:

 $ autopep8 . --recursive --select=E101,E121 --diff

  to make the changes:

 $ autopep8 . --recursive --select=E101,E121 --in-place


