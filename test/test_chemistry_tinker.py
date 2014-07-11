"""
Tests the functionality in the tinker subpackage
"""

import utils
import unittest
from chemistry.tinker import parameterfile, system, tinkerfiles

get_fn = utils.get_fn

class TestTinkerFiles(unittest.TestCase):
    
    def testParameterFile(self):
        param = parameterfile.AmoebaParameterSet(get_fn('amoeba09.prm'))
        attributes = {'angle-sextic': 2.2e-08, 'direct-13-scale': 1.0,
                      'radiustype': 'R-MIN', 'mpole-14-scale': 0.4,
                      'direct-12-scale': 1.0, 'mpole-12-scale': 0.0,
                      'mutual-13-scale': 1.0, 'mpole-13-scale': 0.0,
                      'opbend-pentic': -7e-07, 'vdw-13-scale': 0.0,
                      'angle-cubic': -0.014, 'mutual-12-scale': 1.0,
                      'angle-pentic': -7e-07, 'vdw-14-scale': 1.0,
                      'polarization': 'MUTUAL', 'polar-13-scale': 0.0,
                      'forcefield': 'AMOEBA-2009', 'radiussize': 'DIAMETER',
                      'bond-quartic': 3.793125, 'vdwtype': 'BUFFERED-14-7',
                      'polar-12-scale': 0.0, 'mutual-14-scale': 1.0,
                      'mutual-11-scale': 1.0, 'direct-14-scale': 1.0,
                      'torsionunit': 0.5, 'polar-15-scale': 1.0, 'radiusrule':
                      'CUBIC-MEAN', 'dielectric': 1.0, 'polar-14-intra': 0.5,
                      'vdw-12-scale': 0.0, 'direct-11-scale': 0.0, 'opbendtype':
                      'ALLINGER', 'opbend-quartic': 5.6e-05, 'polar-14-scale':
                      1.0, 'opbend-sextic': 2.2e-08, 'vdw-15-scale': 1.0,
                      'bond-cubic': -2.55, 'opbend-cubic': -0.014,
                      'angle-quartic': 5.6e-05, 'mpole-15-scale': 0.8,
                      'epsilonrule': 'HHG'}
        for key in attributes:
            self.assertEqual(param.attributes[key], attributes[key])

        self.assertEqual(len(param.angles), 18)
        self.assertAlmostEqual(param.angles['27-31-29'].k, 48.2)
        self.assertAlmostEqual(param.angles['27-31-29'].theteq, 109.5)
        self.assertAlmostEqual(param.angles['27-31-29'].theteq2, 110.2)
        self.assertAlmostEqual(param.angles['27-31-29'].theteq3, 111.0)

        self.assertEqual(len(param.bonds), 13)
        self.assertAlmostEqual(param.bonds['18-19'].k, 1072.0)
        self.assertAlmostEqual(param.bonds['18-19'].req, 1.1874)

        self.assertEqual(len(param.dihedrals), 150)
        self.assertEqual(param.dihedrals['41-40-40-51'].k, [0, 0, 0.299])
        self.assertEqual(param.dihedrals['41-40-40-51'].phase, [0, 180.0, 0])
        self.assertEqual(param.dihedrals['41-40-40-51'].periodicity, [1, 2, 3])

        self.assertEqual(len(param.opbends), 35)
        self.assertAlmostEqual(param.opbends['60-62-0-0'].k, 107.9)
        
        self.assertEqual(len(param.torsion_torsions), 0)

        self.assertEqual(len(param.urey_bradleys), 1)
        self.assertEqual(param.urey_bradleys['35-34-35'].k, -7.6)
        self.assertEqual(param.urey_bradleys['35-34-35'].req, 1.5326)

        self.assertEqual(len(param.multipoles), 17)
        self.assertTrue(not any(param.multipoles['2-0-0'].potential_terms))

    def testAnalout(self):
        analout = system.TinkerAnalout(get_fn('jac.analout'))
        self.assertEqual(len(analout.atom_list), 23558)
        self.assertEqual(len(analout.angle_list), 11584)
        self.assertEqual(len(analout.atom_inter_flags), 23)
        self.assertEqual(len(analout.atom_list), 23558)
        self.assertEqual(len(analout.bond_list), 16569)
        self.assertEqual(len(analout.dipole_list), 23558)
        self.assertEqual(len(analout.multipole_list), 23558)
        self.assertEqual(len(analout.oopbend_list), 1566)
        self.assertEqual(len(analout.pair12_list), 16569)
        self.assertEqual(len(analout.pair13_list), 11584)
        self.assertEqual(len(analout.pair14_list), 6556)
        self.assertEqual(len(analout.pair15_list), 7476)
        self.assertEqual(len(analout.pitors_list), 292)
        self.assertEqual(len(analout.pointers), 23)
        self.assertEqual(len(analout.stretchbend_list), 4031)
        self.assertEqual(len(analout.torangle_list), 6701)
        self.assertEqual(len(analout.tortor_list), 147)
        self.assertEqual(len(analout.ureybrad_list), 7023)

        # Sample some random attributes and assume this is comprehensive
        self.assertEqual(analout.multipole_list[5].definition, 'Z-then-X')
        self.assertEqual(analout.multipole_list[5].frame, [1, 2])
        self.assertEqual(analout.multipole_list[5].moment,
                         [0.2124, 0.0, 0.0, -0.1249, 0.03622, 0.0, -0.01437,
                          0.0, 0.0, -0.02185])
        
        self.assertEqual(analout.pitors_list[5].atom1.type, 9)
        self.assertEqual(len(analout.pair12_list), 16569)
    
    def testXyz(self):
        xyz = tinkerfiles.XyzFile(get_fn('nma.xyz'))
        self.assertEqual(xyz.box, [30.735, 30.876, 28.485, 90.0, 90.0, 90.0])
        self.assertEqual(xyz.natom, 2466)
        self.assertEqual(len(xyz.atom_list), xyz.natom)
        self.assertEqual(xyz.atom_list[0].name, 'C')
        self.assertEqual(xyz.atom_list[0].type, 221)
        self.assertEqual(len(xyz.atom_list[0].bonded_partners), 4)
        self.assertEqual(xyz.atom_list[-1].name, 'H')
        self.assertEqual(xyz.atom_list[-1].type, 248)

    def testDyn(self):
        dyn = tinkerfiles.DynFile(get_fn('nma.dyn'))
        self.assertEqual(dyn.natom, 2466)
        for attr in ('accelerations', 'old_accelerations', 'box', 'positions',
                     'velocities'):
            self.assertTrue(hasattr(dyn, attr))

        self.assertAlmostEqual(dyn.positions[10], [-0.1099425448789507,
                               -1.83499212341286, 6.089155631551154])