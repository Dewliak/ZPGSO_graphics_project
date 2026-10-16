from .vec4 import Vec4


def load_obj_file(filename:str) -> tuple[list[Vec4], list[tuple[int, int, int]]]:
    # accept only v and f lines
    # ignore the types where there are textures, so "f 1/1/1 2/2/1 3/3/1"

    vertices:list[Vec4] = []
    faces:list[tuple[int,int,int]] = []
    
    try:
        with open(filename,"r") as f:
            for line in f:
                parameters = line.split()

                if(len(parameters) == 0):
                    continue

                match(parameters[0]):
                    case "v":
                        
                        if(len(parameters)) < 4: # v x y z, throw error
                            raise ValueError("v vertex invalid number of paramters at least 3 !")
                        
                        try:
                            x, y, z = map(float, parameters[1:4])

                        except ValueError:
                            raise ValueError("v vertex invalid formats, not all parameters are floats !")

                        vertices.append(Vec4(x, y, z))
                    case "f":
                        # !!! has the assumption that we have all the vertices !!!

                        if(len(parameters)) < 4: # f i1 i2 i3, throw error
                            raise ValueError("f face invalid number of paramters at least 3 !")
                        
                        try:
                            i1,i2,i3 = list(map(int, parameters[1:4]))
                        except ValueError:
                            raise ValueError("f face, invalid types, not all parameters and ints !")
                        indexes: tuple[int,int,int] = (i1,i2,i3)
                        #check if they are valid index, since they are 1-based
                        
                        actual_indexes:list[int] = []
                        
                        for index in indexes:
                            if(index == 0):
                                raise ValueError("face index cannot be 0, they are 1-based")

                            actual = index - 1 if index > 0 else len(vertices) + index

                            if(actual < 0 or actual >= len(vertices)):
                                raise ValueError("face index out of range")

                            actual_indexes.append(actual)
                    
                        faces.append((actual_indexes[0],actual_indexes[1],actual_indexes[2]))
                        
                    case _: #ignore this case
                        continue
    except FileNotFoundError:
        raise ValueError("File not found!")

    return vertices, faces