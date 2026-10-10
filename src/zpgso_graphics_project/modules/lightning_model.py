from .vec4 import Vec4, dot_product, normalize

from .material import Material
from .light_types import LightSource , SpotLightSource, PointLightSource, DirectionalLightSource

import numpy
from abc import ABC, abstractmethod

# these default paramters for testing were given my an llm
DEFAULT_K_A = 0.1
DEFAULT_K_D = 0.7
DEFAULT_K_S = 0.5
DEFAULT_N = 32







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
        I_L = light_source.calculate_intensity(point=point)

        #diffuse light
        I_D = material.K_D * max(0,dot_product(normal, L)) * I_L 

        #Specular

        H = normalize(Vec4(L[0] + angle_of_viewer[0],
                           L[1] + angle_of_viewer[1],
                           L[2] + angle_of_viewer[2],
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


