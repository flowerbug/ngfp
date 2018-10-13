Sat Oct 13 10:55:04 EDT 2018


v0.1.1 - ?  This TODO

  - comparing boards
    - exact match is easy
    - functional match is harder

  - configuration file

  - load and save any file name at all
    - do a little more basic checks on format/data

  - restructure code (encapsulate, objectify, clean it up, tests and comments)


v0.1.0
  - save and load games the initial simple version (works)
    - load from a gfpoken save file (works)
      - when you save it use file name "save.ngfp"
    - load as json file (works)
      - use file name "save.json"
    - save to json file (works)
      - always overwrites or writes file name "save.json"


    Notes:

      if both files ("save.ngfp" and "save.json") exist for now
    the first one "save.ngfp" is loaded and "save.json" is 
    ignored.  if you only want "save.json" used then, rename 
    "save.ngfp" or remove it.


v0.0.9

  - fix label code a bit (works)
    - can use label.text to change label

  - some animation or way of showing what happens on guess board (works)


v0.0.8

  - a bit of fun showing where the marble is bouncing
    around in the game - this doesn't stay in the final
    version, but i may leave it in as an option/toggle
    anyways because it might help in debugging...


v0.0.7


  - flipping mirrors (3-4,5-8,13-14,17-18,23-30) (works)
  - last two mirrors - they move (works)


v0.0.6

  - some game logic (works)
    - all the easy mirrors (1,2,9,10,11,12,15,16,19,20,21,22) (works)
    - putting a marble in motion (works)
    - detecting where it comes out (works)
    - history with colored markers (works)


v0.0.3-v0.0.5

  - grab widgets and put on guess board (works)
  - update counts text (works)
  - moving items (works)
  - removing items from board to go back to widget piles (works)
  - rotating guesses (works)


v0.0.0 - v0.0.2
  initial import of code so far and a few basic changes



  (I'm not planning on doing networking version at this time)

  Bugs and comments to ant@anthive.com - I'm not always checking
issues here on Salsa as of yet I haven't spent much time figuring
out all the mechanisms of projects/issues/merges/pulls/etc.
