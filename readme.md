# Representação de Malha de Triângulos em um Grafo Dual

Inicialmente este trabalho foi realizado para a cadeira de Geometria Computacional - PUC-Rio

## O que é?

[Malha de Triangulos](https://pt.wikipedia.org/wiki/Malha_triangular)

[Grafo Dual](https://pt.wikipedia.org/wiki/Grafo_dual)

## Notas

* Representação Original da Malha de Triângulos

Tabela de Vertices

| __V__ | x | y |
|:-:|:-:|:-:|
| 0 | x'  | y'  |

Tabela de Triângulos

| __T__ | v0 | v1 | v2|
|:-:|:-:|:-:|:-:|
| 0 | v0'  | v1'  | v2'  |

* Representação da Malha de Triângulos usando Grafo Dual

Tabela de Vertices

| __V__ |  x |  y | __T__  |
|:-:|:--:|:--:|:----:|
| 0 | x' | y' | t' |

Tabela de Triângulos

| __T__ | v0 | v1 | v2|  t0 | t1 | t2|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 0 | v0'  | v1'  | v2'  |t0'  | t1'  | t2'  |

## Uso

```python

#Leitura do Arquivo Original de Malhas
vertices, triangles = getVerticesAndTrianglesFromFile()

#Mudança de Representação
vertices, triangles = GetDualGraphRepresentation(vertices, triangles)

#Salvamento do Arquivo
SaveDualGraphRepresentationInFile(vertices, triangles)

#Recupera os triângulos adjascentes a um triângulo
GetAdjacentTrianglesOfATriangle(triangles, 2)
```



