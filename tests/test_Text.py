from tests.MpfMcTestCase import MpfMcTestCase


class TestText(MpfMcTestCase):
    def get_machine_path(self):
        return 'tests/machine_files/text'

    def get_config_file(self):
        return 'test_text.yaml'

    def get_widget(self):
        return self.mc.targets['default'].current_slide.children[0]

    def test_static_text(self):
        # Very basic test
        self.mc.events.post('static_text')
        self.advance_time()

        self.assertEqual(self.get_widget().text, 'TEST')

    def test_text_from_event_param1(self):
        # widget text is only from event param
        self.mc.events.post('text_from_event_param1', param1='HELLO')
        self.advance_time()

        self.assertEqual(self.get_widget().text, 'HELLO')

    def test_text_from_event_param2(self):
        # widget text puts static text before param text
        self.mc.events.post('text_from_event_param2', param1='HELLO')
        self.advance_time()

        self.assertEqual(self.get_widget().text, 'HI HELLO')

    def test_text_from_event_param3(self):
        # widget text puts static text before and after param text
        self.mc.events.post('text_from_event_param3', param1='AND')
        self.advance_time()

        self.assertEqual(self.get_widget().text, 'MIX AND MATCH')

    def test_text_from_event_param4(self):
        # static and event text with no space between
        self.mc.events.post('text_from_event_param4', param1='SPACE')
        self.advance_time()

        self.assertEqual(self.get_widget().text, 'NOSPACE')

    def test_text_from_event_param5(self):
        #test event text that comes in as non-string
        self.mc.events.post('text_from_event_param5', param1=1)
        self.advance_time()

        self.assertEqual(self.get_widget().text, 'NUMBER 1')

    def test_text_from_event_param6(self):
        # placeholder for event text for a param that doesn't exist
        self.mc.events.post('text_from_event_param6')
        self.advance_time()

        self.assertEqual(self.get_widget().text, '%param1%')

    def test_text_from_event_param7(self):
        # test percent sign hard coded
        self.mc.events.post('text_from_event_param7')
        self.advance_time()

        self.assertEqual(self.get_widget().text, '100%')

    def test_text_from_event_param8(self):
        # test perent next to placeholder text
        self.mc.events.post('text_from_event_param8', param1=100)
        self.advance_time()

        self.assertEqual(self.get_widget().text, '100%')

    def test_player_var1(self):
        # staight var, no player specified
        self.mc.game_start()
        self.advance_time()
        self.mc.add_player(1)
        self.advance_time()
        self.mc.player_start_turn(1)
        self.advance_time()

        self.assertTrue(self.mc.player)

        self.mc.player.test_var = 1

        self.mc.events.post('text_with_player_var1')
        self.advance_time()

        self.assertEqual(self.get_widget().text, '1')
        self.assertEqual(self.get_widget().size, [8, 18])

        # update var, should update widget
        self.mc.player.test_var = 200
        self.advance_time()
        self.assertEqual(self.get_widget().text, '200')
        self.assertEqual(self.get_widget().size, [24, 18])

    def test_player_var2(self):
        # 'player' specified
        self.mc.game_start()
        self.advance_time()
        self.mc.add_player(1)
        self.advance_time()
        self.mc.player_start_turn(1)
        self.advance_time()

        self.assertTrue(self.mc.player)

        self.mc.player.test_var = 1

        self.mc.events.post('text_with_player_var2')
        self.advance_time()

        self.assertEqual(self.get_widget().text, '1')

    def test_player_var3(self):
        # 'player1' specified
        self.mc.game_start()
        self.advance_time()
        self.mc.add_player(1)
        self.advance_time()
        self.mc.player_start_turn(1)
        self.advance_time()

        self.assertTrue(self.mc.player)

        self.mc.player.test_var = 1

        self.mc.events.post('text_with_player_var3')
        self.advance_time()

        self.assertEqual(self.get_widget().text, '1')

    def test_player_var4(self):
        # 'player2' specified with no player 2. Should be blank.
        self.mc.game_start()
        self.advance_time()
        self.mc.add_player(1)
        self.advance_time()
        self.mc.player_start_turn(1)
        self.advance_time()

        self.assertTrue(self.mc.player)

        self.mc.player.test_var = 1

        self.mc.events.post('text_with_player_var4')
        self.advance_time()

        self.assertEqual(self.get_widget().text, '')

        # Add player 2 & set the value. Widget should update
        self.mc.add_player(2)
        self.mc.player_list[1].test_var = 0
        self.advance_time()
        self.assertEqual(self.get_widget().text, '0')

    def test_number_grouping(self):
        self.mc.events.post('number_grouping')
        self.advance_time()

        # should be 00 even though text is 0
        self.assertEqual(self.get_widget().text, '00')
        self.advance_time(1)

        self.get_widget().update_text('2000000')
        self.assertEqual(self.get_widget().text, '2,000,000')
        self.advance_time(1)

    def test_text_string1(self):
        # simple text string in machine config
        self.mc.events.post('text_string1')
        self.advance_time()

        self.assertEqual(self.get_widget().text, 'HELLO')

    def test_text_string2(self):
        # two text strings in machine config
        self.mc.events.post('text_string2')
        self.advance_time()

        # should be 00 even though text is 0
        self.assertEqual(self.get_widget().text, 'HELLO PLAYER')

    def test_text_string3(self):
        # text string not found
        self.mc.events.post('text_string3')
        self.advance_time()

        # should be 00 even though text is 0
        self.assertEqual(self.get_widget().text, '$money')

    def test_text_string4(self):
        # text string found with extra dollar sign in text
        self.mc.events.post('text_string4')
        self.advance_time()

        # should be 00 even though text is 0
        self.assertEqual(self.get_widget().text, '$100')

    def test_mode1_text_string1(self):
        self.mc.modes['mode1'].start()
        self.advance_time()

        self.mc.events.post('text_string1_mode1')
        self.advance_time()

        self.assertEqual(self.get_widget().text, 'HELLO FROM MODE 1')
        self.mc.modes['mode1'].stop()
        self.advance_time()

        self.mc.events.post('text_string1')
        self.advance_time()
        self.assertEqual(self.get_widget().text, 'HELLO')