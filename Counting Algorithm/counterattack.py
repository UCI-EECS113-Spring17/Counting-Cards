import cv2
import matplotlib.pyplot as plot
import numpy as np
from pynq import Overlay
from pynq.board import Button
from pynq.board import RGBLED
from pynq.board import LED
from pynq.board import Switch
from time import sleep

DECK_MAP = (1, 2, 6, 8) # Number of decks corresponding to switch positions.
THRESH = 0.5 # Confidence threshold for player detection (0.0 - 1.0).


Overlay("base.bit").download()


class CounterAttack(object):
    
    # Count for each rank.
    hilo = (-1, 1, 1, 1, 1, 1, 0, 0, 0, -1, -1, -1, -1)
    
    def __init__(self, decks=1, threshold=0.5):
        
        self.cards = []
        self.new_player()
        self.threshold = threshold
        self.decks = decks
        self.shuffle()

    def calculate(self, chips=0):

        # Some chips were covered. Update.
        if not self.bet_history: raise Exception("Start of hand not captured correctly.")
        if self.bet_history[-1] < chips and chips < 2 * self.bet_history[-1]: self.bet_history[-1] = chips # TODO: Length.

        # Calculate player_rating.
        if len(set(self.bet_history)) > 1: self.player_rating = np.corrcoef(self.bet_history, self.count_history)[0][1] # TODO: Length
        else: self.player_rating = 0.0

    def count(self, cards, chips): # A = 1, J = 11, Q = 12, K = 13.
        """Process game data and output results formatted for RGB LEDs."""
        
        output = [0, 0]
        
        # Hand has not begun.
        if not self.cards and not cards: pass
        
        # Hand has just begun.
        elif cards and not self.cards:
            
            print("NEW HAND")
            self.cards = cards
            self.bet_history.append(chips)
            self.count_history.append(self.true_count)
            self.calculate()

        # Hand has just ended.
        elif self.cards and not cards:
            
            self.shoe -= len(self.cards)
            for card in [x for x in self.cards if x in range(1,14)]: self.running_count += self.hilo[card - 1] # TODO: Length.
            self.cards = []
            
            if self.shoe <= 0: raise ShuffleError()
            else: self.true_count = 52 * self.running_count / self.shoe
        
        # cards is set or subset of self.cards. Perhaps some are covered or removed. Check chips.
        elif all([cards.count(card) <= self.cards.count(card) for card in set(cards)]): self.calculate(chips) # TODO: Length.

        # cards contains some not in self.cards. Add them. Check chips.
        else:

            for card in range(1, 13): 
                new = cards.count(card) - self.cards.count(card)
                if new > 0: self.cards += new * [card] # Add new cards.
            self.calculate(chips)

        if self.player_rating < self.threshold: output[0] += 2 # Green.
        if self.player_rating > -self.threshold: output[0] += 4 # Red.
        if self.true_count < 2: output[1] += 2 # Green.
        if self.true_count > -1: output[1] += 4 # Red.
                  
        if self.bet_history and self.cards: print("MEMORY:", self.cards, self.bet_history[-1])
        else: print("MEMORY: [] 0")
        
        return output

    def new_player(self):
        """Reset player history."""
        
        self.player_rating = 0.0
        self.count_history = []
        self.bet_history = []
    
    def shuffle(self):
        """Reset deck."""
        
        self.shoe = 52 * self.decks
        self.running_count = 0.0
        self.true_count = 0.0


class ShuffleError(Exception): pass


