# Functors to the Rescue!

I've recently had the singular pleasure of working with some legacy code written by a team I (thankfully) no longer work with directly. This team had several issues, one of which I'll address in a later post, one I'll discuss today.

Today's issue is that the team was very enamored of new technology, but not overly concerned with readability. This combination produces some quite interesting code. One of the anti-patterns that I see frequently in their code is the use of functors in situations where they only serve to obfuscate the code.

In the example I found, they had a map and wanted to search for a key given a known value. Here's the code the produced:
[cpp]
typedef map<string, string> PresetMap;

struct CompareString {
    CompareString(const string& str) : _str(str) {
    }
    bool operator() (const pair<string, string>& ptz ) const {
        return (_str == ptz.second);
    }
private:
    string _str;
};

string getPreset(const string& preset, PresetMap& myMap) {
    PresetMap::iterator it = find_if(myMap.begin(), myMap.end(), CompareString(preset));
    if (it != myMap.end()) {
        return it->first;
    }
    return "";
}

[/cpp]

One might argue that it's quite reasonable to use a functor in this case if there are other places where that functor is re-used. Alas, this was not the case. This was the sole use of that functor. I haven't verified, but I'd strongly suspect that there are multiple instances of very similar functors scattered throughout the code base, all used exactly once.

For the record, I spent a few minutes rewriting this into what *I* view as a 'sane' approach:

[cpp]
string newGetPreset(const string& presetName, PresetMap& myMap) {
    for (auto preset : myMap) {
        if (preset.second == presetName) {
            return preset.first;
        }
    }
    return "";
}
[/cpp]

While there's an argument to be made that reusing the search algorithm from the stdlib is a higher good, I'd counter that readability is much, much more important, especially for such a trivial use case.

Spreading a simple search across 17 lines when a simple 8 line function will do seems a little extravagant.

To the team's credit, at least in this case the functor was immediately before the `getPreset` function in the source file. I have hit other examples where the two were separated by hundreds of lines of source.

There are lots of reasons why code ends up like this, but the biggest one, in my opinion, is not having a strong code review culture where decisions like this are questioned.

What do you think of this code? Am I completely missing the mark?

## Update

A different former-coworker read this and pointed out that I missed the ball by not including C++'s `lambda` functionality for this problem.  I've
used lambdas in other languages, but my C++ was always limited to pre-C++11 before this, so the syntax was new to me.  Here's what the same function
looks like with a lambda:

[cpp]
string lambdaGetPreset(const string& preset, PresetMap& myMap) {
    auto it = find_if(myMap.begin(), myMap.end(),
            [preset] (const pair<string, string>& ptz) {
                return preset == ptz.second;
            });
    if (it != myMap.end()) {
        return it->first;
    }
    return "";
}
[/cpp]

I'll admit it still looks a bit odd to me, but that's mainly due to the lambda syntax being new.  I suspect once I get used to
it, this will seem more reasonable to me.  I certainly wouldn't be thinking about changing it to make it more readable as I was with the original.

Thanks to Erik for pointing out lambdas!

