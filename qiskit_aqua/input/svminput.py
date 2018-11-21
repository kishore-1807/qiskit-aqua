# -*- coding: utf-8 -*-

# Copyright 2018 IBM.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

import numpy as np

from qiskit_aqua import AlgorithmError
from qiskit_aqua.input import AlgorithmInput


class SVMInput(AlgorithmInput):

    CONFIGURATION = {
        'name': 'SVMInput',
        'description': 'SVM input',
        'input_schema': {
            '$schema': 'http://json-schema.org/schema#',
            'id': 'svm_input_schema',
            'type': 'object',
            'properties': {
                'training_dataset': {
                    'type': ['object', 'null'],
                    'default': None
                },
                'test_dataset': {
                    'type': ['object', 'null'],
                    'default': None
                },
                'datapoints': {
                    'type': ['array', 'null'],
                    'default': None
                }
            },
            'additionalProperties': False
        },
        'problems': ['svm_classification']
    }

    def __init__(self, training_dataset, test_dataset=None, datapoints=None):
        super().__init__()
        self.training_dataset = training_dataset
        self.test_dataset = test_dataset or {}
        self.datapoints = datapoints or np.asarray([])

    def to_params(self):
        params = {}
        params['training_dataset'] = self.training_dataset
        params['test_dataset'] = self.test_dataset
        params['datapoints'] = self.datapoints
        return params

    @classmethod
    def from_params(cls, params):
        if 'training_dataset' not in params:
            raise AlgorithmError("training_dataset is required.")
        training_dataset = params['training_dataset']
        test_dataset = params['test_dataset']
        datapoints = params['datapoints']
        return cls(training_dataset, test_dataset, datapoints)
