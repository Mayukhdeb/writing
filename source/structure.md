---
title: "Structure as Computation"
exports:
  - format: tex
    logo: false
    template: ../templates/plain_latex_book_chapter
    output: exports/structure.tex
---

# Structure as Computation

*January 15th, 2026*

On my walk to the lab, I pass hundreds of trees doing something remarkable: optimizing thousands of leaf angles to maximize sunlight. No central processor. No coordination algorithm. How?

Each leaf is, in a sense, "dumb." It responds only to its immediate environment—the light it receives, the neighbors that shade it. No leaf knows the tree's overall strategy. No leaf has access to the global picture. And yet, the emergent pattern is somehow optimal. 

The computer you're using to read this solves problems the exact opposite way: one central processor, total access to all information, explicit step-by-step calculation. Ask it to optimize leaf angles and it could do it in milliseconds. But that speed requires something the tree doesn't have: expensive, energy-hungry infrastructure to move information everywhere instantly.

Why don't trees work like your computer? Because in nature, communication is the bottleneck. Every long-distance signal costs energy. Every connection means physical infrastructure—pathways that must be grown, maintained, kept alive. Your computer can afford to centralize because moving electrons through copper is cheap. A tree cannot.

Soon enough, I reach the lab and start thinking about brains. Same principle: nature will do almost anything to avoid sending information across long distances.

The brain is obsessively local. Neurons connect primarily to their neighbors. Processing happens in clusters. Long-range connections exist, but they're expensive luxuries—every axon costs energy to build and maintain, every signal costs ATP to fire. So the brain, like the tree, minimizes wiring. Structure becomes the solution to the communication problem.

The visual cortex faces a wiring problem: integrate inputs from two eyes, each sending foveal and peripheral information. Solution? Arrange by eccentricity, not by eye. Left-fovea sits next to right-fovea. Left-periphery next to right-periphery. Result: when the brain needs to compare what both eyes see at any given location, the relevant neurons are already neighbors. No expensive long-distance connections needed.

Or consider orientation selectivity—how the brain detects lines and edges at different angles. The visual cortex organizes this as a literal grid: one axis sweeps through orientations (vertical, horizontal, diagonal), the other through eyes (left, right). Combined with the eccentricity organization, you get an elegant 3D structure where every combination—orientation, eye, location—has its place.

Now imagine the alternative: same neurons, same information, but randomly shuffled. No spatial organization. What breaks?

You'd need a routing system. Some way to find and connect the right neurons for any given computation—which left-eye vertical edge detector goes with which right-eye vertical edge detector? That search and coordination costs energy, requires extra wiring, adds computational overhead.

Structure *is* computation. Organization eliminates the need for a random-access memory system.

Artificial neural networks inherit the computer's design: dense, fully-connected layers where every neuron links to every other. Global information access. The assumption is that any piece of information might be needed anywhere, so the architecture connects everything to everything. We're building intelligence using the most expensive paradigm nature spent millions of years avoiding.

On my walk home, I pass those same trees. They're still computing — just slowly, locally and efficiently. Maybe intelligence doesn't require knowing everything everywhere all at once. Maybe it just requires the right structure, and enough time for simple rules to compound into something remarkable.