# MetaData Loading
## For direct calling as a script
```
> python2 dir_tcga.py [disease_type='LGG'] [mode='SURVIVAL']
```

## For calling as an api
import path and module
```
>import sys
>import os
>simp_path = 'TCGAIntegrator'
>abs_path = os.path.abspath(simp_path)
>sys.path.append(abs_path)
>import TCGAIntegrator.TCGAData as TCGAData
```
calling api
```
>TCGAData.loadData(disease_type,Mode='SURVIVAL')
```
@ default disease_type='LGG'

@ default Mode='SURVIVAL'

