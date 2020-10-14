Design for the future, just not a *specific* future

I've had the, um, *opportunity* to work with some old code I've been avoiding since I re-started this job recently.  The time away and, frankly, a few deeps breaths, have helped me to gain some perspective on this system and why it bothers me so.  

There are lots of things to hate in this code; copy-pasta, cryptic names, language abuse (a 45 line macro, anyone?).  While those are all bad in their own right, the fundamental issue I keep coming back to is the design of the system.  

The system is a simple library which was used in exactly one product line.    It is a library linked into a bigger code base to serve a single purpose.  Unfortunately, the architect of this system had grand plans and ideas.  He was convinced that this library would conquer the world.  

So he built what he described as a "Plug-in architecture, just like Firefox" which would allow us to bring in third party components and integrate them into this library.  He designed it to run on Windows **and** Linux (target product was Linux only).  Worse, because he insisted he needed 'flexibility' for the future, he refused to make use of the system services (logging, configuration, settings) that the bigger product provided. 

Because the library was over designed, it is much larger and much more complex than needed.  And this is where my frustration overflows.  The designer had a very clear vision of a future in mind, but he built this system to a very, very specific set of conditions.   By doing so, he actually eliminated any possibility that another project would pick up his library.  it was too big, too clunky, too complex. 

I'd like to think that if he and the team had kept the system smaller, leaner, less complex, that the end result would have been far more useful.  As it is, we're working hard to eliminate that code from our products.  It'll take a while.

The lesson I'm going to take from this experience is that I should plan for the future, but I should plan for any future by keeping the design lean, flexible, and as small as possible. 