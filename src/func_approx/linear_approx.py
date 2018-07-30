from typing import Sequence, Callable, Tuple, TypeVar
from func_approx.func_approx_base import FuncApproxBase
from scipy.stats import norm
import numpy as np

X = TypeVar('X')


class LinearApprox(FuncApproxBase):

    def __init__(
        self,
        feature_funcs: Sequence[Callable[[X], float]],
        reglr_coeff: float,
        learning_rate: float,
        adam: bool,
        adam_decay1: float,
        adam_decay2: float,
    ):
        super().__init__(
            feature_funcs,
            reglr_coeff,
            learning_rate,
            adam,
            adam_decay1,
            adam_decay2
        )

    def init_params(self) -> Sequence[np.ndarray]:
        return [np.zeros(self.num_features + 1)]

    def init_adam_caches(self)\
            -> Tuple[Sequence[np.ndarray], Sequence[np.ndarray]]:
        return [np.zeros(self.num_features + 1)],\
               [np.zeros(self.num_features + 1)]

    def get_func_eval(self, x_vals: X):
        """
        This must return a float but lint is not happy, so removed the
        return type annotation
        """
        return np.dot(self.params[0], self.get_feature_vals(x_vals))

    def get_gradient(
            self,
            x_vals_seq: Sequence[X],
            supervisory_seq: Sequence[float]
    ) -> Sequence[np.ndarray]:
        # all_features = self.get_feature_vals_pts(x_vals_seq)
        # return [np.dot(np.dot(all_features, self.params[0]) - np.array(supervisory_seq),
        #               all_features)]
        return [np.sum((self.get_func_eval(x) - supervisory_seq[i]) * self.get_feature_vals(x)
                      for i, x in enumerate(x_vals_seq))]


if __name__ == '__main__':
    la = LinearApprox(
        feature_funcs=FuncApproxBase.get_identity_feature_funcs(3),
        reglr_coeff=0.,
        learning_rate=0.1,
        adam=True,
        adam_decay1=0.9,
        adam_decay2=0.999
    )
    alpha = 2.0
    beta_1 = 10.0
    beta_2 = 4.0
    beta_3 = -6.0
    beta = (beta_1, beta_2, beta_3)
    x_pts = np.arange(-10.0, 10.0, 0.5)
    y_pts = np.arange(-10.0, 10.0, 0.5)
    z_pts = np.arange(-10.0, 10.0, 0.5)
    pts = [(x, y, z) for x in x_pts for y in y_pts for z in z_pts]

    # noinspection PyShadowingNames
    def superv_func(pt, alpha=alpha, beta=beta):
        return alpha + np.dot(beta, pt)

    n = norm(loc=0., scale=10.)
    superv_pts = [superv_func(r) for r in pts] + n.rvs(size=len(pts))
    # import matplotlib.pyplot as plt
    for _ in range(1000):
        print(la.params[0])
        la.update_params(pts, superv_pts)
        # pred_pts = [la.get_func_eval(x) for x in pts]
        # print(np.linalg.norm(np.array(pred_pts) - np.array(superv_pts)) / len(superv_pts))

