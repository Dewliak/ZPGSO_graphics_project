from .vec4 import Vec4, dot_product, euclidean_distance, normalize

from dataclasses import dataclass
from abc import ABC, abstractmethod

#These parameters are based on the presentation on the lecture
# The idea was to use the strategy pattern, well maybe isnt the best way to do it, its seemed finer working in java

@dataclass
class LightSource(ABC):
    intensity: float

    @abstractmethod
    def calculate_intensity(self, point: Vec4) -> float:
        pass    

    @abstractmethod
    def get_light_direction(self, point: Vec4) -> Vec4:
        pass    

@dataclass
class PointLightSource(LightSource):
    """
                    I_0
        I_L = ---------------------
                k_c + k_l*d + k_q+d^2
    """
    position: Vec4 # should make a check for w=1
    k_c: float
    k_l: float
    k_q: float

    def calculate_intensity(self, point: Vec4) -> float:
        distance = euclidean_distance(point, self.position)
        return self.intensity / (self.k_c + self.k_l*distance + self.k_q*distance*distance)

    def get_light_direction(self, point: Vec4) -> Vec4:
        return  normalize(point - self.position)

@dataclass
class DirectionalLightSource(LightSource):
    """
    I_L = I_0
    """
    direction: Vec4 # should make a check for w=0
    def calculate_intensity(self, point: Vec4) -> float:   
        return self.intensity

    def get_light_direction(self, point: Vec4) -> Vec4:
        return normalize(self.direction)

