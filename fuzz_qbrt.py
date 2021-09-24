import unittest
import hypothesis.strategies as st
from hypothesis import given, settings


def cubic_root(x):
    # x is taken at base 1e36
    # result is at base 1e18
    D = x // 10**18
    diff = 0
    for i in range(255):
        D_prev = D
        tmp = x // D * 10**18 // D * 10**18 // D
        D = D * (2 * 10**18 + tmp) // (3 * 10**18)
        if D > D_prev:
            diff = D - D_prev
        else:
            diff = D_prev - D
        if diff <= 1 or diff * 10**18 < D:
            return D
    raise ValueError("Did not converge")


class TestQbrt(unittest.TestCase):
    # Will have convergence problems when ETH*BTC is cheaper than 0.01 squared dollar
    # (for example, when BTC < $0.1 and ETH < $0.1)
    @given(
        st.integers(10**34, (10**10 * 10**18) ** 2),
    )
    @settings(max_examples=10000)
    def test_qbrt(self, val):
        qbrt_int = cubic_root(val) / 1e18
        qbrt_ideal = (val / 1e36) ** (1/3)
        assert abs(qbrt_int - qbrt_ideal) < 5e-15 * max(qbrt_ideal, 1)


if __name__ == "__main__":
    unittest.main()
