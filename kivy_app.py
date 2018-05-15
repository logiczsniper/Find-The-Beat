"""A platform to host the service of finding nearby live music

Simple, modern app. Uses the get_all_events() function to
return the bands playing that day or in the near future in Malahide.

All possible arguments for *args and **kwargs for each usage can be found in the kivy documentation at:
https://kivy.org/docs/api-kivy.html
"""


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle, Color
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.effects.opacityscroll import OpacityScrollEffect
from kivy.core.audio import SoundLoader
from reach_db import get_db_info
from store_music_setting import last_setting
import _mysql_exceptions


# Temporary - to create a window about the size of a smart phone screen
from kivy.config import Config
Config.set('graphics', 'width', '255')
Config.set('graphics', 'height', '425')


class MyLabel(Label):
    """
    Sets the colour of the text and font of text to avoid repeating myself for each label (they are all the same)
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

    def __init__(self, live_music_num,  **kwargs):
        super().__init__(**kwargs)
        self.effect_cls = OpacityScrollEffect
        self.output_string = ''
        self.size = (230, 310)
        self.size_hint = (1, None)
        self.layout_display_results = GridLayout(cols=1, spacing=50, size_hint_y=None, padding=[10, 50])
        self.layout_display_results.bind(minimum_height=self.layout_display_results.setter('height'))

        if len(live_music_events[live_music_num]) >= 1:

            for info_list in live_music_events[live_music_num]:

                self.output_string = ''

                for event_property_list in info_list:

                    for event_property in event_property_list:

                        self.output_string += "{} \n".format(event_property)

                label_results = MyLabel(text=self.output_string, text_size=[200, None], size_hint_y=None, font_size=10)
                self.layout_display_results.add_widget(label_results)

        else:
            self.output_string = 'I am sorry, \nI could not find any events!'
            label_results = MyLabel(text=self.output_string, text_size=[200, None])
            self.layout_display_results.add_widget(label_results)

        self.add_widget(self.layout_display_results)


class MyScreen(Screen):
    """
    All of the screens need the get_screen_manager method, therefore I created this object to hold the
    existing methods and variables that a regular Screen needs and also the get_screen_manager method.
    In addition, it draws and updates the background image on each screen.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout_to_home_screen = AnchorLayout(anchor_x='center', anchor_y='top', padding=[5])
        self.opacity = 0
        self.root = root = self
        root.bind(size=self._update_rect, pos=self._update_rect)

        with root.canvas.before:
            Color(0.93, 0.93, 0.93, 1)
            self.rect = Rectangle(size=root.size, pos=root.pos)

    def _update_rect(self, *args):
        self.rect.pos = args[0].pos
        self.rect.size = args[0].size

    def get_screen_manager(self, *args):
        return self.manager


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

    def __init__(self, button_usage, manager=None, destination=None, t_direction=None, **kwargs):
        super().__init__(**kwargs)
        all_buttons.append(self)
        self.usage = button_usage
        self.manager = manager
        self.destination = destination
        self.transition_direction = t_direction
        self.size_hint = (None, None)
        self.last_position = 0
        self.background_normal = 'Images/button.png'
        self.background_down = 'Images/button_down.png'
        self.font_name = font_path
        self.size = (140, 32) if self.usage == 'travel' else (65, 32)
        self.music_setting = True if last_setting is True else False
        self.color = (0.66, 0.66, 0.66, 1)

    def changer(self, *args):
        if self.usage == 'travel':
            darkening_animation = Animation(opacity=0, duration=0.5)
            lighting_animation = Animation(opacity=1.0, duration=0.5)
            darkening_animation.start(self.manager().current_screen)
            lighting_animation.start(self.manager().get_screen(self.destination))
            self.manager().current = self.destination
            self.manager().transition.direction = self.transition_direction

        elif self.usage == 'refresh':
            self.parent.parent.parent.manager.get_screen('today results').canvas.ask_update()
            self.parent.parent.parent.manager.get_screen('future results').canvas.ask_update()

        elif self.usage == 'music':

            if background_music.state == 'stop':
                background_music.play()
                background_music.seek(self.last_position)

                for button in all_buttons:
                    button.music_setting = True

            elif background_music.state == 'play':
                self.last_position = background_music.get_pos()
                background_music.stop()

                for button in all_buttons:
                    button.music_setting = False

    def on_press(self):
        button_animation = Animation(size=(self.size[0]-10, self.size[1]-5), duration=0.04) & \
                           Animation(font_size=7, duration=0.04) + \
                           Animation(size=(self.size[0], self.size[1]), duration=0.04) & \
                           Animation(font_size=self.font_size, duration=0.04)
        button_animation.bind(on_complete=self.changer)
        button_animation.start(self)

        if self.music_setting is True:
            button_sound.play()


