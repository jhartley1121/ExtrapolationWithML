# Common imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn.linear_model as skl
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import os
from pylab import plt, mpl

def NuclearBindingEnergy ():
    infile = open(data_path("MassEval2016.dat"),'r')
    """                                                                                                                         
    This is taken from the data file of the mass 2016 evaluation.                                                               
    All files are 3436 lines long with 124 character per line.                                                                  
           Headers are 39 lines long.                                                                                           
       col 1     :  Fortran character control: 1 = page feed  0 = line feed                                                     
       format    :  a1,i3,i5,i5,i5,1x,a3,a4,1x,f13.5,f11.5,f11.3,f9.3,1x,a2,f11.3,f9.3,1x,i3,1x,f12.5,f11.5                     
       These formats are reflected in the pandas widths variable below, see the statement                                       
       widths=(1,3,5,5,5,1,3,4,1,13,11,11,9,1,2,11,9,1,3,1,12,11,1),                                                            
       Pandas has also a variable header, with length 39 in this case.                                                          
    """

    # Read the experimental data with Pandas
    Masses = pd.read_fwf(infile, usecols=(2,3,4,6,11),
                  names=('N', 'Z', 'A', 'Element', 'Ebinding'),
                  widths=(1,3,5,5,5,1,3,4,1,13,11,11,9,1,2,11,9,1,3,1,12,11,1),
                  header=39,
                  index_col=False)

    # Extrapolated values are indicated by '#' in place of the decimal place, so
    # the Ebinding column won't be numeric. Coerce to float and drop these entries.
    Masses['Ebinding'] = pd.to_numeric(Masses['Ebinding'], errors='coerce')
    Masses = Masses.dropna()
    # Convert from keV to MeV.
    Masses['Ebinding'] /= 1000

    # Group the DataFrame by nucleon number, A.
    Masses = Masses.groupby('A')
    # Find the rows of the grouped DataFrame with the maximum binding energy.
    Masses = Masses.apply(lambda t: t[t.Ebinding==t.Ebinding.max()])

    A = Masses['A']
    Z = Masses['Z']
    N = Masses['N']
    Element = Masses['Element']
    Energies = Masses['Ebinding']
    print(Masses)

    # Now we set up the design matrix X
    X = np.zeros((len(A),5))
    X[:,0] = 1
    X[:,1] = A
    X[:,2] = A**(2.0/3.0)
    X[:,3] = A**(-1.0/3.0)
    X[:,4] = A**(-1.0)
    
    return A, Energies, X
