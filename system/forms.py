from django.forms import ModelForm
from authentication.models import Student

from system.models import VideoComment


class VideoCommentForm(ModelForm):

    class Meta:
        model = VideoComment
        exclude = ()