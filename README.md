# Counting-Cards
# Overview
 
The main purpose of this device is to monitor a game of blackjack and detect potential card counters who might erase or negate any potential profits for the casino hosting the game. Our device carries out this process by using a webcam and object recognition algorithms to detect individual chips and cards on the playing table. Once this data is captured, onboard algorithms calculate the correlation between the player’s bets and the remaining cards in the deck to calculate the likelihood that the player is counting cards with the intent of removing or reversing the house’s advantage in the game.
 
# Required Peripherals
 
The only peripheral required for this project (other than all of the onboard switches, buttons, and LEDs) is a USB webcam. This is used to collect data, such as bet sizes and cards played, from the game being monitored below.
 
# Project Features
 
Easy to comprehend real-time LED feedback on deck “heat” and probabilistic likelihood that the player is counting cards, with adjustable threshold for detection.
 
Support for any number of decks (current configuration allows 1, 2, 6, or 8 decks to ensure compatibility with most Las Vegas blackjack tables, but other values can easily be programmed) with real-time LED feedback on how many decks are currently in play.
 
Dedicated buttons for shuffling, new player, resetting, and exiting the session.
 
Robust error handling with LED feedback for various issues. Most common errors only require a deck shuffle or a session restart, with very few resulting in outright termination of the program.
 
# Responsibilities & Contributions
 
The labor this project is split into three modular components:
 
***Image Processing***
 
- Syed Omer Azeemuddin & Rudy Aquino
 
***Object Recognition***
 
- Cheng Zhu & Brandt Bucher
 
***Data Processing & Feedback***
 
- Brandt Bucher
 
#   Image Processing
 
This stage of the project is tasked with setting up the webcam and using openCV to process the images. The webcam must be able to effectively capture the cards being dealt and chips being spent in real time, and at a sufficiently high resolution. 
 
# Object Recognition
 
The object recognition algorithms in use must be capable of actually making the cards and chips recognizable to the system. This is done by training a Haar cascade classifier with thousands of positive (including target objects) and negative (excluding target objects) images using OpenCV, which should determine the cards and chips in play and forward the information to the onboard algorithm.
 
# Data Processing & Feedback
 
The bulk of our code is devoted to quickly and efficiently processing the incoming data to determine what cards remain in the deck, and correlating this information with the player’s betting history. If the player has a history of betting more when higher-valued cards remain in the deck (and vice-versa), it is extremely likely that the player is secretly counting cards. Direct user inputs and outputs are handled through all of the onboard buttons, switches, and LEDs.
 
# Original Work Schedule
 
***Weeks 2 & 3***
 
- Brainstorm the project idea and begin implementation.
 
***Week 4***
 
- Start Haar cascade classifier training on Windows, develop onboard algorithms and image capturing in Python. 
 
***Week 5***
 
- Start Haar cascade classifier training on Linux, keep working on onboard algorithm and image processing.
 
***Week 6***
 
- Improve classifiers in order to recognize cards and chips with less than 10% error rate.
 
***Week 7***
 
- Build mounting apparatus and have whole system (imaging, detection, and processing) working together.
 
***Week 8***
 
- Fine-tune system to reduce errors, and make processes more efficient with respect to time and memory.
 
***Weeks 9 & 10***
 
- If time allows, implement additional features:
 
- Recognize overlapping cards.
 
- Detect different denominations of chip ($1, $5, $25, $100, etc...).
 
- Use a second, table-level camera to support stacks of chips.
 
# End Result
 
The USB webcam is suspended approximately 2.5 feet above the table, pointed down, using a modified microphone stand. The card classifiers detect and recognize the horizontally placed cards by recognizing and analyzing their centers. We found this to be faster and more accurate than analyzing the corner of the card or the card as a whole. Additionally, this allows for partial overlapping of cards as long as the middle is not obstructed. Cards must be placed horizontally in the camera’s field of view, and chips must be laid out individually. This version is calibrated for Bicycle Jumbo Playing Cards and any circular 1” - 2” chips.
 
For the chips, we utilize openCV’s Hough circle transform function to detect circles, rather than using color detection. We then count these circles to determine how much the player has bet. We found our previous method of chip counting (edge and color detection) to be inconsistent due to variable lighting conditions. 
 
The program handles false negatives for both cards and chips by keeping a running memory of the cards played during each hand. This memory can be added to by subsequent frames, but is only cleared when the hand is finished and no more cards are detected. In this way, it is both quick and accurate. 
 
The initial “calibration” frame may take over thirty seconds to output, as the program is establishing the optimal classifier size in order to make resource-intensive processing of subsequent frames as fast as possible. After this, the program outputs frames at a rate of approximately one frame every five seconds.
 
# Controls
	
***Switches***

The switches are used to set the number of decks being used in the game. Currently, they are configured as:
 
- Down / Down: One deck (lights one green LED to signal status).
- Down / Up: Two decks (lights two green LEDs to signal status).
- Up / Down: Six decks (lights three green LEDs to signal status).
- Up / Up: Eight decks (lights four green LEDs to signal status).
 
This ensures compatibility with most Vegas games, but can be easily modified to virtually any value (i.e. 4, 1.5, 3.14, 500, 1,000,000, etc.). This is read whenever the system is started or reset.
 
***Buttons:***
 
The buttons are used to control the game itself. Due to the computationally intensive nature of the onboard programming, buttons may need to be pressed for five seconds or more. From left to right:
 
- The leftmost button is pressed whenever the dealer shuffles the deck.
- The next button is pressed whenever a new player is replacing the current one. This clears their betting history while maintaining the present state of the deck.
- The next button resets the game. It updates the deck count (according to the switch configuration, above) and clears the player history.
- The far right button exits the program.
 
***LEDs:***
 
The single-color LEDs are used for feedback on the deck count, as outlined above. The RGB LEDs provide real-time feedback on the outputs of the onboard algorithms:
 
The left LED indicates the “heat” of the current deck. When green, the deck favors the casino, but when red, it favors the player. It is advantageous for the dealer to shuffle the deck when this LED is red. Yellow is neutral.
 
The right LED indicates the probabilistic likelihood that the player is counting cards. When green, the player is playing badly and strongly helping the casino, but when red, their betting style indicates there is a very good chance that they are counting cards. It is advantageous to remove the player from the game when this LED is red. Yellow is neutral, and is the most common state of this LED.
 
In addition to these uses, both leds briefly blink blue whenever a new frame is captured.
 
***Errors:***
 
Our project features robust error handling in order to make the game as easy as possible for the users. Whenever the system detects an issue, the RGB LEDs flash bright blue, and the LEDs flash above whatever buttons the user can press to resolve the error. For example, if perhaps the dealer forgot to press the shuffle button when they shuffled recently, the system will prompt them to press the shuffle button. For other, unknown exceptions, the system will prompt them to either reset or exit the game, based on the severity of the issue.
