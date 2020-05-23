# GPU Particular  with Unity GLSL













// GPU Particle Example 2
// By: Brandon Fogerty
// bfogerty at gmail dot com
// xdpixel.com

#ifdef GL_ES
precision mediump float;
#endif

uniform float time;
uniform vec2 resolution;

#define HorizontalAmplitude         0.30
#define VerticleAmplitude           0.20
#define HorizontalSpeed             0.90
#define VerticleSpeed               0.50
#define ParticleMinSize             1.76
#define ParticleMaxSize             1.71
#define ParticleBreathingSpeed      0.30
#define ParticleColorChangeSpeed    0.70
#define ParticleCount               7.0
#define ParticleColor1              vec3(9.0, 5.0, 3.0)
#define ParticleColor2              vec3(1.0, 3.0, 9.0)

void main( void ) 
{
    vec2 pos = ( gl_FragCoord.xy / resolution.xy ) * 2.0 - 1.0;
    pos.x *= (resolution.x / resolution.y);
    
    vec3 c = vec3( 0, 0, 0 );
    
    for( float i = 1.0; i &lt; ParticleCount+1.0; ++i )
    {
        float cs = cos( time * HorizontalSpeed * (i/ParticleCount) ) * HorizontalAmplitude;
        float ss = sin( time * VerticleSpeed   * (i/ParticleCount) ) * VerticleAmplitude;
        vec2 origin = vec2( cs , ss );
        
        float t = sin( time * ParticleBreathingSpeed * i ) * 0.5 + 0.5;
        float particleSize = mix( ParticleMinSize, ParticleMaxSize, t );
        float d = clamp( sin( length( pos - origin )  + particleSize ), 0.0, particleSize);
        
        float t2 = sin( time * ParticleColorChangeSpeed * i ) * 0.5 + 0.5;
        vec3 color = mix( ParticleColor1, ParticleColor2, t2 );
        c += color * pow( d, 70.0 );
    }
    
    gl_FragColor = vec4( c, 1.0 );

}