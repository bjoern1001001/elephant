# -*- coding: utf-8 -*-
import neo
import numpy as np
import quantities as pq

import unittest
import elephant.multiple_filter_test as mft
from numpy.testing.utils import assert_array_almost_equal, assert_allclose
                                     
                                     
np.random.seed(13)


class FilterTestCase(unittest.TestCase):
    def setUp(self):
        self.test_array = [0.4, 0.5, 0.65, 0.7, 0.9, 1.15, 1.2, 1.9]
        '''
        spks_ri = [0.9, 1.15, 1.2]
        spk_le = [0.4, 0.5, 0.65, 0.7]
        '''
        mu_ri = (0.25 + 0.05) / 2
        mu_le = (0.1 + 0.15 + 0.05) / 3
        sigma_ri = ((0.25 - 0.15) ** 2 + (0.05 - 0.15) ** 2) / 2
        sigma_le = ((0.1 - 0.1) ** 2 + (0.15 - 0.1) ** 2 + (
                0.05 - 0.1) ** 2) / 3
        self.targ_t08_h025 = 0
        self.targ_t08_h05 = (3 - 4) / np.sqrt(
            (sigma_ri / mu_ri ** (3)) * 0.5 + (sigma_le / mu_le ** (3)) * 0.5)

    # Window Large #
    def test_filter_with_spiketrain_h05(self):
        st = neo.SpikeTrain(self.test_array, units='s', t_stop=2.0)
        target = self.targ_t08_h05
        res = mft._filter(0.8 * pq.s, 0.5 * pq.s, st)
        assert_array_almost_equal(res, target, decimal=9)
        self.assertRaises(ValueError, mft._filter, 0.8, 0.5 * pq.s, st)
        self.assertRaises(ValueError, mft._filter, 0.8 * pq.s, 0.5, st)
        self.assertRaises(ValueError, mft._filter, 0.8 * pq.s, 0.5 * pq.s,
                          self.test_array)
        
    # Window Small #
    def test_filter_with_spiketrain_h025(self):
        st = neo.SpikeTrain(self.test_array, units='s', t_stop=2.0)
        target = self.targ_t08_h025
        res = mft._filter(0.8 * pq.s, 0.25 * pq.s, st)
        assert_array_almost_equal(res, target, decimal=9)

    def test_filter_with_quantities_h025(self):
        st = pq.Quantity(self.test_array, units='s')
        target = self.targ_t08_h025
        res = mft._filter(0.8 * pq.s, 0.25 * pq.s, st)
        assert_array_almost_equal(res, target, decimal=9)

    def test_filter_with_plain_array_h025(self):
        st = self.test_array
        target = self.targ_t08_h025
        res = mft._filter(0.8 * pq.s, 0.25 * pq.s, st * pq.s)
        assert_array_almost_equal(res, target, decimal=9)
        
    def test_isi_with_quantities_h05(self):
        st = pq.Quantity(self.test_array, units='s')
        target = self.targ_t08_h05
        res = mft._filter(0.8 * pq.s, 0.5 * pq.s, st)
        assert_array_almost_equal(res, target, decimal=9)

    def test_isi_with_plain_array_h05(self):
        st = self.test_array
        target = self.targ_t08_h05
        res = mft._filter(0.8 * pq.s, 0.5 * pq.s, st * pq.s)
        assert_array_almost_equal(res, target, decimal=9)


class FilterProcessTestCase(unittest.TestCase):
    def setUp(self):
        self.test_array = [1.1, 1.2, 1.4, 1.6, 1.7, 1.75, 1.8, 1.85, 1.9, 1.95]
        x = (7 - 3) / np.sqrt(
            (0.0025 / 0.15 ** 3) * 0.5 + (0.0003472 / 0.05833 ** 3) * 0.5)
        self.targ_h05 = [[0.5, 1, 1.5],
                         [(0 - 1.7) / np.sqrt(0.4), (0 - 1.7) / np.sqrt(0.4),
                          (x - 1.7) / np.sqrt(0.4)]]

    def test_filter_process_with_spiketrain_h05(self):
        st = neo.SpikeTrain(self.test_array, units='s', t_stop=2.1)
        target = self.targ_h05
        res = mft._filter_process(0.5 * pq.s, 0.5 * pq.s, st, 2.01 * pq.s,
                                  np.array([[0.5], [1.7], [0.4]]))
        assert_array_almost_equal(res[1], target[1], decimal=3)
        
        self.assertRaises(ValueError, mft._filter_process, 0.5 , 0.5 * pq.s,
                              st, 2.01 * pq.s, np.array([[0.5], [1.7], [0.4]]))
        self.assertRaises(ValueError, mft._filter_process, 0.5 * pq.s, 0.5,
                              st, 2.01 * pq.s, np.array([[0.5], [1.7], [0.4]]))
        self.assertRaises(ValueError, mft._filter_process, 0.5 * pq.s,
                          0.5 * pq.s, self.test_array, 2.01 * pq.s,
                          np.array([[0.5], [1.7], [0.4]]))
      
    def test_filter_proces_with_quantities_h05(self):
        st = pq.Quantity(self.test_array, units='s')
        target = self.targ_h05
        res = mft._filter_process(0.5 * pq.s, 0.5 * pq.s, st, 2.01 * pq.s,
                                  np.array([[0.5], [1.7], [0.4]]))
        assert_array_almost_equal(res[0], target[0], decimal=3)

    def test_filter_proces_with_plain_array_h05(self):
        st = self.test_array
        target = self.targ_h05
        res = mft._filter_process(0.5 * pq.s, 0.5 * pq.s, st * pq.s,
                                  2.01 * pq.s, np.array([[0.5], [1.7], [0.4]]))
        self.assertNotIsInstance(res, pq.Quantity)
        assert_array_almost_equal(res, target, decimal=3)


