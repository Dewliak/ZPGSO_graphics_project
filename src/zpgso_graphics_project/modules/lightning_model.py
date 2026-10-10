from .vec4 import Vec4, dot_product, normalize

from .material import Material
from .light_types import LightSource, PointLightSource, DirectionalLightSource

from abc import ABC, abstractmethod


class LightningModel(ABC):
    @abstractmethod
    def shade(
        self,
        point: Vec4, # based on flat shading should be the center of the polygon
        normal: Vec4, # normal for the polygon
        angle_of_viewer: Vec4, # for the specular reflection
        light_source: LightSource,
        material: Material
    ) -> tuple[int, int, int]:
        pass


class BlinnPhongModel(LightningModel):
    I_A:float = 1.0 # constant for now

    def shade(
        self,
        point: Vec4,
        normal: Vec4, 
        angle_of_viewer: Vec4 ,
        light_source: LightSource,
        material: Material
        ) -> tuple[int, int, int]:

        L: Vec4 = light_source.get_light_direction(point=point) # Light vector
        V = normalize(angle_of_viewer)
        I_L = light_source.calculate_intensity(point=point)

        #diffuse light
        I_D = material.K_D * max(0,dot_product(normal, L)) * I_L 

        #Specular

        H = normalize(Vec4(L[0] + V[0],
                           L[1] + V[1],
                           L[2] + V[2],
                           0))

        I_S = material.K_S*(max(0,dot_product(normal,H))**material.specular_exponent)*I_L

        #Emission
        I_E = 0.0 # for now

        #Ambient
        I_A = material.K_A*self.I_A

        I = I_E + I_D + I_S + I_A


  
        return (max(0,min(255,round(material.color[0]*I))),
                max(0,min(255,round(material.color[1]*I))),
                max(0,min(255,round(material.color[2]*I))))

class PhongModel(LightningModel):
    I_A:float = 1.0 # constant for now

    def shade(
        self,
        point: Vec4,
        normal: Vec4, 
        angle_of_viewer: Vec4 ,
        light_source: LightSource,
        material: Material
        ) -> tuple[int, int, int]:

        L: Vec4 = normalize(light_source.get_light_direction(point=point)) # Light vector
        V = normalize(angle_of_viewer)


        I_L = light_source.calculate_intensity(point=point)

        #diffuse light
        I_D = material.K_D * max(0,dot_product(normal, L)) * I_L 

        #Specular
        
        # since I dint implement constant multiplication for the vectors
        R_k = 2*(dot_product(normal, L))
        R_temp = Vec4(R_k*normal._vector[0],R_k*normal._vector[1],R_k*normal._vector[2],0)
        R = R_temp - L

        I_S = material.K_S*(max(0,dot_product(R, V))**material.specular_exponent)*I_L

        #Emission
        I_E = 0.0 # for now

        #Ambient
        I_A = material.K_A*self.I_A

        I = I_E + I_D + I_S + I_A


  
        return (max(0,min(255,round(material.color[0]*I))),
                max(0,min(255,round(material.color[1]*I))),
                max(0,min(255,round(material.color[2]*I))))


