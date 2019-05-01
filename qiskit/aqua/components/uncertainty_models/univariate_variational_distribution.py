# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
# =============================================================================


import numpy as np

from qiskit.aqua.components.uncertainty_models.univariate_distribution import UnivariateDistribution
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import BasicAer, execute
from qiskit.aqua import QuantumInstance

CONFIGURATION = {
    'name': 'UnivariateVariationalDistribution',
    'description': 'Univariate Variational Distribution',
    'input_schema': {
        '$schema': 'http://json-schema.org/schema#',
        'id': 'UnivariateVariationalDistribution_schema',
        'type': 'object',
        'properties': {
            'num_qubits': {
                'type': 'number',
            },

            'params': {
                'type': 'array',
                "items": {
                    "type": "number"
                }
            },
            'low': {
                'type': 'number',
                'default': 0
            },
            'high': {
                'type': 'number',
                'default': 1
            },
        },
        'additionalProperties': False
    ,
    'depends': [
        {
        'pluggable_type': 'variational_form',
        'default': {'name': 'RY'}
        },
         {'pluggable_type': 'initial_state',
          'default': {'name': 'ZERO'}
          }
        ]
    }
    }


class UnivariateVariationalDistribution(UnivariateDistribution):
    """
    The Univariate Variational Distribution.
    """

    def __init__(self, num_qubits, var_form, params, initial_distribution=None, low=0, high=1):
        self._num_qubits = num_qubits
        self._var_form = var_form
        self.params = params
        self._initial_distribution = initial_distribution
        probabilities = list(np.zeros(2**num_qubits))
        super().__init__(num_qubits, probabilities, low, high)

    def build(self, qc, q, q_ancillas=None, params=None):
        if self._initial_distribution:
            qc.extend(self._initial_distribution.construct_circuit(mode='circuit', register=q))
        circuit_var_form = self._var_form.construct_circuit(self.params, q)
        qc.extend(circuit_var_form)


    def set_probabilities(self, quantum_instance):
        """
        Set Probabilities
        Args:
            quantum_instance: QuantumInstance

        Returns:

        """
        q_ = QuantumRegister(self._num_qubits, name='q')
        if self._initial_distribution:
                qc_= self._initial_distribution.construct_circuit(mode='circuit', register=q_)
        else:
            qc_ = QuantumCircuit(q_)
        circuit_var_form = self._var_form.construct_circuit(self.params, q_)
        qc_ += circuit_var_form


        if quantum_instance.is_statevector:
            pass
        else:
            c_ = ClassicalRegister(self._num_qubits, name='c')
            qc_.add_register(c_)
            qc_.measure(q_, c_)
        result = quantum_instance.execute(qc_)
        if quantum_instance.is_statevector:
            result = result.get_statevector(qc_)
            values = np.multiply(result, np.conj(result))
            values = list(values.real)
        else:
            result = result.get_counts(qc_)
            keys = list(result)
            values = list(result.values())
            values = [float(v) / np.sum(values) for v in values]
            values = [x for _, x in sorted(zip(keys, values))]

        probabilities = values
        self._probabilities = np.array(probabilities)
        return



