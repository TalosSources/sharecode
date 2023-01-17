- send images instead of text
- build a simple web interface
- actually host it somewhere

then later if energy
- refactor it cleanly in src folder and such
- create the feature of being able to reserve an object in advance
- create the feature of actually specifying when using an object, instead of having it registered when served, to prevent false positives (not sure of this one, could lead to users forgetting to do it) -> idea, figure out the api related to the object
- workout the math computation for the necessary k for given n and probability distribution of requests, and desired guarantees of having an object.
- make the system robust to adding objects to the pool at runtime

then later if I want to become a startup lol
- automatise everything, from user payment to computations, object purchasing and integration into the pool
- make a developped interface where users can specify their need and pay for their share of the usage

or maybe function with a more open and trust based approach
- let users add their own objects by trusting that they wont use it themselves or share it elsewhere

-> In fact we probably need to take the trust based approach, because we cannot prevent users from maliciously reusing the objects when they receive them.