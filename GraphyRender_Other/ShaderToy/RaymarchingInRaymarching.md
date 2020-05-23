# Raymarching in Raymarching

 --------Trans Author:	White Robe

![1561480773789](RaymarchingInRaymarching.assets/RayMachine.gif)                                                                                                        

## Shader

```
#define MAT_SCREEN 0.
#define MAT_SPHERE1 1.
#define MAT_FLOOR  2.
#define MAT_CORNER 3.
#define MAT_SCREENZ 4.
#define MAT_MARCHSPHERE 5.
#define MAT_MARCHROUTE 6.
#define MAT_MARCHRADIUS 7.
#define MAT_SPHERE2 8.
#define MAT_SPHERE3 9.
#define MAT_RAYDIRECTION 10.
#define MAT_HITPOINT 11.

float uvToP = 0.0;
float colToUv = 1.0;
float screenZ = 2.5;

float sphereAnim = 1.0;
float radiusAnim = 1.0;
float routeAnim = 1.0;

float raySphereAlpha = 0.0;

float cornersAlpha = 0.0;
float cornersAnim = 0.0;

float screenZAlpha = 0.0;

float radiusAlpha = 1.0;

float rayDirectionAnim = 0.0;
float rayDirectionAnim2 = 0.0;

float screenAlpha = 0.0;

// =====================Camera========================
vec3 cameraPos, cameraTarget;

//================================

float sum = 0.0;

float tl(float val, float offset, float range)
{
    float im = sum + offset;
    float ix = im + range;
    sum += offset + range;
    return clamp((val - im) / (ix - im), 0.0, 1.0);
}

float cio(float t) {
	return t < 0.5
	? 0.5 * (1.0 - sqrt(1.0 - 4.0 * t * t))
	: 0.5 * (sqrt((3.0 - 2.0 * t) * (2.0 * t - 1.0)) + 1.0);
}

float eio(float t) {
	return t == 0.0 || t == 1.0
		? t
		: t < 0.5
		? +0.5 * pow(2.0, (20.0 * t) - 10.0)
		: -0.5 * pow(2.0, 10.0 - (t * 20.0)) + 1.0;
}

void timeLine(float time)
{
    //time += 32.;
    float t = tl(time, 1.0, 0.5);
    uvToP = mix(0.0, 1.0, eio(t));
    
    t = tl(time, 1.0, 1.0);
    cameraPos = mix(vec3(0.0), vec3(5., 5., -2.), eio(t));
    cameraTarget = vec3(0.0, 0.0, 5.);
    
    
    t = tl(time, 0.5, 1.0);
    raySphereAlpha = mix(0., 1., t);
    cornersAlpha = mix(0., 1., t);
    
    t = tl(time, 0.5, 1.0);
    cornersAnim = mix(0., 1., t);
    
    t = tl(time, 1.0, 1.0);
    cameraPos = mix(cameraPos, vec3(2., 3., -3.), eio(t));
    cameraTarget = mix(cameraTarget, vec3(0.0, 0.0, 3.0), eio(t));
    
    t = tl(time, 0.5, 0.5);
    screenZAlpha = mix(0., 1., t);

	t = tl(time, 0.5, .5);
    colToUv = mix(colToUv, 0.0, eio(t));
    
    t = tl(time, 0.5, 1.0);
    screenZ = mix(screenZ, 5.0, eio(t));
    
    t = tl(time, 1.0, 1.0);
    screenZ = mix(screenZ, .75, eio(t));
    
    
    t = tl(time, 1.0, 1.0);
    screenZ = mix(screenZ, 2.5, eio(t));
    
    
    t = tl(time, 0.5, 1.0);
    cornersAlpha = mix(cornersAlpha, 0., t);
    screenZAlpha = mix(screenZAlpha, 0., t);
    colToUv = mix(colToUv, 1.0, eio(t));
    
    t = tl(time, 0.0, 0.0);
    cornersAnim = mix(cornersAnim, 0., t);
    
    t = tl(time, 0.5, 1.0);
    cameraPos = mix(cameraPos, vec3(5., 15., 6.0), eio(t));
    cameraTarget = mix(cameraTarget, vec3(0.0, 0.0, 6.), eio(t));
    
    for (int i=0; i<6; i++) {
        t = tl(time, 0.25, 0.25);
        radiusAnim = mix(radiusAnim, float(i) + 2., t);
        t = tl(time, 0.25, 0.25);
        routeAnim = mix(routeAnim, float(i) + 2., t);
        t = tl(time, 0.25, 0.25);
        sphereAnim = mix(sphereAnim, float(i) + 2., t);
    }
    
    
    t = tl(time, 1.0, 1.0);
    cameraPos = mix(cameraPos, vec3(2., 3., -3.), eio(t));
    cameraTarget = mix(cameraTarget, vec3(0.0, 0.0, 3.0), eio(t));
    radiusAlpha = mix(radiusAlpha, 0.0, t);
    routeAnim = mix(routeAnim, 1.0, t);
    sphereAnim = mix(sphereAnim, 1.0, t);
    colToUv = mix(colToUv, 1.0, eio(t));
    screenAlpha = mix(screenAlpha, 0.0, t);
    
    t = tl(time, 0.5, 1.0);
    rayDirectionAnim2 = mix(rayDirectionAnim2, 1.0, eio(t));
    
    t = tl(time, 0.5, 4.0);
    rayDirectionAnim = mix(rayDirectionAnim, 1.0, t);
    
    
    t = tl(time, 0.5, 1.0);
    raySphereAlpha = mix(raySphereAlpha, 0.0, t);
    rayDirectionAnim2 = mix(rayDirectionAnim2, 0.0, t);
    
    
    t = tl(time, 0.5, 1.0);
    cameraPos = mix(cameraPos, vec3(0.), eio(t));
    cameraTarget = mix(cameraTarget, vec3(0.0, 0.0, 5.), eio(t));
}

vec2 opU(vec2 a, vec2 b)
{
    return a.x < b.x ? a : b;
}

float sdLine( vec3 p, vec3 a, vec3 b, float r )
{
    vec3 pa = p - a, ba = b - a;
    float h = clamp( dot(pa,ba)/dot(ba,ba), 0.0, 1.0 );
    return length( pa - ba*h ) - r;
}

float sdBox( vec3 p, vec3 b )
{
  vec3 d = abs(p) - b;
  return length(max(d,0.0))
         + min(max(d.x,max(d.y,d.z)),0.0); // remove this line for an only partially signed sdf 
}

float sdSphere(vec3 p, float s)
{
    return length(p) - s;
}

vec3 sunDir = normalize(vec3(.3, .25, .2));
vec3 skyColor(vec3 rd)
{
    float sundot = clamp(dot(rd,sunDir),0.0,1.0);
    // sky		
    vec3 col = mix(vec3(0.2,0.5,0.85)*1.1, vec3(0.0,0.15,0.7), rd.y);
    col = mix( col, 0.85*vec3(0.8,0.8,0.7), pow( 1.0-max(rd.y,0.0), 4.0 ) );
    // sun
    col += 0.3*vec3(1.0,0.7,0.4)*pow( sundot,5.0 );
    col += 0.5*vec3(1.0,0.8,0.6)*pow( sundot,64.0 );
    col += 6.0*vec3(1.0,0.8,0.6)*pow( sundot,1024.0 );
    return col * 3.0;
}

vec3 screenPos;

vec2 sceneSpheres(vec3 p)
{
    vec2 s1 = vec2(sdSphere(p - vec3(-2.0, 0.0, 6.0), 1.), MAT_SPHERE1);
    vec2 s2 = vec2(sdSphere(p - vec3(0.0, 0.0, 12.0), 1.), MAT_SPHERE2);
    vec2 s3 = vec2(sdSphere(p - vec3(2.0, 0.0, 9.0), 1.), MAT_SPHERE3);
    return opU(opU(s1, s2), s3);
}

vec2 sceneMap(vec3 p)
{
    vec2 s = sceneSpheres(p);
    vec2 p1 = vec2(p.y + 2.0, MAT_FLOOR);
    return opU(s, p1);
}

vec3 normal(vec3 p)
{
    vec2 e = vec2(0.001, 0.0);
    float d = sceneMap(p).x;
    return normalize(d - vec3(sceneMap(p - e.xyy).x, sceneMap(p - e.yxy).x, sceneMap(p - e.yyx).x));
}

void sceneTrace(inout vec3 pos, vec3 ray, out vec2 mat, inout float depth, float maxD)
{
    vec3 ro = pos;
    for(int i = 0; i < 70; i++) {
        if (depth > maxD) {
        	depth = maxD;
            break;
        }
    	pos = ro + ray * depth;
        mat = sceneMap(pos);
        if (mat.x < 0.001) {
            break;
        }
        depth += mat.x;
    }
}

vec2 screenMap(vec3 p)
{
    vec2 screenSize = iResolution.xy / min(iResolution.x, iResolution.y);
    vec2 b1 = vec2(sdBox(p - vec3(0., 0., screenZ), vec3(screenSize, 0.01)), MAT_SCREEN);
    return b1;
}

void screenTrace(inout vec3 pos, vec3 ray, out vec2 mat, inout float depth, float maxD)
{
    vec3 ro = pos;
    for(int i = 0; i < 20; i++) {
        if (depth > maxD) {
        	depth = maxD;
            break;
        }
    	pos = ro + ray * depth;
        mat = screenMap(pos);
        if (mat.x < 0.001) {
            break;
        }
        depth += mat.x;
    }
}

float remap(float val, float im, float ix, float om, float ox)
{
    return clamp(om + (val - im) * (ox - om) / (ix - im), om, ox);
}

vec2 gizmoCorners(vec3 p)
{
    vec2 screenSize = iResolution.xy / min(iResolution.x, iResolution.y);
    
    float a1 = remap(cornersAnim, 0.0, 0.25, 0.0, 1.0);
    float a2 = remap(cornersAnim, 0.25, 0.5, 0.0, 1.0);
    float a3 = remap(cornersAnim, 0.5, 0.75, 0.0, 1.0);
    float a4 = remap(cornersAnim, 0.75, 1.0, 0.0, 1.0);
    
    vec2 c1 = vec2(sdLine(p, vec3(0.), mix(vec3(0.), vec3(screenSize, screenZ), a1), 0.02), MAT_CORNER);
    vec2 c2 = vec2(sdLine(p, vec3(0.), mix(vec3(0.), vec3(screenSize * vec2(1.,-1.), screenZ), a2), 0.02), MAT_CORNER);
    vec2 c3 = vec2(sdLine(p, vec3(0.), mix(vec3(0.), vec3(screenSize * vec2(-1.,-1.), screenZ), a3), 0.02), MAT_CORNER);
    vec2 c4 = vec2(sdLine(p, vec3(0.), mix(vec3(0.), vec3(screenSize * vec2(-1.,1.), screenZ), a4), 0.02), MAT_CORNER);
    return opU(c1, opU(c2, opU(c3, c4)));
}

vec2 gizmoScreenZ(vec3 p)
{
    vec2 c1 = vec2(sdLine(p, vec3(0.), vec3(0., 0., screenZ), 0.03), MAT_SCREENZ);
    return c1;
}

float sphereID = 0.0;
vec2 gizmoMarching(vec3 p)
{
    vec3 ray = vec3(0., 0., 1.);
    vec2 d = vec2(10000.);
    
    float t = 0.0;
    for(int i=0; i<7; i++) {
    	vec3 pos = ray * t;
        vec2 s = vec2(sdSphere(p - pos, 0.15), MAT_MARCHSPHERE);
        if (s.x < d.x) {
            d = s;
            sphereID = float(i);
        }
        
        float dist = sceneSpheres(pos).x;
        
        float anim = clamp(routeAnim - float(i) - 1., 0.0, 1.0);
        vec2 c1 = vec2(sdLine(p, pos, pos + mix(vec3(0.), ray * dist, anim), 0.03), MAT_MARCHROUTE);
        
        d = opU(d, c1);
        t += dist;
    }
    return d;
}

vec2 gizmoMarchingRadius(vec3 p)
{
    vec2 d = vec2(p.y, MAT_MARCHRADIUS);
    return d;
}


vec2 gizmoRayDirection(vec3 p)
{
    float a1 = fract(rayDirectionAnim * 19.99999);
    float a2 = floor(rayDirectionAnim * 19.99999) / 20.;
    vec2 screenSize = iResolution.xy / min(iResolution.x, iResolution.y);
    screenSize.y *= -1.;
    screenSize = mix(-screenSize, screenSize, vec2(a1, a2));
    vec2 c1 = vec2(sdLine(p, vec3(0.), mix(vec3(0.), vec3(screenSize, screenZ) * 10.0, rayDirectionAnim2), 0.02), MAT_RAYDIRECTION);
    
    vec3 ray = normalize(vec3(screenSize, screenZ));
    vec3 pos;
    float t = 0.01;
    for(int i = 0; i < 20; i++) {
    	pos = ray * t;
        vec2 d = sceneMap(pos);
        t += d.x;
    }
    
    c1 = opU(c1, vec2(sdSphere(p - pos, 0.3), MAT_HITPOINT));
    
    return c1;
}

vec2 gizmoMap(vec3 p)
{
    vec2 d = opU(gizmoCorners(p), gizmoScreenZ(p));
    d = opU(d, gizmoMarching(p));
    d = opU(d, gizmoRayDirection(p));
    return d;
}

void gizmoTrace(inout vec3 pos, vec3 ray, out vec2 mat, inout float depth, float maxD)
{
    vec3 ro = pos;
    for(int i = 0; i < 60; i++) {
        if (depth > maxD) {
        	depth = maxD;
            break;
        }
    	pos = ro + ray * depth;
        mat = gizmoMap(pos);
        if (mat.x < 0.001) {
            break;
        }
        depth += mat.x;
    }
}

vec2 radiusMap(vec3 p)
{
    return gizmoMarchingRadius(p);
}

void radiusTrace(inout vec3 pos, vec3 ray, out vec2 mat, inout float depth, float maxD)
{
    vec3 ro = pos;
    for(int i = 0; i < 40; i++) {
        if (depth > maxD) {
        	depth = maxD;
            break;
        }
    	pos = ro + ray * depth;
        mat = radiusMap(pos);
        if (mat.x < 0.001 || depth > maxD) {
            break;
        }
        depth += mat.x;
    }
}

float shadow(in vec3 p, in vec3 l, float ma)
{
    float t = 0.1;
    float t_max = ma;
    
    float res = 1.0;
    for (int i = 0; i < 16; ++i)
    {
        if (t > t_max) break;
        vec3 pos = p + t*l;
        float d = opU(sceneMap(pos), screenMap(pos)).x;
        if (d < 0.001)
        {
            return 0.0;
        }
        t += d*1.0;
        res = min(res, 10.0 * d / t);
    }
    
    return res;
}

// checkerbord
// https://www.shadertoy.com/view/XlcSz2
float checkersTextureGradBox( in vec2 p, in vec2 ddx, in vec2 ddy )
{
    // filter kernel
    vec2 w = max(abs(ddx), abs(ddy)) + 0.01;  
    // analytical integral (box filter)
    vec2 i = 2.0*(abs(fract((p-0.5*w)/2.0)-0.5)-abs(fract((p+0.5*w)/2.0)-0.5))/w;
    // xor pattern
    return 0.5 - 0.5*i.x*i.y;                  
}

vec3 sceneShade(vec2 mat, vec3 pos, vec3 ray, float depth, float maxD)
{
    vec3 col;
    vec3 sky = skyColor(ray);
    if (depth > maxD - 0.01) {
    	return sky;
    }
    float sha = shadow(pos, sunDir, 10.);
    vec3 norm = normal(pos);
    vec3 albedo = vec3(0.);
    if(mat.y == MAT_SPHERE1) {
        albedo = vec3(1., 0., 0.);
    } else if (mat.y == MAT_SPHERE2) {
        albedo = vec3(0., 1., 0.);
    } else if (mat.y == MAT_SPHERE3) {
        albedo = vec3(0., 0., 1.);
    } else if(mat.y == MAT_FLOOR) {
        vec2 ddx_uvw = dFdx( pos.xz ); 
        vec2 ddy_uvw = dFdy( pos.xz ); 
        float checker = checkersTextureGradBox( pos.xz, ddy_uvw, ddy_uvw );
        albedo = vec3(max(0.2, checker)) * vec3(.8,0.8,0.7) * 2.0;
    }
    
    float diffuse = clamp(dot(norm, sunDir), 0.0, 1.0) * sha * 2.0;
    col = albedo * (diffuse + 0.05);
    
    float fo = 1.0 - exp2(-0.0001 * depth * depth);
    vec3 fco = 0.65*vec3(0.4,0.65,1.0);
    col = mix( col, sky, fo );
    return col;
}

vec3 screenShade(vec2 mat, vec3 pos)
{
    vec3 ro = vec3(0., 0., 0.);
    vec3 ta = vec3(0., 0., 3.);
    vec3 fo = normalize(ta - ro);
    vec3 ri = normalize(cross(vec3(0.,1.,0.), fo));
    vec3 up = normalize(cross(fo,ri));
    mat3 cam = mat3(ri,up,fo);
    vec3 ray = cam * normalize(pos);
    float depth = 0.01;
    vec3 p = ro;
    sceneTrace(p, ray, mat, depth, 100.);
    vec3 col = vec3(0.);
    col = sceneShade(mat, p, ray, depth, 100.);
    
    float a1 = fract(rayDirectionAnim * 19.99999);
    float a2 = floor(rayDirectionAnim * 19.99999 + 1.0) / 20.;
    float a3 = floor(rayDirectionAnim * 19.99999) / 20.;
    
    float aspect = iResolution.y / iResolution.x;
    float halfAspect = aspect * 0.5;
    
    a1 = step(pos.x * halfAspect + 0.5, a1);
    a2 = step(-pos.y * 0.49 + 0.51+ 0.0, a2);
    a3 = step(-pos.y * 0.49 + 0.51 + 0.0, a3);
    //col *= min(screenAlpha + min(a2 * a1 + a3, 1.0), 1.0);
    
    vec3 uvCoord = vec3(pow(clamp(mix(pos.xy*0.5+0.5, pos.xy, uvToP), 0.0, 1.0), vec2(2.2)), 0.0);
    col = mix(col, uvCoord, colToUv - min(screenAlpha + min(a2 * a1 + a3, 1.0), 1.0));
    return col;
    //return vec3(pow(clamp(pos.xy, 0.0, 1.0), vec2(2.2)), 0.0);
}

vec4 gizmoShade(vec2 mat, vec3 p)
{
    vec4 col = vec4(0.);

    if(mat.y == MAT_CORNER) {
        col = vec4(1.,0.,0., cornersAlpha);
    } else if (mat.y == MAT_SCREENZ) {
    	col = vec4(0.05, 0.05, 1., screenZAlpha);
    } else if (mat.y == MAT_MARCHSPHERE) {
        float alpha = clamp(sphereAnim - sphereID, 0.0, 1.0);
        vec3 sc = mix(vec3(.0, .1, 3.), vec3(.02, 1., .02), float(sphereID == 0. || sphereID == 6.));
    	col = vec4(sc, alpha * raySphereAlpha);
    } else if (mat.y == MAT_MARCHROUTE) {
        col = vec4(1., 0., 0., .9);
    } else if (mat.y == MAT_RAYDIRECTION) {
        col = vec4(1., 0., 0., .9);
    } else if (mat.y == MAT_HITPOINT) {
    	col = vec4(.02, 1., .02, raySphereAlpha);
    }
    return col;
}

vec4 radiusShade(vec2 mat, vec3 p)
{
    vec4 col = vec4(0.);

    vec3 ray = vec3(0., 0., 1.);
    vec2 d = vec2(10000.);

    float t = 0.0;
    for(int i=0; i<7; i++) {
        vec3 pos = ray * t;
        vec2 dd = sceneSpheres(pos);
        d = vec2(sdSphere(p - pos, dd.x), MAT_MARCHSPHERE);
        float alpha2 = step(radiusAnim, float(i) + 2.);
        float alpha = clamp(radiusAnim - float(i) - 1., 0.0, 1.0);
        
        vec4 cirCol = mix(vec4(.0, 0.05, 0.1, 0.9), vec4(0.2, 1., 1.4, .6) , alpha2);
        col = mix(col, cirCol, smoothstep(0.01, 0., d.x) * cirCol.a * alpha);
        col = mix(col, vec4(0., 0., 0., 1.), smoothstep(0.02, 0., abs(d.x) - 0.01) * alpha);
        t += dd.x;
    }
    col *= radiusAlpha;
    return col;
}

float luminance(vec3 col)
{
    return dot(vec3(0.298912, 0.586611, 0.114478), col);
}

vec3 reinhard(vec3 col, float exposure, float white) {
    col *= exposure;
    white *= exposure;
    float lum = luminance(col);
    return (col * (lum / (white * white) + 1.0) / (lum + 1.0));
}

vec3 render(vec2 p) {
    screenPos = vec3(p, 2.5);
    vec3 ro = cameraPos;
    vec3 ta = cameraTarget;
    vec3 fo = normalize(ta - ro);
    vec3 ri = normalize(cross(vec3(0.,1.,0.), fo));
    vec3 up = normalize(cross(fo,ri));
    mat3 cam = mat3(ri,up,fo);
    vec3 ray = cam * normalize(screenPos);
    float depth = 0.01;
    vec2 mat;
    vec3 col = vec3(0.);
    
    vec3 pos = ro;
    sceneTrace(pos, ray, mat, depth, 100.);
    
    col = sceneShade(mat, pos, ray, depth, 100.);
    
    float sceneDepth = depth;
    depth = 0.01;
    pos = ro;
    screenTrace(pos, ray, mat, depth, sceneDepth);
    if (depth < sceneDepth) {
        col = screenShade(mat, pos);
    }
    
    float sceneAndScreenDepth = depth;
    depth = 0.01;
    pos = ro;
    radiusTrace(pos, ray, mat, depth, sceneAndScreenDepth);
    if (depth < sceneAndScreenDepth) {
        vec4 radius = radiusShade(mat, pos);
        col = mix(col, radius.rgb, radius.a);
    }
    
    float sceneAndScreenAndGizmoDepth = sceneAndScreenDepth;
    depth = 0.01;
    pos = ro;
    gizmoTrace(pos, ray, mat, depth, sceneAndScreenAndGizmoDepth);
    if (depth < sceneAndScreenAndGizmoDepth) {
        vec4 gizmo = gizmoShade(mat, pos);
        col = mix(col, gizmo.rgb, gizmo.a);
    }
    return col;
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    timeLine(mod(iTime, 41.));

    vec2 p = (fragCoord * 2.0 - iResolution.xy)/min(iResolution.x, iResolution.y);
    vec2 dp = 1. / iResolution.xy;

    vec3 col = vec3(0.);
    
    
    // AA
    // https://www.shadertoy.com/view/Msl3Rr
    for(int y = 0; y < 2; y++) {
        for(int x = 0; x < 2; x++) {
            vec2 off = vec2(float(x),float(y))/2.;
            vec2 xy = (-iResolution.xy+2.0*(fragCoord+off)) / iResolution.y;
        	col += render(xy)*0.25;
        }
    }
    
    col = reinhard(col, 1.0, 1000.0);
    col = pow(col, vec3(1.0/2.2));
    
    //col = mix(col, vec3(mix(uv, p, uvToP), 0.), colToUv);
    
    fragColor = vec4(col,1.0);
}
```



## Reader



这篇收录于RayMachine, 

