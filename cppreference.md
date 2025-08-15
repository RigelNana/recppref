# cppreference中的所有模板

注意，所有的value都是可能包含嵌套模板的值。

应该要注意parser不要解析<!-- -->中的内容。

应该注意html转义。

Template的，一般都是空格

cpp/开头的模板，一般都是空格

还有就是全是下划线的模板，Template:对应的反而是空格

* `{{{n}}}`，可以取得传入的第n个value
* `{{xxx | 1= foo}` 把xxx模板的第一个参数显式设置成foo

* `{{# if}}` `{{# switch }}`

- `{{{tparams}}}` (不带 `|`)：**没有默认值**。
- `{{{tparams|}}}` (带 `|`)：**有一个默认值，这个默认值是“空”**。

### anchor

语法：`{{anchor | value}}`

作用：次标题

### Attr

语法：`{{attr | value | value2 }}`

作用：产生一个[[attribute]]的属性

### box

语法：`{{box | value}}`

作用：加框

### */core

语法：`{{*/core | value}}`

作用：代码体，无高亮

### c

语法：`{{c | value }}`

作用：加框，有高亮

### c multi

语法：`{{c multi | line1 | line2 | ... }}`、`{{c multi | a <CR> b<CR>...}}`

作用：多行加框，有高亮

### cc

语法：`{{cc | value }}`

作用：上下划两条线，高亮

### cc multi

语法：`{{cc multi | line1 | line2 | ... }}`、`{{c multi | a <CR> b<CR>...}}`

作用：多行，表格中，高亮

### closed range

语法：`{{closed range | a | b}}`

作用：闭区间，其中的a和b会带框

### closed range plain

语法：`{{closed range plain | a | b}}`

作用：闭区间，其中的a和b不带框

### co

语法：`{{co | value}}`

作用：高亮，但是不带框

### cot/cob

语法：`{{cot | value}} ... {{cob}}`

作用：创建一个内层盒子

### collapsed top/bottom

语法：`{{collapsed top | value}} ... {{collapsed bottom}}`

作用：创建一个可折叠盒子

### counted range

语法：`{{counted range | a | b}}`

作用：![QQ_1754480805360](/Users/rigelshrimp/Documents/QQ_1754480805360.png)

### */title

语法：`{{*/title | value1 | value2 | ... }}`

作用：产生标题

### */navbar

语法：`{{*/navbar}}`

作用：导航栏

### ctitle

语法：`{{ctitle | value1 | value2 | ... }}`

作用：指明为c库的标题

### cwg

语法：`{{cwg | value }}`

作用：产生 文本为CWG issue value，链接为https://cplusplus.github.io/CWG/issues/value.html

### dcl

语法：`{{dcl | num = | since = | constexpr= |notes=}}`

作用：declaration块

### dcl begin/end

语法：`{{dcl begin}} ... {{dcl end}}`

作用：declaration表格的始末

### dcl h

语法：`{{dcl h | value }}`

作用：在declaration表格中插入一个小标题

### dcl header

语法：`{{dcl header | value }}`

作用：产生一个小标题：Defined in header `<value>`，https://en.cppreference.com/w/cpp/header/value.html

### dcl item

语法：`{{dcl item | since= | num = | ... }}`

作用：未知，应该跟dcl和dcla差不多

### dcl rev begin/end

语法同dcl begin/end

作用同dcl begin/end

### dcl rev multi

语法：`{{dcl rev multi |num = | until1 = |since1 = |dcl1=|until2 = | since2 = |dcl2=|anchor=}}`

作用：一个声明的两个版本对比

### dcl sep

语法：`{{dcl sep}}`

作用：单纯的在dcl中分隔

### dcla

语法：同dcl

作用：同dcl

### ddcl

语法：`{{ddcl | header = | since |}}`

作用：可以直接开始写一个声明，不需要dcl begin end

### ddcla

语法：`{{ddcla | num = | since = | expos= yes/no}}`

作用：跟dcl一样

### div col/end

语法：`{{div col | value}}...{{div end}}` 