class HomeScreen(MyScreen):
    """
    The main screen of the app
    Holds both buttons to tonight's events page and to future's events page
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        title_image = Image(source='Images/best_title_img.png')

        layout_today_events = AnchorLayout(anchor_x='center', anchor_y='bottom', padding=[5, -500])
        layout_future_events = AnchorLayout(anchor_x='center', anchor_y='bottom', padding=[5, -500])
        layout_about = AnchorLayout(anchor_x='center', anchor_y='bottom', padding=[5, -500])
        layout_title = AnchorLayout(anchor_x='center', anchor_y='top', padding=[5, -350, 5, 350])
        layout_music_refresh = AnchorLayout(anchor_x='center', anchor_y='bottom', padding=[0, -500, 35, -500])
        layout_inner_grid = GridLayout(cols=2, height=32, size_hint=(None, None), col_default_width=65, spacing=5)

        button_refresh = MyButton('refresh', text='refresh')
        button_music = MyButton('music', text='music')
        button_today_events = MyButton('travel', self.get_screen_manager, 'today results', 'up', text="tonight's beat")
        button_future_events = MyButton('travel', self.get_screen_manager, 'future results', 'up', text="future's beat")
        button_about = MyButton('travel', self.get_screen_manager, 'about screen', 'up', text='about')

        layout_inner_grid.add_widget(button_refresh)
        layout_inner_grid.add_widget(button_music)
        layout_music_refresh.add_widget(layout_inner_grid)
        layout_future_events.add_widget(button_future_events)
        layout_today_events.add_widget(button_today_events)
        layout_about.add_widget(button_about)
        layout_title.add_widget(title_image)

        for layout in [layout_about, layout_future_events, layout_today_events, layout_music_refresh, layout_title]:
            self.add_widget(layout)

        animation_future = Animation(pos=(0, 575), duration=1.9, t='out_quad')
        animation_today = Animation(pos=(0, 609), duration=1.9, t='out_quad')
        animation_about = Animation(pos=(0, 541), duration=1.9, t='out_quad')
        animation_title = Animation(pos=(0, -265), duration=2.7, t='out_quad')
        animation_twin_button = Animation(pos=(0, 507), duration=1.9, t='out_quad')
        animation_lighting = Animation(opacity=1.0, duration=1.15)

        animation_lighting.start(self)
        animation_twin_button.start(layout_music_refresh)
        animation_about.start(layout_about)
        animation_future.start(layout_future_events)
        animation_today.start(layout_today_events)
        animation_title.start(layout_title)


class TonightResultsScreen(MyScreen):
    """
    Displays the results from get_events_malahide() that are on today
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        base_scroll_view = MyScrollingView(0)
        button_tonight_to_home = MyButton('travel', self.get_screen_manager, 'home screen', 'down', text='back')
        self.layout_to_home_screen.add_widget(button_tonight_to_home)
        self.add_widget(base_scroll_view)
        self.add_widget(self.layout_to_home_screen)


class FutureResultsScreen(MyScreen):
    """
    Displays all the results from get_events_malahide()
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        base_scroll_view = MyScrollingView(1)
        button_future_to_home = MyButton('travel', self.get_screen_manager, 'home screen', 'down', text='back')
        self.layout_to_home_screen.add_widget(button_future_to_home)
        self.add_widget(base_scroll_view)
        self.add_widget(self.layout_to_home_screen)


class AboutScreen(MyScreen):
    """
    Displays information about app and its usage
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout_display_results = BoxLayout(orientation='vertical', spacing=5, padding=[5])
        button_tonight_to_home = MyButton('travel', self.get_screen_manager, 'home screen', 'down', text='back')
        self.layout_to_home_screen.add_widget(button_tonight_to_home)
        self.output_string = '''
Find The Beat allows it\'s users to locate live music playing in their area,
while providing them with the key information to attend the event.
The art for the app was created by Robert Morgan.
The sound effects/music was created by Brandon Duffield.
The idea for the app was provided by Jon Czernel.
The web scraping functionality and the app itself was created by Logan Czernel.
Built with Python. Modules: Kivy, BeautifulSoup and Requests.
'''
        label_results = MyLabel(text=self.output_string, font_size=10, text_size=[200, 200], halign='center')
        layout_display_results.add_widget(label_results)
        self.add_widget(layout_display_results)
        self.add_widget(self.layout_to_home_screen)


class MyApp(App):
    """
    Set everything up, display the background.jpg as the background image.
    Adjust the size of the image based on the size of the screen

    :return app_screen_manager: the screen manager of all the screens in the app
    :rtype: object
    """

    def build(self):
        app_screen_manager = ScreenManager(transition=SlideTransition(duration=0.25))
        home_screen = HomeScreen(name='home screen')
        today_results_screen = TonightResultsScreen(name='today results')
        future_results_screen = FutureResultsScreen(name='future results')
        about_screen = AboutScreen(name='about screen')

        for app_screen in [home_screen, today_results_screen, future_results_screen, about_screen]:
            app_screen_manager.add_widget(app_screen)

        self.title = 'Find The Beat'

        return app_screen_manager


if __name__ == '__main__':

    try:
        live_music_events = get_db_info()
    except _mysql_exceptions.OperationalError as oe:
        live_music_events = [
            [[('Whoops! No internet connection!', 'Connect me to the internet and reboot the app!')]] for i in range(3)
        ]

    all_buttons = []
    font_path = 'Font/Raleway-Regular.ttf'
    background_music = SoundLoader.load('Sounds/Sophomore_Makeout.mp3')
    button_sound = SoundLoader.load('Sounds/buttonsound.wav')

    if button_sound:
        button_sound.volume = 0.25

    if background_music:
        background_music.loop = True
        background_music.volume = 0.3
        if last_setting is True:
            background_music.play()

    MyApp().run()
