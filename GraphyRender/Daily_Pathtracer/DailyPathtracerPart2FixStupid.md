# Daily Pathtracer Part 2: Fix Stupid

​         Posted on                    Mar 28, 2018                

​                  [#rendering](http://aras-p.info/tags/rendering)                  [#code](http://aras-p.info/tags/code)                

*Introduction and index of this series is here*.

At the end of the [last post](http://aras-p.info/blog/2018/03/28/Daily-Pathtracer-Part-1-Initial-C-/), I had the path tracer running at 28.4 million rays/second on a 4 year old Mac laptop, but only at 14.8 Mray/s on AMD ThreadRipper PC. Why? That’s what this post is about.

### The problem? Random number generator

Turns out, the problem was in my little random number generator. A path tracer needs *a lot* of random numbers, and needs them fast. Built-in C `rand()` is fairly limited in many cases (e.g. on Windows MSVC implementation, only returns 15-bit values), and I’ve heard many years ago that [Xorshift](https://en.wikipedia.org/wiki/Xorshift) is supposedly quite good and super fast, so I did this:

```
static uint32_t s_RndState = 1;
static uint32_t XorShift32()
{
    uint32_t x = s_RndState;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 15;
    s_RndState = x;
    return x;
}
```

You all can probably already see the problem, and I should have known better too… here it is:

### Actual problem: cache sharing

The function above is fine in a single-threaded environment. The problems start when multi-threading enters the picture. Yes it’s not “thread safe” too; there’s one “random state” variable that would get read & written by multiple threads without synchronization, this could lead to “incorrect randomness”, so to speak, but that’s a bit hard to notice.

The problem is that the *same* variable is read & written to by many threads very often. Like this:

1. One CPU core writes into the variable,
2. It has to tell all other cores “yo, you had this variable in your caches, I just modified it, please invalidate your cacheline for this, kthxbye”.
3. Then the next CPU core is about to get a random number,
4. Now it has to fetch the variable into the cache,
5. And repeat from step 1.

All this cache invalidation and re-fetching the variable into caches again ends up being very expensive. And the more CPU cores you have, the more expensive it gets! *That’s* why my 16 thread PC was quite a bit slower than a 8-thread laptop.

> In multi-threaded programming, there’s a sneakier phenomenon, called “False Sharing”. This is when several threads are modifying completely different variables – there’s no race conditions or anything. But, the variables happen to be really close to memory, on the same cacheline. The CPU cores still have to do all the cache invalidation dance above, since they can only read memory in cacheline-size chunks. Read more about it [on wikipedia](https://en.wikipedia.org/wiki/False_sharing) or in Sutter’s “[Eliminate False Sharing](http://www.drdobbs.com/parallel/eliminate-false-sharing/217500206)”.

### The fix and performance after it

Simplest [fix](https://github.com/aras-p/ToyPathTracer/commit/a9d633c0bf46dc39e374c66ebfd9bfcf0d6273c1): change `uint32_t s_RndState` to `thread_local uint32_t s_RndState`, to make the random state variable be unique for each thread.

- Mac laptop: **28.1 -> 34.7** Mray/s *(nice)*
- ThreadRipper PC: **14.1 -> 130** Mray/s *(whoa, 9x faster!)*

**Lesson: cache sharing, or false cache sharing, can really bring your performance down**. Watch out!

And yes, I know. I shouldn’t have had that as a global variable in the first place, *mea culpa*. Even with the fix, I should perhaps have made the “random state” be explicitly passed down into functions, instead of slapping an “eh, let’s put into thread local storage, will do the trick”. Don’t do this in production code :)

So, now we are at **130 Mray/s** on Windows PC *(AMD ThreadRipper 1950X 3.4GHz, 16 threads)*, and **34.7 Mray/s** on Mac laptop *(Core i7-4850HQ 2.3GHz, 8 threads)*. Is that good or bad? I still don’t know!

But, for [next time](http://aras-p.info/blog/2018/03/28/Daily-Pathtracer-Part-3-CSharp-Unity-Burst/) let’s try doing the same path tracer in C#.

- [← Older](http://aras-p.info/blog/2018/03/28/Daily-Pathtracer-Part-1-Initial-C-/)
- [Newer →](http://aras-p.info/blog/2018/03/28/Daily-Pathtracer-Part-3-CSharp-Unity-Burst/)

------

##### Possibly Related Posts

- [Pathtracer 17: WebAssembly](http://aras-p.info/blog/2018/11/16/Pathtracer-17-WebAssembly/), from 2018 November
- [SPIR-V Compression: SMOL vs MARK](http://aras-p.info/blog/2018/10/31/SPIR-V-Compression-SMOL-vs-MARK/), from 2018 October
- [Pathtracer 16: Burst SIMD Optimization](http://aras-p.info/blog/2018/10/29/Pathtracer-16-Burst-SIMD-Optimization/), from 2018 October
