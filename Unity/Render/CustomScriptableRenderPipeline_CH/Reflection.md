# 可编程渲染管线7 反射

原文：https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/

- 添加镜面高光
- 环境反射
- 支持非统一缩放
- 使用反射探针
- 透明度和反射度的结合

这是Unity可编程渲染管线系列教程的第七章，本章将添加物体的反射，包括镜面高光和反射探针的采样。

该教程基于Unity 2018.3.0f2。

![img](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/tutorial-image.jpg)

------

# 1 镜面高光

目前为止，我们都只用了最简单的漫反射光照，游戏物体没有任何的高光。现在我们终于要为物体添加高光了。我们将使用和Unity轻量级渲染管线相同的方法。在[Rendering 4, The Fist Light](https://catlikecoding.com/unity/tutorials/rendering/part-4/)中有镜面高光背后的理论介绍，不过它使用的是另一种计算模型，可供参考。

## 1.1 平滑度（Smoothness）

一个完美的漫射表面（理想的漫反射体）是不会产生任何高光反射的。物体表面如果很粗糙就难以产生相对集中的反射光线。而表面越光滑，就会有越多的光线反射而不是散射出去。我们使用材质属性Smoothness的来表达光滑程度，该值应处于0-1之间，默认值为0.5.

```
		_Cutoff ("Alpha Cutoff", Range(0, 1)) = 0.5		_Smoothness ("Smoothness", Range(0, 1)) = 0.5
```

![img](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/specular-highlights/smoothness-slider.png)

同时添加对应的着色器变量

```
CBUFFER_START(UnityPerMaterial)	float4 _MainTex_ST;	float _Cutoff;	float _Smoothness;CBUFFER_END
```

## 1.2 表面数据

高光反射的加入让我们的光照模型变得复杂起来，我们我们把这些代码放到一个单独的文件（*Lighting.hlsl*）。我们在其中定义一个**LitSurface**结构，该结构包含了执行光照计算所需要的所有表面数据。包含表面的法线、位置、漫射/反射颜色以及粗糙度。我们还加上了视角方向，虽然他算不上一个表面属性，但是它对于表面的每个点而言都是一个关联的常量。

```
#ifndef MYRP_LIGHTING_INCLUDED#define MYRP_LIGHTING_INCLUDED struct LitSurface {	float3 normal, position, viewDir;	float3 diffuse, specular;	float roughness;}; #endif // MYRP_LIGHTING_INCLUDED
```

添加一个**GetLitSurface**方法，该方法返回一个LitSurface结构体。在这个HLSL文件中，我们不会依赖任何着色器专用的属性、纹理或定义，所以相关的所有数据都只能作为参数传入。虽然我们输入的是平滑度（Smoothness），但我们实际使用的是粗糙度（roughness),因此反转平滑度来得到粗糙度。此外，我们使用金属工作流，并暂时限定在介电材质范围内。介电材质是非金属，光线只会产生微量的完全反射，它对应的灰度高光平均值为0.04。和Unity的渲染管线做法一样，我们将这个值硬编码进程序。

```
struct LitSurface {	…}; LitSurface GetLitSurface (	float3 normal, float3 position, float3 viewDir,	float3 color, float smoothness) {	LitSurface s;	s.normal = normal;	s.position = position;	s.viewDir = viewDir;	s.diffuse = color;	s.specular = 0.04;	s.roughness = 1.0 - smoothness;	return s;}
```

根据迪士尼的着色模型（Disney Principled BRDF），这里的粗糙度称之为 感官粗糙度（perceptual roughness），物理意义上真正的粗糙度应该是他的平方，这两者我们都需要。

```
struct LitSurface {	float3 normal, position, viewDir;	float3 diffuse, specular;	float perceptualRoughness, roughness;}; LitSurface GetLitSurface (	float3 normal, float3 position, float3 viewDir,	float3 color, float smoothness) {	…	s.perceptualRoughness = 1.0 - smoothness;	s.roughness = s.perceptualRoughness * s.perceptualRoughness;	return s;}
```

在Lit.hlsl中导入Lighting.hlsl。

```
#include …#include "Lighting.hlsl"
```

在**LitPassFragment**执行光照计算前，我们得获取表面数据。视角方向可以通过将摄像机位置减去片元位置，经过归一化后获得。

```
	float3 viewDir = normalize(_WorldSpaceCameraPos - input.worldPos.xyz);	LitSurface surface = GetLitSurface(		input.normal, input.worldPos, viewDir,		albedoAlpha.rgb, _Smoothness	);		float3 diffuseLight = input.vertexLighting;
```

## 1.3 漫反射光照

我们要把关于光照的计算转移到Lighting.hlsl中。为**LightSurface**方法传入表面数据和光线方向，让它完成光照的计算。他会执行漫反射点乘，并呈上表面的漫反射颜色。我们先假设它是一个理想光源，纯白色且没有任何衰减，以简化我们的操作。

