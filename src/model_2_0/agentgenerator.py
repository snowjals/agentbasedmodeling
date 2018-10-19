import json
from agent import NoiseAgent, TrendAgent, ValueAgent
import inspect
import sys

# np is required in the eval function :)
import numpy as np  # noqa


class AgentGenerator:
    @staticmethod
    def n_agents(config_path):
        with open(config_path) as f:
            config = json.load(f)
        tot = 0
        for each in config.keys():
            tot += config[each]['n_agents']
        return tot

    @staticmethod
    def generate(config_path, assets, verbose=False):
        '''
        config_path: str, the path of the configuration.
        '''
        with open(config_path) as f:
            config = json.load(f)

        agent_types = {'noise': NoiseAgent,
                       'trend': TrendAgent,
                       'value': ValueAgent}

        generated_agents = []
        for k, cls in agent_types.items():
            # concatenate `generated_agents` with newly generated.
            generated_agents += AgentGenerator._generate_agents(config[k], assets, cls)

        return generated_agents

    @staticmethod
    def _generate_agents(config, assets, cls):
        '''
        Generate 
        '''
        n_agents = config['n_agents']
        agents = []
        required_args = AgentGenerator._get_required_init_arguments(cls)
        required_args -= {'id', 'assets'}
        # remove `id` and `assets` for now -- provide later.

        for i in range(n_agents):
            # convert config[k] to str(config[k]) to make sure that `eval`
            # evaluates a string and not a number.
            args = {k: eval(str(config[k])) for k in required_args}
            args['id'] = f'{cls.__name__}_{i}'  # supply identifier -- e.g. 'NoiseAgent_102'
            args['assets'] = assets  # supply required assets

            agents.append(cls(**args))
        return agents

    @staticmethod
    def _get_required_init_arguments(cls):
        '''
        returns a set of required arguments of cls.__init__ method.

        Example:
        _get_required_init_arguments(NoiseAgent)
            returns {'id', 'assets', ...}

        '''
        init_signature = inspect.signature(cls)

        # get all the required args. Parse as string and store in a set object.
        required_args = set(str(init_signature).strip('(),').split(', '))
        required_args -= {'self'}  # 'self' is not required...
        return required_args

    @staticmethod
    def _config_has_required_fields(config, cls):
        '''
        config: dict, where key is a field in the constructor
        and value is the corresponding value.
            example: config = {'n_agents': 100, '

        cls: class object.

        Checks whether the given config
        '''

        required_args = AgentGenerator._get_required_init_arguments(cls)
        # `id` should be generated by AgentGenerator -- remove as required
        required_args -= {'id'}

        given_keys = list(config.keys())
        if not all(key in given_keys for key in required_args):
            return False

        # now try to instantiate the object. If it crashes, then prboably no..
        input_args = {key: config[key] for key in required_args}
        try:
            cls(**input_args)
        except:  # noqa
            print('Object could not be instantiated. Here\'s the most recent traceback:')
            sys.exc_info()[0]
            return False
