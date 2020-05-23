# 写在前面

时隔两个月我终于来更新博客了，之前一直在学东西，做一些项目，感觉没什么可以分享的就一直没写。本来之前打算写云彩渲染或是Compute Shader的，觉得时间比较长所以打算先写个简单的。

今天扫项目的时候看到了很早之前下载的Unity Chan的项目，其实很早之前就想要分析下里面的卡通效果是怎么做的。

# Unity Chan

想必很多人都看到或听过Unity  Chan，也可以说是Unity酱、Unity娘……她数次出现在早期的AR程序中，一个萌娘在现实生活中的一张卡片上跳来跳去的我相信你大概可以想起来一点…据传，这个二次元生物是岛国分公司的Unity发布的吉祥物，并提供了开源素材来吸引岛国二次元游戏开发者。鉴于我对二次元世界不甚了解，感兴趣的可以在[萌娘百科](https://zh.moegirl.org/Unity%E5%A8%98)里找到更多介绍。Unity酱的官方资源可以在[商店](https://www.assetstore.unity3d.com/en/#!/content/18705)里找到，资源里自带31个动画和三个内置场景，还没下载的可以去看看，总之就是萌萌哒~



![这里写图片描述](Unity_NPR_01.assets/20160403194555873) ![这里写图片描述](Unity_NPR_01.assets/20160403194618061)



今天发现Unity酱衣服的拉锁是Unity的logo，挺有爱的。

# Unity Chan使用的Shader

当然了，我们还是要谈一下今天的重点，就是Unity酱的卡通效果是怎么实现的。卡通渲染在我的博客里简直是感也赶不走的存在了，比如[【Unity Shader实战】卡通风格的Shader（一）](http://blog.csdn.net/candycat1992/article/details/37882425)、[【Unity Shader实战】卡通风格的Shader（二）](http://blog.csdn.net/candycat1992/article/details/41120019)、[【NPR】漫谈轮廓线的渲染](http://blog.csdn.net/candycat1992/article/details/45577749)、[【Shader拓展】Illustrative Rendering in Team Fortress 2](http://blog.csdn.net/candycat1992/article/details/37696187)，[【NPR】卡通渲染](http://blog.csdn.net/candycat1992/article/details/50167285)。恩，这次还是要学习下一些成熟项目里卡通渲染实现。

Unity酱包含了3个CG文件：

| 名字         | 用途                                                         |
| ------------ | ------------------------------------------------------------ |
| CharaOutline | 包含了最通用的shader，即绘制描边效果。                       |
| CharaMain    | 角色使用的最主要的shader，包含了一些漫反射、阴影、高光、边缘高光、反射等通用的vs和fs的实现。用于渲染**衣服和头发**。 |
| CharaSkin    | 皮肤使用的shader，包含了漫反射、边缘高光和阴影的实现（相较于CharaMain，没有计算高光和反射）。用于渲染**皮肤、眼睛、脸蛋、睫毛**。（脸蛋……原谅我的翻译） |

# CharaOutline：描边

这里所有的卡通效果都需要描边，只是不是描黑边。这里描边的实现也是通过把顶点沿着法线方向扩张后得到的。在我之前写的文章里，例如[【Unity Shader实战】卡通风格的Shader（二）](http://blog.csdn.net/candycat1992/article/details/41120019)中，也是这样的思想。在那篇文章里，。CharaOutline包含了一对vs和fs：

- vert实现：

  ```C++
  // Vertex shader
  v2f vert( appdata_base v )
  {
      v2f o;
      o.uv = TRANSFORM_TEX( v.texcoord.xy, _MainTex );
  
      half4 projSpacePos = mul( UNITY_MATRIX_MVP, v.vertex );
      half4 projSpaceNormal = normalize( mul( UNITY_MATRIX_MVP, half4( v.normal, 0 ) ) );
      half4 scaledNormal = _EdgeThickness * INV_EDGE_THICKNESS_DIVISOR * projSpaceNormal; // * projSpacePos.w;
  
      scaledNormal.z += 0.00001;
      o.pos = projSpacePos + scaledNormal;
  
      return o;
  }
  ```

  上面的实现非常的简单，就是把顶点和法线变换到裁剪坐标空间后，把顶点沿着法线方向进行扩张。不过上面把法线的z分量加了一点值，这一步大概是为了稍微防止一下描边遮挡住正常渲染。当然，这个方法有在[【Unity Shader实战】卡通风格的Shader（二）](http://blog.csdn.net/candycat1992/article/details/41120019)中提到的弊端，也就是说当描边宽度很大时，就会有穿帮镜头。解决方法也请见那篇文章，大家可以改变Unity酱的这种实现。

- frag实现：

  ```C++
  // Fragment shader
  float4 frag( v2f i ) : COLOR
  {
      float4_t diffuseMapColor = tex2D( _MainTex, i.uv );
  
      float_t maxChan = max( max( diffuseMapColor.r, diffuseMapColor.g ), diffuseMapColor.b );
      float4_t newMapColor = diffuseMapColor;
  
      maxChan -= ( 1.0 / 255.0 );
      float3_t lerpVals = saturate( ( newMapColor.rgb - float3( maxChan, maxChan, maxChan ) ) * 255.0 );
      newMapColor.rgb = lerp( SATURATION_FACTOR * newMapColor.rgb, newMapColor.rgb, lerpVals );
  
      return float4( BRIGHTNESS_FACTOR * newMapColor.rgb * diffuseMapColor.rgb, diffuseMapColor.a ) * _Color * _LightColor0; 
  }
  ```

  Unity酱描的并不是黑边，而是在原漫反射贴图颜色的基础上加了一点小trick。总体来讲，是希望这个描边的颜色暗于正常渲染的颜色，起到强调边缘的效果。这个颜色是通过亮度系数BRIGHTNESS_FACTOR、计算得到的新颜色newMapColor和原贴图颜色diffuseMapColor相乘得到的。BRIGHTNESS_FACTOR用于控制整体变暗的程度，这里取的是0.8。newMapColor的计算是重点，它的初始值是原贴图颜色，然后不同分量进行了不同的颜色处理。**值最高的分量颜色保持不变，其他分量通常是对原分量乘以变暗系数SATURATION_FACTOR后的结果**。为了理解上面的代码，我们其实可以关注lerpVals什么时候会取0，什么时候会取1即可。分析可知，值最高的分量会取1，所以说值最高的分量颜色保持不变；而其他分量只要比最高值小，就会取0，所以说它们通常会取到变暗后的颜色值。最后描边颜色还乘以了一个颜色属性_Color和光源颜色_LightColor0，更具可调性。

在需要使用描边的shader里，我们只需要声明**第二个Pass**：

```C++
Pass
{
    Cull Front
    ZTest Less
    CGPROGRAM
    #pragma vertex vert
    #pragma fragment frag
    #include "UnityCG.cginc"
    #include "CharaOutline.cg"
    ENDCG
}
```

在上面的代码里，我们只渲染模型背面，并且设置只有在小于当前深度时才渲染。注意到，**描边的Pass声明在了第二个Pass**，这其实更有利于提高渲染性能，因为描边Pass中的绝大多数像素都由于无法通过深度测试而根本不会被调用fs。



![这里写图片描述](Unity_NPR_01.assets/20160403183324720)



上面的图对比了原实现和仅把颜色变暗的效果。很明显，左边的实现更好通过改变一些饱和度更好地强调了边缘细节。

# CharaMain：衣服和头发

CharaMain主要用于渲染角色的衣服和头发，包含了CharaMain.cg的shader有：Unitychan_chara_hair，Unitychan_chara_hair_ds，Unitychan_chara_fuku，Unitychan_chara_fuku_ds。_hair和_fuku的shader代码其实完全一样，而_ds是表示是不是双面渲染，没有_ds的在渲染时提出了背面（Cull  Back），而有_ds的就关闭了剔除（Cull  Off）。Unity酱的项目里都是使用了双面渲染的版本，这大概是为了保证一些单面片也能不穿帮吧。

下面具体看一下里面的代码。CharaMain中包含了一对vs和fs的实现：

- vert：顶点变换，计算主纹理（_MainTex）的采样坐标，计算世界空间下的法线方向、视角方向、光照方向等；

- frag：主要完成了五个工作：

  1. 计算包含衰减的光照颜色。我们通常计算漫反射是通过对贴图采样后再乘以漫反射系数（n点乘l）。而这里的做法是使用法线和观察方向的点积结果去采样一张**衰减纹理**，得到衰减值。然后靠这个衰减值去混合原贴图颜色和变暗后的原贴图颜色（其实就是取平方）。这样得到的效果其实**并不能说是漫反射光照**，因为**并没有考虑光源方向**，而是使用了类似算边缘高光的方法（算n点乘v）来计算光照衰减。这也是卡通效果里的一些trick吧。附上源码：

     ```C#
     // Falloff. Convert the angle between the normal and the camera direction into a lookup for the gradient
     float_t normalDotEye = dot( normalVec, i.eyeDir.xyz );
     float_t falloffU = clamp( 1.0 - abs( normalDotEye ), 0.02, 0.98 );
     float4_t falloffSamplerColor = FALLOFF_POWER * tex2D( _FalloffSampler, float2( falloffU, 0.25f ) );
     float3_t shadowColor = diffSamplerColor.rgb * diffSamplerColor.rgb;
     float3_t combinedColor = lerp( diffSamplerColor.rgb, shadowColor, falloffSamplerColor.r );
     combinedColor *= ( 1.0 + falloffSamplerColor.rgb * falloffSamplerColor.a );
     ```

  2. 计算高光反射。这一部分同样不按常理出牌，也挺奇葩的。首先计算得到了我们之前所谓的高光反射系数，按正常的写法是n和h的点乘结果，但这里仍然使用了n和v的点乘。然后，把之前得到的”漫反射系数“和这次的”高光反射系数“以及高光反射的指数部分传给[Cg的lit函数](http://http.developer.nvidia.com/Cg/lit.html)，让它计算各个光照系数。当然了，我们其实就是为了得到高光反射光照而已，这一步完全可以自己写代码实现，它这么写应该是为了充分利用GPU的一些native实现，提高一些性能。得到高光反射结果后，再和高光反射颜色和原贴图颜色相乘即可得到最后的高光反射颜色。源码如下：

     ```C++
     // Specular
     // Use the eye vector as the light vector
     float4_t reflectionMaskColor = tex2D( _SpecularReflectionSampler, i.uv.xy );
     float_t specularDot = dot( normalVec, i.eyeDir.xyz );
     float4_t lighting = lit( normalDotEye, specularDot, _SpecularPower );
     float3_t specularColor = saturate( lighting.z ) * reflectionMaskColor.rgb * diffSamplerColor.rgb;
     combinedColor += specularColor;
     ```

  3. 接下来是计算反射部分。这次计算反射向量的部分总算正常了，但是作者这里并没有使用环境贴图来进行采样，而是一张普通的二维纹理。采样坐标是通过把反射方向从[-1,  1]映射到[0,  1]来实现的。这样得到了初始的反射颜色。随后，调用GetOverlayColor函数来计算原光照结果和反射颜色混合后的结果，GetOverlayColor中也是各种trick。然后，使用反射遮罩值来混合之前的计算结果和反射结果，并和颜色属性以及光源颜色相乘得到结果。源码：

     ```C++
     // Reflection
     float3_t reflectVector = reflect( -i.eyeDir.xyz, normalVec ).xzy;
     float2_t sphereMapCoords = 0.5 * ( float2_t( 1.0, 1.0 ) + reflectVector.xy );
     float3_t reflectColor = tex2D( _EnvMapSampler, sphereMapCoords ).rgb;
     reflectColor = GetOverlayColor( reflectColor, combinedColor );
     
     combinedColor = lerp( combinedColor, reflectColor, reflectionMaskColor.a );
     combinedColor *= _Color.rgb * _LightColor0.rgb;
     float opacity = diffSamplerColor.a * _Color.a * _LightColor0.a;
     ```

     上面最后还计算了该像素的透明度，也就是漫反射贴图、颜色属性和光源颜色的透明度的乘积。它会作为输出像素的透明通道值。

  4. 计算阴影。这部分计算也挺有意思的，它并没有直接使用LIGHT_ATTENUATION来乘以之前结果，而是使用阴影衰减值来计算混合一个阴影颜色和现有颜色，这个阴影颜色其实就是漫反射纹理采样结果的平方。这样一来，得到的阴影效果其实就是，在阴影完全覆盖的地方效果就是变暗了的纹理颜色：

     ```C++
     #ifdef ENABLE_CAST_SHADOWS
     
         // Cast shadows
         shadowColor = _ShadowColor.rgb * combinedColor;
         float_t attenuation = saturate( 2.0 * LIGHT_ATTENUATION( i ) - 1.0 );
         combinedColor = lerp( shadowColor, combinedColor, attenuation );
     
     #endif
     ```

  5. 最后是计算边缘高光。众所周知边缘高光是卡通效果的必备效果。不同的是，这里还使用了n和l的点乘结果来和n和v的点乘结果相乘，计算边缘高光的衰减，然后用它对一张边缘高光纹理采样，得到真正的边缘高光衰减值：

     ```C++
     // Rimlight
     float_t rimlightDot = saturate( 0.5 * ( dot( normalVec, i.lightDir ) + 1.0 ) );
     falloffU = saturate( rimlightDot * falloffU );
     falloffU = tex2D( _RimLightSampler, float2( falloffU, 0.25f ) ).r;
     float3_t lightColor = diffSamplerColor.rgb; // * 2.0;
     combinedColor += falloffU * lightColor;
     ```



![这里写图片描述](Unity_NPR_01.assets/20160403162604624)



上图表示了对Unity酱的手臂衣服依次添加上面四个步骤的结果。总结一下它里面用到的一些trick：

- 计算了一个全局的shadowColor，它其实就是漫反射纹理采样结果的平方，效果就是比原贴图颜色暗了一点。
- 漫反射计算不需要考虑光照方向，而是使用n和v的点乘来计算衰减，这个衰减将会混合上面的shadowColor和正常的颜色贴图。得到的效果是模型**边缘部分会较暗**。
- 高光反射的部分同样不考虑光照方向，而是使用n和v的点乘。得到的效果是**正对视角方向的部分高光越明显，和光源无光**。
- 计算环境反射时使用**普通的二维纹理来代替环境贴图**。
- 使用阴影衰减值来混合shadowColor，这样**阴影区域会保留角色的纹理细节**。
- 边缘高光系数是NdotL和NdotV的共同结果，即**那些和光照方向一致、且在模型边缘的地方高光越明显**。

# CharaSkin：皮肤

CharaSkin主要用于渲染皮肤、眼睛、脸蛋、睫毛，这些部分。CharaSkin使用的代码和CharaMain中基本一样，只是精简了一些部分，它去掉了计算环境反射、高光反射的部分，只保留漫反射、边缘高光、和阴影的计算部分。而且，在计算边缘高光时，高光颜色也比CharaMain中的暗了一倍，即只去源颜色的0.5倍。除此之外，皮肤使用的漫反射衰减纹理也与衣服等使用的纹理不同：



![这里写图片描述](Unity_NPR_01.assets/20160403185701963)



越接近边缘的部分皮肤颜色越趋近于肉色。

# 总结

总体来说，Unity酱里面的shader有两个值得学习的地方：

- 描边。描边的颜色并不是取黑色，而是对原纹理颜色进行逐分量处理后的一个加强颜色。
- 光照模型。很多trick： 
  - 漫反射系数是靠NdotV来对衰减纹理采样得到的，然后对两个颜色值进行混合。衰减纹理可以用于控制不同材质的漫反射效果，例如皮肤使用的衰减纹理是由白到肉色渐变，而衣服等其他材质使用的衰减纹理是由黑到白；
  - 环境反射使用二维纹理来代替；
  - 阴影计算是使用衰减值来混合两种颜色；
  - 边缘高光是NdotV和NdotL共同作用的结果。

还有一些优化细小的问题：

- 为了优化在移动平台的性能，都使用了half精度而非float精度；
- 把高光反射颜色（RGB）和反射遮罩值（A）存储在了一张纹理中。

# 写在最后

这种风格化效果实现的一个特点就是，很多效果其实并不符合任何物理原理，而是为了eye  candy而使用的trick。一方面好处是计算量比较小，不需要满足物理模型那样进行复杂计算，但另一方面难度也不见得减少了多少，毕竟这些trick也不是一下子就能想到，要试验好久才能得到满意的效果。多看多写吧，总没坏处。