# -*- coding: utf-8 -*-
"""
Created on Thu May 11 19:40:01 2023

@author: Xela 
"""


import matplotlib
from sympy import Function, Id, Symbol, Matrix
import sympy as syp
syp.init_printing(use_latex=True)
import math


def invert(func, codomain_symbols):
    return syp.solve(func - codomain_symbols, func.free_symbols)[0]

class Coordinate_Patch:
    def __init__(self, coordinate_funcs, domain_tester, codomain_symbols): #each coordinate_func gives a coordinate. e.g. if the domain is the sphere embedded in R^3, then [theta(x,y,z), phi(x,y,z)] is the chart.   
        self.chart = coordinate_funcs
        self.domain_tester = domain_tester #takes a point on the manifold and returns true if the point is in the domain of the chart
        self.inverse_chart = invert(coordinate_funcs, codomain_symbols)
        
class Manifold:
    def __init__(self, domain_symbols, codomain_symbols, atlas):
        self.codomain_symbols = codomain_symbols
        self.dim = len(codomain_symbols)
        self.atlas = atlas
    def attach_domain_representation(self, domain_representation): 
        #e.g. domain_representation may be an embedding into R^3
        self.domain_representation = domain_representation
    def attach_chart(self, chart): 
        self.atlas = self.atlas.col_join(Matrix([chart]))
    def attach_charts(self, charts):
        self.atlas = self.atlas.col_join(charts)
    def Make_Object_On_Manifold_Type(self, name): #creates baseclasses for things that live on a manifold and thus need the relevant smbols
        return type(name, (), {'attached_manifold': self})
    
sphere_x = Symbol('s_x')
sphere_y = Symbol('s_y')
sphere_z = Symbol('s_z')
sphere_domain_symbols = Matrix([sphere_x, sphere_y, sphere_z])

sphere_theta = Symbol('theta')
sphere_phi = Symbol('phi')
sphere_codomain_symbols = Matrix([sphere_theta, sphere_phi])

Sphere = Manifold(sphere_domain_symbols, sphere_codomain_symbols)
make_auxillary_map = syp.sqrt(1-sphere_domain_symbols)
chart_xplus = Chart(sphere_domain_symbols.norm(),)# x>0)
chart_xminus = None
chart_yplus =None
chart_yminus = None
chart_zplus =None
chart_zminus = None
Object_On_Sphere = Sphere.Make_Object_On_Manifold_Type('Object_On_Sphere')

class Local_Coordinates(Object_On_Sphere):
    @classmethod
    def make_coordinate_derivation(cls, coordinate_func, chart, inverse_chart):
        def this_derivation(in_func):
            def output_of_derivation(point_on_manifold):
                chart.subs(point_on_manifold)
            
    def __init__(self, chart):
        self.chart = chart
        
class Frame:
    @classmethod
    def jacobian(cls, coordinate_charts):
        pass
        
    def __init__(self, coordinate_charts): #each coordinate_chart goes from the manifold to the real line, giving the coordinate funcs.
        self.coordinate_charts = coordinate_charts
        self.jacobian = Frame.jacobian(coordinate_charts)
        self.inverse_jacobian = self.jacobian.inv()

        
  

        

class Tensor_Field:
    def __init__(self, coord_funcs, transformation_type, frame): #transformation_type is a list of ints, where each int is 0 for covariant and 1 for contravariant
        self.coord_funcs = coord_funcs
        self.type = transformation_type
        self.frame = frame
    def transform(self, new_frame): #both self.frame and new_frame are expressed in the same frame
        pass
