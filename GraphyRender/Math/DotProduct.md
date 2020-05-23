- 

- # Dot product

- From  Wikipedia, the free encyclopedia

- [Jump to navigation](https://en.wikipedia.org/wiki/Dot_product#mw-head)[Jump to search](https://en.wikipedia.org/wiki/Dot_product#p-search)

- *"Scalar product" redirects  here. For the abstract scalar product, see* [*Inner product space*](https://en.wikipedia.org/wiki/Inner_product_space)*. For the product of a vector and a  scalar, see* [*Scalar multiplication*](https://en.wikipedia.org/wiki/Scalar_multiplication)*.*

- In [mathematics](https://en.wikipedia.org/wiki/Mathematics), the **dot product** or **scalar product**[[note 1\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-1) is an [algebraic operation](https://en.wikipedia.org/wiki/Algebraic_operation) that takes two equal-length sequences of numbers  (usually [coordinate vectors](https://en.wikipedia.org/wiki/Coordinate_vector)) and returns a single number. In [Euclidean geometry](https://en.wikipedia.org/wiki/Euclidean_geometry), the dot product of the [Cartesian coordinates](https://en.wikipedia.org/wiki/Cartesian_coordinates) of two [vectors](https://en.wikipedia.org/wiki/Vector_(mathematics_and_physics)) is widely used and often called "the" **inner product** (or rarely **projection product**) of Euclidean space even though it is  not the only inner product that can be defined on Euclidean space; see  also [inner product space](https://en.wikipedia.org/wiki/Inner_product_space).

- Algebraically, the dot product is the sum of the [products](https://en.wikipedia.org/wiki/Product_(mathematics)) of the corresponding entries of the two sequences  of numbers. Geometrically, it is the product of the [Euclidean  magnitudes](https://en.wikipedia.org/wiki/Euclidean_vector#Length) of the two vectors and  the [cosine](https://en.wikipedia.org/wiki/Cosine) of the angle between them. These definitions are  equivalent when using Cartesian coordinates. In modern [geometry](https://en.wikipedia.org/wiki/Geometry), [Euclidean spaces](https://en.wikipedia.org/wiki/Euclidean_space) are often defined by using [vector spaces](https://en.wikipedia.org/wiki/Vector_space). In this case, the dot product is used for defining  lengths (the length of a vector is the [square root](https://en.wikipedia.org/wiki/Square_root) of the dot product of the vector by itself) and  angles (the cosine of the angle of two vectors is the quotient of their dot  product by the product of their lengths).

- The name "dot product" is derived from  the [centered  dot](https://en.wikipedia.org/wiki/Interpunct) " **·** "  that is often used to designate this operation; the alternative name  "scalar product" emphasizes that the result is a [scalar](https://en.wikipedia.org/wiki/Scalar_(mathematics)), rather than a [vector](https://en.wikipedia.org/wiki/Euclidean_vector), as is the case for the [vector product](https://en.wikipedia.org/wiki/Vector_product) in three-dimensional space.

- **Contents**

- - [1Definition](https://en.wikipedia.org/wiki/Dot_product#Definition)
  - [1.1Algebraic definition](https://en.wikipedia.org/wiki/Dot_product#Algebraic_definition)
  - [1.2Geometric definition](https://en.wikipedia.org/wiki/Dot_product#Geometric_definition)
  - [1.3Scalar projection and first       properties](https://en.wikipedia.org/wiki/Dot_product#Scalar_projection_and_first_properties)
  - [1.4Equivalence of the       definitions](https://en.wikipedia.org/wiki/Dot_product#Equivalence_of_the_definitions)
  - [2Properties](https://en.wikipedia.org/wiki/Dot_product#Properties)
  - [2.1Application to the law of       cosines](https://en.wikipedia.org/wiki/Dot_product#Application_to_the_law_of_cosines)
  - [3Triple product](https://en.wikipedia.org/wiki/Dot_product#Triple_product)
  - [4Physics](https://en.wikipedia.org/wiki/Dot_product#Physics)
  - [5Generalizations](https://en.wikipedia.org/wiki/Dot_product#Generalizations)
  - [5.1Complex vectors](https://en.wikipedia.org/wiki/Dot_product#Complex_vectors)
  - [5.2Inner product](https://en.wikipedia.org/wiki/Dot_product#Inner_product)
  - [5.3Functions](https://en.wikipedia.org/wiki/Dot_product#Functions)
  - [5.4Weight function](https://en.wikipedia.org/wiki/Dot_product#Weight_function)
  - [5.5Dyadics and matrices](https://en.wikipedia.org/wiki/Dot_product#Dyadics_and_matrices)
  - [5.6Tensors](https://en.wikipedia.org/wiki/Dot_product#Tensors)
  - [6Computation](https://en.wikipedia.org/wiki/Dot_product#Computation)
  - [6.1Algorithms](https://en.wikipedia.org/wiki/Dot_product#Algorithms)
  - [6.2Libraries](https://en.wikipedia.org/wiki/Dot_product#Libraries)
  - [7See also](https://en.wikipedia.org/wiki/Dot_product#See_also)
  - [8Notes](https://en.wikipedia.org/wiki/Dot_product#Notes)
  - [9References](https://en.wikipedia.org/wiki/Dot_product#References)
  - [10External links](https://en.wikipedia.org/wiki/Dot_product#External_links)

-  

- The dot product may be defined algebraically or  geometrically. The geometric definition is based on the notions of angle and  distance (magnitude of vectors). The equivalence of these two definitions  relies on having a [Cartesian  coordinate system](https://en.wikipedia.org/wiki/Cartesian_coordinate_system) for Euclidean space.

- In modern presentations of [Euclidean geometry](https://en.wikipedia.org/wiki/Euclidean_geometry), the points of space are defined in terms of  their [Cartesian coordinates](https://en.wikipedia.org/wiki/Cartesian_coordinates), and [Euclidean space](https://en.wikipedia.org/wiki/Euclidean_space) itself  is commonly identified with the [real coordinate space](https://en.wikipedia.org/wiki/Real_coordinate_space) **R***n*. In such a presentation, the notions  of length and angles are defined by means of the dot product. The length of a  vector is defined as the [square  root](https://en.wikipedia.org/wiki/Square_root) of the dot  product of the vector by itself, and the [cosine](https://en.wikipedia.org/wiki/Cosine) of the (non oriented) angle of  two vectors of length one is defined as their dot product. So the equivalence  of the two definitions of the dot product is a part of the equivalence of the  classical and the modern formulations of Euclidean geometry.

- **Algebraic definition**[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=2)]

- The dot product of two vectors **a** = [*a*1, *a*2, …, *a**n*] and **b** = [*b*1, *b*2, …, *b**n*] is  defined as:[[1\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-Lipschutz2009-2)

- where Σ denotes [summation](https://en.wikipedia.org/wiki/Summation) and *n* is the dimension of  the [vector  space](https://en.wikipedia.org/wiki/Vector_space). For instance, in [three-dimensional  space](https://en.wikipedia.org/wiki/Three-dimensional_space_(mathematics)), the dot product of vectors [1, 3, −5] and [4, −2, −1] is:

- If vectors are identified with [row matrices](https://en.wikipedia.org/wiki/Row_matrix), the dot product can also be written as a [matrix product](https://en.wikipedia.org/wiki/Matrix_multiplication)

- where 

-  denotes the [transpose](https://en.wikipedia.org/wiki/Transpose) of 

- .

- Expressing the above example in this way, a 1 × 3 matrix  ([row vector](https://en.wikipedia.org/wiki/Row_vector)) is multiplied by a 3 × 1 matrix ([column vector](https://en.wikipedia.org/wiki/Column_vector)) to get a 1 × 1 matrix that is identified with its  unique entry:

- .

- **Geometric definition**[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=3)]

- [
![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image001.png)](https://en.wikipedia.org/wiki/File:Inner-product-angle.svg)

- Illustration showing how to find the angle between vectors using  the dot product

- In [Euclidean space](https://en.wikipedia.org/wiki/Euclidean_space), a [Euclidean vector](https://en.wikipedia.org/wiki/Euclidean_vector) is a geometric object that possesses both a  magnitude and a direction. A vector can be pictured as an arrow. Its magnitude  is its length, and its direction is the direction that the arrow points to.  The magnitude of a vector **a** is denoted by 

- . The dot product of two Euclidean vectors **a** and **b** is defined by[[2\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-Spiegel2009-3)[[3\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-4)

- where *θ* is the [angle](https://en.wikipedia.org/wiki/Angle) between **a** and **b**.

- In particular, if **a** and **b** are [orthogonal](https://en.wikipedia.org/wiki/Orthogonal) (the angle between vectors is 90°) then due  to 

-  

-  

- At the other extreme, if they are codirectional, then the angle  between them is 0° and

- This implies that the dot product of a vector **a** with itself is

- which gives

- the formula for the [Euclidean length](https://en.wikipedia.org/wiki/Euclidean_length) of the vector.

- **Scalar projection and first properties**[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=4)]

- [
![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image002.png)](https://en.wikipedia.org/wiki/File:Dot_Product.svg)

- Scalar projection

- The [scalar projection](https://en.wikipedia.org/wiki/Scalar_projection) (or scalar component) of a Euclidean vector **a** in  the direction of a Euclidean vector **b** is given by

- where *θ* is the angle between **a** and **b**.

- In terms of the geometric definition of the dot product, this can  be rewritten

- where 

-  is the [unit vector](https://en.wikipedia.org/wiki/Unit_vector) in the direction of **b**.

- [
![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image003.png)](https://en.wikipedia.org/wiki/File:Dot_product_distributive_law.svg)

- Distributive law for the dot product

- The dot product is thus characterized geometrically by[[4\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-5)

- The dot product, defined in this manner, is homogeneous under  scaling in each variable, meaning that for any scalar *α*,

- It also satisfies a [distributive law](https://en.wikipedia.org/wiki/Distributive_law), meaning that

- These properties may be summarized by saying that the  dot product is a [bilinear form](https://en.wikipedia.org/wiki/Bilinear_form). Moreover, this bilinear form is [positive  definite](https://en.wikipedia.org/wiki/Positive_definite_bilinear_form), which means that 

-  is never negative and is zero if and only if 

- , the zero vector.

- **Equivalence of the definitions**[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=5)]

- If **e**1,  ..., **e***n* are the [standard basis vectors](https://en.wikipedia.org/wiki/Standard_basis) in **R***n*, then we may write

- The vectors **e***i* are an [orthonormal basis](https://en.wikipedia.org/wiki/Orthonormal_basis),  which means that they have unit length and are at right angles to each other.  Hence since these vectors have unit length

- and since they form right angles with each other, if *i* ≠ *j*,

- Thus in general we can say that:

- Where δ ij is  the [Kronecker delta](https://en.wikipedia.org/wiki/Kronecker_delta).

- Also, by the geometric definition, for any  vector **e***i* and a vector **a**,  we note

- where *a**i* is the component  of vector **a** in the direction of **e***i*.

- Now applying the distributivity of the geometric version of the dot  product gives

- which is precisely the algebraic definition of the dot product. So  the geometric dot product equals the algebraic dot product.

- Properties[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=6)]

- The dot product fulfills the following properties if **a**, **b**, and **c** are  real [vectors](https://en.wikipedia.org/wiki/Vector_(geometry)) and *r* is a [scalar](https://en.wikipedia.org/wiki/Scalar_(mathematics)).[[1\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-Lipschutz2009-2)[[2\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-Spiegel2009-3)

- 1. [**Commutative**](https://en.wikipedia.org/wiki/Commutative)**:**

- which follows from the definition (*θ* is  the angle between **a** and **b**):

- 1. [**Distributive**](https://en.wikipedia.org/wiki/Distributive_property) **over vector addition:**
  2. [**Bilinear**](https://en.wikipedia.org/wiki/Bilinear_form):
  3. [**Scalar       multiplication**](https://en.wikipedia.org/wiki/Scalar_multiplication)**:**

- 1. **Not** [**associative**](https://en.wikipedia.org/wiki/Associative) because the dot       product between a scalar (**a** **⋅** **b**) and a vector (**c**)       is not defined, which means that the expressions involved in the       associative property, (**a** **⋅**       **b**) ⋅ **c** or **a** ⋅ (**b**       **⋅** **c**)       are both ill-defined.[[5\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-6) Note however that       the previously mentioned scalar multiplication property is sometimes       called the "associative law for scalar and dot product"[[6\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-BanchoffWermer1983-7) or one can say       that "the dot product is associative with respect to scalar       multiplication" because *c* (**a** ⋅ **b**)       = (*c* **a**)       ⋅ **b** = **a** ⋅ (*c* **b**).[[7\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-BedfordFowler2008-8)

- 1. [**Orthogonal**](https://en.wikipedia.org/wiki/Orthogonal)**:**             Two non-zero vectors **a** and **b** are *orthogonal* [if and only if](https://en.wikipedia.org/wiki/If_and_only_if) **a** ⋅ **b** = 0.

- 1. **No** [**cancellation**](https://en.wikipedia.org/wiki/Cancellation_law)**:**             Unlike multiplication of ordinary numbers, where       if *ab* = *ac*, then *b* always       equals *c* unless *a* is zero, the dot       product does not obey the [cancellation       law](https://en.wikipedia.org/wiki/Cancellation_law):
                  If **a** ⋅ **b** = **a** ⋅ **c** and **a** ≠ **0**,       then we can write: **a** ⋅ (**b** − **c**)       = 0 by the [distributive       law](https://en.wikipedia.org/wiki/Distributive_law); the result above says this just means that **a** is       perpendicular to (**b** − **c**),       which still allows (**b** − **c**)       ≠ **0**, and therefore **b** ≠ **c**.

- 1. [**Product Rule**](https://en.wikipedia.org/wiki/Product_Rule)**:** If **a** and **b** are [functions](https://en.wikipedia.org/wiki/Function_(mathematics)), then the       derivative ([denoted by a prime](https://en.wikipedia.org/wiki/Notation_for_differentiation#Lagrange's_notation) ′)       of **a** ⋅ **b** is **a**′ ⋅ **b** + **a** ⋅ **b**′.

- **Application to the law of cosines**[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=7)]

- [
![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image004.png)](https://en.wikipedia.org/wiki/File:Dot_product_cosine_rule.svg)

- Triangle with vector edges **a**and **b**, separated by angle *θ*.

- *Main article:* [*Law of cosines*](https://en.wikipedia.org/wiki/Law_of_cosines)

- Given two vectors **a** and **b** separated  by angle *θ* (see image right), they form a triangle with a  third side **c** = **a** − **b**. The  dot product of this with itself is:

- which is the [law of cosines](https://en.wikipedia.org/wiki/Law_of_cosines).

- Triple product[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=8)]

- *Main article:* [*Triple product*](https://en.wikipedia.org/wiki/Triple_product)

- There are two [ternary operations](https://en.wikipedia.org/wiki/Ternary_operation) involving dot product and [cross product](https://en.wikipedia.org/wiki/Cross_product).

- The **scalar triple product** of  three vectors is defined as

- Its value is the [determinant](https://en.wikipedia.org/wiki/Determinant) of the matrix whose columns are the [Cartesian  coordinates](https://en.wikipedia.org/wiki/Cartesian_coordinates) of the three vectors. It is  the signed [volume](https://en.wikipedia.org/wiki/Volume) of the [parallelogram](https://en.wikipedia.org/wiki/Parallelogram) defined by the three vectors.

- The **vector triple product** is defined by[[1\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-Lipschutz2009-2)[[2\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-Spiegel2009-3)

- This identity, also known as *Lagrange's formula* [may be remembered](https://en.wikipedia.org/wiki/Mnemonic) as "BAC minus CAB", keeping in mind  which vectors are dotted together. This formula finds application in  simplifying vector calculations in [physics](https://en.wikipedia.org/wiki/Physics).

- Physics[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=9)]

- In [physics](https://en.wikipedia.org/wiki/Physics), vector magnitude is a [scalar](https://en.wikipedia.org/wiki/Scalar_(physics)) in  the physical sense, i.e. a [physical quantity](https://en.wikipedia.org/wiki/Physical_quantity) independent  of the coordinate system, expressed as the [product](https://en.wikipedia.org/wiki/Product_(mathematics)) of a [numerical  value](https://en.wikipedia.org/wiki/Number) and a [physical unit](https://en.wikipedia.org/wiki/Physical_unit),  not just a number. The dot product is also a scalar in this sense, given by  the formula, independent of the coordinate system. Examples include:[[8\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-Riley2010-9)[[9\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-10)

- - [Mechanical work](https://en.wikipedia.org/wiki/Mechanical_work) is       the dot product of [force](https://en.wikipedia.org/wiki/Force) and [displacement](https://en.wikipedia.org/wiki/Displacement_(vector)) vectors,
  - [Magnetic flux](https://en.wikipedia.org/wiki/Magnetic_flux) is       the dot product of the [magnetic field](https://en.wikipedia.org/wiki/Magnetic_field) and       the [vector area](https://en.wikipedia.org/wiki/Vector_area),
  - [Power](https://en.wikipedia.org/wiki/Power_(physics)) is       the dot product of [force](https://en.wikipedia.org/wiki/Force) and [velocity](https://en.wikipedia.org/wiki/Velocity).

- Generalizations[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=10)]

- **Complex vectors**[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=11)]

- For vectors with [complex](https://en.wikipedia.org/wiki/Complex_number) entries,  using the given definition of the dot product would lead to quite different  properties. For instance the dot product of a vector with itself would be an  arbitrary complex number, and could be zero without the vector being the zero  vector (such vectors are called [isotropic](https://en.wikipedia.org/wiki/Isotropic_quadratic_form)); this in turn would have consequences for notions like length  and angle. Properties such as the positive-definite norm can be salvaged at  the cost of giving up the symmetric and bilinear properties of the scalar  product, through the alternative definition[[10\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-11)[[1\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-Lipschutz2009-2)

- where *a**i* is the [complex conjugate](https://en.wikipedia.org/wiki/Complex_conjugate) of *a**i*. Then the scalar product of any vector  with itself is a non-negative real number, and it is nonzero except for the  zero vector. However this scalar product is thus [sesquilinear](https://en.wikipedia.org/wiki/Sesquilinear) rather than bilinear: it is [conjugate linear](https://en.wikipedia.org/wiki/Conjugate_linear) and  not linear in **a**, and the  scalar product is not symmetric, since

- The angle between two complex vectors is then given by

- This type of scalar product is nevertheless useful, and  leads to the notions of [Hermitian form](https://en.wikipedia.org/wiki/Hermitian_form) and of general [inner product spaces](https://en.wikipedia.org/wiki/Inner_product_space).

- **Inner product**[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=12)]

- *Main article:* [*Inner product space*](https://en.wikipedia.org/wiki/Inner_product_space)

- The inner product generalizes the dot product to [abstract vector spaces](https://en.wikipedia.org/wiki/Vector_space) over a [field](https://en.wikipedia.org/wiki/Field_(mathematics)) of [scalars](https://en.wikipedia.org/wiki/Scalar_(mathematics)), being either the field of [real numbers](https://en.wikipedia.org/wiki/Real_number) 

-  or the field of [complex numbers](https://en.wikipedia.org/wiki/Complex_number) 

- . It is usually denoted using [angular brackets](https://en.wikipedia.org/wiki/Angular_brackets) by 

- .

- The inner product of two vectors over the field of  complex numbers is, in general, a complex number, and is [sesquilinear](https://en.wikipedia.org/wiki/Sesquilinear_form) instead of bilinear. An inner product space is  a [normed  vector space](https://en.wikipedia.org/wiki/Normed_vector_space), and the inner product of a  vector with itself is real and positive-definite.

- **Functions**[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=13)]

- The dot product is defined for vectors that have a finite  number of [entries](https://en.wikipedia.org/wiki/Coordinate_vector). Thus these vectors  can be regarded as [discrete functions](https://en.wikipedia.org/wiki/Discrete_function): a length-*n* vector *u* is, then, a function with [domain](https://en.wikipedia.org/wiki/Domain_of_a_function) {*k* ∈ ℕ ∣ 1 ≤ *k* ≤ *n*}, and *u**i* is a notation  for the image of *i* by the function/vector *u*.

- This notion can be generalized to [continuous functions](https://en.wikipedia.org/wiki/Continuous_function): just as the inner  product on vectors uses a sum over corresponding components, the inner product  on functions is defined as an integral over some [interval](https://en.wikipedia.org/wiki/Interval_(mathematics)) *a* ≤ *x* ≤ *b* (also denoted [*a*, *b*]):[[1\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-Lipschutz2009-2)

- Generalized further to [complex functions](https://en.wikipedia.org/wiki/Complex_function) *ψ*(*x*) and *χ*(*x*), by analogy with the complex inner product  above, gives[[1\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-Lipschutz2009-2)

- **Weight function**[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=14)]

- Inner products can have a [weight function](https://en.wikipedia.org/wiki/Weight_function), i.e. a function which weights each term of the inner  product with a value. Explicitly, the inner product of functions 

-  and 

-  with respect to the weight function 

-  is

- **Dyadics and matrices**[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=15)]

- [Matrices](https://en.wikipedia.org/wiki/Matrix_(mathematics)) have the [Frobenius inner product](https://en.wikipedia.org/wiki/Frobenius_inner_product), which is analogous to the  vector inner product. It is defined as the sum of the products of the  corresponding components of two matrices **A** and **B** having the same size:

-  

-  (For real matrices)

- [Dyadics](https://en.wikipedia.org/wiki/Dyadics) have a dot product and "double" dot product defined  on them, see [Dyadics (Product of dyadic and dyadic)](https://en.wikipedia.org/wiki/Dyadics#Product_of_dyadic_and_dyadic) for their definitions.

- **Tensors**[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=16)]

- The inner product between a [tensor](https://en.wikipedia.org/wiki/Tensor) of  order *n* and a tensor of order *m* is  a tensor of order *n* + *m* − 2, see [tensor contraction](https://en.wikipedia.org/wiki/Tensor_contraction) for details.

- Computation[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=17)]

- **Algorithms**[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=18)]

- The straightforward algorithm for calculating a  floating-point dot product of vectors can suffer from [catastrophic  cancellation](https://en.wikipedia.org/wiki/Catastrophic_cancellation). To avoid this, approaches such  as the [Kahan summation  algorithm](https://en.wikipedia.org/wiki/Kahan_summation_algorithm) are used.

- **Libraries**[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=19)]

- A dot product function is included in [BLAS](https://en.wikipedia.org/wiki/BLAS) level  1.

- See also[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=20)]

- - [Cauchy–Schwarz       inequality](https://en.wikipedia.org/wiki/Cauchy%E2%80%93Schwarz_inequality)
  - [Cross product](https://en.wikipedia.org/wiki/Cross_product)
  - [Matrix       multiplication](https://en.wikipedia.org/wiki/Matrix_multiplication)
  - [Metric tensor](https://en.wikipedia.org/wiki/Metric_tensor)

- Notes[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=21)]

- 1. [**^**](https://en.wikipedia.org/wiki/Dot_product#cite_ref-1) The term *scalar product* is       often also used more generally to mean a [symmetric bilinear form](https://en.wikipedia.org/wiki/Symmetric_bilinear_form), for       example for a [pseudo-Euclidean space](https://en.wikipedia.org/wiki/Pseudo-Euclidean_space).[[*citation       needed*](https://en.wikipedia.org/wiki/Wikipedia:Citation_needed)]

- References[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=22)]

- 1. ^ [Jump       up to:***a***](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Lipschutz2009_2-0) [***b***](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Lipschutz2009_2-1) [***c***](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Lipschutz2009_2-2) [***d***](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Lipschutz2009_2-3) [***e***](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Lipschutz2009_2-4) [***f***](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Lipschutz2009_2-5) S. Lipschutz; M. Lipson (2009). *Linear       Algebra (Schaum’s Outlines)* (4th ed.). McGraw Hill. [ISBN](https://en.wikipedia.org/wiki/International_Standard_Book_Number) [978-0-07-154352-1](https://en.wikipedia.org/wiki/Special:BookSources/978-0-07-154352-1).
  2. ^ [Jump up to:***a***](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Spiegel2009_3-0) [***b***](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Spiegel2009_3-1) [***c***](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Spiegel2009_3-2) M.R. Spiegel; S. Lipschutz; D.       Spellman (2009). *Vector Analysis (Schaum’s Outlines)* (2nd ed.).       McGraw Hill. [ISBN](https://en.wikipedia.org/wiki/International_Standard_Book_Number) [978-0-07-161545-7](https://en.wikipedia.org/wiki/Special:BookSources/978-0-07-161545-7).

- 1. [**^**](https://en.wikipedia.org/wiki/Dot_product#cite_ref-4) A I Borisenko; I E Taparov (1968). *Vector and tensor analysis with       applications*. Translated by Richard       Silverman. Dover. p. 14.
  2. [**^**](https://en.wikipedia.org/wiki/Dot_product#cite_ref-5) Arfken, G. B.; Weber, H. J. (2000). *Mathematical Methods for Physicists* (5th ed.). Boston, MA: [Academic Press](https://en.wikipedia.org/wiki/Academic_Press). pp. 14–15. [ISBN](https://en.wikipedia.org/wiki/International_Standard_Book_Number) [978-0-12-059825-0](https://en.wikipedia.org/wiki/Special:BookSources/978-0-12-059825-0)..
  3. [**^**](https://en.wikipedia.org/wiki/Dot_product#cite_ref-6) Weisstein, Eric W. "Dot Product." From       MathWorld--A Wolfram Web Resource. <http://mathworld.wolfram.com/DotProduct.html>
  4. [**^**](https://en.wikipedia.org/wiki/Dot_product#cite_ref-BanchoffWermer1983_7-0) T. Banchoff; J. Wermer (1983). *Linear Algebra Through Geometry*. Springer Science & Business Media. p. 12. [ISBN](https://en.wikipedia.org/wiki/International_Standard_Book_Number) [978-1-4684-0161-5](https://en.wikipedia.org/wiki/Special:BookSources/978-1-4684-0161-5).
  5. [**^**](https://en.wikipedia.org/wiki/Dot_product#cite_ref-BedfordFowler2008_8-0) A. Bedford; Wallace L. Fowler (2008). *Engineering Mechanics: Statics* (5th ed.). Prentice Hall. p. 60. [ISBN](https://en.wikipedia.org/wiki/International_Standard_Book_Number) [978-0-13-612915-8](https://en.wikipedia.org/wiki/Special:BookSources/978-0-13-612915-8).
  6. [**^**](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Riley2010_9-0) K.F. Riley; M.P. Hobson; S.J. Bence (2010). *Mathematical methods for physics and       engineering* (3rd ed.). Cambridge       University Press. [ISBN](https://en.wikipedia.org/wiki/International_Standard_Book_Number) [978-0-521-86153-3](https://en.wikipedia.org/wiki/Special:BookSources/978-0-521-86153-3).
  7. [**^**](https://en.wikipedia.org/wiki/Dot_product#cite_ref-10) M. Mansfield; C. O’Sullivan (2011). *Understanding Physics* (4th ed.). John Wiley & Sons. [ISBN](https://en.wikipedia.org/wiki/International_Standard_Book_Number) [978-0-47-0746370](https://en.wikipedia.org/wiki/Special:BookSources/978-0-47-0746370).
  8. [**^**](https://en.wikipedia.org/wiki/Dot_product#cite_ref-11) Berberian, Sterling K. (2014) [1992], *Linear Algebra*, Dover, p. 287, [ISBN](https://en.wikipedia.org/wiki/International_Standard_Book_Number) [978-0-486-78055-9](https://en.wikipedia.org/wiki/Special:BookSources/978-0-486-78055-9)

- External links[[edit](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=23)]

- | 
![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image005.png)|WikimediaCommonshasmediarelatedto[***Scalarproduct***](https://commons.wikimedia.org/wiki/Category:Scalar_product). |
  | ------------------------------------------------------------ | ------------------------------------------------------------ |
  |                                                              |                                                              |

- - [Hazewinkel, Michiel](https://en.wikipedia.org/wiki/Michiel_Hazewinkel), ed.       (2001) [1994], ["Inner       product"](https://www.encyclopediaofmath.org/index.php?title=p/i051240), [*Encyclopedia       of Mathematics*](https://en.wikipedia.org/wiki/Encyclopedia_of_Mathematics), Springer Science+Business Media B.V. / Kluwer       Academic Publishers, [ISBN](https://en.wikipedia.org/wiki/International_Standard_Book_Number) [978-1-55608-010-4](https://en.wikipedia.org/wiki/Special:BookSources/978-1-55608-010-4)
  - [Weisstein, Eric W.](https://en.wikipedia.org/wiki/Eric_W._Weisstein) ["Dot       product"](http://mathworld.wolfram.com/DotProduct.html). [*MathWorld*](https://en.wikipedia.org/wiki/MathWorld).

- - [Explanation of dot product including       with complex vectors](http://www.mathreference.com/la,dot.html)
  - ["Dot       Product"](http://demonstrations.wolfram.com/DotProduct/) by Bruce Torrence, [Wolfram       Demonstrations Project](https://en.wikipedia.org/wiki/Wolfram_Demonstrations_Project), 2007.

-  

- # 翻译

- 在[数学中](https://en.wikipedia.org/wiki/Mathematics)，**点积**或**标量积**[[注1\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-1)是一个[代数运算](https://en.wikipedia.org/wiki/Algebraic_operation)，它采用两个相等长度的数字序列（通常是[坐标向量](https://en.wikipedia.org/wiki/Coordinate_vector)）并返回一个数字。在[欧几里德几何中](https://en.wikipedia.org/wiki/Euclidean_geometry)，两个[向量](https://en.wikipedia.org/wiki/Vector_(mathematics_and_physics))的[笛卡尔坐标](https://en.wikipedia.org/wiki/Cartesian_coordinates)的点积被广泛使用，并且通常被称为欧几里得空间的“ **内”积**（或很少**投影乘积**），即使它不是欧几里德空间上唯一可以定义的内积。  ; 另见[内部产品空间](https://en.wikipedia.org/wiki/Inner_product_space)。

- 代数，点积是总和[产品](https://en.wikipedia.org/wiki/Product_(mathematics))号的两个序列的相应条目。几何上，它是两个向量的[欧几里德量值](https://en.wikipedia.org/wiki/Euclidean_vector#Length)和它们之间角度的[余弦](https://en.wikipedia.org/wiki/Cosine)的乘积。使用笛卡尔坐标时，这些定义是等效的。在现代[几何中](https://en.wikipedia.org/wiki/Geometry)，[欧几里德空间](https://en.wikipedia.org/wiki/Euclidean_space)通常通过使用[向量空间](https://en.wikipedia.org/wiki/Vector_space)来定义。在这种情况下，点积用于定义长度（矢量的长度是矢量自身的点积的[平方根](https://en.wikipedia.org/wiki/Square_root)）和角度（两个矢量的角度的余弦是它们的点积的商）通过他们的长度的产品）。

- 名称“点积”来自[中心点](https://en.wikipedia.org/wiki/Interpunct) “  **·**  ”，常用于指定此操作; 替代名称“标量积”强调结果是[标量](https://en.wikipedia.org/wiki/Scalar_(mathematics))，而不是[矢量](https://en.wikipedia.org/wiki/Euclidean_vector)，就像三维空间中的[矢量积一样](https://en.wikipedia.org/wiki/Vector_product)。

- **内容**

- - [1定义](https://en.wikipedia.org/wiki/Dot_product#Definition)
  - [1.1代数定义](https://en.wikipedia.org/wiki/Dot_product#Algebraic_definition)
  - [1.2几何定义](https://en.wikipedia.org/wiki/Dot_product#Geometric_definition)
  - [1.3标量投影和第一属性](https://en.wikipedia.org/wiki/Dot_product#Scalar_projection_and_first_properties)
  - [1.4定义的等同性](https://en.wikipedia.org/wiki/Dot_product#Equivalence_of_the_definitions)
  - [2属性](https://en.wikipedia.org/wiki/Dot_product#Properties)
  - [2.1适用于余弦定律](https://en.wikipedia.org/wiki/Dot_product#Application_to_the_law_of_cosines)
  - [3三重产品](https://en.wikipedia.org/wiki/Dot_product#Triple_product)
  - [4物理](https://en.wikipedia.org/wiki/Dot_product#Physics)
  - [5概括](https://en.wikipedia.org/wiki/Dot_product#Generalizations)
  - [5.1复杂向量](https://en.wikipedia.org/wiki/Dot_product#Complex_vectors)
  - [5.2内在产品](https://en.wikipedia.org/wiki/Dot_product#Inner_product)
  - [5.3功能](https://en.wikipedia.org/wiki/Dot_product#Functions)
  - [5.4重量函数](https://en.wikipedia.org/wiki/Dot_product#Weight_function)
  - [5.5二元和矩阵](https://en.wikipedia.org/wiki/Dot_product#Dyadics_and_matrices)
  - [5.6张量](https://en.wikipedia.org/wiki/Dot_product#Tensors)
  - [6计算](https://en.wikipedia.org/wiki/Dot_product#Computation)
  - [6.1算法](https://en.wikipedia.org/wiki/Dot_product#Algorithms)
  - [6.2图书馆](https://en.wikipedia.org/wiki/Dot_product#Libraries)
  - [7另见](https://en.wikipedia.org/wiki/Dot_product#See_also)
  - [8注意事项](https://en.wikipedia.org/wiki/Dot_product#Notes)
  - [9参考文献](https://en.wikipedia.org/wiki/Dot_product#References)
  - [10外部链接](https://en.wikipedia.org/wiki/Dot_product#External_links)

- 定义[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=1)]

- 点积可以以代数或几何方式定义。几何定义基于角度和距离（矢量的大小）的概念。这两个定义的等价性依赖于欧几里德空间的[笛卡尔坐标系](https://en.wikipedia.org/wiki/Cartesian_coordinate_system)。

- 在[欧几里德几何的](https://en.wikipedia.org/wiki/Euclidean_geometry)现代表示中，空间点是根据它们的[笛卡尔坐标](https://en.wikipedia.org/wiki/Cartesian_coordinates)定义的，[欧几里德空间](https://en.wikipedia.org/wiki/Euclidean_space)本身通常用[真实坐标空间](https://en.wikipedia.org/wiki/Real_coordinate_space) **R** *n来*标识。在这样的展示中，长度和角度的概念是通过点积定义的。矢量的长度被定义为矢量自身的点积的[平方根](https://en.wikipedia.org/wiki/Square_root)，并且长度为1的两个矢量的（非定向）角的[余弦](https://en.wikipedia.org/wiki/Cosine)被定义为它们的点积。因此，点积的两个定义的等价性是欧几里德几何的经典和现代公式的等价的一部分。

- **代数定义**[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=2)]

- 两个向量**a** = [ *a* 1，*a* 2，...，*a* *n* ]和**b** = [ *b* 1，*b* 2，...，*b* *n* ]的点积定义为：[[1\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-Lipschutz2009-2)

- 其中Σ表示[求和](https://en.wikipedia.org/wiki/Summation)，*n*是[向量空间](https://en.wikipedia.org/wiki/Vector_space)的维数。例如，在[三维空间中](https://en.wikipedia.org/wiki/Three-dimensional_space_(mathematics))，向量[1,3，-5]和[4，-2，-1]的点积为：

- 如果使用[行矩阵](https://en.wikipedia.org/wiki/Row_matrix)标识向量，则点积也可以写为[矩阵乘积](https://en.wikipedia.org/wiki/Matrix_multiplication)

- 哪里 

- 表示[转置](https://en.wikipedia.org/wiki/Transpose)的

- 。

- 以这种方式表达上述示例，将1×3矩阵（[行向量](https://en.wikipedia.org/wiki/Row_vector)）乘以3×1矩阵（[列向量](https://en.wikipedia.org/wiki/Column_vector)）以获得用其唯一条目标识的1×1矩阵：

- 。

- **几何定义**[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=3)]

- [
![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image001.png)](https://en.wikipedia.org/wiki/File:Inner-product-angle.svg)

- 插图显示如何使用点积找到矢量之间的角度

- 在[欧几里得空间中](https://en.wikipedia.org/wiki/Euclidean_space)，[欧几里德向量](https://en.wikipedia.org/wiki/Euclidean_vector)是一个具有大小和方向的几何对象。矢量可以被描绘成箭头。它的大小是它的长度，它的方向是箭头指向的方向。矢量**a的**大小表示为

- 。两个欧几里得矢量**a**和**b**的点积由[[2\] ](https://en.wikipedia.org/wiki/Dot_product#cite_note-Spiegel2009-3)[[3\]定义](https://en.wikipedia.org/wiki/Dot_product#cite_note-4)

- 其中*θ*是**a**和**b**之间的[角度](https://en.wikipedia.org/wiki/Angle)。

- 特别是，如果**a**和**b**是[正交的](https://en.wikipedia.org/wiki/Orthogonal)（矢量之间的角度是90°），那么由于

-  

-  

- 在另一个极端，如果它们是同向的，那么它们之间的角度是0°和

- 这意味着矢量**a**与其自身 的点积

- 这使

- 向量的[欧几里德长度](https://en.wikipedia.org/wiki/Euclidean_length)的公式。

- **标量投影和第一个属性**[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=4)]

- [
![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image002.png)](https://en.wikipedia.org/wiki/File:Dot_Product.svg)

- 标量投影

- 的[标量投影](https://en.wikipedia.org/wiki/Scalar_projection)一个向量的（或标量分量）**一个**在一个向量的方向**b**由下式给出

- 其中*θ*是**a**和**b**之间的角度。

- 就点积的几何定义而言，这可以重写

- 哪里 

- 是**b**方向的[单位向量](https://en.wikipedia.org/wiki/Unit_vector)。

- [
![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image003.png)](https://en.wikipedia.org/wiki/File:Dot_product_distributive_law.svg)

- 点积的分布规律

- 因此，点积在几何上由[[4\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-5)表征。

- 以这种方式定义的点积在每个变量的缩放下是均匀的，这意味着对于任何标量*α*，

- 它也满足[分配法](https://en.wikipedia.org/wiki/Distributive_law)，意思是

- 这些性质可以通过说点积是[双线性形式](https://en.wikipedia.org/wiki/Bilinear_form)来概括。而且，这种双线性形式是[正定的](https://en.wikipedia.org/wiki/Positive_definite_bilinear_form)，这意味着 

-  从来都不是负面的，当且仅当是 

- ，零向量。

- **定义的等价性**[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=5)]

- 如果**ë** 1，...，**Ë** *Ñ*是[标准基向量](https://en.wikipedia.org/wiki/Standard_basis)中**ř** *Ñ*，那么我们可以写成

- 矢量**e** *i*是标准[正交基](https://en.wikipedia.org/wiki/Orthonormal_basis)，这意味着它们具有单位长度并且彼此成直角。因此，因为这些向量具有单位长度

- 并且由于它们彼此形成直角，如果*i* ≠ *j*，

- 因此，一般来说，我们可以说：

- 其中δij是[Kronecker delta](https://en.wikipedia.org/wiki/Kronecker_delta)。

- 此外，通过几何定义，对于任何向量**e** *i*和向量**a**，我们注意到

- 其中*一个**我*是矢量的分量**一个**在方向**ë** *我*。

- 现在应用点积的几何形式的分布给出

- 这正是点积的代数定义。因此几何点积等于代数点积。

- 属性[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=6)]

- 如果**a**，**b**和**c**是实数[向量](https://en.wikipedia.org/wiki/Vector_(geometry))且*r*是[标量](https://en.wikipedia.org/wiki/Scalar_(mathematics))，则点积满足以下属性。[[1\] ](https://en.wikipedia.org/wiki/Dot_product#cite_note-Lipschutz2009-2)[[2\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-Spiegel2009-3)

- 1. [**交换**](https://en.wikipedia.org/wiki/Commutative)**：**

- 从定义得出（*θ*是**a**和**b**之间的角度）：

- 1. **对向量加法的**[**分配**](https://en.wikipedia.org/wiki/Distributive_property)**：**

- 1. [**双线性**](https://en.wikipedia.org/wiki/Bilinear_form)：
  2. [**标量乘法**](https://en.wikipedia.org/wiki/Scalar_multiplication)**：**

- 1. **不是**[**关联的，**](https://en.wikipedia.org/wiki/Associative)因为标量（**a·b**）和向量（**c**）之间的点积没有定义，这意味着关联属性中涉及的表达式，（**a·b**）· **c**或**a** ·（**b·c**）两者都是不明确的。[[5\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-6)然而要注意前面提到的标量乘法属性有时也被称为“结合律为标量和点积” [[6\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-BanchoffWermer1983-7)或可以说，“点积是缔合相对于标量乘法”，因为*Ç*（**一个** ⋅ **b**）=（*c* **a**）⋅**b** = **一个** ⋅（*Ç* **b**）。[[7\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-BedfordFowler2008-8)

- 1. [**正交**](https://en.wikipedia.org/wiki/Orthogonal)**：**             [当且仅当](https://en.wikipedia.org/wiki/If_and_only_if)**a** · **b** = 0时，两个非零向量**a**和**b**是*正交的* 。

- 1. **没有**[**取消**](https://en.wikipedia.org/wiki/Cancellation_law)**：**             与普通数的乘法不同，如果*ab* = *ac*，则*b*总是等于*c，*除非*a*为零，点积不遵守[取消定律](https://en.wikipedia.org/wiki/Cancellation_law)：
                  如果**一个** ⋅ **b** = **一个** ⋅ **Ç**和**一个** ≠ **0**，那么我们可以写出：**一个** ⋅（**b** - **c ^**）= 0由[分配律](https://en.wikipedia.org/wiki/Distributive_law) ; 上面的结果表明这只是意味着**a**垂直于（**b** - **c**），它仍然允许（**b** - **c**）≠ **0**，因此**b** ≠ **c**。

- 1. [**产品规则**](https://en.wikipedia.org/wiki/Product_Rule)**：**如果**一个**和 **b**是[功能](https://en.wikipedia.org/wiki/Function_(mathematics))，则衍生物（[由一原表示](https://en.wikipedia.org/wiki/Notation_for_differentiation#Lagrange's_notation) '）的**一个** ⋅ **b**是**一个** '⋅ **b** + **一个** ⋅ **b** '。

- **应用于余弦定律**[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=7)]

- [
![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image004.png)](https://en.wikipedia.org/wiki/File:Dot_product_cosine_rule.svg)

- 三角形与矢量边缘**a**和**b**，由角度*θ*分开。

- *主要文章：*[*余弦定律*](https://en.wikipedia.org/wiki/Law_of_cosines)

- 给定两个矢量**a**和**b**以角度*θ*分开（见右图），它们形成三角形，第三边**c** = **a** - **b**。这与它本身的点积是：

- 这是[余弦定律](https://en.wikipedia.org/wiki/Law_of_cosines)。

- 三重产品[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=8)]

- *主要文章：*[*三重产品*](https://en.wikipedia.org/wiki/Triple_product)

- 有两个涉及点积和[叉积的](https://en.wikipedia.org/wiki/Cross_product)[三元运算](https://en.wikipedia.org/wiki/Ternary_operation)。

- 三个向量的**标量三重乘积**定义为

- 它的值是矩阵的[行列式](https://en.wikipedia.org/wiki/Determinant)，矩阵的列是三个向量的[笛卡尔坐标](https://en.wikipedia.org/wiki/Cartesian_coordinates)。它是由三个向量定义的[平行四边形](https://en.wikipedia.org/wiki/Parallelogram)的有符号[体积](https://en.wikipedia.org/wiki/Volume)。

- 的**向量三重积**由下式定义[[1\] ](https://en.wikipedia.org/wiki/Dot_product#cite_note-Lipschutz2009-2)[[2\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-Spiegel2009-3)

- 这种身份，也称为*拉格朗日公式，* [可以记](https://en.wikipedia.org/wiki/Mnemonic)为“BAC减去CAB”，记住哪些矢量点缀在一起。该公式适用于简化[物理学中的](https://en.wikipedia.org/wiki/Physics)矢量计算。

- 物理[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=9)]

- 在[物理学](https://en.wikipedia.org/wiki/Physics)，向量幅度是一个[标量](https://en.wikipedia.org/wiki/Scalar_(physics))在物理意义，即一个[物理量](https://en.wikipedia.org/wiki/Physical_quantity)独立的坐标系的，表示为[产品](https://en.wikipedia.org/wiki/Product_(mathematics)) a的[数值](https://en.wikipedia.org/wiki/Number)和一个[物理单元](https://en.wikipedia.org/wiki/Physical_unit)，不只是一个数字。点积也是这个意义上的标量，由公式给出，与坐标系无关。例子包括：[[8\] ](https://en.wikipedia.org/wiki/Dot_product#cite_note-Riley2010-9)[[9\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-10)

- - [机械功](https://en.wikipedia.org/wiki/Mechanical_work)是[力](https://en.wikipedia.org/wiki/Force)和[位移](https://en.wikipedia.org/wiki/Displacement_(vector))矢量的点积，
  - [磁通量](https://en.wikipedia.org/wiki/Magnetic_flux)是[磁场](https://en.wikipedia.org/wiki/Magnetic_field)和[矢量区域](https://en.wikipedia.org/wiki/Vector_area)的点积，
  - [力](https://en.wikipedia.org/wiki/Power_(physics))是[力](https://en.wikipedia.org/wiki/Force)和[速度](https://en.wikipedia.org/wiki/Velocity)的点积。

- 一般化[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=10)]

- **复杂载体**[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=11)]

- 对于具有[复杂](https://en.wikipedia.org/wiki/Complex_number)条目的向量，使用点积的给定定义将导致完全不同的属性。例如，矢量与其自身的点积将是任意复数，并且可以是零，而矢量不是零矢量（这种矢量称为[各向同性](https://en.wikipedia.org/wiki/Isotropic_quadratic_form)）; 这反过来会对长度和角度等概念产生影响。通过替代定义[[10\] ](https://en.wikipedia.org/wiki/Dot_product#cite_note-11)[[1\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-Lipschutz2009-2)，可以以放弃标量积的对称性和双线性特性为代价来挽救诸如正定范数的性质。

- 其中*一个**我*是[复共轭](https://en.wikipedia.org/wiki/Complex_conjugate)的*一个**我*。那么任何矢量与其自身的标量积是非负实数，并且除了零矢量之外它是非零的。然而，这个标量积是[sesquilinear](https://en.wikipedia.org/wiki/Sesquilinear)而不是双线性：它是[共轭线性的](https://en.wikipedia.org/wiki/Conjugate_linear)而不是线性**的**，并且标量积不对称，因为

- 然后给出两个复矢量之间的角度

- 然而，这种类型的标量产品是有用的，并且导致[厄米特形式](https://en.wikipedia.org/wiki/Hermitian_form)和一般[内部产品空间](https://en.wikipedia.org/wiki/Inner_product_space)的概念。

- **内在产品**[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=12)]

- *主条目：*[*内部产品空间*](https://en.wikipedia.org/wiki/Inner_product_space)

- 内积概括的点积，以[抽象的向量空间](https://en.wikipedia.org/wiki/Vector_space)在[字段](https://en.wikipedia.org/wiki/Field_(mathematics))的[标量](https://en.wikipedia.org/wiki/Scalar_(mathematics))，作为任领域[实数](https://en.wikipedia.org/wiki/Real_number) 

- 或[复数](https://en.wikipedia.org/wiki/Complex_number)字段 

- 。它通常是使用表示[角形托架](https://en.wikipedia.org/wiki/Angular_brackets)通过

- 。

- 复数域上的两个向量的内积通常是复数，并且是[sesquilinear](https://en.wikipedia.org/wiki/Sesquilinear_form)而不是双线性。内积空间是一个[赋范的向量空间](https://en.wikipedia.org/wiki/Normed_vector_space)，向量本身的内积是真实的和正定的。

- **功能**[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=13)]

- 点积是针对具有有限数量的[条目的](https://en.wikipedia.org/wiki/Coordinate_vector)向量定义的。因此，这些载体可被视为[离散的功能](https://en.wikipedia.org/wiki/Discrete_function)：一个长度- *Ñ*向量*ü*是的话，用一个功能[域](https://en.wikipedia.org/wiki/Domain_of_a_function) { *ķ* ∈ℕ| 1个≤ *ķ* ≤ *Ñ* }和*ü* *我*为的图像的符号*我*由功能/  vector *u*。

- 这个概念可以推广到[连续函数](https://en.wikipedia.org/wiki/Continuous_function)：正如上向量的内积使用通过相应的组件的总和，对函数的内积被定义为一个整体在一些[间隔](https://en.wikipedia.org/wiki/Interval_(mathematics)) *一个* ≤ *X* ≤ *b*（也表示为[ *一*，*b* ]） ：[[1\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-Lipschutz2009-2)

- 进一步推广到[复函数](https://en.wikipedia.org/wiki/Complex_function) *ψ*（*x*）和*χ*（*x*），类比上面的复数内积，给出[[1\]](https://en.wikipedia.org/wiki/Dot_product#cite_note-Lipschutz2009-2)

- **重量函数**[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=14)]

- 内部产品可以具有[重量函数](https://en.wikipedia.org/wiki/Weight_function)，即用内部产品的每个项加权的函数。明确地，功能的内在产物

-  和 

-  关于重量函数 

-  是

- **二元和矩阵**[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=15)]

- [基质](https://en.wikipedia.org/wiki/Matrix_(mathematics))具有[Frobenius内积](https://en.wikipedia.org/wiki/Frobenius_inner_product)，其类似于载体内积。它被定义为具有相同大小的两个矩阵**A**和**B**的相应组件的乘积之和：

-  

-  （对于真实矩阵）

- [Dyadics](https://en.wikipedia.org/wiki/Dyadics)有一个点积和在它们上面定义的“双”点积，参见[Dyadics（二元和二元的乘积）](https://en.wikipedia.org/wiki/Dyadics#Product_of_dyadic_and_dyadic)的定义。

- **张量**[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=16)]

- *n*阶张量与*m*阶[张量](https://en.wikipedia.org/wiki/Tensor)之间的内积是*n* + *m* - 2 [阶的张量](https://en.wikipedia.org/wiki/Tensor_contraction)，详见[张量收缩](https://en.wikipedia.org/wiki/Tensor_contraction)。

- 计算[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=17)]

- **算法**[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=18)]

- 用于计算向量的浮点数乘积的直接算法可能遭受[灾难性的消除](https://en.wikipedia.org/wiki/Catastrophic_cancellation)。为了避免这种情况，使用诸如[Kahan求和算法之](https://en.wikipedia.org/wiki/Kahan_summation_algorithm)类的方法。

- **图书馆**[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=19)]

- [BLAS](https://en.wikipedia.org/wiki/BLAS) 1级中包含点积函数。

- 另见[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=20)]

- - [Cauchy-Schwarz不等式](https://en.wikipedia.org/wiki/Cauchy%E2%80%93Schwarz_inequality)
  - [交叉产品](https://en.wikipedia.org/wiki/Cross_product)
  - [矩阵乘法](https://en.wikipedia.org/wiki/Matrix_multiplication)
  - [公制张量](https://en.wikipedia.org/wiki/Metric_tensor)

- 笔记[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=21)]

- 1. [**^**](https://en.wikipedia.org/wiki/Dot_product#cite_ref-1) 术语*标量积*通常也使用更一般地指的是[对称双线性形式](https://en.wikipedia.org/wiki/Symmetric_bilinear_form)，例如用于[伪欧几里德空间](https://en.wikipedia.org/wiki/Pseudo-Euclidean_space)。[ [*引证需要*](https://en.wikipedia.org/wiki/Wikipedia:Citation_needed) ]

- 参考文献[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=22)]

- 1. ^ [跳到：***a*** ](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Lipschutz2009_2-0)[***b*** ](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Lipschutz2009_2-1)[***c*** ](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Lipschutz2009_2-2)[***d*** ](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Lipschutz2009_2-3)[***e*** ](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Lipschutz2009_2-4)[***f***](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Lipschutz2009_2-5) S. Lipschutz; M. Lipson（2009年）。*线性代数（Schaum的轮廓）*（第4版）。麦格劳希尔。[ISBN ](https://en.wikipedia.org/wiki/International_Standard_Book_Number) [978-0-07-154352-1](https://en.wikipedia.org/wiki/Special:BookSources/978-0-07-154352-1)。
  2. ^ [跳到：***a*** ](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Spiegel2009_3-0)[***b*** ](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Spiegel2009_3-1)[***c***](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Spiegel2009_3-2) M.R. Spiegel; S.       Lipschutz; D.斯派曼（2009年）。*矢量分析（Schaum的轮廓）*（第2版）。麦格劳希尔。[ISBN ](https://en.wikipedia.org/wiki/International_Standard_Book_Number) [978-0-07-161545-7](https://en.wikipedia.org/wiki/Special:BookSources/978-0-07-161545-7)。

- 1. [**^**](https://en.wikipedia.org/wiki/Dot_product#cite_ref-4) AI       Borisenko; IE Taparov（1968）。*矢量和张量分析与应用程序*。Richard       Silverman翻译。多佛。页。14。
  2. [**^**](https://en.wikipedia.org/wiki/Dot_product#cite_ref-5) Arfken，GB; Weber，HJ（2000）。*物理学家的数学方法*（第5版）。波士顿：[学术出版社](https://en.wikipedia.org/wiki/Academic_Press)。第14-15页。[ISBN ](https://en.wikipedia.org/wiki/International_Standard_Book_Number) [978-0-12-059825-0](https://en.wikipedia.org/wiki/Special:BookSources/978-0-12-059825-0)。。
  3. [**^**](https://en.wikipedia.org/wiki/Dot_product#cite_ref-6) Weisstein，Eric       W.“Dot Product。” 来自MathWorld - Wolfram Web资源。<http://mathworld.wolfram.com/DotProduct.html>
  4. [**^**](https://en.wikipedia.org/wiki/Dot_product#cite_ref-BanchoffWermer1983_7-0) T.       Banchoff; J. Wermer（1983）。*线性代数通过几何*。施普林格科学与商业媒体。页。12. [ISBN ](https://en.wikipedia.org/wiki/International_Standard_Book_Number) [978-1-4684-0161-5](https://en.wikipedia.org/wiki/Special:BookSources/978-1-4684-0161-5)。
  5. [**^**](https://en.wikipedia.org/wiki/Dot_product#cite_ref-BedfordFowler2008_8-0) A.贝德福德; Wallace       L. Fowler（2008）。*工程力学：静力学*（第5版）。普伦蒂斯霍尔。页。60. [ISBN ](https://en.wikipedia.org/wiki/International_Standard_Book_Number) [978-0-13-612915-8](https://en.wikipedia.org/wiki/Special:BookSources/978-0-13-612915-8)。
  6. [**^**](https://en.wikipedia.org/wiki/Dot_product#cite_ref-Riley2010_9-0) KF赖利; MP霍布森; SJ       Bence（2010年）。*物理与工程的数学方法*（第3版）。剑桥大学出版社。[ISBN ](https://en.wikipedia.org/wiki/International_Standard_Book_Number) [978-0-521-86153-3](https://en.wikipedia.org/wiki/Special:BookSources/978-0-521-86153-3)。
  7. [**^**](https://en.wikipedia.org/wiki/Dot_product#cite_ref-10) M.       Mansfield; C. O'Sullivan（2011年）。*理解物理*（第4版）。John       Wiley＆Sons。[ISBN ](https://en.wikipedia.org/wiki/International_Standard_Book_Number) [978-0-47-0746370](https://en.wikipedia.org/wiki/Special:BookSources/978-0-47-0746370)。
  8. [**^**](https://en.wikipedia.org/wiki/Dot_product#cite_ref-11) Berberian，Sterling       K.（2014）[1992]，*线性代数*，多佛，p。287，[ISBN ](https://en.wikipedia.org/wiki/International_Standard_Book_Number) [978-0-486-78055-9](https://en.wikipedia.org/wiki/Special:BookSources/978-0-486-78055-9)

- 外部链接[ [编辑](https://en.wikipedia.org/w/index.php?title=Dot_product&action=edit&section=23)]

- | 
![img](file:///C:/Users/WUMING~1/AppData/Local/Temp/msohtmlclip1/01/clip_image005.png)|WikimediaCommons拥有与[***Scalar产品***](https://commons.wikimedia.org/wiki/Category:Scalar_product)相关的媒体。 |
  | ------------------------------------------------------------ | ------------------------------------------------------------ |
  |                                                              |                                                              |

- - [Hazewinkel，Michiel](https://en.wikipedia.org/wiki/Michiel_Hazewinkel)，ed。（2001）[1994]，[“内在产品”](https://www.encyclopediaofmath.org/index.php?title=p/i051240)，[*数学百科全书*](https://en.wikipedia.org/wiki/Encyclopedia_of_Mathematics)，施普林格科学+商业媒体BV / Kluwer学术出版社，[ISBN ](https://en.wikipedia.org/wiki/International_Standard_Book_Number) [978-1-55608-010-4](https://en.wikipedia.org/wiki/Special:BookSources/978-1-55608-010-4)
  - [Weisstein，Eric       W. ](https://en.wikipedia.org/wiki/Eric_W._Weisstein)[“Dot product”](http://mathworld.wolfram.com/DotProduct.html)。[*MathWorld*](https://en.wikipedia.org/wiki/MathWorld)。

- - [包含复杂向量的点积的说明](http://www.mathreference.com/la,dot.html)
  - [“Dot Product”](http://demonstrations.wolfram.com/DotProduct/)，作者：Bruce       Torrence，[Wolfram演示项目](https://en.wikipedia.org/wiki/Wolfram_Demonstrations_Project)，2007年。

-  

- 来自 <<https://en.wikipedia.org/wiki/Dot_product>> 

-  

- #  
