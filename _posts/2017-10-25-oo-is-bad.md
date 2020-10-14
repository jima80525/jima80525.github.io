# Long Functions

Today at work, a friend shared a youtube video titled "Object Oriented Programming is Bad" (no, I won't share it here as I didn't like it).  There were several points that the narrator made, but my attention was drawn to a section where he discusses function length and how splitting functions into smaller functions is bad.

As I told my coworker, I don't have many hard-and-fast rules when it comes to coding standards as it generally leads to arguments with the team which are almost universally unproductive.   That said, this guy was nuts.

I work in a code base written by people who clearly agreed with his philosophy and, I have to say that it's horrible to maintain.  Now, I can hear the nay-sayers chiming in, "just because those people didn't write readable 1000 line functions, doesn't mean it's not possible!".  While that is a valid point, the counter argument is that it's quite a bit harder to write a 1000 line function that is readable than it is to write a 30 line function that is.

What I've seen over many codebases in several languages is that longer functions always end up with strange control flow issues (lots of gotos in the present codebase) and all sorts of bad coding practices sprinkled about: reusing local variables, resource management issues, copy and paste code.

So again, while I will grant the argument that it is possible to write long functions that make sense.  Experience has shown that really long functions go hand-in-hand will poorly written, hard to understand code.

That's why it's one of my 'rules'.



