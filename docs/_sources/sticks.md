---
title: "Ten Sticks and a Gun"
exports:
  - format: tex
    logo: false
    template: ../templates/plain_latex_book_chapter
    output: exports/structure.tex
---

# Ten Sticks and a Gun

*December, 2025*

When we think of the police in India, we usually think of the [*Havildar*](https://en.wikipedia.org/wiki/Havildar). A stout man with a lathi and sometimes a stern look of authority on his face. But somewhere in the same city, there's another kind of cop—the one with the automatic rifle, the bulletproof vest, the gear that costs more than a year's salary. Same police force, wildly different equipment.

Why so much variance? Why not just have fewer cops who are all armed to the teeth? Or why not go the other way—many more cops, all with sticks?

Turns out the Indian government ran the numbers and discovered something revolutionary: most problems can be solved with a stick and a stern look. Guns? Those are for when things have gone *very* wrong.

The real insight is this: *ten sticks and a gun is better than two guns or twenty sticks*

Fewer cops with better guns? They can only be in a few places at once (and India is a *big big* country). More cops with only sticks? Useless when a situation actually escalates. But many haviladars spread across the city, plus a specialized unit that can rapidly deploy anywhere it's needed? That's the sweet spot.

I stumbled on this analogy while trying to explain receptive field sizes in the visual cortex to a friend. Turns out, human vision plays the exact same optimization game.

Your brain had a problem: not enough neurons to give you high-resolution vision everywhere. It had to choose between resolution and coverage. Let's first look at the two most extreme (and terrible) options:

**1. Maximal resolution** - You get 120 samples per degree everywhere. Incredible detail, but your field of view shrinks to 5x5 degrees. Two guns, and nowhere to point them.

**2. Maximal coverage** - You get 150x150 degrees of vision. You can see everything, except that it's all rendered in the blurriest  quality imaginable. Twenty sticks, all useless when you actually need to identify something.

So what did your brain do? Ten sticks and a gun.

Your peripheral vision covers your entire 150+ degree field with low resolution. One job: detect motion. "Something moved over there!" Your fovea—a tiny 5-degree spot—packs that 120 samples per degree resolution. When periphery spots something, your eyes snap over and fovea investigates.

Low-acuity periphery detects. High-acuity fovea recognizes. There you go. I call this the Havildar strategy.

### References/Further reading:

1. [Emergence of Foveal image sampling from learning to attend in visual scenes - *Brian Cheung, Eric Weiss, Bruno Olshausen.* ICLR 2017](https://openreview.net/forum?id=SJJKxrsgl)
2. [Metamers of the ventral stream - *Jeremy Freeman and Eero Simoncelli.* Nature Neuroscience](https://www.nature.com/articles/nn.2889)
3. [Retinal ganglion cells that project to the dorsal lateral geniculate nucleus in the macaque monkey. *V H Perry, R Oehler and A Cowey*](https://pubmed.ncbi.nlm.nih.gov/6483193/)