def monitor():
    """Monitor a blackjack game."""

    ranks = [2, 3, 4, 5, 6, 7, 7, 8, 9, 10, 11, 1, 1] 

    classifiers = [cv2.CascadeClassifier("classifiers/2.xml"),
                   cv2.CascadeClassifier("classifiers/3.xml"),
                   cv2.CascadeClassifier("classifiers/4.xml"),
                   cv2.CascadeClassifier("classifiers/5.xml"),
                   cv2.CascadeClassifier("classifiers/6.xml"), # Some errors.
                   cv2.CascadeClassifier("classifiers/7l.xml"),
                   cv2.CascadeClassifier("classifiers/7r.xml"),
                   cv2.CascadeClassifier("classifiers/8.xml"),
                   cv2.CascadeClassifier("classifiers/9.xml"), # Some errors.
                   cv2.CascadeClassifier("classifiers/10.xml"),
                   cv2.CascadeClassifier("classifiers/face.xml"),
                   cv2.CascadeClassifier("classifiers/a.xml"), # Some errors.
                   cv2.CascadeClassifier("classifiers/as.xml")] # Some errors. 
    
    chip_classifier = cv2.CascadeClassifier("classifiers/chip.xml")

    def process(img, upper, lower):
        """Detect cards and chips."""
        
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
        detects = []
    
        for index in range(len(ranks)):
        
            try: detects.append(classifiers[index].detectMultiScale(gray, scaleFactor=1.05, minNeighbors=4, maxSize=upper, minSize=lower))
            except: detects.append([])
                
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2.5, 25, minRadius=20, maxRadius=30)
                
        widths = []
        heights = []
        
        out = [[], 0]
        
        index = 0
        windows = []
        
        for found in detects[:-2]:
            
            out[0] += [ranks[index]] * len(detects[index])
            index += 1
            
            for (x, y, w, h) in found: 
                
                widths.append(w)
                heights.append(h)
                windows.append((x, y, w, h))
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 5) 
                
        for found in detects[-2:]: 
            
            for (x, y, w, h) in found:
            
                if any([x + w / 2.0 >= xx 
                        and x + w / 2.0 <= xx + ww 
                        and y + h / 2.0 >= yy 
                        and y + h / 2.0 <= yy + hh 
                        for (xx, yy, ww, hh) in windows]): 
                    
                    continue

                out[0] += [1]
                widths.append(w)
                heights.append(h)

                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 5)
        
        if circles is not None: 
            
            circles = np.round(circles[0, :]).astype("int")
        
            for (x, y, r) in circles: 

                if any([x >= xx 
                        and x <= xx + ww 
                        and y >= yy 
                        and y <= yy + hh 
                        for (xx, yy, ww, hh) in windows]): 

                    continue

                cv2.circle(image, (x, y), r, (255, 0, 255), 4)
                out[1] += 1
            
        if widths and heights: 
            
            upper = (max(widths) + 10, max(heights) + 6)
            lower = (min(widths) - 10, min(heights) - 6)
        
        plot.imshow(image)
        plot.show()
        print("CURRENT:", out[0], out[1])
        
        return out[0], out[1], upper, lower
    
    def update():
        """Clear all history and update number of decks."""

        state = 2 * switches[1].read() + switches[0].read()
        [leds[led].write(led <= state) for led in range(len(leds))]
        
        return CounterAttack(DECK_MAP[state], THRESH)
    
    error_messages = ("[OK]", "[HANDLING FAILED]", "[ATTEMPTING TO HANDLE]", "", "[HANDLED]")
    exit, reset, new_player, shuffle = (Button(button) for button in range(4))
    leds = [LED(led) if led < 4 else RGBLED(led) for led in range(6)]
    switches = [Switch(0), Switch(1)]
    counter = update()
    upper, lower = (150, 90), (50, 30)
    
    error = 0

    while not exit.read():

        try:
            
            if reset.read(): counter = update()
            elif new_player.read(): counter.new_player()
            elif shuffle.read(): counter.shuffle()

            success = False
            cam = cv2.VideoCapture(0)
            while not success: success, img = cam.read()
            cam.release()
            
            detected, chips, upper, lower = process(img, upper, lower)
            
            colors = counter.count(detected, chips)
            
            leds[4].write(colors[0])
            leds[5].write(colors[1])

            if error:
                
                error = 0
                print(error_messages[error])

        except ShuffleError: 

            if error: error = 1
            else: error = 4
            print("SHUFFLE REQUIRED.", error_messages[error])

        except Exception as exception:

            if error: error = 1
            else: error = 2
            print(exception, error_messages[error])

        finally:
            
            if error:

                [led.off() for led in leds[:5]]

                wait = 0

                # Toggle RGBs blue and relevant button LEDs
                while not any(button.read() for button in (exit, reset, None, shuffle)[:error] if button): # TODO: Length.

                    if not wait % error:
                        [led.write(not led.read()) for led in leds[4:6]]
                        [leds[led].toggle() for led in range(error) if led != 2]