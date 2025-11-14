import numpy as np
from process_bigraph import Step



class ComparisonTool(Step):
    config_schema = {
        'ignore_nans': "boolean",
    }

    def inputs(self):
        return {
            "left" : "array",
            "right": "array",
        }

    def outputs(self):
        return {
            "comparison_result": "array"
        }


class SubtractTool(ComparisonTool):
    def update(self, state, interval=None):
        left = state['left']
        right = state['right']
        result = np.array(left) - np.array(right)
        return {"comparison_result": result.tolist()}