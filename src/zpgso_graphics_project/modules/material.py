from dataclasses import dataclass

@dataclass
class Material:
    color: tuple[int,int,int]
    K_D: float
    K_S: float
    K_A: float
    specular_exponent: int # the shineness exponent, n, in the Phong/Blinn-Phong model