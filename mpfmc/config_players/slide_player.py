from mpf.core.config_player import ConfigPlayer


class SlidePlayer(ConfigPlayer):
    """

    Note: This class is loaded by MPF and everything in it is in the context of
    MPF.

    """
    config_file_section = 'slide_player'

    def additional_processing(self, config):

        # The config validator is set to ignore the 'transitions' setting,
        # meaning that a value of 'None' is read as string 'None.' However, the
        # user could also entry 'no' or 'false' which would be processed by the
        # YAML processor as NoneType. So we need to look for that and convert
        # it.

        # This code can be used to force No Transition if we implement default
        # transitions in the future
        # if ('transition' in config and
        #             type(config['transition']) is str and
        #             config['transition'].lower() == 'none'):
        #     config['transition'] = dict(type='none')

        if config.get('transition', None):
            config['transition'] = (
                self.machine.config_processor.process_transition(
                        config['transition']))
        else:
            config['transition'] = None

        return config

    def play(self, settings, mode=None, **kwargs):
        super().play(settings, mode, **kwargs)

        for s in settings:  # settings is a list of one or more slide configs

            name = s['slide']

            if s['target']:
                target = self.machine.targets[s['target']]
            elif mode:
                target = mode.target
            else:
                target = self.machine.targets['default']

            target.show_slide(slide_name=name, transition=s['transition'],
                              mode=mode, force=s['force'],
                              priority=s['priority'], **kwargs)

player_cls = SlidePlayer

def register_with_mpf(machine):
    return 'slide', SlidePlayer(machine)