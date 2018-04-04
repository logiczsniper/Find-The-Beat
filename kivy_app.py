"""A platform to host the service of finding nearby live music

Simple, modern app. Small button to engage with the get_events_malahide() function to
return the bands playing that day or in near future in Malahide.
"""


from TEST_get_malahide_events import get_events_malahide
from kivy.graphics import Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation


# Temporary - to create a window about the size of a smart phone screen
from kivy.config import Config
Config.set('graphics', 'width', '255')
Config.set('graphics', 'height', '425')


class MyScreen(Screen):
    """
    All of the screens need the get_screen_manager method, therefore I created this object to hold the
    existing methods and variables that a regular Screen needs and also the get_screen_manager method
    """

    def __init__(self, **kwargs):
        super(MyScreen, self).__init__(**kwargs)
        self.output_string = ''
        self.layout_to_home_screen = AnchorLayout(anchor_x='center', anchor_y='top', padding=[5, 5])

    def get_screen_manager(self, *args):
        return self.manager


class MyButton(Button):
    """
    Takes everything needed from the built-in Button class and adds in my own animation.
    Shrinks both the button and font-size slightly and then reverts back to the original size.
    """

    def __init__(self, manager, destination, t_direction, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.manager = manager
        self.destination = destination
        self.transition_direction = t_direction

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
        super(HomeScreen, self).__init__(**kwargs)
        layout_today_events = AnchorLayout(anchor_x='center', anchor_y='bottom', padding=[5, 75])
        layout_future_events = AnchorLayout(anchor_x='center', anchor_y='bottom', padding=[5, 15])
        button_today_events = MyButton(self.get_screen_manager, 'today results', 'up',
                                       text='Tonight\'s Beat',
                                       background_color=(0.59, 0.48, 0.32, 0.54),
                                       size_hint_max=(150, 50),
                                       size_hint=(None, None),
                                       width=150,
                                       height=50)
        button_future_events = MyButton(self.get_screen_manager, 'future results', 'up',
                                        text='Future\'s Beat',
                                        background_color=(0.59, 0.48, 0.32, 0.54),
                                        size_hint_max=(150, 50),
                                        size_hint=(None, None),
                                        width=150,
                                        height=50)
        layout_future_events.add_widget(button_future_events)
        layout_today_events.add_widget(button_today_events)
        self.add_widget(layout_future_events)
        self.add_widget(layout_today_events)


class TonightResultsScreen(MyScreen):
    """
    Displays the results from get_events_malahide() that are on today
    """

    def __init__(self, **kwargs):
        super(TonightResultsScreen, self).__init__(**kwargs)
        button_tonight_to_home = MyButton(self.get_screen_manager, 'home screen', 'down',
                                          text='Back To Home',
                                          background_color=(0.59, 0.48, 0.32, 0.54),
                                          size_hint_max=(150, 50),
                                          size_hint=(None, None),
                                          width=150,
                                          height=50)
        self.layout_to_home_screen.add_widget(button_tonight_to_home)
        layout_display_results = BoxLayout(orientation='vertical', spacing=5)

        if len(live_music_events[0]) >= 1:

            for local_event in live_music_events[0]:
                if local_event is not None:
                    for event_property in local_event:
                        self.output_string += "{}: {} \n".format(event_property, local_event.get(event_property))

        else:
            self.output_string = 'I am sorry, \n I could not find any events today!'

        label_results = Label(text=self.output_string, font_size=10)
        layout_display_results.add_widget(label_results)
        self.add_widget(layout_display_results)
        self.add_widget(self.layout_to_home_screen)


class FutureResultsScreen(MyScreen):
    """
    Displays all the results from get_events_malahide()
    """

    def __init__(self, **kwargs):
        super(FutureResultsScreen, self).__init__(**kwargs)
        button_future_to_home = MyButton(self.get_screen_manager, 'home screen', 'down',
                                         text='Back To Home',
                                         background_color=(0.59, 0.48, 0.32, 0.54),
                                         size_hint_max=(150, 50),
                                         size_hint=(None, None),
                                         width=150,
                                         height=50)
        self.layout_to_home_screen.add_widget(button_future_to_home)
        layout_display_results = BoxLayout(orientation='vertical', spacing=5)

        if len(live_music_events[1]) >= 1:

            for local_event in live_music_events[1]:
                if local_event is not None and len(self.output_string) < 400:
                    for event_property in local_event:
                        self.output_string += "{}: {} \n".format(event_property, local_event.get(event_property))

        else:
            self.output_string = 'I am sorry, \n I could not find any events today!'

        label_results = Label(text=self.output_string, font_size=10)
        layout_display_results.add_widget(label_results)
        self.add_widget(layout_display_results)
        self.add_widget(self.layout_to_home_screen)


class ScreenManagement(ScreenManager):
    """
    Change the transition effect to Slide Transition
    """

    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.transition = SlideTransition()


class MyApp(App):
    """
    Set everything up, display the background.jpg as the background image.
    Adjust the size of the image based on the size of the screen
    """

    def build(self):
        app_screen_manager = ScreenManagement()
        home_screen = HomeScreen(name='home screen')
        today_results_screen = TonightResultsScreen(name='today results')
        future_results_screen = FutureResultsScreen(name='future results')
        app_screen_manager.add_widget(home_screen)
        app_screen_manager.add_widget(today_results_screen)
        app_screen_manager.add_widget(future_results_screen)
        self.title = 'Find The Beat'
        self.root = root = app_screen_manager.current_screen
        root.bind(size=self._update_rect, pos=self._update_rect)
        with root.canvas.before:
            self.rect = Rectangle(size=root.size, pos=root.pos, source='background.jpg')

        return app_screen_manager

    def _update_rect(self, *args):
        self.rect.pos = args[0].pos
        self.rect.size = args[0].size


if __name__ == '__main__':
    live_music_events = get_events_malahide()
    MyApp().run()
