"""A platform to host the service of finding nearby live music

Simple, modern app. Uses the get_all_events() function to
return the bands playing that day or in the near future in Malahide.

All possible arguments for *args and **kwargs for each usage can be found in the kivy documentation at:
https://kivy.org/docs/api-kivy.html
"""


from get_events import get_all_events
from kivy.graphics import Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.effects.opacityscroll import OpacityScrollEffect
from kivy.uix.image import Image


# Temporary - to create a window about the size of a smart phone screen
from kivy.config import Config
Config.set('graphics', 'width', '255')
Config.set('graphics', 'height', '425')


class MyScrollingView(ScrollView):
    """
    A scrollable label for both today's results screen and future's results screen

    :param live_music_num: 0 signifies only today's events, while 1 signifies all foreseeable events
    :type: int
    """

    def __init__(self, live_music_num,  **kwargs):
        super().__init__(**kwargs)
        self.effect_cls = OpacityScrollEffect
        self.output_string = ''
        self.size = (230, 310)
        self.size_hint = (1, None)
        self.layout_display_results = GridLayout(cols=1, spacing=2, size_hint_y=None, padding=[10, 50])
        self.layout_display_results.bind(minimum_height=self.layout_display_results.setter('height'))
        if len(live_music_events[live_music_num]) >= 1:

            for local_event in live_music_events[live_music_num]:
                if local_event is not None:
                    self.output_string = ''
                    for event_property in local_event:
                        self.output_string += "{}: {} \n".format(event_property, local_event.get(event_property))
                    label_results = Label(text=self.output_string,
                                          text_size=[220, None],
                                          size_hint_y=None,
                                          font_size=10)
                    self.layout_display_results.add_widget(label_results)

        else:
            self.output_string = 'I am sorry, \nI could not find any events!'
            label_results = Label(text=self.output_string, text_size=[200, None])
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
        self.root = root = self
        root.bind(size=self._update_rect, pos=self._update_rect)
        with root.canvas.before:
            self.rect = Rectangle(size=root.size, pos=root.pos, source='background.jpg')

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

    def __init__(self, manager, destination, t_direction, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        self.destination = destination
        self.transition_direction = t_direction
        self.background_color = (0.59, 0.48, 0.32, 0.54)
        self.size_hint_max = (150, 50)
        self.size_hint = (None, None)
        self.size = (150, 50)

    def changer(self, *args):
        self.manager().current = self.destination
        self.manager().transition.direction = self.transition_direction

    def on_press(self):
        button_animation = Animation(size=(140, 45), duration=0.04) & \
                           Animation(font_size=7, duration=0.04) + \
                           Animation(size=(150, 50), duration=0.04) & \
                           Animation(font_size=self.font_size, duration=0.04)
        button_animation.bind(on_complete=self.changer)
        button_animation.start(self)


class HomeScreen(MyScreen):
    """
    The main screen of the app
    Holds both buttons to tonight's events page and to future's events page
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        title_image = Image(source='title_icon.png')
        layout_today_events = AnchorLayout(anchor_x='center', anchor_y='bottom', padding=[5, -500])
        layout_future_events = AnchorLayout(anchor_x='center', anchor_y='bottom', padding=[5, -500])
        layout_about = AnchorLayout(anchor_x='center', anchor_y='bottom', padding=[5, -500])
        layout_title = AnchorLayout(anchor_x='center', anchor_y='top', padding=[5, -350, 5, 350])
        button_today_events = MyButton(self.get_screen_manager, 'today results', 'up', text='Tonight\'s Beat')
        button_future_events = MyButton(self.get_screen_manager, 'future results', 'up', text='Future\'s Beat')
        button_about = MyButton(self.get_screen_manager, 'about screen', 'up', text='About')
        layout_future_events.add_widget(button_future_events)
        layout_today_events.add_widget(button_today_events)
        layout_about.add_widget(button_about)
        layout_title.add_widget(title_image)
        self.add_widget(layout_about)
        self.add_widget(layout_future_events)
        self.add_widget(layout_today_events)
        self.add_widget(layout_title)

        animation_future = Animation(pos=(0, 558), duration=1.9, t='out_quad')
        animation_today = Animation(pos=(0, 610), duration=1.9, t='out_quad')
        animation_about = Animation(pos=(0, 506), duration=1.9, t='out_quad')
        animation_title = Animation(pos=(0, -270), duration=2.7, t='out_quad')

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
        button_tonight_to_home = MyButton(self.get_screen_manager, 'home screen', 'down', text='Back To Home')
        self.layout_to_home_screen.add_widget(button_tonight_to_home)
        base_scroll_view = MyScrollingView(0)
        self.add_widget(base_scroll_view)
        self.add_widget(self.layout_to_home_screen)


class FutureResultsScreen(MyScreen):
    """
    Displays all the results from get_events_malahide()
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        button_future_to_home = MyButton(self.get_screen_manager, 'home screen', 'down', text='Back To Home')
        self.layout_to_home_screen.add_widget(button_future_to_home)
        base_scroll_view = MyScrollingView(1)
        self.add_widget(base_scroll_view)
        self.add_widget(self.layout_to_home_screen)


class AboutScreen(MyScreen):
    """
    Displays information about app and its usage
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        button_tonight_to_home = MyButton(self.get_screen_manager, 'home screen', 'down', text='Back To Home')
        self.layout_to_home_screen.add_widget(button_tonight_to_home)
        layout_display_results = BoxLayout(orientation='vertical', spacing=5, padding=[5])
        self.output_string = '''
Find The Beat allows it\'s users to locate live music playing in their area,
while providing them with the key information to attend the event.
The art for the app was created by Robert Morgan.
The sound effects/music was created by Brandon Duffield.
The idea for the app was provided by Jon Czernel.
The web scraping functionality and the app itself was created by Logan Czernel.
Built with Python. Modules: Kivy, BeautifulSoup and Requests.
'''
        label_results = Label(text=self.output_string, font_size=10, text_size=[200, 200], halign='center')
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
        app_screen_manager = ScreenManager(transition=SlideTransition())
        home_screen = HomeScreen(name='home screen')
        today_results_screen = TonightResultsScreen(name='today results')
        future_results_screen = FutureResultsScreen(name='future results')
        about_screen = AboutScreen(name='about screen')
        app_screen_manager.add_widget(home_screen)
        app_screen_manager.add_widget(today_results_screen)
        app_screen_manager.add_widget(future_results_screen)
        app_screen_manager.add_widget(about_screen)
        self.title = 'Find The Beat'

        return app_screen_manager


if __name__ == '__main__':
    live_music_events = get_all_events()

    MyApp().run()
