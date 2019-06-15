# Pycon 2019
https://cz.pycon.org/2019/

## Friday

### Leveraging technology and laziness (keynote)
by Josef Svoboda

- Predicting financial markets is difficult (Duh!)
- "Complexity of solution should match complexity of the problem"
- There are forces pushing solutions to become more complex. There are no such forces pushing complex solutions to simplify.

The presentation wasn't about Python or technology at all


### GitHub bots: Rise of the machines
by Sviatoslav Sydorenko

- Manage changelog by https://pypi.org/project/towncrier/
- Usefull tool, github apps: https://github.com/marketplace
- Github apps have access to more API endpoints that are normally hidden from user
- Use serverles when possible, Github will support natively on their own platform: https://github.com/features/actions


### Time series Forecasting in Python
by Petr Simecek

- The best ML method is worst than the worst from statistical methods (some study)
- statmodels.tsa package for simple models
- Book: Forecasting; principles and practice

1. Remove anomalies
2. Holliday adjustment
3. Take seasonal part

- Facebook opensource forecasting: Prophet
- M3: Theta method - won award as best forcasting method
- M4: Top 50 solutions used ML+statistics
- Dimensionality problem - There are sometimes more variables than entry points
- Lately ML is crushing statistics


### The theory and practice of Generative Adversarial Networks (GANs)
by Jakub Langr

- Introduction to ML


#### Unsupervised learning:

- Eg. Generating pictures of people
- Generator tries to generate data that look real from random seed
- Discriminator tries to guess which of two samples (real data vs. generated) is real
- The error get propagated back to the generator which get better at generating but also to discriminatom which gets better at guessing
- Fitness function for generator is just inverted value of fitness function of the discriminator


### Inheriting code ... and I don't mean classes
by Flavio Pecoco

- What are the use-cases? What does the code supposed to do?
- How where things done? What paradigms it follows?
- Learn how the users are using the software
- Evaluate if rewriting is and viable option
    - Good language/ecosystem
    - Would rewrite be faster
    - Easier to rewrite it?
    - Enable other team members to contribute?
    - Good language/ecosystem
    - Would rewrite be faster
    - Easier to maintain it?
- Write down guidelines
- Document everything
- All existing tests muss past, if the don't exist, write them
- Do small and focused changes
- Take the faster path, not the shortest one


### Debugging binaries with Python
by Pevel Simerda

- `$ gdb -angs ping prgcont.cz`
- No idea what he's talking about


### \#! Bang, Bang!
by Miro Hroncok

- DONT!
- There is no shebang that works the same on all machines
- Self destructing file
- Use setup.py instead


## Saturday

### Parallels between career building and home remodeling (keynote)
by Jakie Kazil

- Ask for informational interview
- You will survive
- Never be afraid of anything
- Be intentional about your direction

#### Excercise

**Priorities**

- teeth
- dog
- dbgr
- driving licence
- muay-thai
- marriage
- work
- granma new knees
- weightloss

**Want to do but not doing right now**

- nothing, I'm doing everything I want


### Electronics with Python for beginners
by Jan Bednarik

- Breadboard - prototyping board
- Digital 0 = 0V, 1 = 3.3V or 5V
- Micropython (Python 3.6)
- Interactive SHELL on the board so you can change the code directly
- Available boards: PyBoard, BBC micro:bit, Pycom.iOT (wifi) Adafruit CircuitPython (CircuitPython = alternative to MicroPython)
- micropython.org/unicorn (interactive tutorial)
- learn.adafruit.com (200 tutorials)
- hackaday website (people share their projects)


### To comment or not? A data-driven look at attitude toward code comments
by Veronica Hanus

- Code tells how, comment tells why
- Be nice to beginner, educate them, you was one too


### A day has only 24+-1 hours
by Miroslav Sedivy

- 440 timezones: `len(pytz.common_timezones)`
- www.iana.org/time-zones


### On the edge of leadership (keynote)
by Miroslav Cimpersak


### Keep formating consistent with Black
by Angelina Nikiforova


### Maintaining peace by preparing for war
by Luka Raljevic


### Intro to search using Python
by Nick Lang


### Performance tuning in Python
by Jan Skoda