class MultipleFilterAlgorithmTestCase(unittest.TestCase):
    def setUp(self):
        self.test_array = [1.1, 1.2, 1.4, 1.6, 1.7, 1.75, 1.8, 1.85, 1.9, 1.95]
        self.targ_h05_dt05 = [1.5 * pq.s]

    def test_MultipleFilterAlgorithm_with_spiketrain_h05(self):
        st = neo.SpikeTrain(self.test_array, units='s', t_stop=2.1)
        target = [self.targ_h05_dt05]
        res = mft.multiple_filter_test([0.5] * pq.s, st, 2.1 * pq.s, 5, 100,
                                       dt=0.1 * pq.s)
        assert_array_almost_equal(res, target, decimal=9)

    def test_MultipleFilterAlgorithm_with_quantities_h05(self):
        st = pq.Quantity(self.test_array, units='s')
        target = [self.targ_h05_dt05]
        res = mft.multiple_filter_test([0.5] * pq.s, st, 2.1 * pq.s, 5, 100,
                                       dt=0.5 * pq.s)
        assert_array_almost_equal(res, target, decimal=9)

    def test_MultipleFilterAlgorithm_with_plain_array_h05(self):
        st = self.test_array
        target = [self.targ_h05_dt05]
        res = mft.multiple_filter_test([0.5] * pq.s, st * pq.s, 2.1 * pq.s, 5,
                                       100, dt=0.5 * pq.s)
        #assert not isinstance(res, pq.Quantity)
        assert_array_almost_equal(res, target, decimal=9)
 
    def test_MultipleFilterAlgorithm_with_published_data(self):
        
        def gamma_train(k, teta, tmax):
            x = []

            for i in range(int(tmax * (k * teta) ** (-1) * 3)):
                x.append(np.random.gamma(k, teta))

            s = np.cumsum(x)
            idx = np.where(s < tmax)
            s = s[idx]  # gamma process
            return s

        def alternative_hypothesis(k1, teta1, c1, k2, teta2, c2, k3, teta3, c3,
                                   k4, teta4, T):
            s1 = gamma_train(k1, teta1, c1)
            s2 = gamma_train(k2, teta2, c2) + c1
            s3 = gamma_train(k3, teta3, c3) + c1 + c2
            s4 = gamma_train(k4, teta4, T) + c1 + c2 + c3
            return np.concatenate((s1, s2, s3, s4)), [s1[-1], s2[-1], s3[-1]]

        st = self.h1 = alternative_hypothesis(1, 1 / 8., 150, 2, 1 / 26., 30,
                                              1, 1 / 18., 320,
                                              2, 1 / 33., 200)[0]

        window_size = [10, 25, 50, 75, 100, 125, 150] * pq.s
        self.target_points = [149, 182, 500] * pq.s
        target = self.target_points

        result = mft.multiple_filter_test(window_size, st * pq.s, 700 * pq.s,
                                          5, 10000, dt=1 * pq.s)
        self.assertNotIsInstance(result, pq.Quantity)
        # assert_array_almost_equal(res, target, decimal=0)

        result_concatenated = []
        for i in result:
            result_concatenated = np.hstack([result_concatenated, i])
        result_concatenated = np.sort(result_concatenated)*pq.s
        assert_allclose(result_concatenated[:3], target[:3], rtol=0,
                        atol=5*pq.s)
                        
                        
if __name__ == '__main__':
    unittest.main()