作用：分成value列

### documentation

没用

### dr list begin/end

语法：`{{dr list begin}}...{{dr list end}}`

作用：dr list块的开始结束

### dr list item

语法：`{{dr list item | wg = ... | dr = ... | std= | before = | after=}}`

作用：dr list中的项

### dsc

语法：`{{dsc | value1 | value2 | ...}}`

作用：dsc表格中的项

### dsc sep

语法：`{{dsc sep}}`

作用：分隔线

### dsc begin/end

语法：`{{dsc begin}}...{{dsc end}}`

作用：开始和结束一个dsc表格，是关于类型的

### dsc break

语法：`{{dsc break}}`

作用：结束一个header的dsc

### dsc inc

语法：`{{dsc inc | TEMPLATE}}`

作用：把TEMPLATE引入过来做为dsc表格中的一列

### dsc class

语法：`{{dsc class | header | dec }}`

作用：给dsc增添一列，标注为(class)

### dsc concept/const/fun/expos concept/expos mem class/expos mem fun/expos mem obj/expos mem sconst/expos mem tclass/expos mem type/expos mem var/h1/h2/h3/hash/header/hitem/inc/macro const/mem class/mem ctor/mem dtor/mem enum/mem fun/mem obj/mem sconst/mem sfun/mem vdtor/mem vfun/named req/namespace/prot mem ctor/prot mem dtor/prot mem fun/prot mem obj/prot mem vdtor/prot mem vfun/ptclass/talias/tfun/tvar/typedef

语法：{{dsc ... | header|private=|spec=|id=|title=|notes=}}

作用：都差不多，产生一个表格中的项

### dsc see c/cpp

语法：`{{dsc see c/cpp | link | Some | nomono=}}`

作用：参见c/cpp文档

### dsc todo

语法：`{{dsc todo}}`

作用：todo

### eli

语法：`{{eli | [link desc] text}}`

作用：外链

### elink

同上

### elink begin/end

开始结束块

### enwiki

{{enwiki | A|text}}

链接到enwiki

### eq fun

{{eq fun | 1=}}

可能的实现

### eq impl

{{eq impl | 1=}}

可能的实现

### example

{{example | code= | p = | output=|value}}

示例

### example template

{{example template | TEMPLATE} }

把模板整过来

### feature test macro

{{feature test macro | macro |std=|value=|feature}}

测试宏

### fmbox

{{fmbox | text=}}

一个框

### ftm

{{ftm| macro | rowspan= | name | std= | value=}}

特性宏

### ftm begin/end



### ftml

{{ftml | macro | ver}}

### header

{{header | h}}

### identical

{{identical | text | ...}}



### include/~ editlink/~ page/



### inheritance diagram/*

### inherited

### l2tf/ l2tf std

{{l2tf|link|...}}

### l2tt/ l2tt std

### langlinks

### lc

{{lc | symbol }}

### lconcept

### left

### librow

### libtablebegin/end

## 链接系

### ls

### lsd

### lsi

### lt

### ltf/ltf std

### lti

### ltp

### ltpf

### ltt/ltt std

### lwg

## mark

### mark/mark c++11/14/17/20/23/26 /mark deprecated/ mark deprecated c++17/20/23/26/mark implicit/mark life/mark ok/mark optional/mark since c++11/14/17/20/23/26/mark since reflection ts/mark since tm ts/mark tooltip/mark unreviewed dr/mark until c++11/14/17/20/23/26/mark_cancel/mark_ok/

{{mark life|since=c++11|deprecated=c++17|removed=c++26}}

### math

{{math | ...}}

### mathjax-or

### maybe

### member

### mparen

### n/a

### named req

{{named req|Callable}}

### nbsp

### nbspt

### no

### noexcept

### normal

### open range/open range plain

### p

### par

{{par | name | desc}}

参数

### par begin/end

### par cmp/ccmp/cmp ord

{{par cmp/ccmp | comp |...}}

比较器参数

### par exec pol

Execution policy

### par gen

### par hreq

### par inc

