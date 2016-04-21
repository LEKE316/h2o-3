import sys
sys.path.insert(1,"../../../")
import h2o
from tests import pyunit_utils
from h2o.estimators.glm import H2OGeneralizedLinearEstimator as glm

def reg_path_glm():
    # read in the dataset and construct training set (and validation set)
    d = h2o.import_file(path=pyunit_utils.locate("smalldata/logreg/prostate.csv"))
    m = glm(family='binomial',lambda_search=True,solver='COORDINATE_DESCENT')
    m.train(training_frame=d,x=range(2,9),y=1)
    r = glm.getGLMRegularizationPath(m)

    assert len(r['lambdas']) == 100
    for l in range(0,len(r['lambdas'])):
        m = glm(family='binomial',lambda_search=False,Lambda=r['lambdas'][l],solver='COORDINATE_DESCENT')
        m.train(training_frame=d,x=range(2,9),y=1)
        cs = r['coefficients'][l]
        cs_norm = r['coefficients_std'][l]
        print(cs)
        print(m.coef())
        diff = 0
        diff2 = 0
        for n in cs.keys():
            diff = max(diff,abs(cs[n] - m.coef()[n]))
            diff2 = max(diff2,abs(cs_norm[n] - m.coef_norm()[n]))
        print(diff)
        print(diff2)
        assert diff < 1e-3
        assert diff2 < 1e-3
if __name__ == "__main__":
    pyunit_utils.standalone_test(reg_path_glm)
else:
    reg_path_glm()