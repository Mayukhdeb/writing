---
title: "It's Always Dinner Time in Evolution"
exports:
  - format: tex
    logo: false
    template: ../templates/plain_latex_book_chapter
    output: exports/dinner-time.tex
---

# It's Always Dinner Time in Evolution

The more I read about vision in the brain, the simpler the picture gets. Almost everything makes sense from the perspective of two objectives: find dinner, and don't become someone else's.

**Hunt**

Dinner doesn't want to be found. It hides. A deer standing still in dappled forest light is nearly invisible — evolution spent millions of years painting it that way. So how do you spot it? You wait for it to move. The visual system applies the principle of common fate: pixels that shift together belong to the same object. Camouflage works on a photograph. It fails on video.

But spotting isn't catching. Once dinner bolts, you need to know where it's *going*, not where it *is*. The early visual cortex handles this with something called pre-play — it runs the movie forward a few frames before the world catches up. And the way it does this is surprisingly simple: it straightens curved trajectories in neural space so they can be extended as straight lines. Prediction becomes extrapolation. Pursuit becomes geometry.

**Flee**

Now flip it. You've eaten. You need to get home without something eating you.

The problem is different now. You don't need to resolve a predator's whiskers — you need to notice *something fast in the corner of your eye* before it's too late. This is where the [Havildar strategy](https://mayukhdeb.github.io/writing/sticks.html) earns its keep from the other side: the same low-resolution periphery that detected your dinner for you now detects the thing that wants you for dinner.

**Afford**

Both of these — hunting and fleeing — run on a brain that burns roughly 20 watts of power. That's nothing. And spikes are expensive, long axons are worse, and maintaining wiring is worst of all. So evolution squeezes every bit of efficiency out of the system.

Efficient coding assigns short neural "words" to the inputs you see most often and long ones to the rare stuff — the same trick that makes Morse code work (short code for 'e', long one for 'q'). Receptive fields decorrelate the input in space and time so that neighboring neurons aren't wasting spikes saying the same thing twice. And the brain puts neurons that talk to each other *next to each other*, which is why you get topographic maps everywhere — retinotopy, tonotopy, somatotopy. Not elegance for its own sake.

Hunt. Flee. Afford. Half a billion years of dinner pressure, and these are the engineering principles it produced. Meanwhile we're still building vision systems from scratch. But good artists borrow, and great artists steal — and steal we must.

References:

1. [Max Wertheimer. Experimentelle studien u ̈ber das sehen von bewegung. *Zeitschrift fur psychologie*](https://www.gestalttheory.net/download/Wertheimer1912_Sehen_von_Bewegung.pdf)
2. [Matthias Ekman, Peter Kok, and Floris P de Lange. Time-compressed preplay of anticipated
events in human primary visual cortex. *Nature communications*](https://www.nature.com/articles/ncomms15276)
3. [Olivier J Henaff, Yoon Bai, Julie A Charlton, Ian Nauhaus, Eero P Simoncelli, and Robbe LT Goris. Primary visual cortex straightens natural video trajectories. *Nature communications*](https://www.nature.com/articles/s41467-021-25939-z)
4. [VH Perry, R Oehler, and A Cowey. Retinal ganglion cells that project to the dorsal lateral geniculate nucleus in the macaque monkey. *Neuroscience*](https://pubmed.ncbi.nlm.nih.gov/6483193/)
5. [Horace B Barlow et al. Possible principles underlying the transformation of sensory messages](https://www.cnbc.cmu.edu/~tai/microns_papers/Barlow-SensoryCommunication-1961.pdf)
6. [Chen, B. L., Hall, D. H., & Chklovskii, D. B. (2006). Wiring optimization can relate neuronal structure and function. *Proceedings of the National Academy of Sciences*](https://www.pnas.org/doi/10.1073/pnas.0506806103)