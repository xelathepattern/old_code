This is some of the oldest code I have written, from way back when I was first learning. Some code that was moved to comp_phys is not present.

Some highlights:
crypt contains:
shamir.py, which implements the shamir secret sharing algorithm
cryptModule.py, which is a somewhat consolidated version I made at the time of some past stuff I did before then. The best thing in there is an implementation of Kasiski elimination to crack the Vigenere cipher.

custom-math contains:
fourier, which allowed me to draw with my cursor, and then calculate the fourier series of the path viewed as a function from real valued time to a complex number representing the point on the plane, and then would draw out an animation of summed oscillating circles. I got the inspiration for this from a 3b1b video
wordle, which implements an algorithm to play wordle by trying to maximize the expected information gained each step. I got the inspiration for this from looking at a thumbnail of a 3b1b video, thinking "wait, I know enough to do this!", doing it, then watching the video. Funnily enough, I made the same error he did in implementing the rules. It's also not literally optimal because it maxmizes info gain as opposed to taking it's policy for granted and then trying to maximize winning probability - so it'll 'explore'/'play the early game' too much. In practice, you can do very well at wordle by just maximizing info gain.
julia, which plots and animates some julia sets and multibrot sets under continuous changes in the parameters.
n_body, which is an n_body solver.
typing, which I made to record my progress learning Programmer's Dvorak
misc_short, which has:
rockInduction.py, which tries to do Solomonoff induction on what's basically n-markov models (or at least similar) of what someone playing rock paper scissors plays. It does a terrible job, and I never got around to seeing why. I might revisit this.
unitConv, which does unit conversions. Inspired by reading somewhere about how it's a graph path-finding problem.

draw_dots is some code that takes an image, and then clicks around on a screen that has something like MS Paint open to 'draw' the image. 