```
float3 LightSurface (LitSurface s, float3 lightDir) {	float3 color = s.diffuse;	return color * saturate(dot(s.normal, lightDir));}
```

调整**MainLight**，用结构体代替位置和法线参数。调用**LightSurface**方法来代替自己完成点乘运算。

```
float3 MainLight (LitSurface s) {	float shadowAttenuation = CascadedShadowAttenuation(s.position);	float3 lightColor = _VisibleLightColors[0].rgb;	float3 lightDirection = _VisibleLightDirectionsOrPositions[0].xyz;	//float diffuse = saturate(dot(normal, lightDirection));	float3 color = LightSurface(s, lightDirection);	color *= shadowAttenuation;	return color * lightColor;}
```

用同样的方式调整DiffuseLight，不过就它现在的功能而言，叫做GenericLight更合适。

```
//float3 DiffuseLight (//	int index, float3 normal, float3 worldPos, float shadowAttenuation//) {float3 GenericLight (int index, LitSurface s, float shadowAttenuation) {	…		float3 lightVector =		lightPositionOrDirection.xyz - s.position * lightPositionOrDirection.w;	float3 lightDirection = normalize(lightVector);	//float diffuse = saturate(dot(normal, lightDirection));	float3 color = LightSurface(s, lightDirection);		…		float distanceSqr = max(dot(lightVector, lightVector), 0.00001);	color *= shadowAttenuation * spotFade * rangeFade / distanceSqr;	return color * lightColor;}
```

**LitPassFragment**现在需要将表面数据作为参数传递给各个方法。另外，漫反射颜色之前是在最后统一叠加的，但现在由每个光源独自处理，所以在一开始的时候我们就得为顶点光照叠加上漫反射颜色。

```
	//float3 diffuseLight = input.vertexLighting;	float3 color = input.vertexLighting * surface.diffuse;	#if defined(_CASCADED_SHADOWS_HARD) || defined(_CASCADED_SHADOWS_SOFT)		color += MainLight(surface);	#endif		for (int i = 0; i < min(unity_LightIndicesOffsetAndCount.y, 4); i++) {		int lightIndex = unity_4LightIndices0[i];		float shadowAttenuation = ShadowAttenuation(lightIndex, input.worldPos);		color += GenericLight(lightIndex, surface, shadowAttenuation);	}	//float3 color = diffuseLight * albedoAlpha.rgb;	return float4(color, albedoAlpha.a);
```

我们让顶点光源也使用**GenericLight**。顶点光源只包含漫反射，因此只需要位置和法线，除此之外在表面数据中把颜色设为白色，剩下的值则无关紧要。我们为此在Lighting.hlsl中添加一个包裹函数方便使用。

```
LitSurface GetLitSurfaceVertex (float3 normal, float3 position) {	return GetLitSurface(normal, position, 0, 1, 0);}
```

 接着在**LitPassVertex**中使用该方法获取表面数据结构体变量，并用该数据计算顶点光源

```
	LitSurface surface = GetLitSurfaceVertex(output.normal, output.worldPos);	output.vertexLighting = 0;	for (int i = 4; i < min(unity_LightIndicesOffsetAndCount.y, 8); i++) {		int lightIndex = unity_4LightIndices1[i - 4];		output.vertexLighting += GenericLight(lightIndex, surface, 1);	}
```

## 1.4 可选高光

在添加镜面高光前，我们先跳过这步计算，首先完成对完全漫射材质的支持。我们在表面数据结构体中添加bool字段来判断是否为完全漫射，并将它作为**GetLitSurface**函数的一个参数，默认设为false。我们可以选择硬编码这个参数，又或者用一个着色器关键字来控制。

作为一个完全漫射的物体，平滑度和高光颜色应该设为0。

```
struct LitSurface {	…	bool perfectDiffuser;}; LitSurface GetLitSurface (	float3 normal, float3 position, float3 viewDir,	float3 color, float smoothness, bool perfectDiffuser = false) {	…	s.diffuse = color;	if (perfectDiffuser) {		smoothness = 0.0;		s.specular = 0.0;	}	else {		s.specular = 0.04;	}	s.perfectDiffuser = perfectDiffuser;	s.perceptualRoughness = 1.0 - smoothness; 	return s;}
```

另外我们也可以将所有的高光计算都只在这个bool值为false的条件下执行，只有最后的点乘计算是两者都需要的。

```
float3 LightSurface (LitSurface s, float3 lightDir) {	float3 color = s.diffuse;		if (!s.perfectDiffuser) {}		return color * saturate(dot(s.normal, lightDir));}
```

在顶点光源中，我们正是需要这样一个值来完成纯漫射光照计算。

