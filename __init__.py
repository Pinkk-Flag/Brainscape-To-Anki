from aqt import mw
from aqt.qt import QAction, QInputDialog
from aqt.utils import showInfo
from anki.notes import Note
from bs4 import BeautifulSoup
import requests
import os
import re

def sanitize_filename(filename):
    return re.sub(r'[^\w\-_\. ]', '_', filename)

def fetch_and_create_deck():

    url, ok = QInputDialog.getText(mw, "Brainscape to Anki", "Please enter the URL to the Brainscape flashcards:")

    if not ok or not url:
        showInfo("No URL provided. Operation canceled.")
        return

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        showInfo(f"Failed to fetch the flashcards: {e}")
        return

    soup = BeautifulSoup(response.content, "html.parser")

    card_text = []
    card_answer = []
    n = 0

    flashcard_elements_scf = soup.find_all("div", class_="scf-face")

    for flashcard in flashcard_elements_scf:
        try:

            raw_html = flashcard.decode_contents()
            temp = BeautifulSoup(raw_html, "html.parser")

            for img in temp.find_all("img"):
                img_url = img["src"]
                img_name = sanitize_filename(os.path.basename(img_url))
                img_path = os.path.join(mw.col.media.dir(), img_name)

                try:
                    img_data = requests.get(img_url).content
                    with open(img_path, "wb") as f:
                        f.write(img_data)
                    img['src'] = img_name
                except Exception as e:
                    showInfo(f"Failed to download or save image: {e}")
                    img.decompose()

            processed_text = str(temp).replace("<br>", "\n")

            if n % 2 == 0:
                card_text.append(processed_text)
            else:
                card_answer.append(processed_text)
            n += 1
        except Exception as e:
            showInfo(f"Error parsing flashcard: {e}")

    flashcard_elements_card = soup.find_all("div", class_="card-face")

    for flashcard in flashcard_elements_card:
        try:

            raw_html = flashcard.decode_contents()
            temp = BeautifulSoup(raw_html, "html.parser")

            for img in temp.find_all("img"):
                img_url = img["src"]
                img_name = sanitize_filename(os.path.basename(img_url))
                img_path = os.path.join(mw.col.media.dir(), img_name)

                try:
                    img_data = requests.get(img_url).content
                    with open(img_path, "wb") as f:
                        f.write(img_data)
                    img['src'] = img_name
                except Exception as e:
                    showInfo(f"Failed to download or save image: {e}")
                    img.decompose()

            processed_text = str(temp).replace("<br>", "\n")

            if n % 2 == 0:
                card_text.append(processed_text)
            else:
                card_answer.append(processed_text)
            n += 1
        except Exception as e:
            showInfo(f"Error parsing flashcard: {e}")

    new_deck, ok = QInputDialog.getText(mw, "Brainscape to Anki", "What would you like to call this new deck?")

    if not ok or not new_deck:
        showInfo("No deck name provided. Operation canceled.")
        return

    deck_id = mw.col.decks.id(new_deck)
    showInfo(f"Created {new_deck}")

    model = mw.col.models.byName("Basic")
    if not model:
        showInfo("Model 'Basic' not found. Operation canceled.")
        return

    for i in range(len(card_text)):
        note = Note(mw.col, model)
        note["Front"] = card_text[i]
        note["Back"] = card_answer[i]
        mw.col.add_note(note, deck_id)

    mw.col.reset()
    mw.reset()
    showInfo(f"The end, check your Anki now for the deck called {new_deck}. Thank you, made by Dario G :]")

action = QAction("Brainscape to Anki", mw)
action.triggered.connect(fetch_and_create_deck)
mw.form.menuTools.addAction(action)
