from django.forms import ModelForm
from appAdmin.models import App

# Create your forms here.

class AppForm(ModelForm): 

    class Meta:
	    model = App
	    fields = ["application", "urls", "status", "status_serveur"]


# Creating a form to add an app.
# >>> form = AppForm()

# Creating a form to change an existing app.
# >>> app = App.objects.get(pk=1)
# >>> form = AppForm(instance=app)

    def save(self, commit=True):
        f = ArticleForm(request.POST)
        new_article = f.save()

    #     if commit:
    #         app.save()
    #     return app