```
LitSurface GetLitSurfaceVertex (float3 normal, float3 position) {	return GetLitSurface(normal, position, 0, 1, 0, true);}
```

## 1.5 镜面高光光照

镜面高光表示的是完整的反射。当一束光照射到物体表面，部分光线会反射。如果摄像机恰巧在反射光线的路径上，那么我们就会看到这些光线。但是物体表面并不是完全光滑的，光线实际的反射方向总会有一定程度的分散，所以即使不是和理论上的反射方向完全对齐，摄像机仍能看到部分的反射光线。物体表面越粗糙，高光的过渡区域越大。这就是镜面高光的产生过程。

Unity的轻量级渲染管线使用的是简化的 CookTorrance BRDF模型来计算高光。我们也使用相同的计算方式。可以查看*Lightweight RP* package中的*Lighting.hlsl*文件来了解具体细节，对其中的链接可做进一步的阅读。 

```
	if (!s.perfectDiffuser) {		float3 halfDir = SafeNormalize(lightDir + s.viewDir);		float nh = saturate(dot(s.normal, halfDir));		float lh = saturate(dot(lightDir, halfDir));		float d = nh * nh * (s.roughness * s.roughness - 1.0) + 1.00001;		float normalizationTerm = s.roughness * 4.0 + 2.0;		float specularTerm = s.roughness * s.roughness;		specularTerm /= (d * d) * max(0.1, lh * lh) * normalizationTerm;		color += specularTerm * s.specular;	}
```

反射的光线不可能同时还散射，因此相应的要在**GetLitSurface**中降低漫射颜色，除非这个表面是完全漫射的。

```
	if (perfectDiffuser) {		smoothness = 0.0;		s.specular = 0.0;	}	else {		s.specular = 0.04;		s.diffuse *= 1.0 - 0.04;	}
```

![without](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/specular-highlights/without-specular.png)

![with](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/specular-highlights/with-specular.png)

有高光和没有高光的物体

## 1.6 逐物体的光滑度

通过InstanceColor脚本，我们可以让使用统一材质的物体也能有各自不同的颜色。这个方法同样适用于光滑度的调整，我们将这两个功能合并在同一个脚本中，重命名原脚本，使其描述更符合实际功能。

首先，将在Project窗口中的资源文件由*InstancedColor* 重命名为*InstancedMaterialProperties*。接着修改脚本代码中的类名并添加光滑度变量。前面讲的修改顺序不要乱，这样可以确保Unity编辑器仍能保存所有已存在的脚本引用。不然你就得一个一个的修正丢失的脚本引用了。

```
//public class InstancedColor : MonoBehaviour {public class InstancedMaterialProperties : MonoBehaviour { 	static MaterialPropertyBlock propertyBlock; 	static int colorID = Shader.PropertyToID("_Color");	static int smoothnessId = Shader.PropertyToID("_Smoothness"); 	[SerializeField]	Color color = Color.white; 	[SerializeField, Range(0f, 1f)]	float smoothness = 0.5f; 	… 	void OnValidate () {		…		propertyBlock.SetColor(colorID, color);		propertyBlock.SetFloat(smoothnessId, smoothness);		GetComponent<MeshRenderer>().SetPropertyBlock(propertyBlock);	}}
```

![inspector](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/specular-highlights/smoothness-per-object-inspector.png)
![scene](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/specular-highlights/smoothness-per-object.png)

我们将平滑度变量移至实例缓冲区来使其仍支持GPU实例化。

```
CBUFFER_START(UnityPerMaterial)	float4 _MainTex_ST;	float _Cutoff;	//float _Smoothness;CBUFFER_END … UNITY_INSTANCING_BUFFER_START(PerInstance)	UNITY_DEFINE_INSTANCED_PROP(float4, _Color)	UNITY_DEFINE_INSTANCED_PROP(float, _Smoothness)UNITY_INSTANCING_BUFFER_END(PerInstance)
```

使用宏**UNITY_ACCESS_INSTANCED_PROP**来获取平滑度。

```
	LitSurface surface = GetLitSurface(		input.normal, input.worldPos, viewDir,		albedoAlpha.rgb, UNITY_ACCESS_INSTANCED_PROP(PerInstance, _Smoothness)	);
```

# 2 环境反射

镜面高光指的是来自光源的直接反射，但是光线可能是直接光也可能是间接光，如果是间接光则可能来自任何方向，我们不可能实时追踪所有的间接光反射，因此我们退而求其次使用一个立方体纹理代替，通过对其采样来获取近似的环境光。

## 2.1 采样环境

