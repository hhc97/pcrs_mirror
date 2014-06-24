from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, ButtonHolder, Div, HTML, \
    Submit
from django import forms

from content.models import Challenge, Video, Quest, SectionQuest
from content.tags import Tag
from pcrs.form_mixins import CrispyFormMixin, BaseCrispyForm


class TagForm(BaseCrispyForm, forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name', )


class VideoForm(BaseCrispyForm, forms.ModelForm):
    class Meta:
        model = Video
        fields = ('name', 'description', 'link', 'tags')


class ChallengeForm(CrispyFormMixin, forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ('visibility', 'name', 'description', 'is_graded', 'quest')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Fieldset('', *self.Meta.fields),
        )
        if self.instance.pk:
            add_objects = HTML('<a class="btn btn-success" role="button" '
                               'href="{{ object.get_absolute_url }}/objects">'
                               'Manage content</a>')
            self.helper.layout.append(
                Div(ButtonHolder(self.delete_button,
                    Div(add_objects, self.save_button,
                        css_class='btn-group pull-right'))
                )
            )
        else:
            self.helper.layout.append(ButtonHolder(self.save_button))


class QuestForm(BaseCrispyForm, forms.ModelForm):
    class Meta:
        model = Quest
        fields = ('name', 'description')


class QuestSectionForm(CrispyFormMixin, forms.ModelForm):
    class Meta:
        model = SectionQuest
        fields = ('visibility', 'open_on', 'due_on', 'quest')
        widgets = {'quest': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = False