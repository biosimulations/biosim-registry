import numpy as np
from process_bigraph import Step



class StatsTool(Step):
    config_schema = {
        'ignore_nans': "boolean",
    }

    def inputs(self):
        return {
            "compute_store" : "array",
        }

    def outputs(self):
        return {
            "stats_result": "array"
        }


class SumOfSquaresTool(StatsTool):
    def update(self, state, interval=None):
        compute_store = np.array(state['compute_store'])
        row, col = compute_store.shape
        result = np.empty((row, col))
        means = compute_store.mean(axis=0)
        for r in range(row):
            for c in range(col):
                res = (compute_store[r, c] - means[c])**2
                result[r, c] = res
        return {"stats_result": result.tolist()}
