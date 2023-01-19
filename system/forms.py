from django.forms import ModelForm

from system.models import VideoComment


class VideoCommentForm(ModelForm):

    class Meta:
        model = VideoComment
        exclude = ()