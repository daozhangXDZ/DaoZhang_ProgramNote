# smallpt: Global Illumination in 99 lines of C++

Kevin Beason

 / 

 ![kevin.beason [at] gmail.com](smallpt Global Illumination in 99 lines of C++.assets/beason_email_lblue.gif)

![Cornell box image](smallpt Global Illumination in 99 lines of C++.assets/result640.jpg)

 **smallpt** is a global illumination renderer. It is 99 lines of C++, is open source, and renders the above scene using unbiased Monte Carlo path tracing [(click for full size)](http://www.kevinbeason.com/smallpt/result_25k.png).  

## Features

- Global illumination via unbiased Monte Carlo path tracing 

- 99 lines of 72-column (or less) open source C++ code 

- Multi-threading using OpenMP 

- Soft shadows from diffuse luminaire 

- Specular, Diffuse, and Glass BRDFs 

- Antialiasing via super-sampling with importance-sampled tent distribution,   and 2x2 subpixels 

- Ray-sphere intersection 

- Modified [Cornell box](http://www.graphics.cornell.edu/online/box/)   scene description 

- Cosine importance sampling of the hemisphere for diffuse reflection 

- Russian roulette for path termination 

- Russian roulette and splitting for selecting reflection   and/or refraction for glass BRDF 

- With minor changes compiles to a 4 KB binary (less than 4096 bytes)  

  Added 11/11/2010:    

- [Modifications](http://www.kevinbeason.com/smallpt/#mods) including explicit light sampling and non-branching ray tree. 

- Ports

   to CUDA and BSGP featuring interactive   display and scene editing.    

  Added 3/12/2012:  

- [Presentation slides](http://www.kevinbeason.com/smallpt/#moreinfo) explaining each line, by David Cline 

## Source

  Here is the 

complete

 source code for the entire renderer, including scene description:

​    

 ` #include <math.h>   // smallpt, a Path Tracer by Kevin Beason, 2008   #include <stdlib.h> // Make : g++ -O3 -fopenmp smallpt.cpp -o smallpt   #include <stdio.h>  //        Remove "-fopenmp" for g++ version < 4.2   struct Vec {        // Usage: time ./smallpt 5000 && xv image.ppm     double x, y, z;                  // position, also color (r,g,b)     Vec(double x_=0, double y_=0, double z_=0){ x=x_; y=y_; z=z_; }     Vec operator+(const Vec &b) const { return Vec(x+b.x,y+b.y,z+b.z); }     Vec operator-(const Vec &b) const { return Vec(x-b.x,y-b.y,z-b.z); }     Vec operator*(double b) const { return Vec(x*b,y*b,z*b); }     Vec mult(const Vec &b) const { return Vec(x*b.x,y*b.y,z*b.z); }     Vec& norm(){ return *this = *this * (1/sqrt(x*x+y*y+z*z)); }     double dot(const Vec &b) const { return x*b.x+y*b.y+z*b.z; } // cross:     Vec operator%(Vec&b){return Vec(y*b.z-z*b.y,z*b.x-x*b.z,x*b.y-y*b.x);}   };   struct Ray { Vec o, d; Ray(Vec o_, Vec d_) : o(o_), d(d_) {} };   enum Refl_t { DIFF, SPEC, REFR };  // material types, used in radiance()   struct Sphere {     double rad;       // radius     Vec p, e, c;      // position, emission, color     Refl_t refl;      // reflection type (DIFFuse, SPECular, REFRactive)     Sphere(double rad_, Vec p_, Vec e_, Vec c_, Refl_t refl_):       rad(rad_), p(p_), e(e_), c(c_), refl(refl_) {}     double intersect(const Ray &r) const { // returns distance, 0 if nohit       Vec op = p-r.o; // Solve t^2*d.d + 2*t*(o-p).d + (o-p).(o-p)-R^2 = 0       double t, eps=1e-4, b=op.dot(r.d), det=b*b-op.dot(op)+rad*rad;       if (det<0) return 0; else det=sqrt(det);       return (t=b-det)>eps ? t : ((t=b+det)>eps ? t : 0);     }   };   Sphere spheres[] = {//Scene: radius, position, emission, color, material     Sphere(1e5, Vec( 1e5+1,40.8,81.6), Vec(),Vec(.75,.25,.25),DIFF),//Left     Sphere(1e5, Vec(-1e5+99,40.8,81.6),Vec(),Vec(.25,.25,.75),DIFF),//Rght     Sphere(1e5, Vec(50,40.8, 1e5),     Vec(),Vec(.75,.75,.75),DIFF),//Back     Sphere(1e5, Vec(50,40.8,-1e5+170), Vec(),Vec(),           DIFF),//Frnt     Sphere(1e5, Vec(50, 1e5, 81.6),    Vec(),Vec(.75,.75,.75),DIFF),//Botm     Sphere(1e5, Vec(50,-1e5+81.6,81.6),Vec(),Vec(.75,.75,.75),DIFF),//Top     Sphere(16.5,Vec(27,16.5,47),       Vec(),Vec(1,1,1)*.999, SPEC),//Mirr     Sphere(16.5,Vec(73,16.5,78),       Vec(),Vec(1,1,1)*.999, REFR),//Glas     Sphere(600, Vec(50,681.6-.27,81.6),Vec(12,12,12),  Vec(), DIFF) //Lite   };   inline double clamp(double x){ return x<0 ? 0 : x>1 ? 1 : x; }   inline int toInt(double x){ return int(pow(clamp(x),1/2.2)*255+.5); }   inline bool intersect(const Ray &r, double &t, int &id){     double n=sizeof(spheres)/sizeof(Sphere), d, inf=t=1e20;     for(int i=int(n);i--;) if((d=spheres[i].intersect(r))&&d<t){t=d;id=i;}     return t<inf;   }   Vec radiance(const Ray &r, int depth, unsigned short *Xi){     double t;                               // distance to intersection     int id=0;                               // id of intersected object     if (!intersect(r, t, id)) return Vec(); // if miss, return black     const Sphere &obj = spheres[id];        // the hit object     Vec x=r.o+r.d*t, n=(x-obj.p).norm(), nl=n.dot(r.d)<0?n:n*-1, f=obj.c;     double p = f.x>f.y && f.x>f.z ? f.x : f.y>f.z ? f.y : f.z; // max refl     if (++depth>5) if (erand48(Xi)<p) f=f*(1/p); else return obj.e; //R.R.     if (obj.refl == DIFF){                  // Ideal DIFFUSE reflection       double r1=2*M_PI*erand48(Xi), r2=erand48(Xi), r2s=sqrt(r2);       Vec w=nl, u=((fabs(w.x)>.1?Vec(0,1):Vec(1))%w).norm(), v=w%u;       Vec d = (u*cos(r1)*r2s + v*sin(r1)*r2s + w*sqrt(1-r2)).norm();       return obj.e + f.mult(radiance(Ray(x,d),depth,Xi));     } else if (obj.refl == SPEC)            // Ideal SPECULAR reflection       return obj.e + f.mult(radiance(Ray(x,r.d-n*2*n.dot(r.d)),depth,Xi));     Ray reflRay(x, r.d-n*2*n.dot(r.d));     // Ideal dielectric REFRACTION     bool into = n.dot(nl)>0;                // Ray from outside going in?     double nc=1, nt=1.5, nnt=into?nc/nt:nt/nc, ddn=r.d.dot(nl), cos2t;     if ((cos2t=1-nnt*nnt*(1-ddn*ddn))<0)    // Total internal reflection       return obj.e + f.mult(radiance(reflRay,depth,Xi));     Vec tdir = (r.d*nnt - n*((into?1:-1)*(ddn*nnt+sqrt(cos2t)))).norm();     double a=nt-nc, b=nt+nc, R0=a*a/(b*b), c = 1-(into?-ddn:tdir.dot(n));     double Re=R0+(1-R0)*c*c*c*c*c,Tr=1-Re,P=.25+.5*Re,RP=Re/P,TP=Tr/(1-P);     return obj.e + f.mult(depth>2 ? (erand48(Xi)<P ?   // Russian roulette       radiance(reflRay,depth,Xi)*RP:radiance(Ray(x,tdir),depth,Xi)*TP) :       radiance(reflRay,depth,Xi)*Re+radiance(Ray(x,tdir),depth,Xi)*Tr);   }   int main(int argc, char *argv[]){     int w=1024, h=768, samps = argc==2 ? atoi(argv[1])/4 : 1; // # samples     Ray cam(Vec(50,52,295.6), Vec(0,-0.042612,-1).norm()); // cam pos, dir     Vec cx=Vec(w*.5135/h), cy=(cx%cam.d).norm()*.5135, r, *c=new Vec[w*h];   #pragma omp parallel for schedule(dynamic, 1) private(r)       // OpenMP     for (int y=0; y<h; y++){                       // Loop over image rows       fprintf(stderr,"\rRendering (%d spp) %5.2f%%",samps*4,100.*y/(h-1));       for (unsigned short x=0, Xi[3]={0,0,y*y*y}; x<w; x++)   // Loop cols         for (int sy=0, i=(h-y-1)*w+x; sy<2; sy++)     // 2x2 subpixel rows           for (int sx=0; sx<2; sx++, r=Vec()){        // 2x2 subpixel cols             for (int s=0; s<samps; s++){               double r1=2*erand48(Xi), dx=r1<1 ? sqrt(r1)-1: 1-sqrt(2-r1);               double r2=2*erand48(Xi), dy=r2<1 ? sqrt(r2)-1: 1-sqrt(2-r2);               Vec d = cx*( ( (sx+.5 + dx)/2 + x)/w - .5) +                       cy*( ( (sy+.5 + dy)/2 + y)/h - .5) + cam.d;               r = r + radiance(Ray(cam.o+d*140,d.norm()),0,Xi)*(1./samps);             } // Camera rays are pushed ^^^^^ forward to start in interior             c[i] = c[i] + Vec(clamp(r.x),clamp(r.y),clamp(r.z))*.25;           }     }     FILE *f = fopen("image.ppm", "w");         // Write image to PPM file.     fprintf(f, "P3\n%d %d\n%d\n", w, h, 255);     for (int i=0; i<w*h; i++)       fprintf(f,"%d %d %d ", toInt(c[i].x), toInt(c[i].y), toInt(c[i].z));   }   `

Other formats 

- [smallpt.cpp](http://www.kevinbeason.com/smallpt/smallpt.txt) (plain text) 
- [smallpt4k.cpp](http://www.kevinbeason.com/smallpt/smallpt4k.txt) (4 KB executable version) 
- [smallpt.tar.gz](http://www.kevinbeason.com/smallpt/smallpt.tar.gz) (982 KB) Full distribution.   Includes the above source files, Makefile, README, LICENSE, and   resulting rendered image (losslessly converted to PNG). 

## Usage



 `g++ -O3 -fopenmp smallpt.cpp -o smallpt  time ./smallpt 5000 display image.ppm`

The argument to smallpt ("5000") is the number of samples per pixel, and must be greater than 4. If you don't have ImageMagick's [display](http://www.imagemagick.org/script/display.php) command available, you can use other viewers such as gthumb, gwenview, xv, gimp, etc.  

GCC 4.2 or newer is required for multi-threading, however older versions of gcc will still work without threading. Remove the "-fopenmp" flag to disable threading support.  

 smallpt compiles with [GCC](http://gcc.gnu.org) 4.2 down to a 16 KB executable and produces a 1024x768 resolution image. Rendering using 5000 paths per pixel takes 2.1 hours on an Intel Core 2 Quad machine.    

A slightly modified version is provided which compiles to a 4 KB (4049 bytes) compressed executable. Do "make smallpt4k" to build.  See smallpt4k.cpp and the Makefile in the full distribution for more information. Note [sstrip](http://www.muppetlabs.com/~breadbox/software/elfkickers.html) and [p7zip](http://p7zip.sourceforge.net/) are required.    

If self assembly is used, the binary is only 2.7 KB (2666 bytes). Do "make smallptSA" to build.  

## Details

 

| [
![img](smallptGlobalIlluminationin99linesofC++.assets/result_t_8.jpg)](http://www.kevinbeason.com/smallpt/result_8.png)|[
![img](smallptGlobalIlluminationin99linesofC++.assets/result_t_40.jpg)](http://www.kevinbeason.com/smallpt/result_40.png)|[
![img](smallptGlobalIlluminationin99linesofC++.assets/result_t_200.jpg)](http://www.kevinbeason.com/smallpt/result_200.png)|[
![img](smallptGlobalIlluminationin99linesofC++.assets/result_t_1000.jpg)](http://www.kevinbeason.com/smallpt/result_1000.png)|[
![img](smallptGlobalIlluminationin99linesofC++.assets/result_t_5k.jpg)](http://www.kevinbeason.com/smallpt/result_5k.png)|[
![img](smallptGlobalIlluminationin99linesofC++.assets/result_t_25k.jpg)](http://www.kevinbeason.com/smallpt/result_25k.png) |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| [
![img](smallptGlobalIlluminationin99linesofC++.assets/result_crop_8.jpg)](http://www.kevinbeason.com/smallpt/result_8.png)|[
![img](smallptGlobalIlluminationin99linesofC++.assets/result_crop_40.jpg)](http://www.kevinbeason.com/smallpt/result_40.png)|[
![img](smallptGlobalIlluminationin99linesofC++.assets/result_crop_200.jpg)](http://www.kevinbeason.com/smallpt/result_200.png)|[
![img](smallptGlobalIlluminationin99linesofC++.assets/result_crop_1000.jpg)](http://www.kevinbeason.com/smallpt/result_1000.png)|[
![img](smallptGlobalIlluminationin99linesofC++.assets/result_crop_5k.jpg)](http://www.kevinbeason.com/smallpt/result_5k.png)|[
![img](smallptGlobalIlluminationin99linesofC++.assets/result_crop_25k.jpg)](http://www.kevinbeason.com/smallpt/result_25k.png) |
| 8 spp 13 sec                                                 | 40 spp 63 sec                                                | 200 spp 5 min                                                | 1000 spp 25 min                                              | 5000 spp 124 min                                             | 25000 spp 10.3 hrs                                           |
| Timings and resulting images for different numbers of samples per pixel (spp) on a 2.4 GHz Intel Core 2 Quad CPU using 4 threads. |                                                              |                                                              |                                                              |                                                              |                                                              |

The box scene is constructed out of nine very large spheres which overlap. The camera is very close to their surface so they appear flat, yet each wall is actually the side of a sphere. The light is another sphere poking through the ceiling which is why it's round instead of the normal square. The black area visible in the mirror ball is the front of the box colored black to appear like empty space.  

The image is computed by solving the [rendering equation](http://en.wikipedia.org/wiki/Rendering_equation)   using [numerical   integration](http://mathworld.wolfram.com/MonteCarloIntegration.html). The specific algorithm is Monte Carlo path tracing with [Russian roulette](http://www.iit.bme.hu/~szirmay/russian_link.htm) for path termination.  I highly recommend Shirley's and Jensen's execellent books (linked below) for explanations of these ideas. Due to size constraints and simplicity, explicit light sampling is not used, nor any ray intersection acceleration data structure.  

Parallelism is achieved using an OpenMP `#pragma` to dynamically allocate rows of the image to different threads, with a thread for each processor or core. The variable `Xi` is used to store the state of the random number generator `erand48()`, and is seeded using an arbitrary function of the row number to decorrelate (at least visually) the sequences from row-to-row. In this way the sequences are deterministic and consistent from run to run, and independent of which thread is executing and in what order the rows are executed.  

Anti-aliasing is done using supersampling, which removes all the jaggies except around the light. These are handled by using 2x2 subpixels which are clamped and then averaged.  

Instead of fclose()ing the file, I exploit the [C++ standard](http://dev.feuvan.net/docs/isocpp/basic.html#basic.start.main) which calls return(0) implicitly, which in turn calls exit(0), which flushes and closes open files.  

## More Scenes

  These images were all generated by smallpt by replacing the Cornell box scene definition with 

varying combinations of 4 to 22 spheres

.  

 [
![img](smallptGlobalIlluminationin99linesofC++.assets/sky_t.jpg)](http://www.kevinbeason.com/smallpt/sky.png)[
![img](smallptGlobalIlluminationin99linesofC++.assets/nightsky_t.jpg)](http://www.kevinbeason.com/smallpt/nightsky.png)[
![img](smallptGlobalIlluminationin99linesofC++.assets/wada_t.jpg)](http://www.kevinbeason.com/smallpt/wada.png)[
![img](smallptGlobalIlluminationin99linesofC++.assets/island_t.jpg)](http://www.kevinbeason.com/smallpt/island.png)
 [
![img](smallptGlobalIlluminationin99linesofC++.assets/wada2_t.jpg)](http://www.kevinbeason.com/smallpt/wada2.png)[
![img](smallptGlobalIlluminationin99linesofC++.assets/vista_t.jpg)](http://www.kevinbeason.com/smallpt/vista.png)[
![img](smallptGlobalIlluminationin99linesofC++.assets/overlap_t.jpg)](http://www.kevinbeason.com/smallpt/overlap.png)[
![img](smallptGlobalIlluminationin99linesofC++.assets/forest_t.jpg)](http://www.kevinbeason.com/smallpt/forest.png)  

## License

  The source is released under the MIT license, which is open and compatible with GPL. See LICENSE.txt in the distribution for more information.  

## Modifications

- [explicit.cpp](http://www.kevinbeason.com/smallpt/explicit.cpp)    **Huge** speedup, especially for small lights.   Adds explicit light sampling with   23 additional lines of code and a small   function signature change. Produces [this image](http://www.kevinbeason.com/smallpt/explicit16.png)   in 10 seconds on a Intel Core i7 920 quad-core CPU using 16 samples per pixel. 
- [forward.cpp](http://www.kevinbeason.com/smallpt/forward.cpp) Revision of `radiance()` function   that removes all recursion and uses only a simple loop and no path   branching. That is, the ray tree is always one ray wide. 
- [Single     precision float support](http://ompf.org/forum/viewtopic.php?p=11522#p11522) by Christopher Kulla. Mostly fixes   [crazy   artifacts](http://ompf.org/forum/viewtopic.php?p=11223#p11223) that appear when single precision floats are used, by avoiding self intersection. There is   still a light leak at at the top of the scene though. 

## Ports

-    [tokaspt](http://code.google.com/p/tokaspt/) Interactive version   in CUDA by Thierry Berger-Perrin. Features realtime display and scene   editing.   [       
![img](smallptGlobalIlluminationin99linesofC++.assets/img_ui_bloated_t.jpg)
![img](smallptGlobalIlluminationin99linesofC++.assets/img_hall_of_mirrors_small_t.jpg)](http://code.google.com/p/tokaspt/)  
- [BSGP Port](http://ompf.org/forum/viewtopic.php?p=11483#p11483)   Port to [BSGP](http://www.kunzhou.net/#BSGP) done by Hou Qiming.  
- [JavaScript port](http://www.democopei.de/smallpt.html) by Sven Klose  
- [Haskell port](http://github.com/noteed/smallpt-hs) by   Vo Minh Thu, available on [Hackage](http://hackage.haskell.org/packages/archive/pkg-list.html)  
- [smallpaint](http://cg.tuwien.ac.at/~zsolnai/gfx/smallpaint/) by Károly Zsolnai,   adds explicit light sampling, Halton sequences, a painting effect, and more.   [       
![img](smallptGlobalIlluminationin99linesofC++.assets/smallpaint_t.jpg)](http://cg.tuwien.ac.at/~zsolnai/gfx/smallpaint/)  
- [smallptGPU](http://davibu.interfree.it/opencl/smallptgpu/smallptGPU.html) and [smallptGPU2](http://davibu.interfree.it/opencl/smallptgpu2/smallptGPU2.html) by David Bucciarelli are OpenCL implementations based on smallpt.   [       
![img](smallptGlobalIlluminationin99linesofC++.assets/smallptGPU_t.jpg)](http://davibu.interfree.it/opencl/smallptgpu2/smallptGPU2.html)  
- [Swift port](https://github.com/jackpal/smallpt-swift) by Jack Palevich    

## More Information

-  [Presentation slides about smallpt](https://docs.google.com/open?id=0B8g97JkuSSBwUENiWTJXeGtTOHFmSm51UC01YWtCZw) by David Cline
   Slides with line-by-line explanations of the explicit lighting version of smallpt, which has been reformatted to be 75% longer. Thank you, Dr. Cline! ([mirror](http://www.kevinbeason.com/smallpt/smallpt_cline_slides.ppt))    
-  [ MINILIGHT - a minimal global illumination renderer](http://www.hxa7241.org/minilight/minilight.html), by Harrison Ainsworth
   A similar, earlier project. More general but also larger (10x). The site has some good information on Monte Carlo path tracing. Instead of repeating it here, please visit the site.  
- [ Neos path tracer](http://neos1.wordpress.com/2008/11/02/path-tracing-for-the-win/) by Michal Ciebiada
   381 line Ocaml path tracer. A similar project although somewhat larger (3X) and in Ocaml.  
- [ Realistic Ray Tracing](http://www.amazon.com/Realistic-Ray-Tracing-Peter-Shirley/dp/1568811101), by Peter Shirley
   Almost 100% of smallpt is derived from this book.  
- [ Cornell box images](http://graphics.ucsd.edu/~henrik/images/cbox.html), by Henrik Wann Jensen
   The inpiration of the output generated by smallpt.  
- [ The original Cornell Box](http://www.graphics.cornell.edu/online/box/)
   An icon of graphics research  
- [Realistic Image Synthesis Using Photon Mapping](http://graphics.ucsd.edu/~henrik/papers/book/), by Henrik Wann Jensen
   Explains Russian roulette and a lot more.    
- [Sphereflake](http://ompf.org/ray/sphereflake/), by Thierry Berger-Perrin
   Short ray-sphere intersection code  
- [sf4k](http://ompf.org/stuff/sf4k/), by Thierry Berger-Perrin
   Idea for 4K-ness. (No full GI.) ([more info](http://ompf.org/forum/viewtopic.php?f=8&t=707&start=0&st=0&sk=t&sd=a))  
- [ C++ vs OCaml: Ray tracer comparison](http://www.ffconsultancy.com/languages/ray_tracer/comparison.html), by Jon D. Harrop
   105 line C++ ray tracer. (No full GI.)  
- [ Introduction to Linux as 4 KB Platform](http://in4k.untergrund.net/index.php?title=Linux)
   Some information regarding shrinking binaries to 4 KB on Linux. Plus [this](http://ftp.kameli.net/pub/fit/misc/presis_asm06.pdf) and [this](http://www.muppetlabs.com/~breadbox/software/tiny/teensy.html).   
- [ Ompf.org forum](http://ompf.org/forum/)
   Online ray tracing community, with links to many other ray tracers  

Last update: 11/5/2014
 Initial version: 4/29/2007  
