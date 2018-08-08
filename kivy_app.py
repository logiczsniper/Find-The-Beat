"""A platform to host the service of finding nearby live music

Simple, modern app. Uses the get_all_events() function to
return the bands playing that day or in the near future in Malahide.

All possible arguments for *args and **kwargs for each usage can be found in the kivy documentation at:
https://kivy.org/docs/api-kivy.html
"""

import json
from threading import Thread

import _mysql_exceptions
from kivy.animation import Animation
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.effects.opacityscroll import OpacityScrollEffect
from kivy.graphics import Rectangle, Color, Canvas
from kivy.graphics.context_instructions import PushMatrix, PopMatrix, Rotate
from kivy.properties import NumericProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.utils import escape_markup

from reach_db import get_db_info


def search_events(searched_value, searched_type, all_events):
    """
    Takes the text searched in a search bar and finds all events with any information matching the search

    :param searched_value: the text searched by the user
    :type: str

    :param searched_type: the instance of MyTextInput with the screen that it belongs to
    :type: object

    :param all_events: all events taken from the database
    :type: list

    :return: the events from all events that have information on them that matches the search
    :rtype: list
    """

    base_events = all_events
    new_future_events = list()
    new_today_events = list()
    event_nearness = 0 if str(searched_type) == 'MyTextInput_today results' else 1
    list_destination = new_today_events if event_nearness == 0 else new_future_events

    for info_list in base_events[event_nearness]:

        for event_property_list in info_list:

            for event_property in event_property_list:

                if searched_value.lower() in event_property.lower():
                    list_destination.append(info_list)
                    break

            if info_list in list_destination:
                break

    return [new_today_events, new_future_events, []]


def update_live_music_events():
    """
    Allows me to update the variable live_music_events anywhere in file with error handling

    :return: the updated live_music_events
    :rtype: list
    """

    try:
        new_live_music_events = get_db_info()
    except _mysql_exceptions.OperationalError:
        new_live_music_events = [
            [[('Whoops! No internet connection!', 'Use the refresh button to try again!')]] for i in range(3)
        ]

    return new_live_music_events


class MyLoader(FloatLayout):
    """
    This class contains the methods necessary to rotate an image with kivy. To be used for all the loading animations
    which entail using rotating arrows.
    """

    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.root = root = self
        self.root.canvas = Canvas()
        root.bind(angle=self.on_angle)

        self.rotate_animation = Animation(angle=0.5, duration=1)
        self.rotate_animation.start(self)

    def on_angle(self, item, angle):
        item.rotate_animation.stop(self)
        item.rotate_animation = Animation(angle=1, duration=0.00001)
        item.rotate_animation.start(self)

        if int(angle * 360) == 360:
            item.rotate_animation += Animation(angle=angle + 1, duration=0.00001)
            item.rotate_animation.start(self)

        with self.root.canvas.before:
            PushMatrix()
            Rotate(angle=angle, axis=(0, 0, 1), origin=self.root.center)
        with self.root.canvas.after:
            PopMatrix()


