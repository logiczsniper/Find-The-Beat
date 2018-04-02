"""A platform to host the service of finding nearby live music

Simple, modern app. Small button to engage with the main() function to
return the bands playing that day or in near future in Malahide.
"""


from kivy.graphics import Color, Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from TEST_get_malahide_events import main
from kivy.uix.boxlayout import BoxLayout


class MainScreen(Screen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        my_layout = AnchorLayout(anchor_x='center', anchor_y='top', padding=[5, 5, 5, 5])
        new_button = Button(text='Find The Beat')
        new_button.background_color = (0.89, 0.49, 0.1, 1)
        new_button.size_hint_max = (110, 50)
        new_button.border = [20, 20, 20, 20]
        new_button.bind(on_press=self.changer)
        my_layout.add_widget(new_button)
        self.add_widget(my_layout)

    def changer(self, *args):
        self.manager.current = 'results'
        self.manager.transition.direction = 'up'


class ResultsScreen(Screen):

    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)

        my_layout = AnchorLayout(anchor_x='center', anchor_y='top', padding=[5, 5, 5, 5])
        new_button = Button(text='Back To Home')
        new_button.background_color = (0.89, 0.49, 0.1, 1)
        new_button.size_hint_max = (110, 50)
        new_button.bind(on_press=self.changer)
        my_layout.add_widget(new_button)

        results_layout = BoxLayout(orientation='vertical', spacing=5)
        output_string = ''

        if len(main()) >= 1:
            for local_event in main():
                for event_property in local_event:
                    output_string += "{}: {} \n".format(event_property, local_event.get(event_property))
        else:
            output_string = 'I am sorry, \n I could not find any events today!'

        results_label = Label(text=output_string)
        results_layout.add_widget(results_label)

        self.add_widget(results_layout)
        self.add_widget(my_layout)

    def changer(self, *args):
        self.manager.current = 'main'
        self.manager.transition.direction = 'down'


class ScreenManagement(ScreenManager):

    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.transition = SlideTransition()


class MyApp(App):

    def build(self):
        new_screenmanager = ScreenManagement()
        first_screen = MainScreen(name='main')
        second_screen = ResultsScreen(name='results')
        new_screenmanager.add_widget(first_screen)
        new_screenmanager.add_widget(second_screen)
        self.title = 'Follow The Beat'

        self.root = root = new_screenmanager.current_screen
        root.bind(size=self._update_rect, pos=self._update_rect)
        with root.canvas.before:
            Color(0.71, 0.4, 0.08, 1)
            self.rect = Rectangle(size=root.size, pos=root.pos)

        return new_screenmanager

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == '__main__':
    MyApp().run()
