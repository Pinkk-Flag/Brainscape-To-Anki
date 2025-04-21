# Brainscape-To-Anki
Anki Addon that converts Brainscape Flashcards to Anki Flashcards

# How to install

1. Paste this code into the addon area:
```
403833522
```
2. Restart anki
3. Go to the tools header
4. Click on **Brainscape to Anki**
5. Paste the URL (in this format for example: https://www.brainscape.com/flashcards/topic-8-particle-nuclear-7466676/packs/9913339)
6. Type the location where you want it
7. Done!

# Issues
If there are any issues, don't hesitate to reach out to me to fix the code.

Regards,
DG

### Changelog

v1.0.0 (Initial): Supports basic functionality with the fundamental ability to convert all of the flashcards in a Brainscape pack into an Anki deck.

v1.1.0: Due to a few user requests, additional functionality of images have also been added! I.e. if there are any images within the flashcard, it will also be added to the flashcard within anki. Another request was to support functionality of line breaks within the flashcard that are on Brainscape, but aren't visible on the new Anki deck. This new version supports this and adds the line break to look closest to the brainscape pack as possible. 

v1.1.1: Major bug fixes. Recently, I suspect that brainscape must've added some protection in order to stop webscraping, so this new patch should solve those problems (for now). Extremely sorry for the delayal, I was not aware of this until recently.

v.1.1.2: Major bug fixes. Previously program only loads the first 24 or so flashcards due to changes in the website. Now, should be able to handle lazyloaded content. 
