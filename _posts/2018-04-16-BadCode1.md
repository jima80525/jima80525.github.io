At the ill-advised encouragement of a friend of mine, I've decided to start a series of posts about some of the awful code I stumble across in my day-to-day life.

In a way, I already started this series with my post on [bad functors](https://www.snowboardingcoder.com/coding/2018/03/27/functors-to-the-rescue/), so this is just continuing in that vein.

Today's bad code is titled "How to find the N largest rectangles".  In some motion detection code I've recently reviewed from a vendor, they needed some code that took an array of rectangle structs and found the `max_number_found` biggest rectangles.  Due to hardware limitations, they would never be more than 254 rects in the list.

Now, I know what many of you, at least those of you that are sane, are thinking: "duh, sort the list, take the first max_number_found".   If so, bonus points for you.

Alas, the developers who generated this code didn't think that was a good idea.  No.  That would be wasteful.

I'll show you the code first, then we'll walk through the insanity.

[cpp]
threshold = startingThreshold;
do {
   number_found = 0;
   threshold += threshold_increment;
   for(i = 0;i < 254;i++) {
      if(rectangles[i].area > threshold) {
         number_found++;
      }
   }	
} while(number_found > max_number_found);
for(i = 0;i < 254;i++) {
    if(rectangles[i].area > threshold) {
       // add rectangle[i] to list
    }
}
[/cpp]

## What Does **That** Do?

For starters I should point out that `startingThreshold` and `threshold_increment` are passed in to the function.  Their values don't actually matter to much in terms of what the algorithm does, though they might effect the performance.

The top `do-while` loop is the real doozy here.  It starts at a specified 'threshold' and walks through all 254 rectangles, counting how many are above the threshold.  If the number found is too many, in increases the threshold and tries again.  Repeat until we have a solution.

The second loop then walks through the list one last time to actually do the copy.  That part isn't insane once you've bitten off the first part.

There are so many problems here it's tough to know where to start.  It's tempting to mention that the performance is likely to be quite poor, although this doesn't really matter as it was demo code and, with 254 elements, performance doesn't matter too much.    That said,  the worst case for this algorithm does over 64,000 comparisons.

Next would be the many corner cases here.  What happens if all of the rectangles are the same size (you get a 0 length list)?   How would a caller know what to place for a threshold_increment?

Finally comes the readability issue.  This is code that takes a simple problem and explodes it into a confusion-inducing slab of code.  Even knowing what the intention was, it still took a few minutes to put together all the pieces here.

That's the bad code for this week.  I'll keep my eye out for more gems and share them here.



Thanks for reading!
