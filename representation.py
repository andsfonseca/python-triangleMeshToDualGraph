import re

PATH_MESH_FILE = "data/malha.txt"
PATH_OUTPUT_REPRESENTATION = "data/malha_adj.txt"

def getVerticesAndTrianglesFromFile(path=PATH_MESH_FILE):
    """Recupera os vértices e os triangulos entre as arestas a partir de um arquivo

    References:
        Primeira Linha do arquivo representado por N e M, sendo N o número de vértices e M o número de triangulos

    Parameters:
        path (String): Caminho para o arquivo

    Returns:
        Array: Array de Vértices
        Array: Conjunto de Triangulos representado por pontos (Index)
    """

    vertices = []
    triangles = []
    file = list(open(path, "r"))

    nm = [int(d) for d in re.findall(r'-?\d+', file[0])]

    for i in range(1, nm[0]+1):
        vertex = [int(d) for d in re.findall(r'-?\d+', file[i])]
        vertices.append(vertex)

    for i in range(nm[0]+1, nm[0]+1 +nm[1] ):
        triangle = [int(d) for d in re.findall(r'-?\d+', file[i])]
        triangles.append(triangle)
        
    return vertices, triangles

def getIndexKey( index1, index2): return (str(index1)+ "-"+ str(index2)) if index1 < index2 else (str(index2)+ "-"+ str(index1))

def GetDualGraphRepresentation(vertices, triangles):
    """Transforma a representação de vertices e triangulos em uma representação de Grafo dual

    Parameters:
        vertices (Array): Array de Vertices
        triangles (Array): Array de Triangulos

    Returns:
        Array: Array de Vértices
        Array: Conjunto de Triangulos
    """
    n_vertices = vertices[:]
    n_triangles = triangles[:]

    dictionary = {}

    for v in n_vertices:
        v.append(-1)

    for i in range(len(triangles)):
        triangle = triangles[i]

        v0 = triangle[0]
        v1 = triangle[1]
        v2 = triangle[2]

        #Elemento t do vertice
        n_vertices[v0][2] = i
        n_vertices[v1][2] = i
        n_vertices[v2][2] = i

        #Elemento t dos triangulos
        for _ in range(3):
            n_triangles[i].append(-1)

        #Para cada Aresta
        v0v1 = getIndexKey(v0, v1)
        v1v2 = getIndexKey(v1, v2)
        v2v0 = getIndexKey(v2, v0)

        #>> Para V0V1
        if(not v0v1 in dictionary): 
            dictionary[v0v1] = i
        else:
            triangle[5] = dictionary[v0v1]
            oppositeTriangle = n_triangles[dictionary[v0v1]]

            o_v0v1 = getIndexKey(oppositeTriangle[0], oppositeTriangle[1])
            o_v1v2 = getIndexKey(oppositeTriangle[1], oppositeTriangle[2])
            o_v2v0 = getIndexKey(oppositeTriangle[2], oppositeTriangle[0])

            if(o_v0v1 == v0v1):
                oppositeTriangle[5] = i
            if(o_v1v2 == v0v1):
                oppositeTriangle[3] = i
            if(o_v2v0 == v0v1):
                oppositeTriangle[4] = i

        #>> Para V0V1
        if(not v1v2 in dictionary): 
            dictionary[v1v2] = i
        else:
            triangle[3] = dictionary[v1v2]
            oppositeTriangle = n_triangles[dictionary[v1v2]]

            o_v0v1 = getIndexKey(oppositeTriangle[0], oppositeTriangle[1])
            o_v1v2 = getIndexKey(oppositeTriangle[1], oppositeTriangle[2])
            o_v2v0 = getIndexKey(oppositeTriangle[2], oppositeTriangle[0])

            if(o_v0v1 == v1v2):
                oppositeTriangle[5] = i
            if(o_v1v2 == v1v2):
                oppositeTriangle[3] = i
            if(o_v2v0 == v1v2):
                oppositeTriangle[4] = i

        #>> Para V0V1
        if(not v2v0 in dictionary): 
            dictionary[v2v0] = i
        else:
            triangle[4] = dictionary[v2v0]
            oppositeTriangle = n_triangles[dictionary[v2v0]]

            o_v0v1 = getIndexKey(oppositeTriangle[0], oppositeTriangle[1])
            o_v1v2 = getIndexKey(oppositeTriangle[1], oppositeTriangle[2])
            o_v2v0 = getIndexKey(oppositeTriangle[2], oppositeTriangle[0])

            if(o_v0v1 == v2v0):
                oppositeTriangle[5] = i
            if(o_v1v2 == v2v0):
                oppositeTriangle[3] = i
            if(o_v2v0 == v2v0):
                oppositeTriangle[4] = i

    return n_vertices, n_triangles

def SaveDualGraphRepresentationInFile(vertices, triangles, path=PATH_OUTPUT_REPRESENTATION):
    """Salva um arquivo com os vertices e triangulos

    Parameters:
        vertices (Array): Array de vértices
        triangles (Array): Array de triângulos
        path (String): Caminho para o arquivo
    """

    f= open(path,"w+")
    
    #Linha de Tamanhos
    f.write("%d\t%d\n" % (len(vertices), len(triangles)))

    for v in vertices:
        f.write("%d\t%d\t%d\n" % (v[0], v[1], v[2]))

    for t in triangles:
        f.write("%d\t%d\t%d\t%d\t%d\t%d\n" % (t[0], t[1], t[2], t[3], t[4], t[5]))

def GetAdjacentTrianglesOfATriangle (triangles, triangleIndex):
    """Retorna os triângulos adjascentes a um triângulo

    Parameters:
        triangles (Array): Array de Triangulos
        triangleIndex (Integer): Index do Triângulo

    Returns:
        Array: Conjunto de Index que representam os triângulo adjascentes
    """
    triangle = triangles[triangleIndex]

    v0 = triangle[0]
    v1 = triangle[1]
    v2 = triangle[2]

    visited = {}
    solution = []
    queue = []

    if(triangle[3] != -1): queue.append(triangle[3])
    if(triangle[4] != -1): queue.append(triangle[4])
    if(triangle[5] != -1): queue.append(triangle[5])

    visited[str(triangleIndex)] = True

    while(queue):
        index = queue.pop(0)

        visited[str(index)] = True

        triangle = triangles[index]

        if(triangle [0] == v0 or triangle[1] == v0 or triangle[2] == v0 or 
            triangle [0] == v1 or triangle[1] == v1 or triangle[2] == v1 or
            triangle [0] == v2 or triangle[1] == v2 or triangle[2] == v2):

            solution.append(index)

            if(triangle[3] != -1 and (not str(triangle[3]) in visited) and (not triangle[3] in queue)): queue.append(triangle[3])
            if(triangle[4] != -1 and (not str(triangle[4]) in visited) and (not triangle[4] in queue)): queue.append(triangle[4])
            if(triangle[5] != -1 and (not str(triangle[5]) in visited) and (not triangle[5] in queue)): queue.append(triangle[5])

    return solution

vertices, triangles = getVerticesAndTrianglesFromFile()

vertices, triangles = GetDualGraphRepresentation(vertices, triangles)

SaveDualGraphRepresentationInFile(vertices, triangles)

GetAdjacentTrianglesOfATriangle(triangles, 1)


