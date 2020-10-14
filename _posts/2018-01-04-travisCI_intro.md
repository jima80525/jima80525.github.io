# Travis CI - A quick review

I've recently decided to upgrade a pet-project of mine ([a Python pod-catcher](https://github.com/jima80525/pyres)) to be a bit more "modern" (i.e. Python3, installable, automated builds, etc) I won't go into the details of the project (that's a story for another post), this post is just to document my experience starting up with TravisCI to get builds every time I commit.

## Continuous Integration

I am big fan of continuous integration and running unit tests on every build. In my work-life I've written (a long time ago) and set up (more recently) CI build systems for various types of projects, usually in C++. Tools like Jenkins, Bamboo, and TeamCity have really changed the landscape of how this works in a corporate world and this is a more-than-welcome improvement.

My current set up is different in several key respects:

* it's in Python
* it's open source
* it's dramatically smaller than my work projects usually are

All of these combine to simplify the problem.

## TravisCI

I won't go into the step-by-step of how to set this up (as it's very well documented [here](https://docs.travis-ci.com/user/getting-started/)). I will say, however, that this process worked quite well and was remarkably painless.

The main work to be done, other than creating an account and selecting which github project to build, was in creating the .travis.yml file. I've used yaml a bit in the past but I'm certainly not an expert in it. That said, the examples given were more than sufficient to get me up and running and to play with various options. The only issue I found was an odd permissions problem that started after my first few builds. A quick search showed that this could be fixed by putting <em>sudo: true</em> line in the yaml file.

## Conclusion

So far, I'm quite impressed! In just a short while I was able to get my project building on a per-commit basis on several versions of Python. I even managed to add the badge in the REAMDE.rst file for the project to indicate the status. The most difficult part of this process was getting my project into shape to run unit tests on both Python2 and Python3!

Way to go, TravisCI!