class MyTextInput(TextInput):
    """
    A search bar for today's events and future's events. Each time text updates, updates the scrolling view.

    :param event_screen: the screen that the text input is held in
    :type: object
    """

    def __init__(self, event_screen, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = 'Images/buttons/small_button.png'
        self.background_active = 'Images/buttons/small_button_down.png'
        self.font_name = font_path
        self.foreground_color = (0.66, 0.66, 0.66, 1)
        self.selection_color = (1, 0.23, 0.25, 0.6)
        self.cursor_color = (1, 0.23, 0.25, 1)
        self.hint_text = 'search'
        self.font_size = 15
        self.size = (67.5, 32)
        self.size_hint = (None, None)
        self.hint_text_color = (0.66, 0.66, 0.66, 1)
        self.multiline = False
        self.padding = [10, 7, 0, 7]
        self.parent_screen = event_screen
        self.text = last_today_search if self.parent_screen.name == 'today results' else last_future_search

    def __str__(self):
        try:
            return "MyTextInput_%s" % self.parent_screen.name
        except AttributeError:
            return "MyTextInput"


class MyLabel(Label):
    """
    Sets the colour of the text and font of text to avoid repeating lines for each label (they are all the same)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = (0.66, 0.66, 0.66, 1)
        self.font_name = font_path


class MyScrollingView(ScrollView):
    """
    A scrollable label for both today's results screen and future's results screen

    :param live_music_num: 0 signifies only today's events, while 1 signifies all foreseeable events, while 2 signifies
    past events
    :type: int
    """

    def __init__(self, live_music_num, **kwargs):
        super().__init__(**kwargs)
        self.live_music_num = live_music_num
        self.effect_cls = OpacityScrollEffect
        self.size = (230, 310)
        self.size_hint = (1, None)
        self.layout_display_results = GridLayout(cols=1, spacing=25, size_hint_y=None, padding=[10, 70, 10, 20])
        self.layout_display_results.bind(minimum_height=self.layout_display_results.setter('height'))
        self._output_string = ''
        self.update_event_info()
        self.add_widget(self.layout_display_results)

    def update_event_info(self, specific_events=None):

        updated_live_music_events = specific_events if specific_events else update_live_music_events()
        self.layout_display_results.clear_widgets()

        if len(updated_live_music_events[self.live_music_num]) >= 1:

            for info_list in updated_live_music_events[self.live_music_num]:

                self._output_string = ''
                combined_event_info_list = list()

                for event_property_list in info_list:
                    combined_event_info_list.extend(event_property_list)

                if len(combined_event_info_list) != 2:
                    event_date = combined_event_info_list[0]
                    event_time = combined_event_info_list[1]
                    event_cost = combined_event_info_list[2]
                    event_artist = combined_event_info_list[3]
                    event_venue = combined_event_info_list[5]
                    event_address = combined_event_info_list[6]
                    event_url = combined_event_info_list[7]

                    for event_detail in [event_artist, event_date, event_time, event_cost, event_venue,
                                         event_address, event_url]:
                        cleaned_event_detail = str(event_detail).lower().strip().title()
                        if cleaned_event_detail != '-' and cleaned_event_detail not in self._output_string:
                            self._output_string += "{} \n".format(cleaned_event_detail)

                    artist = self._output_string.split('\n')[0]
                    if info_list != updated_live_music_events[self.live_music_num][-1]:
                        self._output_string += '------------------------------------'
                    label_results = MyLabel(
                        text='[font=Font/Raleway-SemiBold.ttf]' +
                             escape_markup(artist) + '[/font]' +
                             self._output_string[len(artist)::],
                        markup=True, text_size=[Window.width - 10, None], size_hint_y=None, font_size=10,
                        halign='center'
                    )
                    self.layout_display_results.add_widget(label_results)
                else:
                    for sentence in combined_event_info_list:
                        if sentence not in self._output_string:
                            self._output_string += sentence + ' '
                    label_results = MyLabel(text=self._output_string, text_size=[Window.width - 10, None],
                                            halign='center')
                    self.layout_display_results.add_widget(label_results)

        else:
            self._output_string = 'I am sorry, \nI could not find any events!'
            label_results = MyLabel(text=self._output_string, text_size=[Window.width - 10, None], halign='center')
            self.layout_display_results.add_widget(label_results)

        if self.parent is not None:
            Animation(opacity=1, duration=0.1).start(self.parent.base_scroll_view)

    @classmethod
    def new_tonights_results(cls):
        return cls(0)

    @classmethod
    def new_future_results(cls):
        return cls(1)


class MyScreen(Screen):
    """
    All of the screens need the get_screen_manager method, therefore I created this object to hold the
    existing methods and variables that a regular Screen needs and also the get_screen_manager method.
    In addition, it draws and updates the background image on each screen.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.button_to_home = MyButton('travel to home', 'home screen', 'down')
        self.layout_text_input = AnchorLayout(anchor_x='center', anchor_y='top', padding=[11, 93, 11, 299])
        self.layout_back_search = AnchorLayout(anchor_x='center', anchor_y='top', padding=[0, 5, 32, 5])
        self.layout_inner_grid = GridLayout(cols=2, height=32, size_hint=(None, None), col_default_width=65, spacing=3)
        self.layout_back_search.add_widget(self.layout_inner_grid)
        self.layout_hidden = AnchorLayout(anchor_x='center', anchor_y='center', opacity=0)
        self.searching_animation = Animation(opacity=0.58, duration=0.15) + Animation(opacity=0, duration=0.15)
        self.opacity = 0
        self.instance, self.value = None, None
        self.root = root = self
        root.bind(size=self._update_rect, pos=self._update_rect)

        with root.canvas.before:
            Color(0.93, 0.93, 0.93, 1)
            self.rect = Rectangle(size=root.size, pos=root.pos)

    def fill_screen(self):
        self.layout_inner_grid.add_widget(self.button_to_home)
        self.layout_hidden.add_widget(Image(source='Images/icons/search_icon.png'))
        self.add_widget(self.layout_back_search)
        self.add_widget(self.base_scroll_view)
        self.add_widget(self.layout_hidden)

    def _update_rect(self, *args):
        self.rect.pos = args[0].pos
        self.rect.size = args[0].size

    @staticmethod
    def update_events_with_search(instance, value):
        specific_events = search_events(value, instance, live_music_events)
        input_screen_name = str(instance).split('_')[1]

        update_event_info_thread = Thread(
            target=main_app.app_screen_manager.get_screen(input_screen_name).base_scroll_view.update_event_info,
            args=(specific_events,)
        )

        update_event_info_thread.start()

        while update_event_info_thread.is_alive():
            pass

    def callback(self, *args):
        self.update_events_with_search(self.instance, self.value)

    def on_text(self, instance, value):
        self.instance = instance
        self.value = value
        self.searching_animation.start(self.layout_hidden)
        fading_animation = Animation(opacity=0, duration=0.1) + Animation()
        fading_animation.bind(on_complete=lambda *args: self.callback(*args))
        fading_animation.start(self.base_scroll_view)


class MyButton(Button):
    """
    Takes everything needed from the built-in Button class and adds in my own animation.
    Shrinks both the button and font-size slightly and then reverts back to the original size.

    :param manager: give the button access to the screen manager
    :type: object

    :param destination: gives the screen name that the button will change to
    :type: str

    :param t_direction: transition direction of the screen- which direction does it slide, up or down
    :type: str
    """

    def __init__(self, button_usage, destination=None, t_direction=None, **kwargs):
        super().__init__(**kwargs)
        all_buttons.append(self)
        self._usage = button_usage
        self._manager = main_app.app_screen_manager
        self._destination = destination
        self._transition_direction = t_direction
        self._last_position = 0
        self.size_hint = (None, None)

        if self._usage == 'travel to home':
            self.background_normal = 'Images/buttons/small_button_arrow_up.png'
            self.background_down = 'Images/buttons/small_button_arrow_down.png'
        elif self._usage == 'music_change':

            if background_music.state == 'stop':
                self.background_normal = 'Images/buttons/small_button_volume_off.png'
            elif background_music.state == 'play':
                self.background_normal = 'Images/buttons/small_button_volume_on.png'

            self.background_down = 'Images/buttons/small_button_volume_mid.png'

        elif self._usage == 'refresh':
            self.background_normal = 'Images/buttons/small_button_refresh_up.png'
            self.background_down = 'Images/buttons/small_button_refresh_down.png'

        elif self._usage == 'travel':
            self.background_normal = 'Images/buttons/large_button.png'
            self.background_down = 'Images/buttons/large_button_down.png'
        else:
            self.background_normal = 'Images/buttons/small_button.png'
            self.background_down = 'Images/buttons/small_button_down.png'

        self.border = (0, 0, 0, 0)
        self.font_name = font_path
        self.size = (140, 32) if self._usage == 'travel' else (67.5, 32)
        self.music_setting = True if last_setting is True else False
        self.color = (0.66, 0.66, 0.66, 1)

    def update_scrolling_view(self, *args):

        update_event_info_today_thread = Thread(
            target=self._manager.get_screen('today results').base_scroll_view.update_event_info
        )

        update_event_info_future_thread = Thread(
            target=self._manager.get_screen('future results').base_scroll_view.update_event_info
        )

        update_event_info_today_thread.start()
        update_event_info_future_thread.start()

        while update_event_info_today_thread.is_alive() or update_event_info_future_thread.is_alive():
            pass

        out_fading_animation = Animation(opacity=1, duration=1.0)
        hiding_animation = Animation(opacity=0, duration=0.5)
        out_fading_animation.start(self.parent.parent.parent)
        hiding_animation.start(self.parent.parent.parent.children[0].children[0].children[0])

    def changer(self, *args):
        if 'travel' in self._usage:
            darkening_animation.start(self._manager.current_screen)
            lighting_animation.start(self._manager.get_screen(self._destination))
            self._manager.current = self._destination
            self._manager.transition.direction = self._transition_direction

        elif self._usage == 'refresh':

            fading_animation = Animation(opacity=0.6, duration=0.9) + Animation(duration=0)
            revealing_animation = Animation(opacity=1, duration=0.4)
            fading_animation.bind(on_complete=self.update_scrolling_view)
            fading_animation.start(self.parent.parent.parent)
            revealing_animation.start(self.parent.parent.parent.children[0].children[0].children[0])

        elif self._usage == 'music_change':

            if background_music.state == 'stop':
                self.background_normal = 'Images/buttons/small_button_volume_on.png'
                background_music.play()
                background_music.seek(self._last_position)
                self._volume_changer(True)

            elif background_music.state == 'play':
                self.background_normal = 'Images/buttons/small_button_volume_off.png'
                self._last_position = background_music.get_pos()
                background_music.stop()
                self._volume_changer(False)

    def on_press(self):

        button_animation = Animation(size=(self.size[0] - 10, self.size[1] - 5), duration=0.04) & \
                           Animation(font_size=7, duration=0.04) + \
                           Animation(size=(self.size[0], self.size[1]), duration=0.04) & \
                           Animation(font_size=self.font_size, duration=0.04)
        button_animation.bind(on_complete=self.changer)
        button_animation.start(self)

        if self.music_setting is True:
            button_sound.play()

    @classmethod
    def travel(cls, destination, t_direction, **kwargs):
        return cls('travel', destination, t_direction, **kwargs)

    @staticmethod
    def _volume_changer(new_music_setting):

        for button in all_buttons:
            button.music_setting = new_music_setting


class HomeScreen(MyScreen):
    """
    The main screen of the app
    Holds both buttons to tonight's events page and to future's events page
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        _title_image = Image(source='Images/best_title_img.png')

        layout_today_events = AnchorLayout(anchor_x='center', anchor_y='bottom', padding=[5, -500])
        layout_future_events = AnchorLayout(anchor_x='center', anchor_y='bottom', padding=[5, -500])
        layout_about = AnchorLayout(anchor_x='center', anchor_y='bottom', padding=[5, -500])
        layout_title = AnchorLayout(anchor_x='center', anchor_y='top', padding=[5, -350, 5, 350])
        layout_music_refresh = AnchorLayout(anchor_x='center', anchor_y='bottom', padding=[0, -500, 35, -500])
        layout_inner_grid = GridLayout(cols=2, height=32, size_hint=(None, None), col_default_width=65, spacing=3)
        layout_hidden_loading = AnchorLayout(anchor_x='center', anchor_y='center')

        button_refresh = MyButton('refresh')
        button_music = MyButton('music_change')
        button_today_events = MyButton.travel('today results', 'up', text="tonight's beat")
        button_future_events = MyButton.travel('future results', 'up', text="future's beat")
        button_about = MyButton.travel('about screen', 'up', text='about')

        image_hidden_loading = Image(size_hint=[None, None], source='Images/icons/arrow.png',
                                     pos_hint={'center_x': 0.5, 'center_y': 0.5}, opacity=0)
        rotating_hidden_layout = MyLoader()
        rotating_hidden_layout.add_widget(image_hidden_loading)

        for layout, widget in zip([layout_inner_grid, layout_inner_grid, layout_music_refresh, layout_future_events,
                                   layout_today_events, layout_about, layout_title, layout_hidden_loading],
                                  [button_refresh, button_music, layout_inner_grid, button_future_events,
                                   button_today_events, button_about, _title_image,
                                   rotating_hidden_layout]):
            layout.add_widget(widget)

        for layout in [layout_about, layout_future_events, layout_today_events,
                       layout_music_refresh, layout_title, layout_hidden_loading]:
            self.add_widget(layout)

        animation_future = Animation(pos=(0, 575), duration=1.9, t='out_quad')
        animation_today = Animation(pos=(0, 609), duration=1.9, t='out_quad')
        animation_about = Animation(pos=(0, 541), duration=1.9, t='out_quad')
        animation_twin_button = Animation(pos=(0, 507), duration=1.9, t='out_quad')
        animation_title = Animation(pos=(0, -265), duration=2.7, t='out_quad')
        animation_lighting = Animation(opacity=1.0, duration=1.15)

        for animation, layout in zip([animation_lighting, animation_twin_button, animation_about,
                                      animation_future, animation_today, animation_title],
                                     [self, layout_music_refresh, layout_about,
                                      layout_future_events, layout_today_events, layout_title]):
            animation.start(layout)


class TonightResultsScreen(MyScreen):
    """
    Displays the results from get_events_malahide() that are on today
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.base_scroll_view = MyScrollingView.new_tonights_results()
        today_text_input = MyTextInput(self)
        today_text_input.bind(text=self.on_text)
        self.layout_inner_grid.add_widget(today_text_input)
        self.fill_screen()


class FutureResultsScreen(MyScreen):
    """
    Displays all the results from get_events_malahide() that are on in the future
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.base_scroll_view = MyScrollingView.new_future_results()
        future_text_input = MyTextInput(self)
        future_text_input.bind(text=self.on_text)
        self.layout_inner_grid.add_widget(future_text_input)
        self.fill_screen()


class AboutScreen(MyScreen):
    """
    Displays information about app and its usage
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout_display_results = BoxLayout(orientation='vertical', spacing=5, padding=[5])
        self._output_string = '''
Find The Beat allows it\'s users to locate live music playing in their area,
while providing them with the key information to attend the event.
The art for the app was created by Robert Morgan.
The sound effects/music was created by Brandon Duffield.
The idea for the app was provided by Jon Czernel.
The web scraping functionality and the app itself was created by Logan Czernel.
Built with Python. Modules: Kivy, BeautifulSoup and Requests.
'''
        label_results = MyLabel(text=self._output_string, font_size=10, text_size=[200, 200], halign='center')
        self.layout_to_home_screen = AnchorLayout(anchor_x='center', anchor_y='top', padding=[5])

        for page_item, widget in zip([self.layout_to_home_screen, layout_display_results, self, self],
                                     [self.button_to_home, label_results, layout_display_results,
                                      self.layout_to_home_screen]):
            page_item.add_widget(widget)


class MyApp(App):
    """
    Set everything up, display the background.jpg as the background image.
    Adjust the size of the image based on the size of the screen

    :return app_screen_manager: the screen manager of all the screens in the app
    :rtype: object
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._app_screen_manager = ScreenManager(transition=SlideTransition(duration=0.25))

    def build(self):
        home_screen = HomeScreen(name='home screen')
        today_results_screen = TonightResultsScreen(name='today results')
        future_results_screen = FutureResultsScreen(name='future results')
        about_screen = AboutScreen(name='about screen')

        for app_screen in [home_screen, today_results_screen, future_results_screen, about_screen]:
            self._app_screen_manager.add_widget(app_screen)

        self.title = 'Find The Beat'

        return self._app_screen_manager

    @property
    def app_screen_manager(self):
        return self._app_screen_manager


if __name__ == '__main__':

    darkening_animation = Animation(opacity=0, duration=0.5)
    lighting_animation = Animation(opacity=1.0, duration=0.5)
    live_music_events = update_live_music_events()
    all_buttons = []
    font_path = 'Font/Raleway-Regular.ttf'
    background_music = SoundLoader.load('Sounds/backgroundmusic.wav')
    button_sound = SoundLoader.load('Sounds/buttonsound.wav')

    with open('user_settings.json') as fs:
        json_data = json.load(fs)
        last_setting = json_data.get('music_active')
        previous_searches = json_data.get('user_searches')
        last_today_search = previous_searches.get('search_today')
        last_future_search = previous_searches.get('search_future')

    if button_sound:
        button_sound.volume = 0.1

    if background_music:
        background_music.loop = True
        background_music.volume = 0.5
        if last_setting is True:
            background_music.play()

    main_app = MyApp()
    main_app.run()

    with open('user_settings.json', 'w') as fs:
        music_data = main_app.app_screen_manager.get_screen('home screen').children[4].children[0].music_setting
        last_today_text = main_app.app_screen_manager.get_screen('today results').children[2].children[0].children[
            1].text
        last_future_text = main_app.app_screen_manager.get_screen('future results').children[2].children[0].children[
            1].text
        json.dump({"music_active": music_data,
                   "user_searches": {"search_today": last_today_text, "search_future": last_future_text}}, fs)
