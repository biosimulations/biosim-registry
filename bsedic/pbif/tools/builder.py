import copy
import json
from enum import EnumType, Enum
from typing import Any

from process_bigraph import Step, Process, ProcessTypes, Composite
from bsedic.pbif.tools import standard_types

class StepBuilder(Step):
    pass

class ComparisonProcess(Process):
    pass

# def add_comparison_step(viv: Vivarium, edge_id_1: str, edge_id_2: str) -> Vivarium:
#     name = f'compare_{edge_id_1}_to_{edge_id_2}'
#     comparison_process = {
#         'name': name,
#         'process_id': 'Comparison',
#         'config': {'ignore_nans': 'false'},
#         'inputs': {'left': ['array'],
#                    'right': ['array']},
#         'outputs': {'comparison_result': ['array']}
#     }
#     viv.add_process(**comparison_process)
#     viv.connect_process(name=name,
#                         inputs={"left": {edge_id_1: "result"}, "right": {edge_id_2: "result"}},
#                         outputs={"comparison_result": ['array']})
#     return viv


def add_model_changes_process():
    pass

class CompositeOverrides:
    pass

class CompositeParameterScan:
    pass

class CompositeBuilder:
    class CompositeType(Enum):
        CONFIG = 'config'
        STATE = 'state'

    class _PathNavigation:
        def __init__(self, path: list[str], values: list[Any], composite_type) -> None:
            self.path: list[str] = path
            self.values: list[Any] = values
            self.composite_type: CompositeBuilder.CompositeType = composite_type

    def __init__(self, core: ProcessTypes):
        self.core: ProcessTypes = core
        self.step_number: int = 0
        self.state: dict[Any, Any] = {}

    def allocate_step_key(self, step_name: str) -> str:
        step_key = f'{step_name}_{self.step_number}'
        self.step_number += 1
        return step_key

    # Recursively discover which set of items are being iterated upon
        # The result should take the shape of navigation helper class
    # With said set, recursively iterate through all configs
        # That is start with first entry in set, and recursively go until there are no more
        # Then iterate the values actually within the set, once all layers of recursion are reached. Iterating at each layer
        # At each layer, a piece of the dict should be constructed, with the final recursion layer placing the last piece in

    def _deconstruct_dictionary(self, base_path: list[str], dict_values: dict[str, Any],
                                composite_type: CompositeType) -> list[_PathNavigation]:
        keys_of_interest = list(dict_values.keys())
        paths_to_navigate: list[CompositeBuilder._PathNavigation] = []
        for fixated_key in keys_of_interest:
            new_path = base_path + [fixated_key]
            if type(dict_values[fixated_key]) == dict:
                paths_to_navigate += self._deconstruct_dictionary(new_path, dict_values[fixated_key], composite_type)
            elif type(dict_values[fixated_key]) == list:
                paths_to_navigate.append(self._PathNavigation(new_path, dict_values[fixated_key], composite_type))
            else:
                raise TypeError(f"Invalid type for combination for {dict_values} at {fixated_key}: "
                                f"{type(dict_values[fixated_key])}")
        return paths_to_navigate

    def add_parameter_scan(self, step_name: str,
                           step_config: dict[Any, Any],
                           config_values: dict[str, Any],
                           state_values: dict[str, Any],
                           input_mappings: dict[str, list[str]]) -> None:
        inputs: list[CompositeBuilder._PathNavigation] = \
            (self._deconstruct_dictionary([], state_values, CompositeBuilder.CompositeType.STATE)
             + self._deconstruct_dictionary([], config_values, CompositeBuilder.CompositeType.CONFIG))

        def combinatorics(current_step: dict, all_paths: list[CompositeBuilder._PathNavigation]):
            path_of_focus = all_paths[-1]
            for cur_value in path_of_focus.values:
                # put appropriate values
                match path_of_focus.composite_type:
                    case CompositeBuilder.CompositeType.CONFIG:
                        sub_struct = current_step[step_name]['config']
                        i = 0
                        while i < len(path_of_focus.path):
                            if i == len(path_of_focus.path) - 1:
                                sub_struct[path_of_focus.path[i]] = cur_value
                            sub_struct = sub_struct[path_of_focus.path[i]]
                            i += 1

                    case CompositeBuilder.CompositeType.STATE:
                        sub_struct = current_step
                        i = 0
                        while i < len(path_of_focus.path):
                            if i == len(path_of_focus.path) - 1:
                                sub_struct[path_of_focus.path[i]] = cur_value
                            elif path_of_focus.path[i] not in sub_struct:
                                sub_struct[path_of_focus.path[i]] = {}
                            sub_struct = sub_struct[path_of_focus.path[i]]
                            i += 1

                # pass down as needed
                if len(all_paths) > 1:
                    combinatorics(current_step, all_paths[:-1])
                else:
                    step_key = self.allocate_step_key(f'param_scan_{step_name}')
                    self.state[step_key] = copy.deepcopy(current_step)

        combinatorics({
            'results': {},
            step_name: {
                '_type': 'step',
                'address': f'local:{step_name}',
                'config': step_config,
                'inputs': input_mappings,
                'outputs': {'result': ['results']}
            }
        }, inputs)


    def build(self) -> Composite:
        comp = Composite(self.state, core=self.core)
        return comp
    # def build(self) -> str:
    #     final = {
    #         "composition": self.composite,
    #         "state": self.state
    #     }
    #     return json.dumps(final)
    #
    #
    #
    # def add_to_composite(self, key: str, element: str | int | float | dict) -> None:
    #     self.composite[key] = element
    #
    # def add_to_state(self, key: str, element: str | int | float | dict) -> None:
    #     self.state[key] = element