{{par inc | TEMPLATE | txt}}

### par op1

{{par op1|unary_op|rp=OutputIt|p1=InputIt}}

### par op2

{{par op2|binary_op|rp=OutputIt|p1=InputIt1|p2=InputIt2}}

### par opf

{{par opf|f|to be applied to the result of dereferencing every iterator in the range {{range|first|last}}|p1=InputIt}}

### par pred1

{{par pred1|p|for the elements found in the beginning of the range|p1=ForwardIt}}

### par pred2

{{par pred2|comp|if the first argument is ordered before the second|p1=ForwardIt|t2=T}}

### par pred2 eq

{{par pred2 eq|p|p1=InputIt1|p2=InputIt2}}

### par req 

{{par req|{{tt|C}} must be cv-unqualified class type {{vl|1,3}}}}

### par req insertable

### par req named

​       {{par req named|RandomIt|RandomAccessIterator|ValueSwappable}}

### par req named deref

### petty

​       {{petty|({{ltt|cpp/coroutine/generator#Member types|yielded}} is a reference type defined in {{c/core|std::generator}}.)}}

### plot

### posix

​       {{posix|time||POSIX specification}}

### range/range plain

​       {{range|0|std::distance(start, finish)}}

### rconcept

​       {{rconcept|CopyConstructible}}

### ref std

​       {{ref std|section=4.1|title=Implementation compliance|id=intro.compliance|p=10}}

### ref std c++98/03/11/14/17/20/23/26



### ref std end

### rev

{{rev begin}}

{{rev|until=c++20|{{cpp/atomic/sequentially-consistent-cpp11}}}}

{{rev|since=c++20|{{cpp/atomic/sequentially-consistent-cpp20}}}}

{{rev end}}

### rev inl       

{{rev inl|since=c++20|and {{ltt|cpp/types/common_reference|std::basic_common_reference}}}}

### rl/rli

​       {{rl|basic_regex/constants|this page}}

### rlp

{{rlp|comment|Comments}}

### rlpf

​       {{rlpf|}}



### rlpi

​       {{rlpi|/#Data members|base_}}

### rlps

​       {{rlps|/#Data members}}

### rlpsd

​       {{rlpsd|function template#Template argument substitution}}

### rlpsi

​       {{rlpsi|/#base_}}

### rlpst

​       {{rlpst|/#current}}

### rlpt

​       {{rlpt|preprocessor/include|#include}}

### rlt

​       {{rlt|simd|experimental::simd}}

### rltf

​       {{rltf|begin}}

### rrev

{{rrev|since=c++23|

During [[cpp/language/class template argument deduction|class template argument deduction]], only the first argument contributes to the deduction of the container's {{tt|Allocator}} template parameter.

}}

### rrev multi

{{rrev multi|until1=c++23|rev1=
Returns an iterator to the first element of the const-qualified argument that is treated as a reversed sequence.
|rev2=

### satisfies bitmask

​       {{satisfies bitmask|copy_options}}

### sdsc

​       {{sdsc|num=1|{{ttb|/*}} {{spar|comment}} {{ttb|*/}}}}

### sdsc begin/end

### sep

### small

### source

{{source|1=
std::vector<int> v {7, 1, 4, 0, -1};
std::ranges::sort(v); // constrained algorithm
}}

### spar

{{spar|cv}}

### spar optional

{{spar optional|cv}}

### spar sep

{{spar sep|expression}}

### stddoc

{{stddoc|P0847R7}}

### stddoc latest draft

### su

### sub

### sup

### title

​       {{title|1=C++ reference}}

### todo

​       {{todo|Check that all significant features are mentioned (using the Compiler Support tables below). Add more links and maybe regroup some lines.}}

### tt

{{tt | ...}}

作用：代码体

### ttb/tti/ttn/ttni/ttt/

### v

{{v | 7}}

### vertical

​       {{vertical|{{tt|std::int}}'''x'''{{tt|_t}}}}

### vl

​       {{vl|1}}

### wg21

​       {{wg21|P2210R2}}

### yes

{{yes | }}