默认的环境光来自于天空盒，在着色器中通过`samplerunity_SpecCube0`访问获取。这是一个立方体贴图格式的纹理资源。我们用宏`**TEXTURECUBE**` 来定义该纹理，并使用`samplerunity_SpecCube0` 来表示他的采样器状态。在Lighting.hlsl中将它们和其他的变量、资源定义在一起，因为我们获取环境数据的具体细节与光照计算无关。

```
TEXTURECUBE(unity_SpecCube0);SAMPLER(samplerunity_SpecCube0);
```

回到 *Lit.hlsl*，定义一个`SampleEnvironment` 方法，该方法传入表面数据，返回环境光颜色。采样立方体贴图的方法在[Rendering 8, Reflections](https://catlikecoding.com/unity/tutorials/rendering/part-8/)有提到。首先，reflect方法传入反视角方向和表面法线，得到反射方向。接着调用`PerceptualRoughnessToMipmapLevel` ，基于感官粗糙度获取正确的mip级别。接着我们就可以使用宏`**SAMPLE_TEXTURECUBE_LOD**` 来采样立方体贴图，并将结果作为最终颜色返回。

```
float3 SampleEnvironment (LitSurface s) {	float3 reflectVector = reflect(-s.viewDir, s.normal);	float mip = PerceptualRoughnessToMipmapLevel(s.perceptualRoughness);		float3 uvw = reflectVector;	float4 sample = SAMPLE_TEXTURECUBE_LOD(		unity_SpecCube0, samplerunity_SpecCube0, uvw, mip	);	float3 color = sample.rgb;	return color;}
```

`PerceptualRoughnessToMipmapLevel` 定义在*ImageBasedLighting*里。粗糙表面会产生相对不集中的模糊的反射，为此我们需要选择一个合适的mip级别。Unity会生成特定的mipmap来表示零散非集中的反射。

```
#include "Packages/com.unity.render-pipelines.core/ShaderLibrary/ImageBasedLighting.hlsl"#include "Lighting.hlsl"
```

为了检查是否可以正常使用，我们在的最后采样环境光，并用它代替原本的光照作为最终颜色输出。

```
float4 LitPassFragment (	VertexOutput input, FRONT_FACE_TYPE isFrontFace : FRONT_FACE_SEMANTIC) : SV_TARGET {	…		color = SampleEnvironment(surface);		return float4(color, albedoAlpha.a);}
```

最终显示的将会是统一的灰色，这意味着没有可以访问的立方体贴图。我们需要通知Unity取绑定环境贴图，为此我们在MyPipeline中对渲染配置添加`RendererConfiguration.PerObjectReflectionProbes` 标签。因为我们现在没有用到任何的反射探针，所以所有物体最终得到的都是天空盒的立方体贴图

```
		if (cull.visibleLights.Count > 0) {			drawSettings.rendererConfiguration =				RendererConfiguration.PerObjectLightIndices8;		}		drawSettings.rendererConfiguration |=			RendererConfiguration.PerObjectReflectionProbes;
```

![img](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/reflecting-the-environment/sampling-skybox.png)采样天空盒的结果

### 2.2 调整反射

会产生多少的环境反射取决于物体表面的粗糙度。在*Lighting.hlsl*添加一个`ReflectEnvironment` 方法。该方法输入表面数据和环境颜色，输出调整后的环境反射。注意该方法不会在意环境颜色实际是来自立方体贴图还是一个统一的值或者别的。

一个完美的漫射体不会有任何的反射，所以结果恒为0。不然的话最终结果就得乘以镜面反射颜色，再将结果除以（粗糙度的平方+1）

```
float3 ReflectEnvironment (LitSurface s, float3 environment) {	if (s.perfectDiffuser) {		return 0;	}		environment *= s.specular;	environment /= s.roughness * s.roughness + 1.0;	return environment;}
```

使用该方法对采样的环境颜色做进一步的调整。

```
	color = ReflectEnvironment(surface, SampleEnvironment(surface));
```

![img](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/reflecting-the-environment/modulated-reflections.png)调整后的环境反射

## 2.3 菲涅尔

在掠射角（glancing  angles）内，大部分光线都会反射，表面表现的性质和镜子类似。我们称之为菲涅尔反射。该角度基于表面法线和视角方向，会有效的增幅镜面反射。我们使用pow(1-saturate(dot(normal,viewdirection)),4)来计算得到菲涅尔值。Core  RP Library为此还定义了一个`Pow4` 方法。在`ReflectEnvironment`方法中，将镜面颜色和纯白色使用菲涅尔值进行插值计算，并将结果值乘到环境颜色中。

```
	float fresnel = Pow4(1.0 - saturate(dot(s.normal, s.viewDir)));	environment *= lerp(s.specular, 1, fresnel);
```

![img](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/reflecting-the-environment/fresnel.png)菲涅尔反射

然而粗糙度同样会影响菲涅尔反射。表面越粗糙，菲涅尔效果越弱。我们在表面数据结构体中添加一个`fresnelStrength` 字段来记录它，这里我们简单的让它等同于光滑度。

```
struct LitSurface {	float3 normal, position, viewDir;	float3 diffuse, specular;	float perceptualRoughness, roughness, fresnelStrength,	bool perfectDiffuser;}; LitSurface GetLitSurface (	float3 normal, float3 position, float3 viewDir,	float3 color, float smoothness, bool perfectDiffuser = false) {	…	s.fresnelStrength = smoothness;	return s;}
```

现在让增幅依赖于菲涅尔强度，不再永远都是最大强度。

```
	environment *= lerp(s.specular, s.fresnelStrength, fresnel);
```

 

![img](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/reflecting-the-environment/modulated-fresnel.png)修正后的菲涅尔反射

最终将环境反射叠加到直接光照中，而不是简单的置换输出颜色。

```
	color += ReflectEnvironment(surface, SampleEnvironment(surface));
```

![img](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/reflecting-the-environment/reflections-added.png)添加到直接光照中的反射

## 2.4 金属表面

对于介电材质，使用固定的0.04单色镜面高光值就足够了，但是对于金属而言这远远不够。纯金属会反射所有的光线且不会改变它的颜色。我们用一个着色器属性来表示某一物体是否为金属。再次使用0-1范围的滑杆控件，这样就可以很轻松的调整某一材质在介电和金属之间的混合系数。

```
		_Metallic ("Metallic", Range(0, 1)) = 0		_Smoothness ("Smoothness", Range(0, 1)) = 0.5
```

我们同样在`**InstancedMaterialProperties**` 脚本中添加金属属性。

```
	static int metallicId = Shader.PropertyToID("_Metallic");	static int smoothnessId = Shader.PropertyToID("_Smoothness"); 	[SerializeField]	Color color = Color.white; 	[SerializeField, Range(0f, 1f)]	float metallic; 	[SerializeField, Range(0f, 1f)]	float smoothness = 0.5f; 	… 	void OnValidate () {		…		propertyBlock.SetFloat(metallicId, metallic);		propertyBlock.SetFloat(smoothnessId, smoothness);		GetComponent<MeshRenderer>().SetPropertyBlock(propertyBlock);	}}
```

![img](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/reflecting-the-environment/metallic-per-object.png)

同样要添加的地方还有着色器中的实例缓冲区

```
UNITY_INSTANCING_BUFFER_START(PerInstance)	UNITY_DEFINE_INSTANCED_PROP(float4, _Color)	UNITY_DEFINE_INSTANCED_PROP(float, _Metallic)	UNITY_DEFINE_INSTANCED_PROP(float, _Smoothness)UNITY_INSTANCING_BUFFER_END(PerInstance)
```

在`LitPassFragment`中把它传给`**LitSurface**` ，顺序放在平滑度前面。

```
	LitSurface surface = GetLitSurface(		input.normal, input.worldPos, viewDir, albedoAlpha.rgb,		UNITY_ACCESS_INSTANCED_PROP(PerInstance, _Metallic),		UNITY_ACCESS_INSTANCED_PROP(PerInstance, _Smoothness)	);
```

在`GetLitSurface` 方法中添加对应的参数，并在`**LitSurface**` 结构体中添加一个字段存储反射率。如果是一个理想的漫射体，它的值应当恒为0。

```
struct LitSurface {	float3 normal, position, viewDir;	float3 diffuse, specular;	float perceptualRoughness, roughness, fresnelStrength, reflectivity;	bool perfectDiffuser;}; LitSurface GetLitSurface (	float3 normal, float3 position, float3 viewDir,	float3 color, float metallic, float smoothness, bool perfectDiffuser = false) {	…	if (perfectDiffuser) {		s.reflectivity = 0.0;		smoothness = 0.0;		s.specular = 0.0;	}	…} LitSurface GetLitSurfaceVertex (float3 normal, float3 position) {	return GetLitSurface(normal, position, 0, 1, 0, 0, true);}
```

如果是金属，那么提供的颜色应当用于高光反射而不是漫反射。但是金属度不是一个非此即彼的二进制数。我们要用它在代表明非金属的0.04和金属的颜色之间插值以得到最终的镜面高光颜色。在这之后，我们可以把反射度近似的等同于金属度，但是要确保它不会小于0.04的最小值。所以我们用金属度在0.04和1之间插值得到最终的反射度。最后反射度要添加到菲涅尔强度中，但是不应超出最大值1。

```
	if (perfectDiffuser) {		…	}	else {		s.specular = lerp(0.04, color, metallic);		s.reflectivity = lerp(0.04, 1.0, metallic);		s.diffuse *= 1.0 - s.reflectivity;	}	…	s.fresnelStrength = saturate(smoothness + s.reflectivity);	return s;}
```

![half](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/reflecting-the-environment/half-metallic.png)

![fully](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/reflecting-the-environment/fully-metallic.png)半金属和全金属

# 3 非统一缩放

在我们更进一步之前，让我们重新考虑我们的假设，即所有对象都具有统一的比例。对于简单的场景而言，这个限制不成问题。但是如果要搭建一个复杂的场景，对原有的形状做进一步的拉伸是很常用的，最终就会导致非统一的缩放。如果我们真的这么做了，那么我们就会得到错误的着色结果，在[Rendering 4, The First Light](https://catlikecoding.com/unity/tutorials/rendering/part-4/)中有具体的解释。

![img](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/non-uniform-scaling/incorrect-shading.png)拉伸球体后的错误渲染

## 3.1 解除假设

想要让任何类型的物体缩放都可以正确渲染，在我们的着色器中首先的取消`assumeuniformscaling` 着色器指令。

```
			//#pragma instancing_options assumeuniformscaling
```

在非统一缩放的情况下，我们要使用物体的世界-对象矩阵转换得到正确的法线向量，所以在`UnityPerDraw`缓冲区，除了`unity_ObjectToWorld` ，我们还需要`unity_WorldToObject` 。

```
CBUFFER_START(UnityPerDraw)	float4x4 unity_ObjectToWorld, unity_WorldToObject;	float4 unity_LightIndicesOffsetAndCount;	float4 unity_4LightIndices0, unity_4LightIndices1;CBUFFER_END
```

另外，在Unity的代码中,假设它被定义为`**UNITY_MATRIX_I_M**` 这个宏，即`**UNITY_MATRIX_M**`的转置。

```
#define UNITY_MATRIX_M unity_ObjectToWorld#define UNITY_MATRIX_I_M unity_WorldToObject
```

在`LitPassVertex`中转换法线时，我们要切换矩阵，并交换相乘的顺序，最终归一化结果。但实际上我们只需要在非统一缩放的情况下使用这些操作。如果真的是非统一缩放，那么*UNITY_ASSUME_UNIFORM_SCALING* 将会被定义，这样我们就可以保留性能更好的旧方法用于统一缩放物体了。

```
	#if defined(UNITY_ASSUME_UNIFORM_SCALING)		output.normal = mul((float3x3)UNITY_MATRIX_M, input.normal);	#else		output.normal = normalize(mul(input.normal, (float3x3)UNITY_MATRIX_I_M));	#endif
```

![img](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/non-uniform-scaling/correct-shading.png)拉伸的球得到了正确的着色渲染。

# 4 反射探针

当没有反射探针时，环境反射只会包含天空盒。你可以通过 *GameObject / Light / Reflection Probe*在场景中添加反射探针。反射探针的Type默认设为Baked，该模式下反射探针的立方体贴图只会渲染1次，并且只会渲染被标记为相对于反射探针为静态的物体。如果一些静态物体发生了变化，相关的反射探针也会更新。当设为Realtime模式时，反射探针会渲染整个场景。立方体贴图何时渲染取决于 *Refresh Mode*和*Time Slicing*。但是在编辑模式下，实时（realtime）的反射探针并不会场景一有变化就刷新。具体细节见[Rendering 8, Reflections](https://catlikecoding.com/unity/tutorials/rendering/part-8/)。

![img](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/reflection-probes/reflection-probe.png)设为实时渲染的反射探针

反射探针需要有可以反射内容，所以将探针放在一个围满物体的场景中。你可以把探针放在物体内部，当然前提是该物体使用的是剔除背面的材质。这样该物体得到的反射会更加的精确。

 

![img](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/reflection-probes/one-reflection-probe.png)中央有一个反射探针的场景

渲染立方体纹理的每个面时，Unity使用的同样是我们的pipeline，虽然我们无法再frame  debugger中观察到。你可以在MyPipeline的Render方法中打印摄像机类型来验证这一点。立方体贴图默认只会在需要时渲染一次。这意味着反射表面在环境纹理中会比预期的要按，因为他们所依赖的环境贴图就是现在正在渲染的。你可以在light  settings里提升光线反弹（bounces）次数。比如反弹两次意味着立方体贴图先正常地渲染一遍，接着基于先前渲染好的环境纹理再渲染一遍。

![img](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/reflection-probes/two-bounces.png)二次反弹的反射

## 4.1 盒状投影（Box Projection）

目前我们采样立方体纹理时，默认光线是来自无穷远的地方，这对于近处物体的反射效果不是很好。盒状映射可以让小范围内的反射更加准确。Unity轻量级渲染管线并没有开启该功能，但我们自己的渲染管线将完成对其的支持，具体的方法描述在[Rendering 8, Reflections](https://catlikecoding.com/unity/tutorials/rendering/part-8/)里，和Unity的旧版渲染管线匹配

在`UnityPerDraw` 缓冲区添加位置变量表示反射探针的最大最小范围。

```
CBUFFER_START(UnityPerDraw)	…	float4 unity_SpecCube0_BoxMin, unity_SpecCube0_BoxMax;	float4 unity_SpecCube0_ProbePosition;CBUFFER_END
```

直接从前面提到的教程中复制`BoxProjection` 方法。

```
float3 BoxProjection (	float3 direction, float3 position,	float4 cubemapPosition, float4 boxMin, float4 boxMax) {	UNITY_BRANCH	if (cubemapPosition.w > 0) {		float3 factors =			((direction > 0 ? boxMax.xyz : boxMin.xyz) - position) / direction;		float scalar = min(min(factors.x, factors.y), factors.z);		direction = direction * scalar + (position - cubemapPosition.xyz);	}	return direction;}
```

在`SampleEnvironment`中用这个方法调整采样坐标。

```
	float3 uvw = BoxProjection(		reflectVector, s.position, unity_SpecCube0_ProbePosition,		unity_SpecCube0_BoxMin, unity_SpecCube0_BoxMax	);
```

启用反射探针的 *Box* *Projection* ，调整它的范围使之与反射区域相匹配。

![inspector](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/reflection-probes/box-projection-inspector.png)![scene](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/reflection-probes/box-projection.png)

 

## 4.2 探针混合

在一些调整后，反射探针可以产生一个不错的结果，但这只是对于离反射探针足够近的物体而言。如果离得太远，反射可能会错位甚至反射自己。如果错误太明显，你就得考虑使用更多的探针。

![img](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/reflection-probes/two-probes.png)用两个反射探针代替单独一个

使用哪个反射探针取决于物体在哪个反射探针的立方体范围内，物体会选择最近或者最重要的反射探针。如果一个物体不在任何一个探针的立方体范围内，那么便由天空盒替代。但是从一个反射探针转移到另一个，会产生很生硬的变化。所以我们最好可以混合两个反射探针来缓解这个问题，这一点每一个物体都可以配置。这种方式最多可以混合两个探针。

为了支持混合，我们得在着色器中添加有关于第二个探针的相关变量。

```
	float4 unity_SpecCube0_BoxMin, unity_SpecCube0_BoxMax;	float4 unity_SpecCube0_ProbePosition;	float4 unity_SpecCube1_BoxMin, unity_SpecCube1_BoxMax;	float4 unity_SpecCube1_ProbePosition;
```

我们需要定义第二个立方体纹理，但是可以使用同一个采样器状态。

```
TEXTURECUBE(unity_SpecCube0);TEXTURECUBE(unity_SpecCube1);SAMPLER(samplerunity_SpecCube0);
```

这部分实现代码仍然复制自其它教程。

```
float3 SampleEnvironment (LitSurface s) {	…	float3 color = sample.rgb;		float blend = unity_SpecCube0_BoxMin.w;	if (blend < 0.99999) {		uvw = BoxProjection(			reflectVector, s.position,			unity_SpecCube1_ProbePosition,			unity_SpecCube1_BoxMin, unity_SpecCube1_BoxMax		);		sample = SAMPLE_TEXTURECUBE_LOD(			unity_SpecCube1, samplerunity_SpecCube0, uvw, mip		);		color = lerp(sample.rgb, color, blend);	}	return color;}
```

![img](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/reflection-probes/blending-probes.png)探针混合

## 4.3 HDR解码

我们现在支持的反射探针默认它对应纹理存储的是未编码的光照数据。通常情况下这是成立的，但是当烘焙贴图是HDR编码或者反射探针的强度改变时就不适用了。我们需要靠`DecodeHDREnvironment`来实现HDR解码，他定义在*EntityLighting.hlsl*中。

```
#include "Packages/com.unity.render-pipelines.core/ShaderLibrary/ImageBasedLighting.hlsl"#include "Packages/com.unity.render-pipelines.core/ShaderLibrary/EntityLighting.hlsl"
```

每个探针都需要一个HDR解码结构体，为此我们添加对应变量。

```
	float4 unity_SpecCube0_BoxMin, unity_SpecCube0_BoxMax;	float4 unity_SpecCube0_ProbePosition, unity_SpecCube0_HDR;	float4 unity_SpecCube1_BoxMin, unity_SpecCube1_BoxMax;	float4 unity_SpecCube1_ProbePosition, unity_SpecCube1_HDR;
```

接着解码立方体纹理的采样结果。

```
	float3 color = DecodeHDREnvironment(sample, unity_SpecCube0_HDR);		float blend = unity_SpecCube0_BoxMin.w;	if (blend < 0.99999) {		…        /* 原文是这样的，应该是笔误		color = lerp(			sample.rgb, DecodeHDREnvironment(sample, unity_SpecCube1_HDR), blend		);        */        color = lerp(DecodeHDREnvironment(sample, unity_SpecCube1_HDR), color, blend);	}
```

![img](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/reflection-probes/double-intensity.png)双倍强度

注意使用多次反弹，那么反射强度的提升可能会产生戏剧性的结果，因为每次反弹都会进一步提升光照的强度。

# 5 透明表面

我们以对半透明材质的探讨作为本章的结尾。在前面的章节中我们添加了对渐变材质的支持。我们淡出了物体表面的所有颜色，这其中就包括了反射。如果你本来就是想渐变所有的光照颜色这自然没问题，但是水晶玻璃这些材质的半透明效果不应该是这样的，反射部分不应该受透明度的限制。

![img](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/transparent-surfaces/fade.png)

## 5.1 左乘Alpha

玻璃一般是完全透明的，但它仍会反射光线。要实现这种效果，我们需要让不透明度只应用到漫反射光照。我们通过将漫反射颜色乘以alpha值来完成这一步。所以我们改用左乘alpha值，而不是像之前一样依靠着色器的混合选项将透明度应用到最终的完整片元颜色中。接着我们基于反射度对alpha值进行增幅，这样之后的计算都将算进反射的部分。在 *Lighting.hlsl*添加这个方法来调整相应的表面数据和alpha值。

```
void PremultiplyAlpha (inout LitSurface s, inout float alpha) {	s.diffuse *= alpha;	alpha = lerp(alpha, 1, s.reflectivity);}
```

`LitPassFragment`里如果*_PREMULTIPLY_ALPHA* 关键字被定义，就在得到表面数据后调用该方法。

```
	LitSurface surface = GetLitSurface(		input.normal, input.worldPos, viewDir, albedoAlpha.rgb,		UNITY_ACCESS_INSTANCED_PROP(PerInstance, _Metallic),		UNITY_ACCESS_INSTANCED_PROP(PerInstance, _Smoothness)	);	#if defined(_PREMULTIPLY_ALPHA)		PremultiplyAlpha(surface, albedoAlpha.a);	#endif
```

添加一个用于切换关键字的着色器属性。

```
		[Toggle(_RECEIVE_SHADOWS)] _ReceiveShadows ("Receive Shadows", Float) = 1		[Toggle(_PREMULTIPLY_ALPHA)] _PremulAlpha ("Premultiply Alpha", Float) = 0
```

想让他正确显示，我们要把源混合模式设为one。

![inspector](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/transparent-surfaces/premultiplied-alpha-inspector.png)
![scene](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/transparent-surfaces/premultiplied-alpha.png)

## 5.2 预设

让我们在中添加透明材质（transparent ）的预设。添加一个属性用于设置*_PREMULTIPLY_ALPHA* 关键字和它附带的着色器属性。

```
	bool PremultiplyAlpha {		set {			FindProperty("_PremulAlpha", properties).floatValue =				value ? 1 : 0;			SetKeywordEnabled("_PREMULTIPLY_ALPHA", value);		}	}
```

在先前所有的预设中将该属性设为false。

```
		PremultiplyAlpha = false;
```

复制两个渐变预设方法，调整它们让他们用于透明材质。方法里`PremultiplyAlpha` 应该设为true，`SrcBlend` 应该设为`BlendMode.One`。

```
	void TransparentPreset () {		if (!GUILayout.Button("Transparent")) {			return;		}		editor.RegisterPropertyChangeUndo("Transparent Preset");		Clipping = ClipMode.Off;		Cull = CullMode.Back;		SrcBlend = BlendMode.One;		DstBlend = BlendMode.OneMinusSrcAlpha;		ZWrite = false;		ReceiveShadows = false;		PremultiplyAlpha = true;		SetPassEnabled("ShadowCaster", false);		RenderQueue = RenderQueue.Transparent;	} 	void TransparentWithShadowsPreset () {		if (!GUILayout.Button("Transparent with Shadows")) {			return;		}		editor.RegisterPropertyChangeUndo("Transparent with Shadows Preset");		Clipping = ClipMode.Shadows;		Cull = CullMode.Back;		SrcBlend = BlendMode.One;		DstBlend = BlendMode.OneMinusSrcAlpha;		ZWrite = false;		ReceiveShadows = true;		PremultiplyAlpha = true;		SetPassEnabled("ShadowCaster", true);		RenderQueue = RenderQueue.Transparent;	}
```

最后一步，在OnGUI中调用这两个预设方法。

```
		if (showPresets) {			OpaquePreset();			ClipPreset();			ClipDoubleSidedPreset();			FadePreset();			FadeWithShadowsPreset();			TransparentPreset();			TransparentWithShadowsPreset();		}
```

![img](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/reflections/transparent-surfaces/presets.png)