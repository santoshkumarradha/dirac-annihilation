from ase.io import read
from gpaw import GPAW, PW, FermiDirac, restart
import pickle

licoo2 = read("gdn2.cif")
licoo2.set_initial_magnetic_moments(magmoms=[1, 0, 0])

calc = GPAW(mode=PW(600),
            xc='PBE',
            kpts=(12, 12, 1),
            random=True,
            occupations=FermiDirac(0.01),
            nbands=-30,
            txt='licoo2_gs.txt')
licoo2.calc = calc

licoo2.get_potential_energy()
calc.write('gs.gpw')

calc = GPAW('gs.gpw',
            nbands=-20,
            fixdensity=True,
            symmetry='off',
            kpts={
                'path': 'GKMG',
                'npoints': 60
            },
            convergence={'bands': -20})
calc.get_potential_energy()
bs = calc.band_structure()
bs.plot(filename='bandstructure.png', show=False, emax=5.0, emin=-5.0)
calc.write('bands_gs.gpw')

pickle.dump(bs, open("bands_data.pickle", "wb"))