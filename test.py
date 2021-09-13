import sys
import os
simp_path = 'TCGAIntegrator'
abs_path = os.path.abspath(simp_path)
sys.path.append(abs_path)

from TCGAIntegrator import TCGAData as TCGAData

def main():
    df = TCGAData.loadData("LGG",mode="Hybird")
    print(df.shape)




if __name__ == '__main__':
    main()
